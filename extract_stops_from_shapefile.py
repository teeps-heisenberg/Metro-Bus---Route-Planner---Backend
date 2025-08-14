import shapefile
import os

# Paths to shapefiles (without .shp extension for pyshp)
green_shapefile = os.path.join('data', 'green_line', 'GREEN_STATIONS')
blue_shapefile = os.path.join('data', 'blue_line', 'BLUE_STATIONS')

def extract_stops(shapefile_path, line_name):
    print(f'\nStops for {line_name}:')
    try:
        # Read the shapefile
        sf = shapefile.Reader(shapefile_path)
        
        # Get field names (column headers)
        fields = [field[0] for field in sf.fields[1:]]  # Skip first field (deletion flag)
        print(f'Columns: {fields}')
        
        # Get all records (rows)
        records = sf.records()
        shapes = sf.shapes()
        
        print(f'Total stops found: {len(records)}')
        
        # Print each stop
        for i, (record, shape) in enumerate(zip(records, shapes)):
            # Get station name from sta_name field
            station_name = record[fields.index('sta_name')] if 'sta_name' in fields else f"Station_{i+1}"
            station_id = record[fields.index('id')] if 'id' in fields else i+1
            line_code = record[fields.index('line_code')] if 'line_code' in fields else 'Unknown'
            is_interchange = record[fields.index('interchg')] if 'interchg' in fields else False
            
            # Get coordinates
            if shape.points:
                coords = shape.points[0]  # First point
                interchange_info = " (Interchange)" if is_interchange else ""
                print(f'- ID: {station_id}, Name: {station_name}, Line: {line_code}{interchange_info}')
                print(f'  Coordinates: ({coords[0]:.6f}, {coords[1]:.6f})')
            else:
                print(f'- ID: {station_id}, Name: {station_name}, Line: {line_code} (No coordinates)')
                
    except Exception as e:
        print(f'Error reading {line_name}: {e}')

def main():
    if os.path.exists(green_shapefile + '.shp'):
        extract_stops(green_shapefile, 'Green Line')
    else:
        print('Green Line shapefile not found.')
        
    if os.path.exists(blue_shapefile + '.shp'):
        extract_stops(blue_shapefile, 'Blue Line')
    else:
        print('Blue Line shapefile not found.')

if __name__ == '__main__':
    main()
