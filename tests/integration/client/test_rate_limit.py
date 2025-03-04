"""Integration tests for rate limit handling.

These tests verify that rate limit detection and handling work correctly
with both real GitHub API and simulated rate limits.
"""

import time
import logging
import pytest
from datetime import datetime, timedelta

from github import Github, RateLimitExceededException

from pygithub_mcp_server.client.rate_limit import (
    check_rate_limit,
    wait_for_rate_limit_reset,
    exponential_backoff,
    handle_rate_limit_with_backoff
)
from pygithub_mcp_server.client.client import GitHubClient


# Configure logging
logger = logging.getLogger(__name__)


@pytest.mark.integration
class TestRateLimit:
    """Tests for rate limit handling."""
    
    def test_check_rate_limit_real_api(self, github_client):
        """Test checking real GitHub API rate limit."""
        # Test with real GitHub client
        remaining, limit, reset_time = check_rate_limit(github_client)
        
        # Verify rate limit information
        assert isinstance(remaining, int)
        assert isinstance(limit, int)
        assert remaining <= limit
        assert isinstance(reset_time, datetime)
        
        # Reset time should be in the future
        assert reset_time > datetime.now().astimezone()
    
    def test_exponential_backoff(self):
        """Test exponential backoff calculation."""
        # Test with different attempt numbers
        delay0 = exponential_backoff(0, deterministic=True)
        delay1 = exponential_backoff(1, deterministic=True)
        delay2 = exponential_backoff(2, deterministic=True)
        
        # Each delay should be exponentially larger
        assert delay1 == delay0 * 2
        assert delay2 == delay1 * 2
        
        # Test with custom base delay
        custom_delay = exponential_backoff(1, base_delay=3.0, deterministic=True)
        assert custom_delay == 3.0 * 2
        
        # Test with jitter (non-deterministic)
        delay_with_jitter = exponential_backoff(1, deterministic=False)
        # With jitter, the delay should be slightly larger than the deterministic value
        assert delay_with_jitter >= delay1
    
    def test_exponential_backoff_max_attempts(self):
        """Test exponential backoff with max attempts."""
        # Test with attempt >= max_attempts
        with pytest.raises(ValueError, match="Maximum retry attempts"):
            exponential_backoff(5, max_attempts=5)
    
    def test_wait_for_rate_limit_reset_past_time(self):
        """Test waiting for rate limit reset with a past time."""
        # Create a time in the past
        past_time = datetime.now() - timedelta(minutes=5)
        
        # Should wait for buffer_seconds only
        buffer_seconds = 0.1
        start_time = time.time()
        wait_for_rate_limit_reset(past_time, buffer_seconds=buffer_seconds)
        elapsed = time.time() - start_time
        
        # Should wait approximately buffer_seconds
        assert elapsed >= buffer_seconds
        assert elapsed < buffer_seconds + 0.5  # Allow some execution time
    
    def test_wait_for_rate_limit_reset_future_time(self):
        """Test waiting for rate limit reset with a future time."""
        # Create a time very slightly in the future
        future_time = datetime.now() + timedelta(seconds=0.2)
        buffer_seconds = 0.1
        
        start_time = time.time()
        wait_for_rate_limit_reset(future_time, buffer_seconds=buffer_seconds)
        elapsed = time.time() - start_time
        
        # Should wait approximately 0.2 + 0.1 seconds
        assert elapsed >= 0.2
        assert elapsed < 0.5  # Allow some execution time
    
    def test_handle_rate_limit_with_backoff_test_mode(self):
        """Test handling rate limit in test mode."""
        # Create a mock exception
        exception = RateLimitExceededException(
            403, {"message": "API rate limit exceeded"}
        )
        
        # Set up for test mode with short delays
        github_client = GitHubClient.get_instance()
        
        start_time = time.time()
        handle_rate_limit_with_backoff(
            github_client, 
            exception, 
            attempt=0, 
            max_attempts=5, 
            deterministic=True, 
            test_mode=True
        )
        elapsed = time.time() - start_time
        
        # Should use short delays in test mode
        assert elapsed < 0.5  # Very short delay in test mode
    
    def test_handle_rate_limit_with_backoff_max_attempts(self):
        """Test handling rate limit with maximum attempts reached."""
        # Create a mock exception
        exception = RateLimitExceededException(
            403, {"message": "API rate limit exceeded"}
        )
        
        # Set up for test mode
        github_client = GitHubClient.get_instance()
        
        # Should raise exception when max attempts reached
        with pytest.raises(RateLimitExceededException):
            handle_rate_limit_with_backoff(
                github_client, 
                exception, 
                attempt=5,  # Already at max attempts
                max_attempts=5, 
                test_mode=True
            )
    
    def test_handle_rate_limit_with_exception_reset_time(self, monkeypatch):
        """Test handling rate limit with reset time from exception."""
        # Create a mock rate with reset time
        class MockRate:
            reset = datetime.now() + timedelta(seconds=0.2)
        
        # Create a mock exception with rate
        exception = RateLimitExceededException(
            403, {"message": "API rate limit exceeded"}
        )
        exception.rate = MockRate()
        
        # Set up for test mode
        github_client = GitHubClient.get_instance()
        
        # Mock wait_for_rate_limit_reset to verify it's called with the right reset time
        mock_called_with = None
        original_wait = wait_for_rate_limit_reset
        
        def mock_wait(reset_time, buffer_seconds=5):
            nonlocal mock_called_with
            mock_called_with = reset_time
            # Use a very short wait to speed up the test
            time.sleep(0.1)
        
        monkeypatch.setattr(
            "pygithub_mcp_server.client.rate_limit.wait_for_rate_limit_reset", 
            mock_wait
        )
        
        try:
            # Handle rate limit
            handle_rate_limit_with_backoff(
                github_client, 
                exception, 
                attempt=0, 
                max_attempts=5, 
                test_mode=False  # Not in test mode, should use reset time
            )
            
            # Verify wait_for_rate_limit_reset was called with the right reset time
            assert mock_called_with == exception.rate.reset
        finally:
            # Restore original function
            monkeypatch.setattr(
                "pygithub_mcp_server.client.rate_limit.wait_for_rate_limit_reset",
                original_wait
            )
    
    def test_handle_rate_limit_without_reset_time(self, monkeypatch):
        """Test handling rate limit without reset time."""
        # Create a mock exception without rate
        exception = RateLimitExceededException(
            403, {"message": "API rate limit exceeded"}
        )
        
        # Set up for test mode
        github_client = GitHubClient.get_instance()
        
        # Mock check_rate_limit to return no reset time
        def mock_check_rate_limit(github):
            return 0, 100, None
        
        # Mock exponential_backoff for faster tests
        def mock_exponential_backoff(attempt, max_attempts=5, base_delay=2.0, deterministic=False):
            return 0.1  # Very short delay for tests
        
        monkeypatch.setattr(
            "pygithub_mcp_server.client.rate_limit.check_rate_limit", 
            mock_check_rate_limit
        )
        monkeypatch.setattr(
            "pygithub_mcp_server.client.rate_limit.exponential_backoff", 
            mock_exponential_backoff
        )
        
        # Mock time.sleep for faster tests
        original_sleep = time.sleep
        sleep_called = False
        
        def mock_sleep(seconds):
            nonlocal sleep_called
            sleep_called = True
            original_sleep(0.01)  # Short sleep for tests
        
        monkeypatch.setattr("time.sleep", mock_sleep)
        
        try:
            # Handle rate limit
            handle_rate_limit_with_backoff(
                github_client, 
                exception, 
                attempt=0, 
                max_attempts=5, 
                deterministic=True,
                test_mode=False
            )
            
            # Verify exponential backoff was used (via sleep being called)
            assert sleep_called
        finally:
            # Restore original sleep
            monkeypatch.setattr("time.sleep", original_sleep)
