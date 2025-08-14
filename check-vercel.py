import os
from pathlib import Path
import json

# This is the same logic you use in __init__
json_file_path = os.path.join(os.path.dirname(__file__), "routes_analysis.json")

print(f"Looking for file at: {json_file_path}")

# Check existence
if not os.path.exists(json_file_path):
    print("❌ File not found! Make sure it's in the same folder and committed to git.")
else:
    print("✅ File exists!")

    # Try reading it
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("✅ File loaded successfully!")
        print(f"First 200 chars: {json.dumps(data)[:200]}...")
    except Exception as e:
        print("❌ Failed to read file:", e)

# Extra: Confirm current working directory
print(f"Current working directory: {os.getcwd()}")
