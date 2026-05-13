"""
Pydantic schemas for request/response validation.
Defines the structure of data coming in and going out of the API.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum


class SessionStatus(str, Enum):
    """Valid session status values"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    TERMINATED = "terminated"


class SessionCreate(BaseModel):
    """
    Schema for creating a new session.
    Used in POST /start-session endpoint.
    """
    candidate_id: int = Field(..., gt=0, description="Candidate's unique identifier")
    interviewer_id: int = Field(..., gt=0, description="Interviewer's unique identifier")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "candidate_id": 101,
                "interviewer_id": 201
            }
        }
    )


class SessionUpdate(BaseModel):
    """
    Schema for updating session status.
    Used in PUT /update-session/{session_id} endpoint.
    """
    status: SessionStatus = Field(..., description="New session status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "paused"
            }
        }
    )


class SessionResponse(BaseModel):
    """
    Schema for session response data.
    Used in all endpoints that return session information.
    """
    id: int
    session_id: str
    candidate_id: int
    interviewer_id: int
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    ended_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode for SQLAlchemy models
        json_schema_extra={
            "example": {
                "id": 1,
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "candidate_id": 101,
                "interviewer_id": 201,
                "status": "active",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
                "ended_at": None
            }
        }
    )


class SessionStartResponse(BaseModel):
    """
    Simplified response for session start.
    Returns only essential information.
    """
    session_id: str
    status: SessionStatus
    created_at: datetime
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "active",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    )


class ErrorResponse(BaseModel):
    """
    Standard error response schema.
    Provides consistent error format across all endpoints.
    """
    detail: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Session not found"
            }
        }
    )
