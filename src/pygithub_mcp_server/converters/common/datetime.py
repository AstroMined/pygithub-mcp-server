"""Date and time conversion utilities.

This module provides functions for converting between datetime objects and ISO format strings
and other datetime-related conversions.
"""

from datetime import datetime
from typing import Optional, Union


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
