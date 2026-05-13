"""
Main FastAPI application entry point.
Initializes the application, configures routes, and starts the server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import init_db
from app.routes import session_routes

# Get application settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Initializes database on startup.
    """
    # Startup: Initialize database tables
    print("🚀 Starting Session Manager Service...")
    print("📊 Initializing database...")
    init_db()
    print("✅ Database initialized successfully!")
    
    yield
    
    # Shutdown: Cleanup if needed
    print("👋 Shutting down Session Manager Service...")


# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    Session Manager Service for AI Interview Platform
    
    This service manages the complete lifecycle of interview sessions:
    - Start new sessions with unique IDs
    - Track session state and status
    - Update session status (active, paused, completed, terminated)
    - End sessions with timestamp recording
    - Retrieve session details and history
    
    Built with FastAPI and PostgreSQL for reliability and performance.
    """,
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)

# Configure CORS (Cross-Origin Resource Sharing)
# Allows frontend applications to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(session_routes.router)


@app.get("/", tags=["health"])
def root():
    """
    Root endpoint - Health check.
    Returns basic API information.
    """
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint.
    Used by monitoring systems to verify service is running.
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # Use this for development only
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
