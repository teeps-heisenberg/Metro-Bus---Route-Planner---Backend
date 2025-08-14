import os
import shapefile
from supabase import create_client, Client

# --- CONFIGURATION ---
SUPABASE_URL = "https://cpgehduezbtpbpclalei.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNwZ2VoZHVlemJ0cGJwY2xhbGVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUxMjI0MDksImV4cCI6MjA3MDY5ODQwOX0.h74wjTUcoKeuNEnZrc7aWGt4ZDs1dRvAf4xzd18JaDg"

# Table name in Supabase
TABLE_NAME = "metro_stops"

# Paths to shapefiles (without .shp extension)
SHAPEFILES = [
    (os.path.join('data', 'green_line', 'GREEN_STATIONS'), 'GREEN'),
    (os.path.join('data', 'blue_line', 'BLUE_STATIONS'), 'BLUE'),
]

# --- MAIN LOGIC ---
def extract_stops(shapefile_path, line_code):
    stops = []
    try:
        sf = shapefile.Reader(shapefile_path)
        fields = [field[0] for field in sf.fields[1:]]
        records = sf.records()
        shapes = sf.shapes()
        for record, shape in zip(records, shapes):
            station_name = record[fields.index('sta_name')]
            station_id = str(record[fields.index('id')])
            is_interchange = bool(record[fields.index('interchg')])
            coords = shape.points[0] if shape.points else (None, None)
            stop = {
                "id": station_id,
                "name": station_name,
                "line_code": line_code,
                "is_interchange": is_interchange,
                "latitude": coords[1],
                "longitude": coords[0],
                "line_name": "Green Line" if line_code == "GREEN" else "Blue Line"
            }
            stops.append(stop)
    except Exception as e:
        print(f"[ERROR] Failed to extract stops from {shapefile_path}: {e}")
    return stops

def upload_stops_to_supabase(stops, supabase: Client):
    for stop in stops:
        try:
            # Upsert to avoid duplicates
            supabase.table(TABLE_NAME).upsert(stop).execute()
            print(f"[OK] Uploaded: {stop['name']} ({stop['line_code']})")
        except Exception as e:
            print(f"[ERROR] Failed to upload {stop['name']} ({stop['line_code']}): {e}")

def main():
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("[ERROR] Please set SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables.")
        return
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    all_stops = []
    for shapefile_path, line_code in SHAPEFILES:
        if os.path.exists(shapefile_path + '.shp'):
            stops = extract_stops(shapefile_path, line_code)
            print(f"[INFO] Extracted {len(stops)} stops for {line_code} line.")
            all_stops.extend(stops)
        else:
            print(f"[WARN] Shapefile not found: {shapefile_path}.shp")
    if all_stops:
        upload_stops_to_supabase(all_stops, supabase)
        print(f"[DONE] Uploaded {len(all_stops)} stops to Supabase.")
    else:
        print("[ERROR] No stops extracted. Nothing uploaded.")

if __name__ == "__main__":
    main()

"""
Instructions:
1. Install dependencies:
   pip install pyshp supabase
2. Set your Supabase credentials as environment variables:
   - SUPABASE_URL
   - SUPABASE_SERVICE_KEY
3. Run the script:
   python upload_stops_to_supabase.py
"""
