"""GitHub repository operations.

This module provides functions for working with GitHub repositories,
including creation, forking, and searching.
"""

from typing import Any, Dict, List, Optional

from ..common.errors import GitHubError
from ..common.types import CreateRepositoryParams
from ..common.utils import (
    get_session,
    format_query_params,
    process_response,
    build_url,
)


def search_repositories(
    query: str, page: Optional[int] = None, per_page: Optional[int] = None
) -> Dict[str, Any]:
    """Search for GitHub repositories.

    Args:
        query: Search query string
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        Search results from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(q=query, page=page, per_page=per_page)

    with get_session() as session:
        response = session.get(
            build_url("search/repositories"), params=params
        )
        return process_response(response)


def create_repository(params: CreateRepositoryParams) -> Dict[str, Any]:
    """Create a new GitHub repository.

    Args:
        params: Repository creation parameters

    Returns:
        Created repository details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "name": params.name,
        "description": params.description,
        "private": params.private,
        "auto_init": params.auto_init,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.post(
            build_url("user/repos"), json=data
        )
        return process_response(response)


def fork_repository(
    owner: str, repo: str, organization: Optional[str] = None
) -> Dict[str, Any]:
    """Fork a GitHub repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        organization: Optional organization to fork to

    Returns:
        Forked repository details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {}
    if organization:
        data["organization"] = organization

    with get_session() as session:
        response = session.post(
            build_url(f"repos/{owner}/{repo}/forks"), json=data
        )
        return process_response(response)


def get_repository(owner: str, repo: str) -> Dict[str, Any]:
    """Get details about a GitHub repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name

    Returns:
        Repository details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}")
        )
        return process_response(response)


def update_repository(
    owner: str,
    repo: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    private: Optional[bool] = None,
    default_branch: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a GitHub repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        name: New repository name
        description: New repository description
        private: New private/public status
        default_branch: New default branch

    Returns:
        Updated repository details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "name": name,
        "description": description,
        "private": private,
        "default_branch": default_branch,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.patch(
            build_url(f"repos/{owner}/{repo}"), json=data
        )
        return process_response(response)


def delete_repository(owner: str, repo: str) -> None:
    """Delete a GitHub repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.delete(
            build_url(f"repos/{owner}/{repo}")
        )
        process_response(response)


def list_repositories(
    username: Optional[str] = None,
    type: str = "all",
    sort: str = "full_name",
    direction: str = "asc",
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """List GitHub repositories for a user.

    Args:
        username: Optional username (defaults to authenticated user)
        type: Type of repositories to list
            (all, owner, public, private, member)
        sort: Sort field (created, updated, pushed, full_name)
        direction: Sort direction (asc or desc)
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        List of repository details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(
        type=type,
        sort=sort,
        direction=direction,
        page=page,
        per_page=per_page,
    )

    with get_session() as session:
        if username:
            url = build_url(f"users/{username}/repos")
        else:
            url = build_url("user/repos")

        response = session.get(url, params=params)
        return process_response(response)
