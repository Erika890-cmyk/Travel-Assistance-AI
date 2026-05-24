import requests
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
from langchain_core.tools import tool
from utils.data_loader import load_all_data


# Load data once
_travel_data = load_all_data()


def search_flights(source: str, destination: str, number_of_travelers: int = 1) -> str:
    """Search for available flights from source to destination.
    
    Args:
        source: Departure city
        destination: Arrival city
        number_of_travelers: Number of passengers
        
    Returns:
        JSON string with available flights or error message
    """
    try:
        flights = _travel_data.get("flights", [])
        
        # Filter flights
        matching_flights = [
            f for f in flights 
            if f.get("source", "").lower() == source.lower() 
            and f.get("destination", "").lower() == destination.lower()
            and f.get("seats_available", 0) >= number_of_travelers
        ]
        
        if not matching_flights:
            return json.dumps({
                "status": "no_flights",
                "message": f"No flights found from {source} to {destination} for {number_of_travelers} travelers."
            })
        
        # Sort by price (cheapest first)
        matching_flights.sort(key=lambda x: x.get("price", float('inf')))
        
        result = {
            "status": "success",
            "source": source,
            "destination": destination,
            "number_of_travelers": number_of_travelers,
            "flights_found": len(matching_flights),
            "flights": [
                {
                    "id": f.get("id"),
                    "airline": f.get("airline"),
                    "departure_time": f.get("departure_time"),
                    "arrival_time": f.get("arrival_time"),
                    "price": f.get("price"),
                    "duration_minutes": f.get("duration_minutes"),
                    "seats_available": f.get("seats_available"),
                    "total_price": f.get("price", 0) * number_of_travelers
                }
                for f in matching_flights[:5]  # Return top 5 options
            ]
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def search_hotels(destination: str, number_of_nights: int = 1, budget: int = None) -> str:
    """Search for hotels in a destination city.
    
    Args:
        destination: City name
        number_of_nights: Number of nights to stay
        budget: Maximum price per night (optional)
        
    Returns:
        JSON string with available hotels or error message
    """
    try:
        hotels = _travel_data.get("hotels", [])
        
        # Filter hotels by destination
        matching_hotels = [
            h for h in hotels 
            if h.get("city", "").lower() == destination.lower()
        ]
        
        # Filter by budget if provided
        if budget:
            matching_hotels = [h for h in matching_hotels if h.get("price_per_night", float('inf')) <= budget]
        
        if not matching_hotels:
            return json.dumps({
                "status": "no_hotels",
                "message": f"No hotels found in {destination}" + (f" within budget ₹{budget}" if budget else "")
            })
        
        # Sort by rating (highest first)
        matching_hotels.sort(key=lambda x: x.get("rating", 0), reverse=True)
        
        result = {
            "status": "success",
            "destination": destination,
            "number_of_nights": number_of_nights,
            "hotels_found": len(matching_hotels),
            "hotels": [
                {
                    "id": h.get("id"),
                    "name": h.get("name"),
                    "rating": h.get("rating"),
                    "price_per_night": h.get("price_per_night"),
                    "total_for_stay": h.get("price_per_night", 0) * number_of_nights,
                    "rooms_available": h.get("rooms_available"),
                    "amenities": h.get("amenities", [])
                }
                for h in matching_hotels[:5]  # Return top 5 options
            ]
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def discover_places(destination: str, place_type: str = None) -> str:
    """Discover tourist attractions and places of interest in a destination.
    
    Args:
        destination: City name
        place_type: Type of place (Beach, Heritage, Adventure, etc.) - optional
        
    Returns:
        JSON string with places and attractions or error message
    """
    try:
        places = _travel_data.get("places", [])
        
        # Filter by destination
        matching_places = [
            p for p in places 
            if p.get("city", "").lower() == destination.lower()
        ]
        
        # Filter by place type if provided
        if place_type:
            matching_places = [
                p for p in matching_places 
                if p.get("type", "").lower() == place_type.lower()
            ]
        
        if not matching_places:
            return json.dumps({
                "status": "no_places",
                "message": f"No attractions found in {destination}" + (f" of type {place_type}" if place_type else "")
            })
        
        # Sort by rating
        matching_places.sort(key=lambda x: x.get("rating", 0), reverse=True)
        
        result = {
            "status": "success",
            "destination": destination,
            "place_type": place_type or "All",
            "places_found": len(matching_places),
            "places": [
                {
                    "name": p.get("name"),
                    "type": p.get("type"),
                    "rating": p.get("rating"),
                    "description": p.get("description"),
                    "entry_fee": p.get("entry_fee"),
                    "duration_hours": p.get("duration_hours"),
                    "best_time": p.get("best_time")
                }
                for p in matching_places
            ]
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def get_weather_forecast(city: str, latitude: float, longitude: float, days: int = 3) -> str:
    """Get weather forecast for a destination using Open-Meteo API.
    
    Args:
        city: City name
        latitude: Latitude of the city
        longitude: Longitude of the city
        days: Number of days to forecast
        
    Returns:
        JSON string with weather forecast or error message
    """
    try:
        # Open-Meteo API call (free, no API key required)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract weather data
        daily_data = data.get("daily", {})
        temps_max = daily_data.get("temperature_2m_max", [])
        temps_min = daily_data.get("temperature_2m_min", [])
        weather_codes = daily_data.get("weather_code", [])
        
        weather_descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            61: "Slight rain",
            71: "Slight snow",
            80: "Moderate rain",
            95: "Thunderstorm"
        }
        
        forecasts = []
        for i in range(min(days, len(temps_max))):
            weather_code = weather_codes[i] if i < len(weather_codes) else 0
            forecasts.append({
                "day": i + 1,
                "max_temp": temps_max[i] if i < len(temps_max) else "N/A",
                "min_temp": temps_min[i] if i < len(temps_min) else "N/A",
                "condition": weather_descriptions.get(weather_code, "Unknown")
            })
        
        result = {
            "status": "success",
            "city": city,
            "days": days,
            "forecast": forecasts
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Weather API error: {str(e)}"})


def estimate_budget(flight_price: int, hotel_price_per_night: int, number_of_nights: int, 
                   number_of_travelers: int, daily_expenses: int = 1000) -> str:
    """Estimate total trip budget.
    
    Args:
        flight_price: Price of one flight ticket
        hotel_price_per_night: Hotel price per night
        number_of_nights: Number of nights
        number_of_travelers: Number of travelers
        daily_expenses: Daily expenses per person (food, transport, etc.)
        
    Returns:
        JSON string with budget breakdown
    """
    try:
        flight_total = flight_price * number_of_travelers
        hotel_total = hotel_price_per_night * number_of_nights
        daily_total = daily_expenses * number_of_nights * number_of_travelers
        
        # Add ~15% buffer for miscellaneous
        miscellaneous = int((flight_total + hotel_total + daily_total) * 0.15)
        
        total = flight_total + hotel_total + daily_total + miscellaneous
        
        result = {
            "status": "success",
            "breakdown": {
                "flights": flight_total,
                "accommodation": hotel_total,
                "daily_expenses": daily_total,
                "miscellaneous": miscellaneous
            },
            "total_estimated_cost": total,
            "cost_per_person": int(total / number_of_travelers)
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
