"""Parameter formatting utilities.

This module provides functions for formatting parameters for GitHub API requests.
"""

from datetime import datetime
from typing import Any, Dict


def format_query_params(**kwargs: Any) -> Dict[str, str]:
    """Format query parameters for GitHub API requests.

    Args:
        **kwargs: Query parameters to format

    Returns:
        Formatted query parameters
    """
    params: Dict[str, str] = {}
    for key, value in kwargs.items():
        if value is not None:
            if isinstance(value, bool):
                params[key] = str(value).lower()
            elif isinstance(value, (list, tuple)):
                params[key] = ",".join(str(v) for v in value)
            elif isinstance(value, datetime):
                params[key] = value.isoformat()
            else:
                params[key] = str(value)
    return params
