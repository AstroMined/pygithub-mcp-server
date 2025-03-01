"""Unit test configuration and fixtures.

This module provides shared pytest fixtures and configuration for unit testing
the PyGithub MCP Server.
"""

import os
import pytest

from pygithub_mcp_server.utils.environment import load_dotenv, ENV_TEST


@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    """Load test environment variables from .env.test file."""
    # Set environment type to test
    os.environ["PYGITHUB_ENV"] = ENV_TEST
    
    # Load .env.test file
    load_dotenv(ENV_TEST)
    
    # Yield to tests
    yield
