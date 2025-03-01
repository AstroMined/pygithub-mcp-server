"""Date and time conversion utilities.

This module provides functions for converting datetime objects to ISO format strings
and other datetime-related conversions.
"""

from datetime import datetime
from typing import Optional


def convert_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to ISO format string.

    Args:
        dt: Datetime object

    Returns:
        ISO format string or None
    """
    return dt.isoformat() if dt else None
