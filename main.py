# main.py
from fastapi import FastAPI
from app.api.v1.router import api_router
import app.models  # This ensures all models are loaded

app = FastAPI(title="Social Protection MIS API")
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)