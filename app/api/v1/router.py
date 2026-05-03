from fastapi import APIRouter
from app.api.v1.endpoints import webhook, dashboard

api_router = APIRouter()

# Include webhook endpoints
api_router.include_router(
    webhook.router,
    tags=["webhook"]
)

# Include dashboard/conversations/stats endpoints
api_router.include_router(
    dashboard.router,
    tags=["dashboard"]
)

# Made with Bob
