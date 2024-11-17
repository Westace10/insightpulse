# components/sensor_charts.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import re

def plot_sensor_data(data, sensor_id):
    """Plots sensor data and trends using Plotly, with separate charts for each metric."""
    # Log raw data for debugging
    print("Raw data received:", data)

    if data is None or len(data) == 0:
        st.warning("No data available to plot.")
        return

    # Parse data into a structured DataFrame
    parsed_data = []
    for item in data:
        try:
            timestamp = item.get("metadata", {}).get("timestamp")
            page_content = item.get("page_content", "")
            
            # Extract sensor values using regex
            matches = re.findall(r"(\w+):\s([\d.]+)", page_content)
            sensor_values = {key.lower(): float(value) for key, value in matches}
            
            parsed_data.append({"timestamp": timestamp, **sensor_values})
        except Exception as e:
            print(f"Error processing item: {item}, Error: {e}")
            continue

    # Convert parsed data into a DataFrame
    if not parsed_data:
        st.error("Failed to parse sensor data.")
        return

    df = pd.DataFrame(parsed_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Check for available metrics
    metrics = [col for col in df.columns if col != "timestamp"]
    if not metrics:
        st.warning("No valid metrics found in the data.")
        return

    # Define unique colors for each metric
    color_palette = px.colors.qualitative.Plotly  # Default Plotly qualitative color palette

    # Generate separate charts for each metric
    for i, metric in enumerate(metrics):
        color = [color_palette[i % len(color_palette)]]  # Cycle through colors if more metrics than colors
        fig = px.line(
            df, 
            x="timestamp", 
            y=metric, 
            title=f"{metric.capitalize()} Over Time (Sensor ID: {sensor_id})",
            labels={"timestamp": "Time", metric: metric.capitalize()},
            color_discrete_sequence=color
        )
        st.plotly_chart(fig)



