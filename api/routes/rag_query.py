import logging
from fastapi import APIRouter, HTTPException
from api.services.prompt_handler import generate_rag_query_insight

# Set up logging for error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/get_rag_query")
async def get_rag_query(query: str = None):
    """Fetch and generate insights based on sensor data."""
    try:
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter is required.")
        
        # Call the service function to generate insight based on query
        rag_query = generate_rag_query_insight(query)
        
        if rag_query is None:
            raise HTTPException(status_code=404, detail="No insights found for the given query.")
        
        return {"answer": rag_query}

    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {ve}")

    except ConnectionError as ce:
        logger.error(f"ConnectionError: {ce}")
        raise HTTPException(status_code=503, detail="Service unavailable. Please try again later.")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating insights.")
