import json
import re
from datetime import datetime, time
from typing import Dict, List, Optional, Tuple
from models import Route, Trip, Stop, Direction

class RouteParser:
    def __init__(self, json_file_path: str = "../routes_analysis.json"):
        self.json_file_path = json_file_path
        self.routes_cache: Dict[str, Route] = {}
        
    def parse_time(self, time_str: str) -> time:
        """Parse time string in HH:MM:SS format to time object."""
        try:
            return datetime.strptime(time_str.strip(), "%H:%M:%S").time()
        except ValueError:
            # Try HH:MM format
            try:
                return datetime.strptime(time_str.strip(), "%H:%M").time()
            except ValueError:
                return time(0, 0)
    
    def extract_route_info_from_lines(self, lines: List[str]) -> Dict[str, str]:
        """Extract basic route information from lines array."""
        info = {}
        
        for line in lines:
            if 'Route ID' in line:
                info['route_id'] = line.split('Route ID')[-1].strip()
            elif 'Short Name' in line:
                info['short_name'] = line.split('Short Name')[-1].strip()
            elif 'Long Name' in line:
                info['long_name'] = line.split('Long Name')[-1].strip()
            elif 'Direction' in line:
                info['direction'] = line.split('Direction')[-1].strip()
            elif 'Total Trips' in line:
                info['total_trips'] = int(line.split('Total Trips')[-1].strip())
            elif 'Average Headway' in line:
                headway_str = line.split('Average Headway (min)')[-1].strip()
                info['average_headway'] = int(headway_str)
        
        return info
    
    def extract_trips_from_lines(self, lines: List[str]) -> List[Trip]:
        """Extract trip information from lines array."""
        trips = []
        current_trip = None
        current_stops = []
        
        for line in lines:
            line = line.strip()
            
            # Check for trip start (pattern: trip_id time)
            if re.match(r'\d+-\d+\s+\d{2}:\d{2}:\d{2}', line):
                # Save previous trip if exists
                if current_trip and current_stops:
                    current_trip.stops = current_stops
                    trips.append(current_trip)
                
                # Start new trip
                parts = line.split()
                trip_id = parts[0]
                start_time = self.parse_time(parts[1])
                current_trip = Trip(trip_id=trip_id, start_time=start_time, stops=[])
                current_stops = []
                
            # Check for stop information (pattern: stop_name arrival_time departure_time)
            elif current_trip and len(line.split()) >= 3:
                parts = line.split()
                # Try to parse as stop information
                try:
                    # Find where times start (last two parts should be times)
                    for i in range(len(parts) - 2):
                        time1 = parts[-2]
                        time2 = parts[-1]
                        if (re.match(r'\d{2}:\d{2}:\d{2}', time1) and 
                            re.match(r'\d{2}:\d{2}:\d{2}', time2)):
                            stop_name = ' '.join(parts[:i+1])
                            arrival_time = self.parse_time(time1)
                            departure_time = self.parse_time(time2)
                            
                            stop = Stop(
                                name=stop_name,
                                arrival_time=arrival_time,
                                departure_time=departure_time,
                                sequence=len(current_stops) + 1
                            )
                            current_stops.append(stop)
                            break
                except:
                    continue
        
        # Add last trip
        if current_trip and current_stops:
            current_trip.stops = current_stops
            trips.append(current_trip)
        
        return trips
    
    def parse_route_from_json(self, route_key: str, route_data: Dict) -> Optional[Route]:
        """Parse a single route from JSON data."""
        try:
            lines = route_data.get('lines', [])
            
            # Extract route information
            route_info = self.extract_route_info_from_lines(lines)
            if not route_info:
                return None
            
            # Extract trips
            trips = self.extract_trips_from_lines(lines)
            
            # Create Route object
            route = Route(
                route_id=route_info.get('route_id', ''),
                short_name=route_info.get('short_name', ''),
                long_name=route_info.get('long_name', ''),
                direction=Direction(route_info.get('direction', 'Forward')),
                total_trips=route_info.get('total_trips', 0),
                average_headway=route_info.get('average_headway', 60),
                trips=trips
            )
            
            return route
            
        except Exception as e:
            print(f"Error parsing route {route_key}: {e}")
            return None
    
    def load_all_routes(self) -> Dict[str, Route]:
        """Load all routes from JSON file and cache them."""
        if self.routes_cache:
            return self.routes_cache
        
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                routes_data = json.load(f)
            
            for route_key, route_data in routes_data.items():
                route = self.parse_route_from_json(route_key, route_data)
                if route:
                    self.routes_cache[route_key] = route
                    print(f"Loaded route: {route_key} with {len(route.trips)} trips")
            
            print(f"Total routes loaded: {len(self.routes_cache)}")
            return self.routes_cache
            
        except Exception as e:
            print(f"Error loading routes from JSON: {e}")
            return {}
    
    def get_all_stops(self) -> List[str]:
        """Get all unique stop names from the JSON file."""
        routes = self.load_all_routes()
        stops = set()
        
        for route in routes.values():
            for trip in route.trips:
                for stop in trip.stops:
                    stops.add(stop.name)
        
        return sorted(list(stops))
    
    def search_stops(self, query: str) -> List[str]:
        """Search stops by name."""
        all_stops = self.get_all_stops()
        query_lower = query.lower()
        
        # Exact matches first
        exact_matches = [stop for stop in all_stops if stop.lower() == query_lower]
        
        # Partial matches
        partial_matches = [stop for stop in all_stops 
                          if query_lower in stop.lower() and stop not in exact_matches]
        
        return exact_matches + partial_matches[:10]  # Limit results
    
    def find_routes_between_stops(self, origin: str, destination: str) -> List[Tuple[str, Route]]:
        """Find routes that connect origin and destination."""
        routes = self.load_all_routes()
        connecting_routes = []
        
        for route_key, route in routes.items():
            origin_found = False
            destination_found = False
            origin_sequence = -1
            destination_sequence = -1
            
            for trip in route.trips:
                for stop in trip.stops:
                    if stop.name.lower() == origin.lower():
                        origin_found = True
                        origin_sequence = stop.sequence
                    elif stop.name.lower() == destination.lower():
                        destination_found = True
                        destination_sequence = stop.sequence
                
                if origin_found and destination_found:
                    # Check if direction is correct (origin should come before destination)
                    if origin_sequence < destination_sequence:
                        connecting_routes.append((route_key, route))
                    break
        
        return connecting_routes