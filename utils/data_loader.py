import json
import os
from typing import List, Dict, Any
from config.settings import FLIGHTS_FILE, HOTELS_FILE, PLACES_FILE


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """Load JSON data from file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data as list of dictionaries
    """
    try:
        if not os.path.exists(file_path):
            print(f"[v0] Warning: File not found: {file_path}")
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"[v0] Loaded {len(data)} items from {os.path.basename(file_path)}")
        return data
    except Exception as e:
        print(f"[v0] Error loading {file_path}: {str(e)}")
        return []


def load_all_data() -> Dict[str, List[Dict[str, Any]]]:
    """Load all travel data files.
    
    Returns:
        Dictionary with keys 'flights', 'hotels', 'places'
    """
    return {
        "flights": load_json_data(FLIGHTS_FILE),
        "hotels": load_json_data(HOTELS_FILE),
        "places": load_json_data(PLACES_FILE),
    }


def format_itinerary(itinerary_data: Dict[str, Any]) -> str:
    """Format itinerary data into human-readable string.
    
    Args:
        itinerary_data: Dictionary containing trip information
        
    Returns:
        Formatted itinerary string
    """
    output = []
    output.append("=" * 70)
    output.append("🧳 YOUR AI-PLANNED TRIP ITINERARY 🧳".center(70))
    output.append("=" * 70)
    
    # Trip Summary
    output.append(f"\n📍 TRIP QUERY: {itinerary_data.get('query', 'N/A')}")
    output.append(f"✅ STATUS: {itinerary_data.get('status', 'N/A').upper()}")
    
    # Flights
    if "flights" in itinerary_data and itinerary_data["flights"]:
        output.append(f"\n✈️  AVAILABLE FLIGHTS:")
        flights_text = itinerary_data["flights"]
        if isinstance(flights_text, str):
            output.append(flights_text[:300])
        else:
            output.append(str(flights_text)[:300])
    
    # Hotels
    if "hotels" in itinerary_data and itinerary_data["hotels"]:
        output.append(f"\n🏨 AVAILABLE HOTELS:")
        hotels_text = itinerary_data["hotels"]
        if isinstance(hotels_text, str):
            output.append(hotels_text[:300])
        else:
            output.append(str(hotels_text)[:300])
    
    # Places
    if "places" in itinerary_data and itinerary_data["places"]:
        output.append(f"\n🎯 ATTRACTIONS & PLACES:")
        places_text = itinerary_data["places"]
        if isinstance(places_text, str):
            output.append(places_text[:300])
        else:
            output.append(str(places_text)[:300])
    
    # Weather
    if "weather" in itinerary_data and itinerary_data["weather"]:
        output.append(f"\n☀️  WEATHER FORECAST:")
        weather_text = itinerary_data["weather"]
        if isinstance(weather_text, str):
            output.append(weather_text[:300])
        else:
            output.append(str(weather_text)[:300])
    
    # Budget
    if "budget" in itinerary_data and itinerary_data["budget"]:
        output.append(f"\n💵 BUDGET ESTIMATION:")
        budget_text = itinerary_data["budget"]
        if isinstance(budget_text, str):
            output.append(budget_text[:300])
        else:
            output.append(str(budget_text)[:300])
    
    # Tools called
    if "tools_called" in itinerary_data:
        output.append(f"\n🔧 TOOLS USED:")
        output.append(f"   {', '.join(itinerary_data['tools_called'])}")
    
    output.append("\n" + "=" * 70)
    return "\n".join(output)


def format_json_output(itinerary_data: Dict[str, Any]) -> str:
    """Format itinerary data as pretty JSON.
    
    Args:
        itinerary_data: Dictionary containing trip information
        
    Returns:
        Formatted JSON string
    """
    return json.dumps(itinerary_data, indent=2, ensure_ascii=False)
