"""
API route handlers for session management endpoints.
Defines all REST API endpoints and their request/response handling.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.session_schema import (
    SessionCreate,
    SessionUpdate,
    SessionResponse,
    SessionStartResponse
)
from app.services.session_service import SessionService

# Create router instance
router = APIRouter(
    prefix="/api/v1",
    tags=["sessions"]
)


@router.post(
    "/start-session",
    response_model=SessionStartResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start a new interview session",
    description="Creates a new interview session with unique session ID"
)
def start_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db)
):
    """
    Start a new interview session.
    
    - **candidate_id**: Unique identifier for the candidate
    - **interviewer_id**: Unique identifier for the interviewer
    
    Returns session_id, status, and created_at timestamp.
    Prevents duplicate active sessions for the same candidate.
    """
    session = SessionService.create_session(db, session_data)
    
    return SessionStartResponse(
        session_id=session.session_id,
        status=session.status,
        created_at=session.created_at
    )


@router.get(
    "/session/{session_id}",
    response_model=SessionResponse,
    summary="Get session details",
    description="Retrieve complete details of a specific session"
)
def get_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific session by session_id.
    
    - **session_id**: UUID of the session to retrieve
    
    Returns complete session information including all timestamps.
    """
    return SessionService.get_session_by_id(db, session_id)


@router.get(
    "/sessions",
    response_model=List[SessionResponse],
    summary="Get all sessions",
    description="Retrieve list of all interview sessions"
)
def get_all_sessions(
    db: Session = Depends(get_db)
):
    """
    Get all interview sessions.
    
    Returns list of all sessions ordered by creation date (newest first).
    """
    return SessionService.get_all_sessions(db)


@router.put(
    "/update-session/{session_id}",
    response_model=SessionResponse,
    summary="Update session status",
    description="Update the status of an existing session"
)
def update_session(
    session_id: str,
    update_data: SessionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update session status.
    
    - **session_id**: UUID of the session to update
    - **status**: New status (active, paused, completed, terminated)
    
    Prevents updating already completed or terminated sessions.
    Automatically updates the updated_at timestamp.
    """
    return SessionService.update_session_status(db, session_id, update_data)


@router.post(
    "/end-session/{session_id}",
    response_model=SessionResponse,
    summary="End interview session",
    description="Mark session as completed and record end time"
)
def end_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    End an interview session.
    
    - **session_id**: UUID of the session to end
    
    Marks session as completed, sets ended_at timestamp.
    Prevents ending already completed sessions.
    """
    return SessionService.end_session(db, session_id)
