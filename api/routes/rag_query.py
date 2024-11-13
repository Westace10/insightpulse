# insights.py
from fastapi import APIRouter, HTTPException
from api.services.prompt_handler import generate_rag_query_insight

router = APIRouter()

@router.get("/get_rag_query")
async def get_rag_query(query: str = None):
    """Fetch and generate insights based on sensor data."""
    try:
        rag_query = generate_rag_query_insight(query)
        return {"answer": rag_query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while generating insights: {e}")