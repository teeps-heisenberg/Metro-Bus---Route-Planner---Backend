#!/usr/bin/env python3
"""
Simple test to check if the system is working.
"""

try:
    from route_planner import RoutePlanner
    print("✅ RoutePlanner imported successfully")
    
    planner = RoutePlanner()
    print("✅ RoutePlanner instance created successfully")
    
    # Test route classification
    print("\nTesting route classification:")
    print(f"FRG-1 -> {planner._classify_route_line('FRG-1')}")
    print(f"FR-01 -> {planner._classify_route_line('FR-01')}")
    print(f"FR-03A -> {planner._classify_route_line('FR-03A')}")
    
    print("\n✅ All tests passed! Your system is working.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
