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
        # Use timezone-aware comparison for datetime
        now = datetime.now().astimezone()
        if reset_time.tzinfo is None:
            reset_time = reset_time.astimezone()
        assert reset_time > now - timedelta(hours=1)  # Should be recent or in the future


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
    # Test with deterministic mode for predictable results
    delay0 = exponential_backoff(0, deterministic=True)
    delay1 = exponential_backoff(1, deterministic=True)
    delay2 = exponential_backoff(2, deterministic=True)
    
    # Verify exact exponential growth in deterministic mode
    assert delay0 == 2.0  # Base delay
    assert delay1 == 4.0  # 2.0 * 2^1
    assert delay2 == 8.0  # 2.0 * 2^2
    
    # Also test with jitter to ensure it's different
    delay0_with_jitter = exponential_backoff(0)
    assert delay0_with_jitter != delay0  # Should include jitter
    
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
            github_client.github, exception, attempt=2, max_attempts=2,
            test_mode=True  # Use test mode to avoid long waits
        )
    assert "rate limit" in str(exc.value).lower()
    
    # Test with valid attempt in deterministic mode and test mode
    start_time = time.time()
    handle_rate_limit_with_backoff(
        github_client.github, exception, attempt=0, max_attempts=3, 
        deterministic=True, test_mode=True
    )
    elapsed = time.time() - start_time
    # Should be very quick in test mode with base_delay=0.1
    assert elapsed < 0.2  # Should be around 0.1 seconds in test mode
    
    # Test backoff behavior (should have increasing delays)
    start_time = time.time()
    handle_rate_limit_with_backoff(
        github_client.github, exception, attempt=1, max_attempts=3, 
        deterministic=True, test_mode=True
    )
    elapsed1 = time.time() - start_time
    
    start_time = time.time()
    handle_rate_limit_with_backoff(
        github_client.github, exception, attempt=2, max_attempts=3, 
        deterministic=True, test_mode=True
    )
    elapsed2 = time.time() - start_time
    
    # Verify exponential backoff (second attempt should take longer than first)
    assert elapsed2 > elapsed1
