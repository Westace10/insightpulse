# utils.py
import requests
import streamlit as st

# BASE_API_URL = "http://127.0.0.1:8000/api/v1"
BASE_API_URL = "https://insightpulse.onrender.com/api/v1"

@st.cache_data
def fetch_insights_from_api(sensor_id):
    """Fetches insights from FastAPI based on the provided sensor ID."""
    try:
        API_URL = f"{BASE_API_URL}/get_insights"
        response = requests.get(API_URL, params={"sensor_id": sensor_id})
        
        if response.status_code == 200:
            data = response.json()
            return data.get("insights", "No insights available.")
        else:
            return "Error fetching data from the API."
    except Exception as e:
        return f"An error occurred: {str(e)}"

@st.cache_data
def fetch_rag_response_from_api(query):
    """Fetches insights from FastAPI based on the provided sensor ID."""
    try:
        API_URL = f"{BASE_API_URL}/get_rag_query"
        response = requests.get(API_URL, params={"query": query})
        
        if response.status_code == 200:
            data = response.json()
            return data.get("answer", "No answer available.")
        else:
            return "Error fetching data from the API."
    except Exception as e:
        return f"An error occurred: {str(e)}"
