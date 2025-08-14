import requests
import json
from datetime import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_stops():
    """Test getting all stops."""
    print("Testing get all stops...")
    response = requests.get(f"{BASE_URL}/stops")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total stops: {data['count']}")
        print(f"First 10 stops: {data['stops'][:10]}")
    else:
        print(f"Error: {response.text}")
    print()

def test_search_stops():
    """Test stop search functionality."""
    print("Testing stop search...")
    test_queries = ["NUST", "Metro", "Station"]
    
    for query in test_queries:
        print(f"Searching for: {query}")
        response = requests.get(f"{BASE_URL}/search-stops", params={"query": query})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['count']} stops: {data['stops']}")
        else:
            print(f"Error: {response.text}")
        print()

def test_plan_route():
    """Test route planning."""
    print("Testing route planning...")
    
    # Test case 1: Direct route
    route_request = {
        "origin": "Nust Metro Station",
        "destination": "Khanna Pul",
        "preferred_time": "08:00:00",
        "max_wait_time": 30
    }
    
    print(f"Planning route: {route_request['origin']} -> {route_request['destination']}")
    response = requests.post(f"{BASE_URL}/plan-route", json=route_request)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Message: {data['message']}")
        if data['route_plans']:
            plan = data['route_plans'][0]
            print(f"Best route duration: {plan['total_duration']} minutes")
            print(f"Instructions: {plan['instructions']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_chat():
    """Test AI chat functionality."""
    print("Testing AI chat...")
    
    chat_message = {
        "message": "Hello! I need help planning my journey from NUST to Khanna Pul. What's the best way to get there?",
        "user_id": "test_user"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=chat_message)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"AI Response: {data['response']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_api_info():
    """Test API info endpoint."""
    print("Testing API info...")
    response = requests.get(f"{BASE_URL}/api-info")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"API Name: {data['name']}")
        print(f"Version: {data['version']}")
        print(f"Description: {data['description']}")
        print(f"Features: {data['features']}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("=== Green Metro Bus Route Planner API Tests ===\n")
    
    try:
        test_health()
        test_get_stops()
        test_search_stops()
        test_plan_route()
        test_chat()
        test_api_info()
        
        print("=== All tests completed ===")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}") 