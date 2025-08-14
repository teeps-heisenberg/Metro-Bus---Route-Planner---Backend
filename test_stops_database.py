from stops_database import stops_db

def test_stops_database():
    print("=== Testing Stops Database ===\n")
    
    # Test 1: Get all available lines
    print("1. Available Lines:")
    lines = stops_db.get_available_lines()
    for line in lines:
        line_info = stops_db.get_line_info(line)
        print(f"   - {line}: {line_info['name']} (Theme: {line_info['theme_color']})")
    
    print(f"\n2. Total Stations: {len(stops_db.stations)}")
    
    # Test 2: Get stops for each line
    print("\n3. Stops by Line:")
    for line in lines:
        line_stops = stops_db.get_all_stops(line)
        print(f"\n   {line} Line ({len(line_stops)} stops):")
        for stop in line_stops:
            station_info = stops_db.get_station_info(stop)
            interchange_marker = " 🔄" if station_info.is_interchange else ""
            print(f"     - {stop}{interchange_marker}")
    
    # Test 3: Test interchange detection
    print("\n4. Interchange Stations:")
    interchange_stations = [name for name, station in stops_db.stations.items() 
                           if station.is_interchange]
    for station_name in interchange_stations:
        station = stops_db.get_station_info(station_name)
        print(f"   - {station_name}: {station.line_code}")
    
    # Test 4: Test search functionality
    print("\n5. Search Test:")
    search_results = stops_db.search_stops("PIMS")
    print(f"   Searching for 'PIMS': {search_results}")
    
    # Test 5: Line-specific search
    print("\n6. Line-Specific Search:")
    green_pims = stops_db.search_stops("PIMS", "GREEN")
    blue_pims = stops_db.search_stops("PIMS", "BLUE")
    print(f"   PIMS in Green Line: {green_pims}")
    print(f"   PIMS in Blue Line: {blue_pims}")

if __name__ == "__main__":
    test_stops_database()
