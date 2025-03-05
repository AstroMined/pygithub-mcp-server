"""Integration test configuration and fixtures.

This module provides shared pytest fixtures and configuration for integration testing
the PyGithub MCP Server with the real GitHub API.
"""

import os
import pytest
import time
import uuid
from datetime import datetime

from github import GithubException

from pygithub_mcp_server.utils.environment import load_dotenv, ENV_TEST
from pygithub_mcp_server.client.client import GitHubClient


@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    """Load test environment variables from .env.test file."""
    os.environ["PYGITHUB_ENV"] = ENV_TEST
    load_dotenv(ENV_TEST)
    yield


@pytest.fixture(scope="session")
def github_client():
    """Get GitHub client instance for testing."""
    return GitHubClient.get_instance()


@pytest.fixture(scope="session")
def test_repo(github_client):
    """Get test repository for integration tests."""
    owner = os.getenv("GITHUB_TEST_OWNER")
    repo = os.getenv("GITHUB_TEST_REPO")
    if not owner or not repo:
        pytest.skip("Test repository not configured")
    return github_client.get_repo(f"{owner}/{repo}")


@pytest.fixture(scope="session")
def test_owner():
    """Get test repository owner for integration tests."""
    owner = os.getenv("GITHUB_TEST_OWNER")
    if not owner:
        pytest.skip("Test repository owner not configured")
    return owner


@pytest.fixture(scope="session")
def test_repo_name():
    """Get test repository name for integration tests."""
    repo = os.getenv("GITHUB_TEST_REPO")
    if not repo:
        pytest.skip("Test repository name not configured")
    return repo


@pytest.fixture
def unique_id():
    """Generate a unique identifier for test resources."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_id = uuid.uuid4().hex[:8]
    return f"test-{timestamp}-{random_id}"


def retry_on_rate_limit(func):
    """Decorator for retrying functions on rate limit errors."""
    def wrapper(*args, **kwargs):
        max_retries = 3
        retry_count = 0
        last_exception = None
        
        while retry_count < max_retries:
            try:
                print(f"DEBUG: Executing {func.__name__} (attempt {retry_count + 1}/{max_retries})")
                return func(*args, **kwargs)
            except GithubException as e:
                if e.status == 403 and "rate limit" in str(e).lower():
                    retry_count += 1
                    wait_time = 2 ** retry_count  # Exponential backoff
                    print(f"Rate limit hit, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    last_exception = e
                else:
                    print(f"DEBUG: GitHub exception in {func.__name__}: {e.status} - {e.data}")
                    raise
            except Exception as e:
                print(f"DEBUG: Unexpected exception in {func.__name__}: {type(e).__name__}: {str(e)}")
                raise
        
        if last_exception:
            print(f"DEBUG: Rate limit exceeded after {max_retries} retries in {func.__name__}")
            raise GithubException(403, {"message": f"Rate limit exceeded after {max_retries} retries"})
        
        # This should never happen since we either return or raise above
        raise RuntimeError(f"Unexpected error in retry logic for {func.__name__}")
    return wrapper


@pytest.fixture
def with_retry():
    """Fixture that provides the retry_on_rate_limit decorator."""
    return retry_on_rate_limit
