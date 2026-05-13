"""
Business logic for session management.
Contains all the core functionality for session lifecycle operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from datetime import datetime
import uuid

from app.models.session_model import SessionModel, SessionStatus
from app.schemas.session_schema import SessionCreate, SessionUpdate


class SessionService:
    """
    Service class containing all session-related business logic.
    Separates business logic from route handlers for better organization.
    """
    
    @staticmethod
    def generate_session_id() -> str:
        """
        Generate a unique session ID using UUID4.
        UUID4 generates random UUIDs with very low collision probability.
        """
        return str(uuid.uuid4())
    
    
    @staticmethod
    def check_duplicate_active_session(
        db: Session,
        candidate_id: int
    ) -> bool:
        """
        Check if candidate already has an active session.
        Prevents duplicate active sessions for the same candidate.
        
        Args:
            db: Database session
            candidate_id: Candidate's ID to check
            
        Returns:
            True if active session exists, False otherwise
        """
        existing_session = db.query(SessionModel).filter(
            and_(
                SessionModel.candidate_id == candidate_id,
                SessionModel.status == SessionStatus.ACTIVE
            )
        ).first()
        
        return existing_session is not None
    
    
    @staticmethod
    def create_session(
        db: Session,
        session_data: SessionCreate
    ) -> SessionModel:
        """
        Create a new interview session.
        
        Args:
            db: Database session
            session_data: Session creation data
            
        Returns:
            Created session model
            
        Raises:
            HTTPException: If candidate already has active session
        """
        # Check for duplicate active session
        if SessionService.check_duplicate_active_session(
            db,
            session_data.candidate_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Candidate {session_data.candidate_id} already has an active session"
            )
        
        # Generate unique session ID
        session_id = SessionService.generate_session_id()
        
        # Create new session model
        new_session = SessionModel(
            session_id=session_id,
            candidate_id=session_data.candidate_id,
            interviewer_id=session_data.interviewer_id,
            status=SessionStatus.ACTIVE
        )
        
        # Add to database
        db.add(new_session)
        db.commit()
        db.refresh(new_session)  # Refresh to get generated values
        
        return new_session
    
    
    @staticmethod
    def get_session_by_id(
        db: Session,
        session_id: str
    ) -> SessionModel:
        """
        Retrieve session by session_id.
        
        Args:
            db: Database session
            session_id: UUID of the session
            
        Returns:
            Session model
            
        Raises:
            HTTPException: If session not found
        """
        session = db.query(SessionModel).filter(
            SessionModel.session_id == session_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session with ID {session_id} not found"
            )
        
        return session
    
    
    @staticmethod
    def get_all_sessions(db: Session) -> list[SessionModel]:
        """
        Retrieve all sessions from database.
        
        Args:
            db: Database session
            
        Returns:
            List of all session models
        """
        return db.query(SessionModel).order_by(
            SessionModel.created_at.desc()
        ).all()
    
    
    @staticmethod
    def update_session_status(
        db: Session,
        session_id: str,
        update_data: SessionUpdate
    ) -> SessionModel:
        """
        Update session status.
        
        Args:
            db: Database session
            session_id: UUID of the session
            update_data: New status data
            
        Returns:
            Updated session model
            
        Raises:
            HTTPException: If session not found or already completed
        """
        # Get existing session
        session = SessionService.get_session_by_id(db, session_id)
        
        # Prevent updating completed sessions
        if session.status == SessionStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update a completed session"
            )
        
        # Prevent updating terminated sessions
        if session.status == SessionStatus.TERMINATED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update a terminated session"
            )
        
        # Update status
        session.status = update_data.status
        session.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(session)
        
        return session
    
    
    @staticmethod
    def end_session(
        db: Session,
        session_id: str
    ) -> SessionModel:
        """
        End an interview session by marking it as completed.
        
        Args:
            db: Database session
            session_id: UUID of the session
            
        Returns:
            Completed session model
            
        Raises:
            HTTPException: If session not found or already completed
        """
        # Get existing session
        session = SessionService.get_session_by_id(db, session_id)
        
        # Prevent ending already completed sessions
        if session.status == SessionStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is already completed"
            )
        
        # Mark as completed
        session.status = SessionStatus.COMPLETED
        session.ended_at = datetime.utcnow()
        session.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(session)
        
        return session
