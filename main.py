from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.router import api_router
from app.models.conversation import init_db

# Configure structured logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    
    Handles startup and shutdown events.
    """
    # Startup: Initialize database
    logger.info("🚀 Starting ChatOps-Bob Gateway...")
    await init_db()
    logger.info(f"✅ Database initialized")
    logger.info(f"🤖 AI Mode: {'MOCK' if settings.USE_MOCK_AI else 'IBM Watsonx ' + settings.WATSONX_MODEL}")
    logger.info(f"📡 Telegram Bot: {'configured' if settings.TELEGRAM_BOT_TOKEN else 'NOT configured'}")
    logger.info(f"🌐 Server ready at http://{settings.HOST}:{settings.PORT}")
    yield
    # Shutdown
    logger.info("👋 Shutting down ChatOps-Bob Gateway...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ChatOps gateway bridging Telegram with IBM Bob AI via RPA automation",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for dashboard
import os
static_dir = os.path.join(os.path.dirname(__file__), "app", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API v1 router
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint - serves dashboard redirect"""
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard", tags=["dashboard"], response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard HTML page"""
    from pathlib import Path
    template_path = Path(__file__).parent / "app" / "templates" / "dashboard.html"
    if template_path.exists():
        return HTMLResponse(content=template_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Dashboard template not found</h1>", status_code=404)


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint with real system status"""
    import aiosqlite
    from app.models.conversation import get_db_path
    
    db_status = "healthy"
    db_records = 0
    try:
        async with aiosqlite.connect(get_db_path()) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM messages")
            db_records = (await cursor.fetchone())[0]
    except Exception:
        db_status = "error"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "components": {
            "database": {"status": db_status, "records": db_records},
            "ai_engine": {
                "status": "mock" if settings.USE_MOCK_AI else "live",
                "model": settings.WATSONX_MODEL
            },
            "telegram": {
                "status": "configured" if settings.TELEGRAM_BOT_TOKEN else "not_configured"
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

# Made with Bob
