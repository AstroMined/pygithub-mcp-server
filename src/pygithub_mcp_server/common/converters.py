"""Conversion utilities for PyGithub objects.

DEPRECATED: This module is deprecated. Import from pygithub_mcp_server.converters instead.

This module re-exports all converters from the new location for backward compatibility.
"""

import warnings

# Show deprecation warning
warnings.warn(
    "The pygithub_mcp_server.common.converters module is deprecated. "
    "Import from pygithub_mcp_server.converters instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export all converters from the new location
from pygithub_mcp_server.converters import (
    convert_user,
    convert_label,
    convert_milestone,
    convert_issue,
    convert_issue_comment,
    convert_datetime,
    convert_repository,
    convert_file_content,
)

__all__ = [
    "convert_user",
    "convert_label",
    "convert_milestone",
    "convert_issue",
    "convert_issue_comment",
    "convert_datetime",
    "convert_repository",
    "convert_file_content",
]
