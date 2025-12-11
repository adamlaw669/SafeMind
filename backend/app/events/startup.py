from app.db.base import init_db, engine
from app.events.message_queue import message_queue
from app.services.nlp_service import NLPService
import logging

logger = logging.getLogger(__name__)

async def initialize_database():
    """Initialize database and create tables."""
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

async def initialize_message_queue():
    """Initialize message queue."""
    try:
        await message_queue.initialize()
        logger.info("Message queue initialized")
    except Exception as e:
        logger.error(f"Failed to initialize message queue: {str(e)}")

async def initialize_connection_manager():
    """Initialize WebSocket connection manager."""
    try:
        from app.services.websocket_service import manager
        logger.info("WebSocket connection manager initialized")
        return manager
    except Exception as e:
        logger.error(f"Failed to initialize connection manager: {str(e)}")

async def preload_nlp_model():
    """Preload NLP keywords."""
    try:
        high_count = len(NLPService.HIGH_RISK_KEYWORDS)
        medium_count = len(NLPService.MEDIUM_RISK_KEYWORDS)
        total = high_count + medium_count
        logger.info(f"NLP model loaded with {total} keywords ({high_count} high-risk, {medium_count} medium-risk)")
    except Exception as e:
        logger.error(f"Failed to preload NLP model: {str(e)}")

async def shutdown_database():
    """Close database connections on shutdown."""
    try:
        engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Failed to shutdown database: {str(e)}")
