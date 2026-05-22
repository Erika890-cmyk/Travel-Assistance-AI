import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Weather API
WEATHER_API_BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FLIGHTS_FILE = os.path.join(DATA_DIR, "flights.json")
HOTELS_FILE = os.path.join(DATA_DIR, "hotels.json")
PLACES_FILE = os.path.join(DATA_DIR, "places.json")

# Agent settings
AGENT_MODEL = LLM_MODEL
AGENT_TEMPERATURE = 0.7
MAX_ITERATIONS = 10

# Streamlit settings
STREAMLIT_PAGE_TITLE = "AI Travel Planning Assistant"
STREAMLIT_LAYOUT = "wide"
