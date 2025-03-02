"""Integration tests for GitHub error handling.

This module tests the error handling functionality with the real GitHub API.
"""

import pytest
from datetime import datetime

from github import GithubException, RateLimitExceededException

from pygithub_mcp_server.errors.handlers import (
    handle_github_exception,
    format_validation_error,
)
from pygithub_mcp_server.errors.exceptions import (
    GitHubError,
    GitHubAuthenticationError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubResourceNotFoundError,
    GitHubValidationError,
)


@pytest.mark.integration
def test_handle_github_exception_not_found(github_client, test_owner, with_retry):
    """Test handling of 'not found' exceptions."""
    nonexistent_repo = f"{test_owner}/nonexistent-repo-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    @with_retry
    def get_nonexistent_repo():
        try:
            github_client.github.get_repo(nonexistent_repo)
            pytest.fail("Should have raised an exception")
        except GithubException as e:
            return e
    
    # Get a real GithubException for a nonexistent repo
    exception = get_nonexistent_repo()
    
    # Handle the exception
    error = handle_github_exception(exception, resource_hint="repository")
    
    # Verify
    assert isinstance(error, GitHubResourceNotFoundError)
    assert "repository" in str(error).lower()
    assert "not found" in str(error).lower()


@pytest.mark.integration
def test_handle_github_exception_invalid_input(github_client, test_owner, test_repo_name, with_retry):
    """Test handling of validation error exceptions."""
    @with_retry
    def create_invalid_issue():
        try:
            # Try to create an issue with an empty title (invalid)
            repo = github_client.github.get_repo(f"{test_owner}/{test_repo_name}")
            repo.create_issue(title="")
            pytest.fail("Should have raised an exception")
        except GithubException as e:
            return e
    
    # Get a real GithubException for invalid input
    exception = create_invalid_issue()
    
    # Handle the exception
    error = handle_github_exception(exception, resource_hint="issue")
    
    # Verify
    assert isinstance(error, GitHubValidationError) or isinstance(error, GitHubError)
    assert error.response is not None


@pytest.mark.integration
def test_handle_github_exception_rate_limit(github_client):
    """Test handling of rate limit exceptions."""
    # Create a synthetic rate limit exception
    exception = RateLimitExceededException(
        403, 
        {"message": "API rate limit exceeded"}, 
        {"X-RateLimit-Reset": str(int(datetime.now().timestamp()) + 3600)}
    )
    
    # Handle the exception
    error = handle_github_exception(exception)
    
    # Verify
    assert isinstance(error, GitHubRateLimitError)
    assert "rate limit exceeded" in str(error).lower()
    assert error.reset_at is not None or error.reset_timestamp is not None


@pytest.mark.integration
def test_format_validation_error():
    """Test formatting of validation errors."""
    # Test with a validation error response
    error_msg = "Validation Failed"
    data = {
        "message": "Validation Failed",
        "errors": [
            {
                "resource": "Issue",
                "field": "title",
                "code": "missing_field"
            },
            {
                "resource": "Issue",
                "field": "body",
                "code": "invalid",
                "message": "Body is too long (maximum is 65536 characters)"
            }
        ]
    }
    
    # Format the error
    formatted = format_validation_error(error_msg, data)
    
    # Verify
    assert "Validation failed" in formatted
    assert "title" in formatted
    assert "body" in formatted
    assert "missing_field" in formatted or "invalid" in formatted


@pytest.mark.integration
def test_format_validation_error_no_errors():
    """Test formatting of validation errors without error details."""
    # Test with a validation error response without errors array
    error_msg = "Validation Failed"
    data = {
        "message": "Validation Failed"
    }
    
    # Format the error
    formatted = format_validation_error(error_msg, data)
    
    # Verify
    assert formatted == error_msg


@pytest.mark.integration
def test_format_validation_error_no_data():
    """Test formatting of validation errors without data."""
    # Test with a validation error response without data
    error_msg = "Validation Failed"
    
    # Format the error
    formatted = format_validation_error(error_msg, None)
    
    # Verify
    assert formatted == error_msg
