"""Utility functions for GitHub API operations.

This module provides helper functions for working with the GitHub API,
including request handling, response processing, and error management.
"""

import os
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Union, cast

import requests
from requests import Response

from .errors import (
    GitHubAuthenticationError,
    GitHubConflictError,
    GitHubError,
    GitHubPermissionError,
    GitHubRateLimitError,
    GitHubResourceNotFoundError,
    GitHubValidationError,
)
from .types import ResponseContent, TextContent, ToolResponse

# GitHub API constants
API_BASE_URL = "https://api.github.com"
API_VERSION = "2022-11-28"
DEFAULT_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": API_VERSION,
}

def get_session() -> requests.Session:
    """Create a requests Session configured for GitHub API.

    Returns:
        Configured requests Session
    """
    session = requests.Session()
    session.headers.update({
        **DEFAULT_HEADERS,
        "Authorization": f"Bearer {get_github_token()}"
    })
    # Don't set base_url as an attribute, use it directly in URL construction
    return session

def build_url(endpoint: str) -> str:
    """Build a full GitHub API URL.

    Args:
        endpoint: API endpoint path

    Returns:
        Full API URL
    """
    # Remove leading slash if present
    if endpoint.startswith('/'):
        endpoint = endpoint[1:]
    return f"{API_BASE_URL}/{endpoint}"

def get_github_token() -> str:
    """Get GitHub personal access token from environment.

    Returns:
        GitHub personal access token

    Raises:
        GitHubError: If token is not set in environment
    """
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise GitHubError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
    return token


def parse_rate_limit_headers(response: Response) -> Tuple[int, datetime]:
    """Parse rate limit headers from GitHub API response.

    Args:
        response: API response with rate limit headers

    Returns:
        Tuple of (remaining requests, reset time)
    """
    remaining = int(response.headers.get("X-RateLimit-Remaining", "0"))
    reset_timestamp = int(response.headers.get("X-RateLimit-Reset", "0"))
    reset_time = datetime.fromtimestamp(reset_timestamp)
    return remaining, reset_time


def process_error_response(
    response: Response, error_data: Optional[Dict[str, Any]] = None
) -> None:
    """Process error response from GitHub API.

    Args:
        response: Error response from API
        error_data: Optional parsed error data

    Raises:
        GitHubError: Appropriate error type based on response
    """
    if error_data is None:
        try:
            error_data = response.json()
        except ValueError:
            error_data = {"message": response.text}

    message = error_data.get("message", "Unknown error")

    if response.status_code == 401:
        raise GitHubAuthenticationError(message, error_data)
    elif response.status_code == 403:
        remaining, reset_time = parse_rate_limit_headers(response)
        if remaining == 0:
            raise GitHubRateLimitError(message, reset_time, error_data)
        raise GitHubPermissionError(message, error_data)
    elif response.status_code == 404:
        raise GitHubResourceNotFoundError(message, error_data)
    elif response.status_code == 409:
        raise GitHubConflictError(message, error_data)
    elif response.status_code == 422:
        raise GitHubValidationError(message, error_data)
    else:
        raise GitHubError(f"API error ({response.status_code}): {message}", error_data)


def process_response(response: Response) -> Any:
    """Process successful response from GitHub API.

    Args:
        response: Successful response from API

    Returns:
        Parsed response data

    Raises:
        GitHubError: If response indicates an error
    """
    if not response.ok:
        process_error_response(response)

    if response.status_code == 204:  # No content
        return None

    try:
        return response.json()
    except ValueError as e:
        raise GitHubError(f"Invalid JSON response: {e}") from e


def create_tool_response(
    data: Any, is_error: bool = False
) -> Dict[str, Union[list, bool]]:
    """Create a standardized tool response.

    Args:
        data: Response data to format
        is_error: Whether this is an error response

    Returns:
        Formatted tool response
    """
    content: ResponseContent
    if isinstance(data, str):
        content = TextContent(type="text", text=data)
    else:
        content = TextContent(type="text", text=str(data))

    return ToolResponse(
        content=[cast(Dict[str, Any], content.model_dump())],
        is_error=is_error,
    ).model_dump()


def format_query_params(**kwargs: Any) -> Dict[str, str]:
    """Format query parameters for GitHub API requests.

    Args:
        **kwargs: Query parameters to format

    Returns:
        Formatted query parameters
    """
    params: Dict[str, str] = {}
    for key, value in kwargs.items():
        if value is not None:
            if isinstance(value, bool):
                params[key] = str(value).lower()
            elif isinstance(value, (list, tuple)):
                params[key] = ",".join(str(v) for v in value)
            elif isinstance(value, datetime):
                params[key] = value.isoformat()
            else:
                params[key] = str(value)
    return params
