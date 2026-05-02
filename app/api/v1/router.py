from fastapi import APIRouter
from app.api.v1.endpoints import webhook

api_router = APIRouter()

# Include webhook endpoints
api_router.include_router(
    webhook.router,
    tags=["webhook"]
)

# Made with Bob
