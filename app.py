import streamlit as st
import json
from datetime import datetime, timedelta
from agents.travel_agent import TravelPlanningAgent
from utils.data_loader import format_itinerary, format_json_output
from config.settings import STREAMLIT_PAGE_TITLE, STREAMLIT_LAYOUT

# Set page configuration
st.set_page_config(
    page_title=STREAMLIT_PAGE_TITLE,
    page_icon="✈️",
    layout=STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.5em;
        background: linear-gradient(to right, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #555;
        margin-bottom: 2em;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1em;
        border-radius: 0.5em;
        margin-bottom: 1em;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1em;
        border-radius: 0.5em;
        margin-bottom: 1em;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = TravelPlanningAgent()
    print("[v0] Initialized TravelPlanningAgent in session state")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "itinerary" not in st.session_state:
    st.session_state.itinerary = None


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-title">✈️ AI TRAVEL PLANNING ASSISTANT ✈️</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Plan your perfect trip with AI-powered insights</div>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🗺️ Plan Trip", "📋 View Itinerary", "ℹ️ About"])
    
    with tab1:
        st.header("Trip Planning Form")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Travel Details")
            
            origin = st.selectbox(
                "📍 Where are you traveling from?",
                options=["Delhi", "Mumbai", "Bangalore", "Kolkata", "Other"],
                help="Select your departure city"
            )
            
            if origin == "Other":
                origin = st.text_input("Enter your city:", placeholder="e.g., Chennai")
            
            destination = st.selectbox(
                "🎯 Where do you want to go?",
                options=["Goa", "Jaipur", "Agra", "Other"],
                help="Select your destination"
            )
            
            if destination == "Other":
                destination = st.text_input("Enter destination:", placeholder="e.g., Kerala")
        
        with col2:
            st.subheader("Trip Duration & Budget")
            
            trip_start = st.date_input(
                "📅 Start Date",
                value=datetime.now() + timedelta(days=7)
            )
            
            num_days = st.slider(
                "📆 Number of Days",
                min_value=1,
                max_value=14,
                value=3,
                help="Duration of your trip"
            )
            
            trip_end = trip_start + timedelta(days=num_days - 1)
            
            budget = st.number_input(
                "💰 Total Budget (₹)",
                min_value=5000,
                max_value=500000,
                value=50000,
                step=5000
            )
        
        col3, col4 = st.columns(2)
        
        with col3:
            num_travelers = st.number_input(
                "👥 Number of Travelers",
                min_value=1,
                max_value=10,
                value=1
            )
            
            preferences = st.multiselect(
                "🎨 Preferences",
                options=["Beach", "Heritage", "Adventure", "Luxury", "Budget", "Food"],
                default=["Beach"],
                help="Select your travel preferences"
            )
        
        with col4:
            st.subheader("Additional Info")
            
            travel_style = st.radio(
                "✨ Travel Style",
                options=["Relaxed", "Moderate", "Fast-paced"],
                help="How packed do you want your itinerary?"
            )
            
            dietary = st.text_input(
                "🍽️ Dietary Restrictions (if any)",
                placeholder="e.g., Vegetarian, No seafood"
            )
        
        # Info box
        with st.container():
            st.markdown(f"""
            <div class="info-box">
                <strong>📊 Trip Summary:</strong><br>
                • <strong>From:</strong> {origin} | <strong>To:</strong> {destination}<br>
                • <strong>Duration:</strong> {num_days} days ({trip_start.strftime('%d %b')} - {trip_end.strftime('%d %b')})<br>
                • <strong>Budget:</strong> ₹{budget:,} for {num_travelers} traveler(s)<br>
                • <strong>Preferences:</strong> {', '.join(preferences)}
            </div>
            """, unsafe_allow_html=True)
        
        # Plan button
        if st.button("🚀 Generate My Trip Plan", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is planning your perfect trip..."):
                try:
                    # Build the query
                    query = f"""
                    Please plan a {num_days}-day trip for {num_travelers} traveler(s) from {origin} to {destination}.
                    
                    Trip Details:
                    - Travel Dates: {trip_start.strftime('%B %d')} to {trip_end.strftime('%B %d')}
                    - Total Budget: ₹{budget}
                    - Travel Style: {travel_style}
                    - Preferences: {', '.join(preferences)}
                    - Dietary Restrictions: {dietary if dietary else 'None'}
                    
                    Please provide:
                    1. Best flight option (considering price and timing)
                    2. Best hotel option (considering rating and price)
                    3. Day-wise itinerary with attractions matching preferences
                    4. Weather forecast for the travel dates
                    5. Complete budget breakdown
                    6. Reasoning for selections
                    
                    Format the response as a JSON object.
                    """
                    
                    print(f"[v0] User query: {query[:100]}...")
                    
                    # Run the agent
                    itinerary = st.session_state.agent.plan_trip(query)
                    st.session_state.itinerary = itinerary
                    
                    # Store in chat history
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": query
                    })
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": json.dumps(itinerary)
                    })
                    
                    print(f"[v0] Generated itinerary successfully")
                    
                except Exception as e:
                    st.error(f"❌ Error planning trip: {str(e)}")
                    print(f"[v0] Error: {str(e)}")
    
    with tab2:
        st.header("Your Trip Itinerary")
        
        if st.session_state.itinerary:
            itinerary = st.session_state.itinerary
            
            # Check for errors
            if itinerary.get("status") == "error":
                st.error(f"❌ {itinerary.get('message', 'Error generating itinerary')}")
            else:
                # Display formatted itinerary
                st.markdown(format_itinerary(itinerary), unsafe_allow_html=True)
                
                # Display as JSON
                st.subheader("📄 JSON Format")
                with st.expander("View detailed JSON output"):
                    st.code(format_json_output(itinerary), language="json")
                
                # Download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download as JSON",
                        data=format_json_output(itinerary),
                        file_name=f"trip_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                with col2:
                    st.download_button(
                        label="📥 Download as Text",
                        data=format_itinerary(itinerary),
                        file_name=f"trip_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
        else:
            st.info("👈 Generate a trip plan first by filling the form on the left and clicking 'Generate My Trip Plan'")
    
    with tab3:
        st.header("About This App")
        
        st.markdown("""
        ### 🤖 AI Travel Planning Assistant
        
        This is an intelligent travel planning system powered by:
        
        **Technology Stack:**
        - **LangChain**: Multi-agent framework for complex reasoning
        - **OpenAI GPT**: Advanced language model for decision-making
        - **Streamlit**: Interactive web interface
        - **Open-Meteo API**: Free real-time weather data
        
        **Features:**
        - ✈️ Smart flight search and recommendations
        - 🏨 Hotel suggestions based on ratings and budget
        - 🗺️ Place discovery with ratings and details
        - 🌤️ Real-time weather forecasts
        - 💰 Automated budget planning
        - 📋 Day-wise activity planning
        
        **How It Works:**
        1. You provide your travel preferences
        2. The AI agent searches flights, hotels, and attractions
        3. It analyzes multiple options and recommends the best
        4. You get a complete, ready-to-execute itinerary
        
        **Data Sources:**
        - Local JSON datasets for flights, hotels, and places
        - Open-Meteo API for weather (free, no API key required)
        
        **Best Practices:**
        - Be specific about your preferences
        - The system optimizes for value (best price-to-quality ratio)
        - Weather data helps plan activities
        - Budget includes estimated daily expenses
        """)
        
        st.divider()
        
        # Agent Info
        agent_info = st.session_state.agent.get_agent_info()
        st.subheader("🔧 Agent Configuration")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Model", agent_info["model"])
        with col2:
            st.metric("Temperature", agent_info["temperature"])
        with col3:
            st.metric("Max Iterations", agent_info["max_iterations"])
        
        st.subheader("🛠️ Available Tools")
        for tool in agent_info["tools_available"]:
            st.write(f"• {tool}")


if __name__ == "__main__":
    main()
