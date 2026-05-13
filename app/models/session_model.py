"""
SQLAlchemy ORM model for interview sessions.
Defines the database table structure and relationships.
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from app.database import Base


class SessionStatus(str, enum.Enum):
    """
    Enum for valid session statuses.
    Ensures only valid status values can be stored.
    """
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    TERMINATED = "terminated"


class SessionModel(Base):
    """
    ORM model representing an interview session.
    Maps to 'sessions' table in PostgreSQL database.
    """
    
    __tablename__ = "sessions"
    
    # Primary key - auto-incrementing integer
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Unique session identifier - UUID stored as string
    session_id = Column(String, unique=True, index=True, nullable=False)
    
    # Candidate and interviewer identifiers
    candidate_id = Column(Integer, nullable=False, index=True)
    interviewer_id = Column(Integer, nullable=False, index=True)
    
    # Session status with enum constraint
    status = Column(
        SQLEnum(SessionStatus),
        nullable=False,
        default=SessionStatus.ACTIVE
    )
    
    # Timestamps - automatically managed
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # Set by database on insert
        nullable=False
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # Set by database on insert
        onupdate=func.now(),  # Updated by database on update
        nullable=False
    )
    
    ended_at = Column(
        DateTime(timezone=True),
        nullable=True  # Only set when session ends
    )
    
    def __repr__(self):
        """String representation for debugging"""
        return f"<Session(session_id={self.session_id}, status={self.status})>"
