"""Test configuration and environment setup.

This module handles loading test configuration from environment variables
and provides fixtures for setting up test infrastructure.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def get_required_env(name: str) -> str:
    """Get a required environment variable or raise an error."""
    value = os.getenv(name)
    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}\n"
            "Please check .env.example for required configuration."
        )
    return value

def get_optional_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get an optional environment variable or return default."""
    return os.getenv(name, default)

# Required test configuration
GITHUB_TEST_TOKEN = get_required_env("GITHUB_TEST_TOKEN")
GITHUB_TEST_OWNER = get_required_env("GITHUB_TEST_OWNER")
GITHUB_TEST_REPO = get_required_env("GITHUB_TEST_REPO")

# Optional test configuration
GITHUB_API_BASE_URL = get_optional_env("GITHUB_API_BASE_URL", "https://api.github.com")
