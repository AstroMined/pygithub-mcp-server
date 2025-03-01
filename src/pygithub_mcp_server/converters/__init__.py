"""Conversion utilities for PyGithub objects and API interactions.

This module provides functions for converting between different data formats:
- PyGithub objects to our schema representations
- Parameters to API-compatible formats
- API responses to standardized tool responses
- Date/time conversions

This package replaces the monolithic converters.py and parts of utils.py
to provide better organization and separation of concerns.
"""

# Re-export all converters for backward compatibility
from .users.users import convert_user
from .issues.issues import convert_issue, convert_label, convert_milestone
from .issues.comments import convert_issue_comment
from .repositories.repositories import convert_repository
from .repositories.contents import convert_file_content
from .common.datetime import convert_datetime
from .responses import create_tool_response
from .parameters import format_query_params

__all__ = [
    # User converters
    "convert_user",
    
    # Issue converters
    "convert_issue",
    "convert_label",
    "convert_milestone",
    "convert_issue_comment",
    
    # Repository converters
    "convert_repository",
    "convert_file_content",
    
    # Common converters
    "convert_datetime",
    
    # Response formatters
    "create_tool_response",
    
    # Parameter formatters
    "format_query_params",
]
