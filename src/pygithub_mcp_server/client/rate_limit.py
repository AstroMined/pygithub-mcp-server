"""Rate limit handling for GitHub API.

This module provides functions for handling GitHub API rate limits,
including checking rate limits and implementing exponential backoff.
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple

from github import Github, RateLimitExceededException

# Get logger
logger = logging.getLogger(__name__)


def check_rate_limit(github: Github) -> Tuple[int, int, Optional[datetime]]:
    """Check current rate limit status.

    Args:
        github: PyGithub instance

    Returns:
        Tuple of (remaining requests, limit, reset time)
    """
    try:
        rate_limit = github.get_rate_limit()
        core_rate = rate_limit.core
        
        return core_rate.remaining, core_rate.limit, core_rate.reset
    except Exception as e:
        logger.warning(f"Failed to check rate limit: {e}")
        return 0, 0, None


def wait_for_rate_limit_reset(reset_time: datetime, buffer_seconds: int = 5) -> None:
    """Wait until rate limit resets.

    Args:
        reset_time: When the rate limit will reset
        buffer_seconds: Additional seconds to wait as buffer
    """
    # Ensure both are timezone-aware for comparison
    now = datetime.now().astimezone()
    if reset_time.tzinfo is None:
        reset_time = reset_time.astimezone()  # Local timezone if none specified
        
    if reset_time > now:
        wait_seconds = (reset_time - now).total_seconds() + buffer_seconds
        logger.info(f"Rate limit exceeded. Waiting {wait_seconds:.1f} seconds until reset.")
        time.sleep(wait_seconds)
    else:
        # If reset_time is in the past, wait a small amount of time
        logger.info(f"Rate limit reset time is in the past. Waiting {buffer_seconds} seconds.")
        time.sleep(buffer_seconds)


def exponential_backoff(
    attempt: int, max_attempts: int = 5, base_delay: float = 2.0, deterministic: bool = False
) -> float:
    """Calculate exponential backoff delay.

    Args:
        attempt: Current attempt number (0-based)
        max_attempts: Maximum number of attempts
        base_delay: Base delay in seconds
        deterministic: If True, don't add jitter (useful for testing)

    Returns:
        Delay in seconds
    """
    if attempt >= max_attempts:
        raise ValueError(f"Maximum retry attempts ({max_attempts}) exceeded")
    
    # Calculate exponential backoff
    delay = base_delay * (2 ** attempt)
    
    # Add jitter unless in deterministic mode
    if not deterministic:
        import random
        jitter = random.uniform(0, 0.1 * delay)  # 10% jitter
        return delay + jitter
    
    return delay


def handle_rate_limit_with_backoff(
    github: Github, 
    exception: RateLimitExceededException,
    attempt: int = 0,
    max_attempts: int = 5,
    deterministic: bool = False,
    test_mode: bool = False
) -> None:
    """Handle rate limit exception with exponential backoff.

    Args:
        github: PyGithub instance
        exception: Rate limit exception
        attempt: Current attempt number (0-based)
        max_attempts: Maximum number of attempts
        deterministic: If True, use deterministic backoff (for testing)
        test_mode: If True, use short delays instead of waiting for real reset times (for testing)

    Raises:
        RateLimitExceededException: If max attempts are exceeded
    """
    if attempt >= max_attempts:
        logger.error(f"Maximum retry attempts ({max_attempts}) exceeded for rate limit")
        raise exception
    
    # In test mode, use exponential backoff with very short delays
    if test_mode:
        delay = exponential_backoff(attempt, max_attempts, base_delay=0.1, deterministic=deterministic)
        logger.info(f"Test mode: Using short delay instead of waiting for reset: {delay:.1f} seconds.")
        time.sleep(delay)
        return
    
    # Try to get reset time from exception
    reset_time = None
    rate = getattr(exception, 'rate', None)
    if rate:
        reset_time = getattr(rate, 'reset', None)
    
    # If we couldn't get reset time from exception, check rate limit
    if not reset_time:
        _, _, reset_time = check_rate_limit(github)
    
    # If we have a reset time, wait until then
    if reset_time:
        wait_for_rate_limit_reset(reset_time)
    else:
        # Otherwise use exponential backoff
        delay = exponential_backoff(attempt, max_attempts, deterministic=deterministic)
        logger.info(f"Rate limit exceeded. Using exponential backoff: waiting {delay:.1f} seconds.")
        time.sleep(delay)
