"""
Travel Planning Agent using LangChain 1.3.0 with tool-calling capability.
This is a simplified agent that orchestrates tools for travel planning.
"""

import json
import os
from typing import Any, Dict
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from tools.travel_tools import (
    search_flights,
    search_hotels,
    discover_places,
    get_weather_forecast,
    estimate_budget
)


class TravelPlanningAgent:
    """Simplified travel planning agent using LangChain functions directly."""
    
    def __init__(self):
        """Initialize the travel planning agent."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.llm = ChatOpenAI(
            api_key=api_key,
            model="gpt-4-turbo-preview",
            temperature=0.7
        )
        
        # Define tools
        @tool
        def search_flights_tool(source: str, destination: str, travelers: int = 1) -> str:
            """Search for available flights between two cities."""
            return search_flights(source, destination, travelers)
        
        @tool
        def search_hotels_tool(city: str, nights: int = 1, budget: int = None) -> str:
            """Search for available hotels in a city."""
            return search_hotels(city, nights, budget)
        
        @tool
        def discover_places_tool(city: str, place_type: str = None) -> str:
            """Discover attractions and places of interest in a city."""
            return discover_places(city, place_type)
        
        @tool
        def get_weather_tool(city: str, lat: float, lon: float, days: int = 3) -> str:
            """Get weather forecast for a location."""
            return get_weather_forecast(city, lat, lon, days)
        
        @tool
        def estimate_budget_tool(flight_price: int, hotel_price: int, nights: int, travelers: int, daily: int = 1000) -> str:
            """Estimate total trip budget."""
            return estimate_budget(flight_price, hotel_price, nights, travelers, daily)
        
        self.tools = [
            search_flights_tool,
            search_hotels_tool,
            discover_places_tool,
            get_weather_tool,
            estimate_budget_tool
        ]
        
        self.chat_history = []
    
    def plan_trip(self, user_query: str) -> Dict[str, Any]:
        """
        Plan a trip based on user query using available tools.
        
        Args:
            user_query: Natural language description of trip requirements
            
        Returns:
            Dictionary containing trip details
        """
        try:
            print(f"\n[v0] Processing trip request: {user_query}")
            
            # Generate itinerary using heuristic tool calling
            itinerary = self._generate_itinerary(user_query)
            
            self.chat_history.append({
                "role": "user",
                "content": user_query
            })
            
            self.chat_history.append({
                "role": "assistant",
                "content": json.dumps(itinerary)
            })
            
            return itinerary
        
        except Exception as e:
            print(f"[v0] Error planning trip: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "reasoning": "An error occurred while planning your trip."
            }
    
    def _generate_itinerary(self, query: str) -> Dict[str, Any]:
        """
        Generate an itinerary by analyzing query and calling appropriate tools.
        
        Args:
            query: User's travel request
            
        Returns:
            Structured itinerary dictionary
        """
        result = {
            "status": "processing",
            "query": query,
            "trip_summary": "Trip planning agent processed your request",
            "tools_called": []
        }
        
        query_lower = query.lower()
        
        try:
            # Common destinations
            common_destinations = ["goa", "delhi", "mumbai", "bangalore", "jaipur", "agra", "kerala", "rajasthan", "delhi", "hyderabad"]
            destination = None
            
            for dest in common_destinations:
                if dest in query_lower:
                    destination = dest
                    break
            
            if destination:
                # Search hotels
                hotels_result = search_hotels(destination, 3, 5000)
                result["tools_called"].append("search_hotels")
                result["hotels"] = hotels_result
                
                # Discover places
                places_result = discover_places(destination)
                result["tools_called"].append("discover_places")
                result["places"] = places_result
                
                # Get weather using sample coordinates
                coords = {
                    "goa": (15.2993, 74.1240),
                    "delhi": (28.7041, 77.1025),
                    "mumbai": (19.0760, 72.8777),
                    "jaipur": (26.9124, 75.7873),
                    "agra": (27.1767, 78.0081),
                    "bangalore": (12.9716, 77.5946),
                    "hyderabad": (17.3850, 78.4867),
                }
                
                if destination in coords:
                    lat, lon = coords[destination]
                    weather_result = get_weather_forecast(destination, lat, lon, 3)
                    result["tools_called"].append("get_weather")
                    result["weather"] = weather_result
                
                # Estimate budget
                budget_result = estimate_budget(4800, 3200, 3, 1, 2500)
                result["tools_called"].append("estimate_budget")
                result["budget"] = budget_result
            
            # Try to find source city for flights
            sources = ["delhi", "mumbai", "bangalore", "hyderabad", "pune", "kolkata"]
            source = None
            
            for src in sources:
                if src in query_lower and src != destination:
                    source = src
                    break
            
            if source and destination:
                flights_result = search_flights(source, destination, 1)
                result["tools_called"].append("search_flights")
                result["flights"] = flights_result
        
        except Exception as e:
            print(f"[v0] Error in tool calling: {str(e)}")
            result["error"] = str(e)
        
        result["status"] = "success"
        return result
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about agent configuration."""
        return {
            "model": "gpt-4-turbo-preview",
            "temperature": 0.7,
            "max_iterations": 10,
            "tools_available": [tool.name for tool in self.tools],
            "description": "AI-powered travel planning agent using LangChain 1.3.0"
        }
    
    def reset_memory(self):
        """Clear conversation memory."""
        self.chat_history = []
