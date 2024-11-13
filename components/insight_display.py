# components/insights_display.py
import streamlit as st

def display_insights(insights):
    """Displays the insights received from the API"""
    if insights:
        st.subheader("Sensor Insights")
        content = insights.get("content", "No insights available.")
        st.markdown(content)

        # Optionally show metadata
        with st.expander("Show detailed metadata"):
            st.write(insights.get("response_metadata", {}))
    else:
        st.warning("No insights available for the provided sensor ID.")

