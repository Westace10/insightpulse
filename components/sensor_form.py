# components/sensor_form.py
import streamlit as st

def sensor_form():
    """Displays input form for Sensor ID"""
    sensor_id = st.text_input("Enter Sensor ID", value="", max_chars=20)
    
    if sensor_id:
        if st.button("Fetch Insights"):
            return sensor_id
    return None
