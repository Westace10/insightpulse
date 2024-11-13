# components/sensor_charts.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def plot_sensor_data(sensor_id):
    """Plots sensor data and trends using Plotly"""
    # Simulating sensor data fetching from MongoDB (for illustration)
    # In a real-world scenario, you can fetch the data using API requests.
    data = fetch_sensor_data(sensor_id)
    
    if data is not None:
        # Creating a DataFrame for visualizations
        df = pd.DataFrame(data)

        # Line chart to show sensor data trends over time
        fig = px.line(df, x='timestamp', y='value', title=f'Sensor Data Over Time (ID: {sensor_id})')
        st.plotly_chart(fig)

def fetch_sensor_data(sensor_id):
    """Simulating data fetch for visualization. Replace this with real API call."""
    timestamps = pd.date_range("2024-11-01", periods=50, freq="h")
    values = np.random.randn(50) * 10 + 50  # Random sensor data
    return {'timestamp': timestamps, 'value': values}
