from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import time
from enum import Enum

class Direction(str, Enum):
    FORWARD = "Forward"
    BACKWARD = "Backward"

class MetroLine(str, Enum):
    GREEN = "GREEN"
    BLUE = "BLUE"

class Stop(BaseModel):
    name: str
    arrival_time: Optional[time] = None
    departure_time: Optional[time] = None
    sequence: int

class Trip(BaseModel):
    trip_id: str
    start_time: time
    stops: List[Stop]

class Route(BaseModel):
    route_id: str
    short_name: str
    long_name: str
    direction: Direction
    total_trips: int
    average_headway: int  # in minutes
    trips: List[Trip]

class RoutePlanningRequest(BaseModel):
    origin: str = Field(..., description="Starting location")
    destination: str = Field(..., description="Destination location")
    preferred_time: Optional[time] = Field(None, description="Preferred departure time")
    max_wait_time: int = Field(30, description="Maximum wait time in minutes")
    metro_line: Optional[MetroLine] = Field(None, description="Preferred metro line (GREEN or BLUE)")

class RouteSegment(BaseModel):
    route_name: str
    direction: Direction
    trip_id: str
    start_stop: str
    end_stop: str
    departure_time: time
    arrival_time: time
    duration_minutes: int
    metro_line: Optional[MetroLine] = Field(None, description="Metro line for this segment")

class RoutePlan(BaseModel):
    origin: str
    destination: str
    total_duration: int  # in minutes
    segments: List[RouteSegment]
    total_wait_time: int  # in minutes
    instructions: List[str]
    metro_lines: List[MetroLine] = Field(..., description="Metro lines used in this route")

class RoutePlanningResponse(BaseModel):
    success: bool
    message: str
    route_plans: List[RoutePlan]
    alternative_routes: Optional[List[RoutePlan]] = None

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    preferred_time: Optional[str] = None  # optional, for route planning
    metro_line: Optional[MetroLine] = None  # optional, for line-specific requests

class ChatResponse(BaseModel):
    response: str
    status: str = "success"
    route_suggestion: Optional[RoutePlan] = None

class LineInfo(BaseModel):
    line_code: MetroLine
    name: str
    color: str
    theme_color: str
    total_stops: int

class StopsResponse(BaseModel):
    success: bool
    stops: List[str]
    count: int
    metro_line: Optional[MetroLine] = None 