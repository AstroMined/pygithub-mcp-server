"""Date and time conversion utilities.

This module provides functions for converting between datetime objects and ISO format strings
and other datetime-related conversions.
"""

from datetime import datetime, timezone
from typing import Optional, Union
import functools


def convert_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to ISO format string.

    Args:
        dt: Datetime object

    Returns:
        ISO format string or None
    """
    return dt.isoformat() if dt else None


def convert_iso_string_to_datetime(value: Union[str, datetime]) -> datetime:
    """Convert ISO 8601 string to datetime object.
    
    Handles various ISO formats including:
    - ISO 8601 format strings with timezone (e.g., "2020-01-01T00:00:00Z")
    - ISO 8601 format strings with timezone without colon (e.g., "2020-01-01T12:30:45-0500")
    - ISO 8601 format strings with short timezone (e.g., "2020-01-01T12:30:45+05")
    - datetime objects (returned as-is)
    
    Args:
        value: ISO 8601 string or datetime object
        
    Returns:
        datetime object
        
    Note:
        This function assumes the input has already been validated as a proper
        ISO 8601 format by the schema. It focuses solely on conversion.
    """
    if isinstance(value, datetime):
        return value
    
    # Handle 'Z' timezone indicator by replacing with +00:00
    value = value.replace('Z', '+00:00')
    
    # Handle timezone formats without colons
    if ('+' in value or '-' in value.split('T')[1]):
        # Find the position of the timezone sign
        sign_pos = max(value.rfind('+'), value.rfind('-'))
        if sign_pos > 0:
            timezone_part = value[sign_pos:]
            # If timezone doesn't have a colon
            if ':' not in timezone_part:
                if len(timezone_part) == 5:  # Format like "+0500"
                    # Insert colon between hours and minutes
                    value = value[:sign_pos+3] + ':' + value[sign_pos+3:]
                elif len(timezone_part) == 3:  # Format like "+05"
                    # Add ":00" for minutes
                    value = value + ":00"
                elif len(timezone_part) == 2:  # Format like "+5"
                    # Add "0:00" to make it "+05:00"
                    value = value[:sign_pos+1] + "0" + value[sign_pos+1:] + ":00"
    
    # Let fromisoformat handle any remaining conversion errors
    return datetime.fromisoformat(value)


def ensure_utc_datetime(dt: Union[str, datetime]) -> datetime:
    """Ensure datetime is timezone-aware and in UTC.
    
    Handles:
    - Naive datetime objects (assumes UTC)
    - Timezone-aware datetime objects (converts to UTC)
    - ISO 8601 strings (converts to UTC datetime)
    
    Args:
        dt: datetime object or ISO string
        
    Returns:
        UTC timezone-aware datetime
    """
    # Convert string to datetime if needed
    if isinstance(dt, str):
        dt = convert_iso_string_to_datetime(dt)
        
    # Make naive datetime timezone-aware (assume UTC)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    # Always convert to UTC to ensure consistent timezone handling
    else:
        dt = dt.astimezone(timezone.utc)
        
    # Truncate microseconds for consistency with API expectations
    dt = dt.replace(microsecond=0)
    
    return dt


def with_utc_datetimes(param_names=None):
    """Decorator to convert datetime parameters to UTC.
    
    Args:
        param_names: List of parameter names to convert (None for all datetime-like params)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Convert kwargs that are datetime-like
            for key, value in list(kwargs.items()):
                if param_names is None or key in param_names:
                    if isinstance(value, (str, datetime)):
                        kwargs[key] = ensure_utc_datetime(value)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
