from fastapi import APIRouter

from app.patients.api import endpoints

api_router = APIRouter()
api_router.include_router(
    endpoints.router, prefix="/patients", tags=["patients"]
)
