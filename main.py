from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, time
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv
from google.genai import types

# Load environment variables from .env file
load_dotenv()

from models import (
    RoutePlanningRequest, RoutePlanningResponse, ChatMessage, 
    ChatResponse, RoutePlan, MetroLine, LineInfo, StopsResponse
)
from route_planner import RoutePlanner
from ai_assistant import AIAssistant

# Initialize FastAPI app
app = FastAPI(
    title="Green Metro Bus Route Planner",
    description="AI-powered route planning system for Green Metro Bus in Islamabad",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
route_planner = RoutePlanner()
ai_assistant = AIAssistant()

# Basic health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Green Metro Bus Route Planner API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "green-metro-route-planner",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/check-routes-file")
def check_routes_file():
    json_file_path = os.path.join(os.path.dirname(__file__), "routes_analysis.json")

    if not os.path.exists(json_file_path):
        return {"exists": False, "message": "File not found."}

    try:
        size_bytes = os.path.getsize(json_file_path)
        with open(json_file_path, "r", encoding="utf-8") as f:
            content_preview = f.read(200)  # first 200 characters
        return {
            "exists": True,
            "size_bytes": size_bytes,
            "content_preview": content_preview
        }
    except Exception as e:
        return {"exists": True, "error": str(e)}

# Route planning endpoints
@app.post("/plan-route", response_model=RoutePlanningResponse)
async def plan_route(request: RoutePlanningRequest):
    """Plan routes from origin to destination."""
    try:
        route_plans = route_planner.plan_route(request)
        
        if not route_plans:
            return RoutePlanningResponse(
                success=False,
                message="No routes found between the specified locations. Please check the stop names and try again.",
                route_plans=[]
            )
        
        return RoutePlanningResponse(
            success=True,
            message=f"Found {len(route_plans)} route(s) from {request.origin} to {request.destination}",
            route_plans=route_plans
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error planning route: {str(e)}")

@app.get("/stops", response_model=StopsResponse)
async def get_all_stops(metro_line: Optional[MetroLine] = Query(None, description="Filter stops by metro line")):
    """Get all available stops, optionally filtered by metro line."""
    try:
        if metro_line:
            # Use route planner for line-specific filtering (maintains route compatibility)
            stops = route_planner.get_all_stops(metro_line.value)
        else:
            # Use original route planner for all stops (maintains compatibility)
            stops = route_planner.get_all_stops()
        
        return StopsResponse(
            success=True,
            stops=stops,
            count=len(stops),
            metro_line=metro_line
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stops: {str(e)}")

@app.get("/search-stops")
async def search_stops(
    query: str = Query(..., min_length=2),
    metro_line: Optional[MetroLine] = Query(None, description="Filter stops by metro line")
):
    """Search stops by name, optionally filtered by metro line."""
    try:
        if metro_line:
            # Use route planner for line-specific filtering (maintains route compatibility)
            stops = route_planner.search_stops(query, metro_line.value)
        else:
            # Use original route planner for search (maintains compatibility)
            stops = route_planner.search_stops(query)
        
        return {
            "success": True,
            "query": query,
            "stops": stops,
            "count": len(stops),
            "metro_line": metro_line
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching stops: {str(e)}")

@app.get("/lines", response_model=List[LineInfo])
async def get_available_lines():
    """Get information about all available metro lines."""
    try:
        # Create line info based on route classification
        lines = []
        
        # Get all routes to classify them
        routes = route_planner.route_parser.load_all_routes()
        green_stops = set()
        blue_stops = set()
        
        for route_key, route in routes.items():
            line = route_planner._classify_route_line(route.short_name)
            if line == 'GREEN':
                for trip in route.trips:
                    for stop in trip.stops:
                        green_stops.add(stop.name)
            elif line == 'BLUE':
                for trip in route.trips:
                    for stop in trip.stops:
                        blue_stops.add(stop.name)
        
        # Green Line
        lines.append(LineInfo(
            line_code=MetroLine('GREEN'),
            name="Green Line",
            color="#22c55e",
            theme_color="green",
            total_stops=len(green_stops)
        ))
        
        # Blue Line
        lines.append(LineInfo(
            line_code=MetroLine('BLUE'),
            name="Blue Line", 
            color="#3b82f6",
            theme_color="blue",
            total_stops=len(blue_stops)
        ))
        
        return lines
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lines: {str(e)}")

@app.get("/line/{line_code}", response_model=LineInfo)
async def get_line_info(line_code: MetroLine):
    """Get information about a specific metro line."""
    try:
        # Get line info based on route classification
        routes = route_planner.route_parser.load_all_routes()
        line_stops = set()
        
        for route_key, route in routes.items():
            line = route_planner._classify_route_line(route.short_name)
            if line == line_code.value:
                for trip in route.trips:
                    for stop in trip.stops:
                        line_stops.add(stop.name)
        
        if line_code.value == 'GREEN':
            line_info = {
                'name': 'Green Line',
                'color': '#22c55e',
                'theme_color': 'green'
            }
        elif line_code.value == 'BLUE':
            line_info = {
                'name': 'Blue Line',
                'color': '#3b82f6', 
                'theme_color': 'blue'
            }
        else:
            raise HTTPException(status_code=404, detail=f"Line {line_code} not found")
        
        return LineInfo(
            line_code=line_code,
            name=line_info['name'],
            color=line_info['color'],
            theme_color=line_info['theme_color'],
            total_stops=len(line_stops)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching line info: {str(e)}")

# AI Assistant endpoints
@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat with the AI travel assistant."""
    try:
        # First, let the AI analyze the message and extract locations if it's a route request
        # Use route planner stops for compatibility with actual routes
        if hasattr(message, 'metro_line') and message.metro_line:
            available_stops = route_planner.get_all_stops(message.metro_line.value)
        else:
            available_stops = route_planner.get_all_stops()
        
        analysis_prompt = f"""
Analyze this user message and determine if it's a route planning request.

User message: "{message.message}"

Available stops in our system: {', '.join(available_stops)}

Please respond in this exact JSON format:
{{
    "is_route_request": true/false,
    "origin": "extracted_origin_stop_name_or_null",
    "destination": "extracted_destination_stop_name_or_null",
    "confidence": "high/medium/low",
    "reasoning": "brief explanation of your analysis"
}}

If it's a route request, try to match the mentioned locations to our available stops. 
If it's not a route request, set is_route_request to false and origin/destination to null.
"""

        try:
            # Get AI analysis of the message
            analysis_response = ai_assistant.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=analysis_prompt
            )
            
            # Parse the AI response
            import json
            analysis_text = analysis_response.text.strip()
            
            # Clean up the response (remove markdown if present)
            if analysis_text.startswith("```json"):
                analysis_text = analysis_text[7:]
            if analysis_text.endswith("```"):
                analysis_text = analysis_text[:-3]
            
            analysis = json.loads(analysis_text)
            
            # If it's a route request with high/medium confidence, try to plan the route
            if analysis.get("is_route_request") and analysis.get("confidence") in ["high", "medium"]:
                origin = analysis.get("origin")
                destination = analysis.get("destination")
                
                if origin and destination:
                    try:
                        # Use preferred_time from user if provided, else current time
                        from datetime import datetime
                        preferred_time = None
                        if hasattr(message, 'preferred_time') and message.preferred_time:
                            preferred_time = message.preferred_time
                        else:
                            preferred_time = datetime.now().strftime("%H:%M:%S")
                        
                        # Create route request with line preference if specified
                        route_request = RoutePlanningRequest(
                            origin=origin,
                            destination=destination,
                            preferred_time=preferred_time,
                            max_wait_time=60,
                            metro_line=message.metro_line
                        )
                        
                        route_plans = route_planner.plan_route(route_request)
                        
                        if route_plans:
                            # Get AI explanation of the route
                            explanation = ai_assistant.explain_route(route_plans[0])
                            
                            return ChatResponse(
                                response=explanation,
                                status="success",
                                route_suggestion=route_plans[0]
                            )
                        # If no route for preferred time, try without preferred_time
                        route_request_no_time = RoutePlanningRequest(
                            origin=origin,
                            destination=destination,
                            preferred_time=None,
                            max_wait_time=60,
                            metro_line=message.metro_line
                        )
                        route_plans_no_time = route_planner.plan_route(route_request_no_time)
                        if route_plans_no_time:
                            explanation = ai_assistant.explain_route(route_plans_no_time[0])
                            return ChatResponse(
                                response=f"No route was found at your preferred time, but here is the next available route:\n\n" + explanation,
                                status="success",
                                route_suggestion=route_plans_no_time[0]
                            )
                        # No route at all, fallback to friendly AI message
                        no_route_prompt = f"""
The user asked for a route from "{origin}" to "{destination}" but no route was found.

Available stops: {', '.join(available_stops)}

Please provide a helpful response that:
1. Acknowledges their request
2. Suggests they check the spelling of stop names
3. Mentions they can search for available stops
4. Offers to help with other questions

Be friendly and encouraging.
"""
                        
                        response = ai_assistant.client.models.generate_content(
                            model="gemini-2.0-flash-exp",
                            config=types.GenerateContentConfig(
                                system_instruction=ai_assistant.system_prompt
                            ),
                            contents=no_route_prompt
                        )
                        
                        return ChatResponse(
                            response=response.text,
                            status="success"
                        )
                        
                    except Exception as route_error:
                        print(f"Route planning error: {route_error}")
                        # Fall back to general AI response
                        response = ai_assistant.handle_general_query(message.message)
                        return ChatResponse(
                            response=response,
                            status="success"
                        )
                else:
                    # AI couldn't extract locations clearly, ask for clarification
                    clarification_prompt = f"""
The user seems to be asking about a route, but I couldn't clearly identify the origin and destination.

User message: "{message.message}"
Available stops: {', '.join(available_stops)}

Please ask them to clarify their origin and destination, and mention they can search for available stops.
"""
                    
                    response = ai_assistant.client.models.generate_content(
                        model="gemini-2.0-flash-exp",
                        config=types.GenerateContentConfig(
                            system_instruction=ai_assistant.system_prompt
                        ),
                        contents=clarification_prompt
                    )
                    
                    return ChatResponse(
                        response=response.text,
                        status="success"
                    )
            else:
                # Not a route request, handle as general conversation
                response = ai_assistant.handle_general_query(message.message)
                
                return ChatResponse(
                    response=response,
                    status="success"
                )
                
        except Exception as ai_error:
            print(f"AI analysis error: {ai_error}")
            # Fall back to general AI response
            response = ai_assistant.handle_general_query(message.message)
            return ChatResponse(
                response=response,
                status="success"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@app.post("/explain-route")
async def explain_route(route_plan: RoutePlan):
    """Get AI explanation of a route plan."""
    try:
        explanation = ai_assistant.explain_route(route_plan)
        
        return {
            "success": True,
            "explanation": explanation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error explaining route: {str(e)}")

@app.post("/travel-tips")
async def get_travel_tips(route_plan: RoutePlan):
    """Get travel tips for a route plan."""
    try:
        tips = ai_assistant.get_travel_tips(route_plan)
        
        return {
            "success": True,
            "tips": tips
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting travel tips: {str(e)}")

# Utility endpoints
@app.get("/api-info")
async def get_api_info():
    """Get API information and available endpoints."""
    return {
        "name": "Green Metro Bus Route Planner",
        "version": "1.0.0",
        "description": "AI-powered route planning system for Green Metro Bus in Islamabad",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Root endpoint"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/plan-route", "method": "POST", "description": "Plan routes between stops"},
            {"path": "/stops", "method": "GET", "description": "Get all available stops"},
            {"path": "/search-stops", "method": "GET", "description": "Search stops by name"},
            {"path": "/lines", "method": "GET", "description": "Get all available metro lines"},
            {"path": "/line/{line_code}", "method": "GET", "description": "Get specific line information"},
            {"path": "/chat", "method": "POST", "description": "Chat with AI travel assistant"},
            {"path": "/explain-route", "method": "POST", "description": "Get AI explanation of route"},
            {"path": "/travel-tips", "method": "POST", "description": "Get travel tips for route"}
        ],
        "features": [
            "Route planning between any two stops",
            "Multi-line support (Green Line, Blue Line)",
            "AI-powered travel assistance",
            "Real-time route optimization",
            "Travel tips and explanations",
            "Stop search functionality",
            "Line-specific filtering"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
