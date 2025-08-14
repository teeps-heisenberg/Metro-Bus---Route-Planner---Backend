import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from typing import List, Optional
from models import RoutePlan, ChatMessage, ChatResponse
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

class AIAssistant:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not set. AI features will be limited.")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
        
        # System prompt for the conductor/travel guide
        self.system_prompt = """You are a friendly and knowledgeable conductor/travel guide for the Green Metro Bus system in Islamabad, Pakistan. 

Your role is to:
1. Help passengers find the best routes between locations
2. Provide clear, step-by-step travel instructions
3. Explain bus schedules and timing
4. Offer helpful travel tips and advice
5. Be patient and understanding with passenger questions
6. Use simple, clear language that everyone can understand
7. Provide information about stops, transfers, and journey times
8. Be encouraging and make passengers feel confident about their journey

Always be:
- Polite and professional
- Clear and concise
- Helpful and informative
- Patient with questions
- Encouraging about public transport use

When providing route information, include:
- Clear departure and arrival times
- Journey duration
- Any transfers needed
- Important landmarks or stops to watch for
- Tips for a comfortable journey

Remember: You're helping people navigate the city safely and efficiently!"""

    def generate_response(self, message: str, route_plan: Optional[RoutePlan] = None) -> str:
        """Generate a response using Gemini AI."""
        if not self.client:
            return "I'm sorry, but the AI assistant is currently not available. Please set the GEMINI_API_KEY environment variable to enable AI features. For now, you can use the route planning features directly."
        
        try:
            # Prepare the content
            content = message
            
            # If we have a route plan, include it in the context
            if route_plan:
                route_context = self._format_route_for_ai(route_plan)
                content += f"\n\nRoute Information:\n{route_context}"
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt
                ),
                contents=content
            )
            
            return response.text
            
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request right now. Please try again or contact support if the issue persists. Error: {str(e)}"
    
    def _format_route_for_ai(self, route_plan: RoutePlan) -> str:
        """Format route plan information for AI context."""
        formatted = f"""
Journey Details:
- From: {route_plan.origin}
- To: {route_plan.destination}
- Total Duration: {route_plan.total_duration} minutes
- Wait Time: {route_plan.total_wait_time} minutes

Route Instructions:
"""
        
        for i, segment in enumerate(route_plan.segments, 1):
            formatted += f"""
Step {i}:
- Route: {segment.route_name} ({segment.direction.value})
- From: {segment.start_stop}
- To: {segment.end_stop}
- Departure: {segment.departure_time.strftime('%H:%M')}
- Arrival: {segment.arrival_time.strftime('%H:%M')}
- Duration: {segment.duration_minutes} minutes
"""
        
        formatted += f"""
Detailed Instructions:
"""
        for instruction in route_plan.instructions:
            formatted += f"- {instruction}\n"
        
        return formatted
    
    def get_travel_tips(self, route_plan: RoutePlan) -> str:
        """Generate travel tips for a specific route."""
        tips_prompt = f"""
Based on this route plan, provide helpful travel tips for the passenger:

{self._format_route_for_ai(route_plan)}

Please provide:
1. 2-3 practical travel tips
2. What to expect during the journey
3. Any important reminders
4. Encouraging words about using public transport

Keep it friendly and helpful!
"""
        
        return self.generate_response(tips_prompt)
    
    def explain_route(self, route_plan: RoutePlan) -> str:
        """Provide a detailed explanation of the route."""
        explain_prompt = f"""
Please explain this route plan in a clear, friendly way as if you're a helpful conductor:

{self._format_route_for_ai(route_plan)}

Explain:
1. The overall journey
2. What the passenger should expect
3. Any important details about timing
4. How to identify their stops
5. What to do if they miss their stop

Make it sound like you're personally helping them with their journey!
"""
        
        return self.generate_response(explain_prompt)
    
    def handle_general_query(self, message: str) -> str:
        """Handle general queries about the metro system."""
        general_prompt = f"""
A passenger is asking: "{message}"

As a helpful and knowledgeable conductor for the Green Metro Bus system in Islamabad, please provide a friendly and informative response.

Available information:
- We have comprehensive route coverage across Islamabad
- Real-time route planning with current timing
- Multiple routes and transfer options
- Detailed stop information

If they're asking about routes, suggest they can:
1. Use the route planner for specific origin-destination queries
2. Ask me directly like "What's the route from Khanna to NUST?"
3. Search for available stops

If it's a general question about the metro system, provide helpful information and encourage them to use our services.

Keep your response conversational, friendly, and encouraging about using public transport!
"""
        
        return self.generate_response(general_prompt) 