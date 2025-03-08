"""Version information for the PyGithub MCP Server.

This module provides version constants and utilities for the package.
Version follows semantic versioning (major.minor.patch).

TODO: Future Implementation Plan
Once the project stabilizes, replace this manual version management with importlib.metadata:

```python
from importlib.metadata import version
from typing import Tuple

# Get version from package metadata (which uses pyproject.toml)
VERSION = version("pygithub-mcp-server")

# Parse version components
VERSION_PARTS = VERSION.split(".")
VERSION_MAJOR = int(VERSION_PARTS[0])
VERSION_MINOR = int(VERSION_PARTS[1])
VERSION_PATCH = int(VERSION_PARTS[2].split("+")[0].split("rc")[0])  # Handle potential suffixes
VERSION_TUPLE = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
```

This approach will read the version directly from the installed package metadata,
which is derived from pyproject.toml during installation, creating a single source of truth.
"""

from typing import Final, Tuple

# Version components - IMPORTANT: Keep in sync with pyproject.toml
# TODO: Once project stabilizes, replace with importlib.metadata approach to read version from package metadata
VERSION_MAJOR: Final[int] = 0
VERSION_MINOR: Final[int] = 5
VERSION_PATCH: Final[int] = 20

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
