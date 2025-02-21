"""GitHub search operations.

This module provides functions for searching various GitHub resources,
including code, issues, pull requests, and users.
"""

from typing import Any, Dict, Optional

from ..common.errors import GitHubError
from ..common.types import SearchCodeParams, SearchIssuesParams, SearchUsersParams
from ..common.utils import get_session, format_query_params, process_response, build_url


def search_code(params: SearchCodeParams) -> Dict[str, Any]:
    """Search for code across GitHub repositories.

    Args:
        params: Code search parameters

    Returns:
        Search results from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    query_params = format_query_params(
        q=params.q,
        sort=params.sort,
        order=params.order,
        per_page=params.per_page,
        page=params.page,
    )

    with get_session() as session:
        response = session.get(
            build_url("search/code"), params=query_params
        )
        return process_response(response)


def search_issues(params: SearchIssuesParams) -> Dict[str, Any]:
    """Search for issues and pull requests across GitHub repositories.

    Args:
        params: Issue search parameters

    Returns:
        Search results from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    query_params = format_query_params(
        q=params.q,
        sort=params.sort,
        order=params.order,
        per_page=params.per_page,
        page=params.page,
    )

    with get_session() as session:
        response = session.get(
            build_url("search/issues"), params=query_params
        )
        return process_response(response)


def search_users(params: SearchUsersParams) -> Dict[str, Any]:
    """Search for users on GitHub.

    Args:
        params: User search parameters

    Returns:
        Search results from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    query_params = format_query_params(
        q=params.q,
        sort=params.sort,
        order=params.order,
        per_page=params.per_page,
        page=params.page,
    )

    with get_session() as session:
        response = session.get(
            build_url("search/users"), params=query_params
        )
        return process_response(response)


def search_commits(
    query: str,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> Dict[str, Any]:
    """Search for commits across GitHub repositories.

    Args:
        query: Search query string
        sort: Sort field (author-date, committer-date)
        order: Sort order (asc, desc)
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        Search results from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(
        q=query,
        sort=sort,
        order=order,
        page=page,
        per_page=per_page,
    )

    with get_session() as session:
        response = session.get(
            build_url("search/commits"), params=params
        )
        return process_response(response)


def search_topics(
    query: str,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> Dict[str, Any]:
    """Search for repository topics on GitHub.

    Args:
        query: Search query string
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        Search results from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(
        q=query,
        page=page,
        per_page=per_page,
    )

    with get_session() as session:
        response = session.get(
            build_url("search/topics"), params=params
        )
        return process_response(response)


def search_labels(
    repository_id: int,
    query: str,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> Dict[str, Any]:
    """Search for labels in a repository.

    Args:
        repository_id: Repository ID to search in
        query: Search query string
        sort: Sort field (created, updated)
        order: Sort order (asc, desc)
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        Search results from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(
        repository_id=repository_id,
        q=query,
        sort=sort,
        order=order,
        page=page,
        per_page=per_page,
    )

    with get_session() as session:
        response = session.get(
            build_url("search/labels"), params=params
        )
        return process_response(response)


def search_repositories_by_topic(
    topic: str,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> Dict[str, Any]:
    """Search for repositories by topic.

    Args:
        topic: Topic to search for
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        Search results from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(
        q=f"topic:{topic}",
        page=page,
        per_page=per_page,
    )

    with get_session() as session:
        response = session.get(
            build_url("search/repositories"), params=params
        )
        return process_response(response)
