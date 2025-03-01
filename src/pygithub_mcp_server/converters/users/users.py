"""User converters.

This module provides functions for converting PyGithub user objects to our schema
representations.
"""

from typing import Any, Dict, Optional

from github.NamedUser import NamedUser


def convert_user(user: Optional[NamedUser]) -> Optional[Dict[str, Any]]:
    """Convert a PyGithub NamedUser to our schema.

    Args:
        user: PyGithub NamedUser object

    Returns:
        User data in our schema format
    """
    if user is None:
        return None

    return {
        "login": user.login,
        "id": user.id,
        "type": user.type,
        "site_admin": user.site_admin,
    }
