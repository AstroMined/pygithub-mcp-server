"""Integration tests for GitHub rate limit handling.

This module tests the rate limit handling functions with the real GitHub API.
"""

import pytest
import time
from datetime import datetime, timedelta

from github import Github, RateLimitExceededException

from pygithub_mcp_server.client.rate_limit import (
    check_rate_limit,
    wait_for_rate_limit_reset,
    exponential_backoff,
    handle_rate_limit_with_backoff,
)


@pytest.mark.integration
def test_check_rate_limit(github_client, with_retry):
    """Test check_rate_limit function with real GitHub API."""
    @with_retry
    def check_rate():
        return check_rate_limit(github_client.github)
    
    # Check rate limit
    remaining, limit, reset_time = check_rate()
    
    # Verify
    assert isinstance(remaining, int)
    assert isinstance(limit, int)
    assert limit > 0
    assert remaining <= limit
    assert reset_time is None or isinstance(reset_time, datetime)
    if reset_time:
        assert reset_time > datetime.now() - timedelta(hours=1)  # Should be recent or in the future


@pytest.mark.integration
def test_wait_for_rate_limit_reset():
    """Test wait_for_rate_limit_reset function."""
    # Test with reset time in the past
    past_time = datetime.now() - timedelta(seconds=10)
    start_time = time.time()
    wait_for_rate_limit_reset(past_time, buffer_seconds=1)
    elapsed = time.time() - start_time
    assert elapsed >= 1  # Should wait at least buffer_seconds
    
    # Test with reset time in the near future
    future_time = datetime.now() + timedelta(seconds=2)
    start_time = time.time()
    wait_for_rate_limit_reset(future_time, buffer_seconds=1)
    elapsed = time.time() - start_time
    assert elapsed >= 3  # Should wait at least until reset_time + buffer_seconds


@pytest.mark.integration
def test_exponential_backoff():
    """Test exponential_backoff function."""
    # Test with different attempt numbers
    delay0 = exponential_backoff(0)
    delay1 = exponential_backoff(1)
    delay2 = exponential_backoff(2)
    
    # Verify exponential growth
    assert delay0 > 0
    assert delay1 > delay0
    assert delay2 > delay1
    assert delay1 >= delay0 * 2  # Should at least double
    assert delay2 >= delay1 * 2  # Should at least double
    
    # Test max attempts
    with pytest.raises(ValueError) as exc:
        exponential_backoff(5, max_attempts=5)
    assert "Maximum retry attempts" in str(exc.value)


@pytest.mark.integration
def test_handle_rate_limit_with_backoff(github_client):
    """Test handle_rate_limit_with_backoff function."""
    # Create a rate limit exception
    exception = RateLimitExceededException(
        403, {"message": "API rate limit exceeded"}, {}
    )
    
    # Test with attempt exceeding max_attempts
    with pytest.raises(RateLimitExceededException) as exc:
        handle_rate_limit_with_backoff(
            github_client.github, exception, attempt=2, max_attempts=2
        )
    assert "rate limit" in str(exc.value).lower()
    
    # Test with valid attempt (should not raise, just wait)
    start_time = time.time()
    handle_rate_limit_with_backoff(
        github_client.github, exception, attempt=0, max_attempts=3
    )
    elapsed = time.time() - start_time
    assert elapsed > 0  # Should have waited some time
