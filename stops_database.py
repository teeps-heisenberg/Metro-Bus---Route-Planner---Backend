import shapefile
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Station:
    id: int
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
        self.load_stops()
    
    def load_stops(self):
        """Load stops from both Green Line and Blue Line shapefiles."""
        green_shapefile = os.path.join('data', 'green_line', 'GREEN_STATIONS')
        blue_shapefile = os.path.join('data', 'blue_line', 'BLUE_STATIONS')
        
        # Load Green Line stops
        if os.path.exists(green_shapefile + '.shp'):
            self._load_line_stops(green_shapefile, 'GREEN')
        
        # Load Blue Line stops  
        if os.path.exists(blue_shapefile + '.shp'):
            self._load_line_stops(blue_shapefile, 'BLUE')
    
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

# Global instance
stops_db = StopsDatabase()
