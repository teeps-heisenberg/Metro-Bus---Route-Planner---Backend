from datetime import datetime, time, timedelta
from typing import List, Optional, Tuple
from models import RoutePlan, RouteSegment, RoutePlanningRequest, Trip, Stop, Route
from route_parser import RouteParser

class RoutePlanner:
    def __init__(self):
        self.route_parser = RouteParser()
        
    def _classify_route_line(self, route_short_name: str) -> str:
        """Classify which metro line a route belongs to based on its short name."""
        if route_short_name.startswith('FRG-'):
            return 'GREEN'
        elif route_short_name.startswith('FR-'):
            return 'BLUE'
        else:
            return 'UNKNOWN'
    
    def _filter_routes_by_line(self, routes: List[Tuple[str, Route]], metro_line: Optional[str] = None) -> List[Tuple[str, Route]]:
        """Filter routes by metro line if specified."""
        if not metro_line:
            return routes
        
        filtered_routes = []
        for route_key, route in routes:
            route_line = self._classify_route_line(route.short_name)
            if route_line == metro_line:
                filtered_routes.append((route_key, route))
        
        return filtered_routes
        
    # ---- Time helpers ----
    def minutes_forward(self, from_time: time, to_time: time) -> int:
        """
        Minimal non-negative minutes from from_time -> to_time,
        wrapping to next day if needed (i.e., next occurrence).
        """
        dt1 = datetime.combine(datetime.today(), from_time)
        dt2 = datetime.combine(datetime.today(), to_time)
        if dt2 < dt1:
            dt2 += timedelta(days=1)
        return int((dt2 - dt1).total_seconds() // 60)

    def circular_abs_minutes(self, t1: time, t2: time) -> int:
        """
        Minimal absolute difference in minutes on a 24h circle between t1 and t2.
        e.g., 23:58 and 00:02 -> 4 minutes.
        """
        fwd = self.minutes_forward(t1, t2)
        bwd = self.minutes_forward(t2, t1)
        return min(fwd, bwd)

    def calculate_time_difference(self, time1: time, time2: time) -> int:
        """Backwards-compatible: minutes forward from time1 -> time2 (wrap-safe)."""
        return self.minutes_forward(time1, time2)
    
    def find_best_trip(self, route, origin: str, destination: str, 
                   preferred_time: Optional[time] = None) -> Optional[Tuple[Trip, Stop, Stop]]:
        """Find the best trip for a given route and stops."""
        best_trip = None
        best_origin_stop = None
        best_destination_stop = None

        # Use tuple scoring:
        # If preferred_time: (abs_minutes_to_preferred, journey_minutes)
        # Else: (pseudo_wait_from_06_00, journey_minutes)
        best_score: Tuple[int, int] = (float('inf'), float('inf'))
        
        for trip in route.trips:
            origin_stop = None
            destination_stop = None
            
            # Find origin and destination stops in this trip
            for stop in trip.stops:
                if stop.name.lower() == origin.lower():
                    origin_stop = stop
                elif stop.name.lower() == destination.lower():
                    destination_stop = stop
            
            if origin_stop and destination_stop and origin_stop.sequence < destination_stop.sequence:
                # Journey duration between those two stops
                journey_time = self.calculate_time_difference(
                    origin_stop.departure_time, destination_stop.arrival_time
                )

                if preferred_time:
                    # ABSOLUTE closest to preferred_time (before OR after)
                    fwd = self.calculate_time_difference(preferred_time, origin_stop.departure_time)
                    bwd = self.calculate_time_difference(origin_stop.departure_time, preferred_time)
                    abs_diff = min(fwd, bwd)
                    score = (abs_diff, journey_time)
                else:
                    # No preferred_time: earlier departures (relative to 06:00), then shorter journeys
                    pseudo_wait = self.calculate_time_difference(time(6, 0), origin_stop.departure_time)
                    score = (pseudo_wait, journey_time)
                
                if score < best_score:
                    best_score = score
                    best_trip = trip
                    best_origin_stop = origin_stop
                    best_destination_stop = destination_stop
        
        return (best_trip, best_origin_stop, best_destination_stop) if best_trip else None

    
    def plan_route(self, request: RoutePlanningRequest) -> List[RoutePlan]:
        """Plan routes from origin to destination."""
        connecting_routes = self.route_parser.find_routes_between_stops(
            request.origin, request.destination
        )
        
        # Filter routes by metro line if specified
        if hasattr(request, 'metro_line') and request.metro_line:
            connecting_routes = self._filter_routes_by_line(connecting_routes, request.metro_line.value)
    
        route_plans: List[RoutePlan] = []
        
        for route_key, route in connecting_routes:
            trip_info = self.find_best_trip(
                route, request.origin, request.destination, request.preferred_time
            )
            print(f"trip_info: {trip_info}")  # fixed concat
            if trip_info:
                trip, origin_stop, destination_stop = trip_info
                
                # Journey details
                journey_time = self.calculate_time_difference(
                    origin_stop.departure_time, destination_stop.arrival_time
                )

                # Segment
                segment = RouteSegment(
                    route_name=route.short_name,
                    direction=route.direction,
                    trip_id=trip.trip_id,
                    start_stop=origin_stop.name,
                    end_stop=destination_stop.name,
                    departure_time=origin_stop.departure_time,
                    arrival_time=destination_stop.arrival_time,
                    duration_minutes=journey_time,
                    metro_line=request.metro_line.value if request.metro_line else None
                )
                
                # Instructions
                instructions = [
                    f"Take {route.short_name} ({route.long_name}) from {origin_stop.name}",
                    f"Departure time: {origin_stop.departure_time.strftime('%H:%M')}",
                    f"Arrive at {destination_stop.name} at {destination_stop.arrival_time.strftime('%H:%M')}",
                    f"Journey duration: {journey_time} minutes"
                ]
                
                # Wait metric for sorting when preferred_time is provided:
                # use absolute closeness (before OR after)
                wait_time = 0
                if request.preferred_time:
                    fwd = self.calculate_time_difference(request.preferred_time, origin_stop.departure_time)
                    bwd = self.calculate_time_difference(origin_stop.departure_time, request.preferred_time)
                    wait_time = min(fwd, bwd)
                    print(f"wait_time: {wait_time}")  # fixed concat
                
                route_plan = RoutePlan(
                    origin=request.origin,
                    destination=request.destination,
                    total_duration=journey_time + wait_time,
                    segments=[segment],
                    total_wait_time=wait_time,
                    instructions=instructions,
                    metro_lines=[request.metro_line] if request.metro_line else []
                )
                
                route_plans.append(route_plan)
        
        # Sort & return
        if request.preferred_time:
            # Primary: absolute closeness to preferred_time; Secondary: shortest journey
            route_plans.sort(key=lambda x: (x.total_wait_time, x.segments[0].duration_minutes))
            return route_plans[:5]  # return top 5 closest instead of just one
        else:
            route_plans.sort(key=lambda x: x.total_duration)
            return route_plans[:5]

    
    def get_all_stops(self, metro_line: Optional[str] = None) -> List[str]:
        """Get all available stops, optionally filtered by metro line."""
        all_stops = self.route_parser.get_all_stops()
        
        if not metro_line:
            return all_stops
        
        # Filter stops by checking which routes they appear in
        filtered_stops = set()
        routes = self.route_parser.load_all_routes()
        
        for route_key, route in routes.items():
            route_line = self._classify_route_line(route.short_name)
            if route_line == metro_line:
                for trip in route.trips:
                    for stop in trip.stops:
                        filtered_stops.add(stop.name)
        
        return sorted(list(filtered_stops))
    
    def search_stops(self, query: str, metro_line: Optional[str] = None) -> List[str]:
        """Search stops by name, optionally filtered by metro line."""
        all_stops = self.get_all_stops(metro_line)
        query_lower = query.lower()
        
        # Exact matches first
        exact_matches = [stop for stop in all_stops if stop.lower() == query_lower]
        
        # Partial matches
        partial_matches = [stop for stop in all_stops 
                          if query_lower in stop.lower() and stop not in exact_matches]
        
        return exact_matches + partial_matches[:10]  # Limit results
