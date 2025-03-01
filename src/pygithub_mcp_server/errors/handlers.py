"""Error handling utilities.

This module provides functions for handling GitHub API errors, including
mapping PyGithub exceptions to our custom exceptions.
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from github import GithubException, RateLimitExceededException

from .exceptions import (
    GitHubAuthenticationError,
    GitHubError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubResourceNotFoundError,
    GitHubValidationError,
)

# Get logger
logger = logging.getLogger(__name__)


def handle_github_exception(
    error: GithubException, resource_hint: Optional[str] = None
) -> GitHubError:
    """Map PyGithub exceptions to our error types.

    Args:
        error: PyGithub exception
        resource_hint: Optional hint about the resource type being accessed

    Returns:
        Appropriate GitHubError subclass instance
    """
    try:
        # Handle RateLimitExceededException specifically
        if isinstance(error, RateLimitExceededException):
            logger.error("Rate limit exceeded")
            rate = getattr(error, "rate", None)
            reset_time = None
            remaining = 0
            limit = None

            if rate:
                reset_time = getattr(rate, "reset", None)
                remaining = getattr(rate, "remaining", 0)
                limit = getattr(rate, "limit", None)

            msg = f"API rate limit exceeded ({remaining}/{limit} calls remaining)"
            if reset_time:
                try:
                    msg += f". Reset at {reset_time.strftime('%Y-%m-%d %H:%M:%S UTC')}"
                except (AttributeError, TypeError):
                    # Handle case where reset_time doesn't have strftime or isn't a datetime
                    msg += f". Reset at {reset_time}"
            return GitHubRateLimitError(msg, reset_time, None)

        data = error.data if hasattr(error, "data") else {}
        if isinstance(data, str):
            try:
                import json

                data = json.loads(data)
            except:
                data = {"message": data}

        logger.error(f"Handling GitHub exception: status={error.status}, data={data}")

        # Extract error message
        error_msg = data.get("message", str(error)) if data else str(error)

        # Determine resource type, prioritizing the hint
        resource_type = resource_hint
        if not resource_type:
            if data and "resource" in data:
                resource_type = data["resource"]
            elif "issue" in error_msg.lower():
                resource_type = "issue"
            elif "repository" in error_msg.lower():
                resource_type = "repository"
            elif "comment" in error_msg.lower():
                resource_type = "comment"
            elif "label" in error_msg.lower():
                resource_type = "label"

        if error.status == 401:
            logger.error("Authentication error")
            return GitHubAuthenticationError(
                "Authentication failed. Please verify your GitHub token.", data
            )
        elif error.status == 403:
            if "rate limit" in error_msg.lower():
                logger.error("Rate limit exceeded")
                headers = getattr(error, "headers", {}) or {}
                reset_time = headers.get("X-RateLimit-Reset")
                msg = "API rate limit exceeded"
                if reset_time:
                    from datetime import datetime

                    reset_dt = datetime.fromtimestamp(int(reset_time))
                    msg += f". Reset at {reset_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}"
                return GitHubRateLimitError(msg, reset_time, data)
            logger.error("Permission denied")
            return GitHubPermissionError(
                f"Permission denied: Resource not accessible by integration", data
            )
        elif error.status == 404:
            logger.error("Resource not found")
            msg = "Not Found"
            if resource_type:
                msg = f"{resource_type.title()} not found"
            return GitHubResourceNotFoundError(msg, data)
        elif error.status == 422:
            logger.error("Validation error")
            return GitHubValidationError(error_msg, data)
        else:
            logger.error(f"Unknown GitHub error: {error.status}")
            return GitHubError(f"GitHub API Error ({error.status}): {error_msg}", data)
    except Exception as e:
        logger.error(f"Error handling GitHub exception: {e}")
        return GitHubError(str(error), None)


def format_validation_error(error_msg: str, data: Optional[Dict[str, Any]]) -> str:
    """Format validation error message to be more user-friendly.

    Args:
        error_msg: Original error message
        data: Error response data

    Returns:
        Formatted error message
    """
    if not data:
        return error_msg

    # Extract validation errors from response data
    errors = data.get("errors", [])
    if not errors:
        return error_msg

    # Format each validation error
    formatted_errors = []
    for error in errors:
        if "field" in error:
            field = error["field"]
            code = error.get("code", "invalid")
            message = error.get("message", "is invalid")
            formatted_errors.append(f"- {field}: {message} ({code})")

    if formatted_errors:
        return "Validation failed:\n" + "\n".join(formatted_errors)
    return error_msg
