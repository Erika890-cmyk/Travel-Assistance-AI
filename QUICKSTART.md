# Quick Start Guide - AI Travel Planning Assistant

## 30-Second Setup

```bash
# 1. Navigate to project
cd /vercel/share/v0-project

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Set OpenAI API key
export OPENAI_API_KEY="sk-your-api-key-here"

# 4. Run Streamlit app
streamlit run app.py

# 5. Open browser to http://localhost:8501
```

## What to Do in the App

1. **Enter Trip Details:**
   - Source city (e.g., "Delhi")
   - Destination city (e.g., "Goa")
   - Number of travelers
   - Budget (in rupees)
   - Dates (optional)

2. **Click "Plan My Trip"**
   - Agent will call all 5 tools
   - Each tool searches relevant data
   - System generates complete itinerary

3. **View Results:**
   - **Itinerary Tab:** Human-readable trip plan
   - **JSON Tab:** Structured data format
   - **Raw Data Tab:** Tool outputs

## Example Query

**Input:**
```
I need a 3-day trip to Goa from Delhi for 2 people with a budget of 50,000 rupees
```

**System will:**
1. Search for flights Delhi → Goa
2. Find hotels in Goa
3. Discover attractions (beaches, temples, etc.)
4. Get weather forecast for Goa (3 days)
5. Calculate budget breakdown

**Output:**
- Best flight option with price and time
- Recommended hotels with ratings
- Day-wise activity itinerary
- Weather for each day
- Complete budget breakdown

## Available Destinations

Tested destinations (included in data):
- Goa
- Delhi
- Mumbai
- Jaipur
- Agra
- Bangalore
- Kerala
- Rajasthan

## Testing Without OpenAI Key

For testing the system without an OpenAI key:

```bash
# 1. Set a dummy key
export OPENAI_API_KEY="sk-test-key"

# 2. Run test script
python test_cli.py

# This will show complete trip planning without API calls
```

## File Structure

```
├── app.py              # Main Streamlit UI
├── requirements.txt    # Install with: pip install -r requirements.txt
├── agents/
│   └── travel_agent.py # AI agent logic
├── tools/
│   └── travel_tools.py # 5 travel tools
├── utils/
│   └── data_loader.py  # Data utilities
├── data/
│   ├── flights.json    # Flight data
│   ├── hotels.json     # Hotel data
│   └── places.json     # Attractions data
└── README.md           # Full documentation
```

## Features

✅ Natural language trip planning
✅ Real-time weather integration
✅ Budget optimization
✅ Multi-day itinerary generation
✅ Place recommendations
✅ JSON and text output formats
✅ Error handling
✅ Caching for performance

## Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'streamlit'`
```bash
# Solution:
pip install -r requirements.txt
```

**Issue:** `OPENAI_API_KEY not set`
```bash
# Solution:
export OPENAI_API_KEY="your-api-key"
# Or create .env file with: OPENAI_API_KEY=your-api-key
```

**Issue:** Streamlit not opening in browser
```bash
# Try:
streamlit run app.py --logger.level=debug

# Or manually open: http://localhost:8501
```

## Next Steps

1. **Run the application** and test with different destinations
2. **Review the generated itineraries** to understand the system
3. **Check the JSON output** for programmatic integration
4. **Read README.md** for detailed documentation
5. **Explore the code** to understand the agentic AI pattern

## Support

- Check README.md for detailed documentation
- See PROJECT_COMPLETION.md for system architecture
- Review code docstrings for function details
- Check comments in agent and tools code

---

**Happy travel planning!** ✈️
