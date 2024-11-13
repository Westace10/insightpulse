# main.py
from fastapi import FastAPI
from api.routes.insights import router as insights_router
from api.routes.rag_query import router as rag_router

app = FastAPI()

# Include the insights router
app.include_router(insights_router, prefix="/api/v1", tags=["insights"])

# Include the insights router
app.include_router(rag_router, prefix="/api/v1", tags=["rag_query"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the InsightPulse API"}
