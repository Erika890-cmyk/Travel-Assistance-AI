# 🧳 AI Travel Planning Assistant with LangChain

An intelligent, agentic travel planning system that autonomously creates personalized trip itineraries using LangChain, OpenAI, and real-time data integration.

## 📋 Project Overview

This project demonstrates advanced agentic AI capabilities by building a travel planning system that:
- **Autonomously reasons** through multiple travel options
- **Integrates real data** (flights, hotels, attractions, weather)
- **Makes optimized decisions** based on user preferences and budget
- **Generates structured outputs** in both human-readable and JSON formats

### Problem Statement
Travelers spend hours switching between multiple websites, comparing inconsistent information, and manually building itineraries. This system automates and optimizes the entire travel planning process using AI reasoning.

### Business Use Cases
- 🏢 Travel agencies seeking AI-powered self-service planning
- 🏨 Hotel and airline platforms offering personalized recommendations
- 📱 Tourism companies implementing conversational booking systems
- 🤖 Businesses adopting agentic AI for complex decision-making

## 🏗️ Architecture

### Tech Stack
```
Frontend:     Streamlit 1.57+ (Interactive UI)
Backend:      Python 3.13
LLM:          OpenAI GPT-4o-mini via Langchain 1.3+
Framework:    LangChain (Agent Orchestration)
APIs:         Open-Meteo (Weather - Free)
Data:         JSON datasets (Flights, Hotels, Places)
```

### Project Structure
```
ai-travel-planner/
├── app.py                      # Streamlit UI application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── config/
│   └── settings.py            # Configuration management
├── agents/
│   └── travel_agent.py        # LangChain agent orchestrator
├── tools/
│   └── travel_tools.py        # Tool definitions (5 tools)
├── utils/
│   └── data_loader.py         # Data loading & formatting utilities
└── data/
    ├── flights.json           # Flight database
    ├── hotels.json            # Hotel database
    └── places.json            # Tourist attractions database
```

## 🛠️ 5 LangChain Tools

The agent autonomously uses these tools to plan trips:

### 1. **search_flights(source, destination, number_of_travelers)**
- Searches flight database filtered by route
- Returns top 5 cheapest options
- Calculates total cost for all travelers

### 2. **search_hotels(destination, number_of_nights, budget)**
- Finds hotels by city and budget constraints
- Ranks by customer rating (quality over price)
- Returns top options with amenities

### 3. **discover_places(destination, place_type)**
- Discovers attractions and POIs
- Filters by type (Beach, Heritage, Adventure, etc.)
- Includes ratings, entry fees, and duration

### 4. **get_weather_forecast(city, latitude, longitude, days)**
- Calls free Open-Meteo API (no API key required)
- Provides 7-day forecast with temp and conditions
- Helps plan weather-appropriate activities

### 5. **estimate_budget(flight_price, hotel_price, number_of_nights, travelers, daily_expenses)**
- Calculates complete trip cost breakdown
- Includes flights, accommodation, daily expenses
- Adds 15% contingency buffer
- Returns per-person cost

## 📊 Agent Workflow (ReAct Pattern)

```
User Query
    ↓
[Agent Reasoning] "I need to search flights first..."
    ↓
[Tool: search_flights] → Get flight options
    ↓
[Agent Reasoning] "Now I need hotels in this city..."
    ↓
[Tool: search_hotels] → Get hotel options
    ↓
[Agent Reasoning] "Let me find attractions..."
    ↓
[Tool: discover_places] → Get attractions
    ↓
[Agent Reasoning] "Get weather for planning..."
    ↓
[Tool: get_weather_forecast] → Get forecast
    ↓
[Agent Reasoning] "Calculate total budget..."
    ↓
[Tool: estimate_budget] → Get cost breakdown
    ↓
[Final Response] Complete structured itinerary
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API key (from https://platform.openai.com/api-keys)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-travel-planner
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
uv pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_key_here
```

5. **Run the Streamlit app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 💡 Usage

### Through Web UI
1. Select origin and destination cities
2. Choose travel dates and duration
3. Set total budget
4. Select preferences (Beach, Heritage, Adventure, etc.)
5. Click "Generate My Trip Plan"
6. View itinerary in human-readable format
7. Download as JSON or Text

