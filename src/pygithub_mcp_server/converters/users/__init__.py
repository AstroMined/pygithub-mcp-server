"""User-related converters.

This module provides functions for converting PyGithub user objects to our schema
representations.
"""

from .users import convert_user

__all__ = [
    "convert_user",
]
