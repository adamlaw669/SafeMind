from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.routers import (
    auth_router,
    report_router,
    emergency_router,
    notification_router,
    agency_router,
    followup_router
)
from app.events import startup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SafeMind",
    version="1.0.0",
    description="Mental health emergency response platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    """Initialize application on startup."""
    try:
        logger.info("SafeMind backend starting up...")
        await startup.initialize_database()
        await startup.initialize_message_queue()
        await startup.initialize_connection_manager()
        await startup.preload_nlp_model()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

@app.on_event("shutdown")
async def on_shutdown():
    """Cleanup on application shutdown."""
    try:
        logger.info("SafeMind backend shutting down...")
        await startup.shutdown_database()
        logger.info("Application shutdown completed")
    except Exception as e:
        logger.error(f"Shutdown error: {str(e)}")

app.include_router(auth_router.router, prefix="/api/auth", tags=["authentication"])
app.include_router(report_router.router, prefix="/api/reports", tags=["reports"])
app.include_router(emergency_router.router, prefix="/api/emergency", tags=["emergency"])
app.include_router(notification_router.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(agency_router.router, prefix="/api/agencies", tags=["agencies"])
app.include_router(followup_router.router, prefix="/api/followup", tags=["followup"])

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "SafeMind",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "SafeMind",
        "version": "1.0.0"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status_code": 500,
            "message": "Internal server error",
            "data": None
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )