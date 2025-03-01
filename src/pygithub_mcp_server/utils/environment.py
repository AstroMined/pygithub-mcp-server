"""Environment and configuration utilities.

This module provides functions for accessing environment variables and
configuration settings.
"""

import os
from pathlib import Path
from typing import Any, Optional, TypeVar, cast

from pygithub_mcp_server.errors import GitHubError

T = TypeVar('T')

# Environment types
ENV_TEST = "test"
ENV_DEV = "dev"
ENV_PROD = "prod"


def load_dotenv(env_type: Optional[str] = None) -> None:
    """Load environment variables from .env file.
    
    Args:
        env_type: Environment type (test, dev, prod)
    """
    # Determine environment type
    if env_type is None:
        env_type = os.getenv("PYGITHUB_ENV", ENV_PROD)
    
    # Determine .env file path
    if env_type == ENV_TEST:
        env_file = ".env.test"
    elif env_type == ENV_DEV:
        env_file = ".env.dev"
    else:
        env_file = ".env"
    
    # Find project root (where .env file should be)
    current_dir = Path.cwd()
    env_path = current_dir / env_file
    
    # Load .env file if it exists
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                # Only set if not already in environment
                if key not in os.environ:
                    os.environ[key] = value


def get_github_token() -> str:
    """Get GitHub personal access token from environment.

    Returns:
        GitHub personal access token

    Raises:
        GitHubError: If token is not set in environment
    """
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise GitHubError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
    return token


def get_env_var(name: str, default: Optional[T] = None) -> Any:
    """Get environment variable with optional default.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If variable is not set and no default provided
    """
    value = os.getenv(name)
    if value is None:
        if default is None:
            raise ValueError(f"Environment variable {name} not set")
        return default
    return value


def get_bool_env_var(name: str, default: Optional[bool] = None) -> bool:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value of environment variable

    Raises:
        ValueError: If variable is not set and no default provided
                   or if value is not a valid boolean
    """
    value = get_env_var(name, None if default is None else str(default))
    
    if value is None:
        raise ValueError(f"Environment variable {name} not set")
    
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        value = value.lower()
        if value in ('true', 'yes', '1', 'y'):
            return True
        if value in ('false', 'no', '0', 'n'):
            return False
    
    raise ValueError(f"Environment variable {name} has invalid boolean value: {value}")
