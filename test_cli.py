#!/usr/bin/env python3
"""
CLI Test Script for Travel Planning Agent
Tests the agent without the Streamlit UI
"""

import sys
from agents.travel_agent import TravelPlanningAgent
from utils.data_loader import format_itinerary, format_json_output


def main():
    """Main CLI interface."""
    print("\n" + "=" * 60)
    print("🧳 AI TRAVEL PLANNING AGENT - CLI TEST".center(60))
    print("=" * 60 + "\n")
    
    try:
        # Initialize agent
        print("🤖 Initializing Travel Planning Agent...")
        agent = TravelPlanningAgent()
        print("✅ Agent initialized successfully!\n")
        
        # Get agent info
        info = agent.get_agent_info()
        print(f"📊 Agent Configuration:")
        print(f"   Model: {info['model']}")
        print(f"   Temperature: {info['temperature']}")
        print(f"   Max Iterations: {info['max_iterations']}")
        print(f"   Available Tools: {len(info['tools_available'])}\n")
        
        # Example query
        print("📝 Planning a sample trip...\n")
        
        query = """
        Plan a 3-day trip for 2 travelers from Delhi to Goa.
        
        Trip Details:
        - Start Date: December 15, 2024
        - Budget: ₹50,000
        - Preferences: Beach activities, heritage sites
        - Travel Style: Relaxed
        
        Please provide:
        1. Best flight (most affordable)
        2. Best hotel (good rating and value)
        3. Day-wise itinerary with attractions
        4. Weather forecast
        5. Budget breakdown
        """
        
        print("🚀 Sending query to agent...\n")
        itinerary = agent.plan_trip(query)
        
        # Display results
        if itinerary.get("status") == "error":
            print(f"❌ Error: {itinerary.get('message')}")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("✅ TRIP PLANNING COMPLETED!")
        print("=" * 60 + "\n")
        
        # Display formatted itinerary
        print(format_itinerary(itinerary))
        
        # Save JSON output
        json_output = format_json_output(itinerary)
        with open("sample_itinerary.json", "w") as f:
            f.write(json_output)
        print(f"\n💾 Detailed JSON saved to: sample_itinerary.json")
        
        print("\n✅ CLI test completed successfully!")
        print("You can now run: streamlit run app.py\n")
        
    except ImportError as e:
        print(f"❌ Import Error: {str(e)}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
