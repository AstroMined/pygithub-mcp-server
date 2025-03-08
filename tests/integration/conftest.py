"""Integration test configuration and fixtures.

This module provides shared pytest fixtures and configuration for integration testing
the PyGithub MCP Server with the real GitHub API.
"""

import os
import pytest
import time
import uuid
from datetime import datetime
import logging

from github import GithubException
from pygithub_mcp_server.utils.environment import load_dotenv, ENV_TEST
from pygithub_mcp_server.client.client import GitHubClient
from pygithub_mcp_server.errors import GitHubError

# Load environment variables as early as possible
os.environ["PYGITHUB_ENV"] = ENV_TEST
load_dotenv(ENV_TEST)

# Logger for integration tests
logger = logging.getLogger("integration_tests")

# Check for required environment variables early in the process
GITHUB_TEST_OWNER = os.environ.get("GITHUB_TEST_OWNER")
GITHUB_TEST_REPO = os.environ.get("GITHUB_TEST_REPO")
GITHUB_TOKEN = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")

def pytest_report_header(config):
    """Report integration test configuration in the pytest header."""
    if config.getoption("--run-integration"):
        env_status = []
        env_status.append("Integration Test Configuration:")
        env_status.append(f"  GITHUB_TEST_OWNER: {'✓' if GITHUB_TEST_OWNER else '✗'}")
        env_status.append(f"  GITHUB_TEST_REPO: {'✓' if GITHUB_TEST_REPO else '✗'}")
        env_status.append(f"  GITHUB_PERSONAL_ACCESS_TOKEN: {'✓' if GITHUB_TOKEN else '✗'}")
        return env_status


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


class TestResourceCleanup:
    """Helper class to track and clean up test resources."""
    
    def __init__(self):
        """Initialize the test cleanup tracker."""
        self.issues = []
        self.comments = []
        self.branches = []
        self.labels = []
        self.files = []
        
    def add_issue(self, owner, repo, issue_number):
        """Track an issue for cleanup."""
        self.issues.append((owner, repo, issue_number))
        
    def add_comment(self, owner, repo, issue_number, comment_id):
        """Track a comment for cleanup."""
        self.comments.append((owner, repo, issue_number, comment_id))
        
    def add_branch(self, owner, repo, branch):
        """Track a branch for cleanup."""
        self.branches.append((owner, repo, branch))
        
    def add_label(self, owner, repo, label):
        """Track a label for cleanup."""
        self.labels.append((owner, repo, label))
        
    def add_file(self, owner, repo, path, branch="main"):
        """Track a file for cleanup."""
        self.files.append((owner, repo, path, branch))
        
    def cleanup_all(self):
        """Clean up all tracked resources with retry logic."""
        client = GitHubClient.get_instance()
        
        # Clean up issues
        for owner, repo, issue_number in self.issues:
            try:
                logger.info(f"Cleaning up issue {owner}/{repo}#{issue_number}")
                repository = client.get_repo(f"{owner}/{repo}")
                issue = repository.get_issue(issue_number)
                if issue.state != "closed":
                    issue.edit(state="closed")
            except Exception as e:
                logger.warning(f"Failed to clean up issue {owner}/{repo}#{issue_number}: {e}")
        
        # Clean up comments
        for owner, repo, issue_number, comment_id in self.comments:
            try:
                logger.info(f"Cleaning up comment {comment_id} on {owner}/{repo}#{issue_number}")
                repository = client.get_repo(f"{owner}/{repo}")
                issue = repository.get_issue(issue_number)
                for comment in issue.get_comments():
                    if comment.id == comment_id:
                        comment.delete()
                        break
            except Exception as e:
                logger.warning(f"Failed to clean up comment {comment_id}: {e}")
        
        # Clean up branches (would use client if implemented)
        for owner, repo, branch in self.branches:
            try:
                logger.info(f"Skipping branch cleanup for {owner}/{repo}:{branch} (not implemented)")
                # This would be implemented if we had write access to test repositories
                # For safety, we're not actually deleting branches in this example
            except Exception as e:
                logger.warning(f"Failed to clean up branch {owner}/{repo}:{branch}: {e}")


@pytest.fixture
def test_cleanup():
    """Fixture to track and clean up test resources.
    
    Usage:
        def test_something(test_owner, test_repo_name, test_cleanup):
            # Create a resource
            issue = create_issue(...)
            
            # Register it for cleanup
            test_cleanup.add_issue(test_owner, test_repo_name, issue["issue_number"])
            
            # Test operations...
    """
    cleanup = TestResourceCleanup()
    yield cleanup
    cleanup.cleanup_all()


@pytest.fixture
def test_repo_obj(test_owner, test_repo_name):
    """Get PyGithub Repository object for the test repository.
    
    This is different from test_repo as it directly returns the PyGithub Repository
    object rather than using the client.get_repo() method.
    """
    if not test_owner or not test_repo_name:
        pytest.skip("Test repository information not configured")
    
    client = GitHubClient.get_instance()
    return client.get_repo(f"{test_owner}/{test_repo_name}")
