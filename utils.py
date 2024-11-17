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

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            return data.get("insights", "No insights available.")
        # Handle specific error responses from the API
        elif response.status_code == 400:
            return "Bad request: Please check your input parameters."
        elif response.status_code == 404:
            return "No insights found for the provided sensor ID."
        elif response.status_code == 503:
            return "The API service is temporarily unavailable. Please try again later."
        else:
            return f"Error fetching data: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        # Specific error handling for network or request-related issues
        return f"Network error: {str(e)}"
    except Exception as e:
        # General exception handling
        return f"An unexpected error occurred: {str(e)}"

@st.cache_data
def fetch_rag_response_from_api(query):
    """Fetches insights from FastAPI based on the provided query."""
    try:
        API_URL = f"{BASE_API_URL}/get_rag_query"
        response = requests.get(API_URL, params={"query": query})

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            return data.get("answer", "No answer available.")
        # Handle specific error responses from the API
        elif response.status_code == 400:
            return "Bad request: Please check your input parameters."
        elif response.status_code == 404:
            return "No answer found for the provided query."
        elif response.status_code == 503:
            return "The API service is temporarily unavailable. Please try again later."
        else:
            return f"Error fetching data: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        # Specific error handling for network or request-related issues
        return f"Network error: {str(e)}"
    except Exception as e:
        # General exception handling
        return f"An unexpected error occurred: {str(e)}"
