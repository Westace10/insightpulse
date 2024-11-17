from fastapi import APIRouter, HTTPException
from api.services.prompt_handler import generate_insight

router = APIRouter()

@router.get("/get_insights")
async def get_insights(sensor_id: str = None):
    """Fetch and generate insights based on sensor data."""
    try:
        if not sensor_id:
            raise HTTPException(status_code=400, detail="Sensor ID is required.")
        insights, sensor_data = generate_insight(sensor_id)
        response = {"data": {"insights": insights, "sensor_data": sensor_data}}
        return response
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {ve}")
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Service unavailable. Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while generating insights: {e}")
