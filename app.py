import streamlit as st
from components.sensor_form import sensor_form
from components.insight_display import display_insights
from components.sensor_charts import plot_sensor_data
from utils import fetch_insights_from_api, fetch_rag_response_from_api
from typing import List, Dict

# Constants
VIEW_SENSOR_INSIGHTS = "View Sensor Insights"
CHAT_WITH_SENSOR_DATA = "Chat with Sensor Data"
USER_AVATAR = "😎"
ASSISTANT_AVATAR = "🤖"
MAX_CHAT_HISTORY = 50  # Adjust as needed

def display_sensor_insights(sensor_id: str) -> None:
    """
    Display insights and sensor data visualizations.
    
    Args:
        sensor_id (str): The ID of the sensor.
    """
    with st.spinner("Fetching sensor insights..."):
        try:
            # Use the cached version if you created a wrapper, otherwise use the original
            # insights = cached_fetch_insights_from_api(sensor_id) # If using the wrapper
            insights_data = fetch_insights_from_api(sensor_id)  
            # print(insights_data)

            st.write("this is a simple message")
            st.write(insights_data.get("insights"))
            st.write(insights_data.get("sensor_data"))

            insights = insights_data.get("insights")
            plot_data = insights_data.get("sensor_data")
            
            st.session_state.insights = insights_data.get("insights")  # Save insights in session

            # Display insights
            display_insights(insights)

            # Plot sensor data and visualizations
            plot_sensor_data(plot_data, sensor_id)
        except Exception as e:
            st.error(f"An error occurred while fetching sensor insights: {str(e)}")

def chat_with_sensor_data():
    """Handle RAG-based chat for querying sensor data with persistent chat history."""

    message_container = st.container(height=500, border=True)
    
    # Initialize chat history in session state if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history: List[Dict[str, str]] = [] # type: ignore

    # Display chat history
    for message in st.session_state.chat_history:
        avatar = ASSISTANT_AVATAR if message["role"] == "assistant" else USER_AVATAR
        with message_container.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Handle new user input
    if prompt := st.chat_input("Enter a prompt here..."):
        try:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            message_container.chat_message("user", avatar=USER_AVATAR).markdown(prompt)

            # Get and display assistant response
            with message_container.chat_message("assistant", avatar=ASSISTANT_AVATAR):
                with st.spinner("Give me a moment..."):
                    response = fetch_rag_response_from_api(prompt)
                st.markdown(response)

            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Limit chat history size
            if len(st.session_state.chat_history) > MAX_CHAT_HISTORY:
                st.session_state.chat_history = st.session_state.chat_history[-MAX_CHAT_HISTORY:]

        except Exception as e:
            st.error(f"An error occurred: {str(e)}", icon="⛔️")

def main():
    # Set the page title and layout
    st.set_page_config(page_title="Sensor Insights Dashboard", page_icon=":bar_chart:", layout="wide")
    
    st.title("Real-Time Sensor Insights")
    st.markdown(
        """
        This app allows you to interact with sensor data stored in MongoDB, analyze it through visualizations and insights, 
        and ask questions about the data to receive intelligent answers.
        """
    )

    # Sidebar for selecting actions
    st.sidebar.header("Select Action")
    action = st.sidebar.radio(
        "What would you like to do?",
        (VIEW_SENSOR_INSIGHTS, CHAT_WITH_SENSOR_DATA)
    )

    if action == VIEW_SENSOR_INSIGHTS:
        sensor_id = sensor_form()
        if sensor_id:
            display_sensor_insights(sensor_id)
    elif action == CHAT_WITH_SENSOR_DATA:
        chat_with_sensor_data()

if __name__ == "__main__":
    main()
