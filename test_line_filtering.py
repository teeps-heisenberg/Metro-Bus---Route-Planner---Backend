#!/usr/bin/env python3
"""
Test script to verify line filtering is working correctly.
"""

from route_planner import RoutePlanner
from models import MetroLine

def test_line_filtering():
    """Test that line filtering works correctly."""
    planner = RoutePlanner()
    
    print("=== Testing Line Filtering ===\n")
    
    # Test all stops
    print("1. All stops (no filter):")
    all_stops = planner.get_all_stops()
    print(f"   Total: {len(all_stops)} stops")
    print(f"   First 10: {all_stops[:10]}")
    print()
    
    # Test Green Line stops
    print("2. Green Line stops (FRG- routes):")
    green_stops = planner.get_all_stops('GREEN')
    print(f"   Total: {len(green_stops)} stops")
    print(f"   All: {green_stops}")
    print()
    
    # Test Blue Line stops
    print("3. Blue Line stops (FR- routes):")
    blue_stops = planner.get_all_stops('BLUE')
    print(f"   Total: {len(blue_stops)} stops")
    print(f"   First 15: {blue_stops[:15]}")
    print()
    
    # Test route classification
    print("4. Route Classification:")
    routes = planner.route_parser.load_all_routes()
    green_routes = []
    blue_routes = []
    
    for route_key, route in routes.items():
        line = planner._classify_route_line(route.short_name)
        if line == 'GREEN':
            green_routes.append(route.short_name)
        elif line == 'BLUE':
            blue_routes.append(route.short_name)
    
    print(f"   Green Line routes: {green_routes}")
    print(f"   Blue Line routes: {blue_routes}")
    print()
    
    # Test specific route planning
    print("5. Test Route Planning:")
    
    # Test Green Line route
    print("   Green Line: CDA -> PIMS")
    from models import RoutePlanningRequest, MetroLine
    green_request = RoutePlanningRequest(
        origin="CDA",
        destination="PIMS",
        preferred_time=None,
        max_wait_time=60,
        metro_line=MetroLine('GREEN')
    )
    green_routes = planner.plan_route(green_request)
    print(f"   Found {len(green_routes)} routes")
    
    # Test Blue Line route
    print("   Blue Line: Khanna Pul -> NUST")
    blue_request = RoutePlanningRequest(
        origin="Khanna Pul",
        destination="NUST",
        preferred_time=None,
        max_wait_time=60,
        metro_line=MetroLine('BLUE')
    )
    blue_routes = planner.plan_route(blue_request)
    print(f"   Found {len(blue_routes)} routes")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_line_filtering()
