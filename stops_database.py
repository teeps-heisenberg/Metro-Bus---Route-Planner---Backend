import shapefile
import json
import os
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

@dataclass
class Station:
    id: Union[str, int]  # Allow both string and integer IDs
    name: str
    line_code: str
    is_interchange: bool
    coordinates: Tuple[float, float]
    line_name: str

class StopsDatabase:
    def __init__(self):
        self.stations: Dict[str, Station] = {}  # name -> Station
        self.lines = {
            'GREEN': {
                'name': 'Green Line',
                'color': '#22c55e',  # Tailwind green-500
                'theme_color': 'green'
            },
            'BLUE': {
                'name': 'Blue Line', 
                'color': '#3b82f6',  # Tailwind blue-500
                'theme_color': 'blue'
            }
        }
        
        # Stop name mapping for Blue Line (shapefile names -> route names)
        self.blue_line_stop_mapping = {
            'GULBERG': 'Gulberg',
            'KORAL CHOWK': 'Koral Town', 
            'GANGAL': 'Gangal',
            'FAZAIA': 'Fazaia',
            'KHANNA PUL': 'Khanna Pul',
            'ZIA MASJID': 'Zia Masjid',
            'KURI ROAD': 'Kuri Road',
            'IQBAL TOWN': 'Iqbal Town',
            'DHOKE KALA KHAN': 'Dhok Kala Khan',
            'SOHAN': 'Sohan',
            'PARADE GROUND': 'Parade Ground',
            'SHAKARPARIAN': 'Shakarparian',
            'G-7 / G-8': 'G-8 Markaz',
            'CHILDREN HOSPITAL': 'Children Hospital',
            'PIMS GATE': 'PIMS Hospital',
            'PIMS STATION': 'PIMS Metro Station'
        }
        
        # Reverse mapping (route names -> shapefile names)
        self.blue_line_reverse_mapping = {v: k for k, v in self.blue_line_stop_mapping.items()}
        
        self.load_stops()
    
    def load_stops(self):
        """Load Green Line stops from routes JSON, Blue Line from shapefiles."""
        # Load Green Line stops from routes JSON to match route planning data
        self.load_green_line_from_routes()
        
        # Load Blue Line stops from shapefiles
        blue_shapefile = os.path.join('data', 'blue_line', 'BLUE_STATIONS')
        if os.path.exists(blue_shapefile + '.shp'):
            self._load_line_stops(blue_shapefile, 'BLUE')

    def load_green_line_from_routes(self):
        """Load Green Line stops from routes_analysis.json to match route planning data."""
        try:
            with open('routes_analysis.json', 'r', encoding='utf-8') as f:
                routes_data = json.load(f)
            
            green_stops_loaded = 0
            
            for route_key, route_data in routes_data.items():
                # Only process Green Line routes (FRG-)
                if not route_key.startswith('FRG-'):
                    continue
                
                # Extract stops from the route data
                lines = route_data.get('lines', [])
                stops_found = set()
                
                for line in lines:
                    # Look for stop information in the lines
                    if 'stop_name arrival_time departure_time' in line:
                        # This line indicates stop data follows
                        continue
                    
                    # Check if line contains stop data (has times)
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        # Try to find where times start
                        for i in range(len(parts) - 2):
                            time1 = parts[-2]
                            time2 = parts[-1]
                            if (':' in time1 and ':' in time2 and 
                                len(time1.split(':')) == 3 and len(time2.split(':')) == 3):
                                # This looks like stop data
                                stop_name = ' '.join(parts[:i+1])
                                if stop_name and stop_name not in stops_found:
                                    stops_found.add(stop_name)
                                    
                                    # Create station object
                                    station = Station(
                                        id=f"GL_{green_stops_loaded + 1}",
                                        name=stop_name,
                                        line_code='GREEN',
                                        is_interchange=False,
                                        coordinates=(0.0, 0.0),  # Placeholder coordinates
                                        line_name=self.lines['GREEN']['name']
                                    )
                                    
                                    # Store by name
                                    if stop_name not in self.stations:
                                        self.stations[stop_name] = station
                                        green_stops_loaded += 1
                                    else:
                                        # Station exists in multiple lines - mark as interchange
                                        existing = self.stations[stop_name]
                                        if existing.line_code != 'GREEN':
                                            existing.line_code = f"{existing.line_code}/GREEN"
                                            existing.is_interchange = True
                
                print(f"[INFO] Loaded {len(stops_found)} Green Line stops from route {route_key}")
            
            print(f"[INFO] Total Green Line stations loaded from routes: {green_stops_loaded}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load Green Line stops from routes: {e}")
    
    def _load_line_stops(self, shapefile_path: str, line_code: str):
        """Load stops from a specific line's shapefile."""
        try:
            sf = shapefile.Reader(shapefile_path)
            fields = [field[0] for field in sf.fields[1:]]
            records = sf.records()
            shapes = sf.shapes()
            
            for record, shape in zip(records, shapes):
                station_name = record[fields.index('sta_name')]
                station_id = record[fields.index('id')]
                is_interchange = record[fields.index('interchg')]
                
                if shape.points:
                    coords = shape.points[0]
                    
                    # Create station object
                    station = Station(
                        id=station_id,
                        name=station_name,
                        line_code=line_code,
                        is_interchange=is_interchange,
                        coordinates=coords,
                        line_name=self.lines[line_code]['name']
                    )
                    
                    # Store by name (handle duplicates by appending line code if needed)
                    key = station_name
                    if key in self.stations:
                        # If station exists, it's an interchange between lines
                        existing = self.stations[key]
                        if existing.line_code != line_code:
                            # Update to show it's multi-line
                            existing.line_code = f"{existing.line_code}/{line_code}"
                            existing.is_interchange = True
                    else:
                        self.stations[key] = station
                        
        except Exception as e:
            print(f"Error loading {line_code} stops: {e}")
    
    def get_all_stops(self, line_code: Optional[str] = None) -> List[str]:
        """Get all stops, optionally filtered by line."""
        if line_code:
            return [name for name, station in self.stations.items() 
                   if line_code in station.line_code]
        return list(self.stations.keys())
    
    def get_station_info(self, station_name: str) -> Optional[Station]:
        """Get detailed information about a specific station."""
        return self.stations.get(station_name)
    
    def search_stops(self, query: str, line_code: Optional[str] = None) -> List[str]:
        """Search stops by name, optionally filtered by line."""
        all_stops = self.get_all_stops(line_code)
        query_lower = query.lower()
        
        # Exact matches first
        exact_matches = [stop for stop in all_stops if stop.lower() == query_lower]
        
        # Partial matches
        partial_matches = [stop for stop in all_stops 
                          if query_lower in stop.lower() and stop not in exact_matches]
        
        return exact_matches + partial_matches[:10]
    
    def get_line_info(self, line_code: str) -> Optional[Dict]:
        """Get information about a specific line."""
        return self.lines.get(line_code)
    
    def get_available_lines(self) -> List[str]:
        """Get list of available line codes."""
        return list(self.lines.keys())
    
    def is_interchange_station(self, station_name: str) -> bool:
        """Check if a station is an interchange between lines."""
        station = self.stations.get(station_name)
        return station.is_interchange if station else False

    def map_stop_name_for_routes(self, stop_name: str, line_code: str) -> str:
        """Map stop name from shapefile format to route format for route finding."""
        if line_code == 'BLUE' and stop_name in self.blue_line_stop_mapping:
            return self.blue_line_stop_mapping[stop_name]
        return stop_name

    def map_stop_name_for_display(self, stop_name: str, line_code: str) -> str:
        """Map stop name from route format to shapefile format for display."""
        if line_code == 'BLUE' and stop_name in self.blue_line_reverse_mapping:
            return self.blue_line_reverse_mapping[stop_name]
        return stop_name

# Global instance
stops_db = StopsDatabase()
