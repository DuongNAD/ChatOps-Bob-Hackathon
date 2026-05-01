from fastapi import APIRouter
from app.api.v1.endpoints import scan

api_router = APIRouter()

# Include scan endpoint
api_router.include_router(
    scan.router,
    tags=["scan"]
)

# Made with Bob
