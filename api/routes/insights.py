# insights.py
from fastapi import APIRouter, HTTPException
from api.services.prompt_handler import generate_insight

router = APIRouter()

@router.get("/get_insights")
async def get_insights(sensor_id: str = None):
    """Fetch and generate insights based on sensor data."""
    try:
        insights = generate_insight(sensor_id)
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while generating insights: {e}")
