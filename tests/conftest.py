"""Shared test configuration and fixtures.

This module provides shared pytest fixtures and configuration for testing
the PyGithub MCP Server.
"""

import os
import pytest

from pygithub_mcp_server.utils.environment import load_dotenv, ENV_TEST


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test that uses the real GitHub API"
    )


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests that use the real GitHub API",
    )


def pytest_collection_modifyitems(config, items):
    """Skip integration tests unless --run-integration is specified."""
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(reason="Need --run-integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    """Load test environment variables from .env.test file."""
    # Set environment type to test
    os.environ["PYGITHUB_ENV"] = ENV_TEST
    
    # Load .env.test file
    load_dotenv(ENV_TEST)
    
    # Yield to tests
    yield