### Example Trip Plan Output
```
============================================================
        🧳 YOUR AI-PLANNED TRIP ITINERARY 🧳
============================================================

📍 DESTINATION: Goa
📅 DATES: 2024-12-15 to 2024-12-17
👥 TRAVELERS: 2
💰 BUDGET: ₹50,000

✈️  FLIGHT SELECTED:
   Airline: IndiGo
   Departure: 14:00 from Delhi
   Price: ₹4,800

🏨 HOTEL BOOKED:
   Name: Sea View Resort
   Rating: 4.5⭐
   Price per Night: ₹3,200

☀️  WEATHER FORECAST:
   Day 1: Sunny (31°C)
   Day 2: Partly Cloudy
   Day 3: Light Breeze

📋 DAY-WISE ITINERARY:

   Day 1:
      • Baga Beach (Beach)
        Popular beach known for water sports and nightlife
      • Candolim Market (Heritage)

   Day 2:
      • Basilica of Bom Jesus (Heritage)
        UNESCO World Heritage Site
      • Water Sports at Calangute (Adventure)

   Day 3:
      • Old Goa Heritage Walk (Heritage)

💵 BUDGET BREAKDOWN:
   Flights: ₹9,600
   Accommodation: ₹6,400
   Daily Expenses: ₹3,000
   Miscellaneous: ₹2,880

   ========================================
   TOTAL ESTIMATED COST: ₹21,880

🤖 AI REASONING:
   Selected IndiGo for best price-to-timing ratio. 
   Sea View Resort offers excellent value with beachfront access. 
   Itinerary balances heritage, beach, and adventure activities.
```

## 📈 Expected Results

The system generates:
- ✅ Complete day-wise itineraries
- ✅ Optimized flight & hotel selections
- ✅ Realistic weather forecasts
- ✅ Detailed budget breakdowns
- ✅ AI reasoning/justification
- ✅ Both JSON & human-readable formats

## 🔄 Data Management

### Sample Data Included
- **10 flights** across major Indian cities
- **8 hotels** with ratings and amenities
- **12 attractions** with types and details

### Adding Custom Data
Edit JSON files in `/data/` directory:
```json
{
  "id": "F001",
  "airline": "IndiGo",
  "source": "Delhi",
  "destination": "Goa",
  "price": 4800,
  "duration_minutes": 150
}
```

## 🧠 Key Features

### Agentic AI Highlights
- **Multi-step reasoning**: Agent plans which tools to use in what order
- **Tool orchestration**: Combines results from 5+ tools intelligently
- **Error handling**: Gracefully handles missing data and API errors
- **Budget optimization**: Finds best value (not just cheapest)
- **Preference matching**: Filters attractions by user interests

### Code Quality
- ✅ Modular architecture (agents, tools, utils separate)
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ Error handling with try-except blocks
- ✅ PEP 8 compliant formatting
- ✅ Configuration management
- ✅ Logging support

## 🔐 Security & Best Practices

- API keys stored in `.env` (never committed)
- Input validation on all user inputs
- Safe JSON parsing with error handling
- Rate limiting considerations for external APIs
- No hardcoded credentials

## 📝 Example Queries

```python
# Simple trip planning
"I want to go to Goa for 3 days with ₹50,000 budget"

# Detailed requirements
"Plan a 5-day family trip to Jaipur for 4 people with ₹1,00,000 budget. 
 We love heritage sites and want luxury hotels."

# Adventure-focused
"I'm a solo traveler going to Goa for 7 days. 
 I have ₹40,000 and want adventure activities, not luxury."
```

## 🎓 Learning Outcomes

By completing this project, you'll understand:
- ✅ **LangChain agents**: How to build reasoning systems
- ✅ **Tool calling**: Implementing structured tool integration
- ✅ **Prompt engineering**: Crafting system prompts for agents
- ✅ **API integration**: Connecting multiple data sources
- ✅ **JSON handling**: Parsing and generating structured data
- ✅ **Streamlit development**: Building interactive UIs
- ✅ **Agentic workflows**: ReAct pattern implementation

## 🚦 Evaluation Criteria Met

✅ **Problem Statement**: Clear explanation of travel planning challenges  
✅ **Data Integration**: Uses JSON datasets + free Open-Meteo API  
✅ **Agentic AI**: ReAct pattern with tool calling  
✅ **Code Quality**: Modular, documented, PEP 8 compliant  
✅ **Final Output**: Complete itineraries with flights, hotels, weather, budget  
✅ **Justification**: AI reasoning included in responses  

## 🐛 Troubleshooting

**"OPENAI_API_KEY not found"**
- Check `.env` file exists and has valid OpenAI key
- Run: `echo $OPENAI_API_KEY` to verify

**"No flights found"**
- Try cities in the database: Delhi, Mumbai, Bangalore, Goa, Jaipur
- Check data/flights.json for available routes

**"Streamlit not responding"**
- Restart: `streamlit run app.py --logger.level=debug`
- Check console for error messages

## 📚 References

- [LangChain Documentation](https://docs.langchain.com/)
- [OpenAI API Docs](https://platform.openai.com/docs/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Open-Meteo API](https://open-meteo.com/en/docs)
- [ReAct Pattern Paper](https://arxiv.org/abs/2210.03629)

## 📄 License

MIT License - Feel free to use and modify

## 👨‍💻 Author

Erika Binu

BCA student

-----
