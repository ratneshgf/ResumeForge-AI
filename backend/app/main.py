import asyncio
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import ats, document, enhance, job_description, payment, resume
from app.config import settings
from app.workers.cleanup_job import run_periodic_cleanup

# Configure structured logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info(f"Starting {settings.APP_NAME} in {settings.ENV} mode")
    logger.info(f"AI Provider: {settings.AI_PROVIDER}")
    logger.info(f"Redis enabled: {settings.USE_REDIS}")
    
    # Start background cleanup task
    cleanup_task = asyncio.create_task(run_periodic_cleanup())
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down application")
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    version="2.0.0",
    description="AI-powered resume optimization with template preservation"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router)
app.include_router(job_description.router)
app.include_router(enhance.router)
app.include_router(ats.router)
app.include_router(document.router)
app.include_router(payment.router)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": "2.0.0",
        "environment": settings.ENV,
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.APP_NAME,
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
    }
