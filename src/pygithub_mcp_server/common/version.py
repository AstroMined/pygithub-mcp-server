"""Version information for the PyGithub MCP Server.

This module provides version constants and utilities for the package.
Version follows semantic versioning (major.minor.patch).
"""

from typing import Final, Tuple

# Version components
VERSION_MAJOR: Final[int] = 0
VERSION_MINOR: Final[int] = 1
VERSION_PATCH: Final[int] = 0

# Full version string
VERSION: Final[str] = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

# Version tuple for programmatic access
VERSION_TUPLE: Final[Tuple[int, int, int]] = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

def get_version() -> str:
    """Get the current version string.

    Returns:
        Current version in format "major.minor.patch"
    """
    return VERSION

def get_version_tuple() -> Tuple[int, int, int]:
    """Get the current version as a tuple.

    Returns:
        Tuple of (major, minor, patch) version numbers
    """
    return VERSION_TUPLE
