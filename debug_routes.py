from route_parser import RouteParser
from route_planner import RoutePlanner

def debug_route_finding():
    """Debug the route finding functionality."""
    print("=== Route Finding Debug ===\n")
    
    # Initialize parser and planner
    parser = RouteParser()
    planner = RoutePlanner()
    
    # Load all routes
    print("Loading routes...")
    routes = parser.load_all_routes()
    print(f"Loaded {len(routes)} routes\n")
    
    # Get all stops
    print("Getting all stops...")
    stops = parser.get_all_stops()
    print(f"Total stops: {len(stops)}")
    print(f"First 20 stops: {stops[:20]}\n")
    
    # Test specific route finding
    test_cases = [
        ("NUST", "Khanna"),
        ("Airport", "Bank"),
        ("Nust Metro Station", "Khanna Pul"),
        ("Nust", "Khanna")
    ]
    
    for origin, destination in test_cases:
        print(f"Testing route: {origin} -> {destination}")
        
        # Check if stops exist
        origin_exists = any(stop.lower() == origin.lower() for stop in stops)
        dest_exists = any(stop.lower() == destination.lower() for stop in stops)
        
        print(f"  Origin '{origin}' exists: {origin_exists}")
        print(f"  Destination '{destination}' exists: {dest_exists}")
        
        if origin_exists and dest_exists:
            # Find connecting routes
            connecting_routes = parser.find_routes_between_stops(origin, destination)
            print(f"  Connecting routes found: {len(connecting_routes)}")
            
            for route_key, route in connecting_routes:
                print(f"    Route: {route_key} - {route.long_name}")
                
                # Check if stops are in the route
                for trip in route.trips[:1]:  # Check first trip only
                    origin_stop = None
                    dest_stop = None
                    
                    for stop in trip.stops:
                        if stop.name.lower() == origin.lower():
                            origin_stop = stop
                        elif stop.name.lower() == destination.lower():
                            dest_stop = stop
                    
                    if origin_stop and dest_stop:
                        print(f"      Origin stop: {origin_stop.name} (seq: {origin_stop.sequence})")
                        print(f"      Dest stop: {dest_stop.name} (seq: {dest_stop.sequence})")
                        print(f"      Direction correct: {origin_stop.sequence < dest_stop.sequence}")
        else:
            print("  Cannot find route - stops don't exist")
        
        print()

if __name__ == "__main__":
    debug_route_finding() 