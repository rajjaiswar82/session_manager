"""
Utility functions and helper methods.
Contains reusable functions used across the application.
"""

from datetime import datetime
from typing import Optional


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """
    Format datetime object to ISO 8601 string.
    
    Args:
        dt: Datetime object to format
        
    Returns:
        ISO formatted string or None
    """
    if dt is None:
        return None
    return dt.isoformat()


def validate_positive_integer(value: int, field_name: str) -> None:
    """
    Validate that an integer is positive.
    
    Args:
        value: Integer to validate
        field_name: Name of the field (for error messages)
        
    Raises:
        ValueError: If value is not positive
    """
    if value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")


def get_current_utc_timestamp() -> datetime:
    """
    Get current UTC timestamp.
    
    Returns:
        Current datetime in UTC
    """
    return datetime.utcnow()


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Check if string is a valid UUID.
    
    Args:
        uuid_string: String to validate
        
    Returns:
        True if valid UUID, False otherwise
    """
    import uuid
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, AttributeError):
        return False
