# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import programs, households

api_router = APIRouter()

api_router.include_router(
    programs.router,
    prefix="/programs",
    tags=["programs"]
)

api_router.include_router(
    households.router,
    prefix="/households",
    tags=["households"]
)