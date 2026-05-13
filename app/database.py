"""
Database connection and session management module.
Handles PostgreSQL connection using SQLAlchemy ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import get_settings

# Get database URL from settings
settings = get_settings()

# Create SQLAlchemy engine
# echo=True will log all SQL statements (useful for debugging)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=10,  # Maximum number of connections to keep in pool
    max_overflow=20  # Maximum overflow connections
)

# Create SessionLocal class for database sessions
# Each instance will be a database session
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-commit transactions
    autoflush=False,   # Don't auto-flush changes
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency function that provides database session to routes.
    Automatically closes session after request completes.
    
    Usage in FastAPI routes:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db here
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.
    Should be called on application startup.
    """
    Base.metadata.create_all(bind=engine)
