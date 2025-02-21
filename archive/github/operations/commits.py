"""GitHub commit operations.

This module provides functions for working with commits in GitHub repositories,
including listing, getting details, and comparing commits.
"""

from typing import Any, Dict, List, Optional

from ..common.errors import GitHubError
from ..common.utils import get_session, format_query_params, process_response, build_url


def list_commits(
    owner: str,
    repo: str,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    sha: Optional[str] = None,
    path: Optional[str] = None,
    author: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List commits in a repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        page: Page number for pagination
        per_page: Number of results per page (max 100)
        sha: SHA or branch to start listing commits from
        path: Only commits containing this file path
        author: GitHub username, name, or email
        since: ISO 8601 date - only commits after this date
        until: ISO 8601 date - only commits before this date

    Returns:
        List of commits from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(
        page=page,
        per_page=per_page,
        sha=sha,
        path=path,
        author=author,
        since=since,
        until=until,
    )

    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/commits"), params=params
        )
        return process_response(response)


def get_commit(owner: str, repo: str, ref: str) -> Dict[str, Any]:
    """Get a specific commit.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        ref: Commit SHA

    Returns:
        Commit details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/commits/{ref}")
        )
        return process_response(response)


def compare_commits(
    owner: str, repo: str, base: str, head: str
) -> Dict[str, Any]:
    """Compare two commits.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        base: Base commit SHA or branch
        head: Head commit SHA or branch

    Returns:
        Comparison details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/compare/{base}...{head}")
        )
        return process_response(response)


def list_commit_comments(
    owner: str,
    repo: str,
    ref: str,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """List comments for a specific commit.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        ref: Commit SHA
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        List of commit comments from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(page=page, per_page=per_page)

    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/commits/{ref}/comments"),
            params=params,
        )
        return process_response(response)


def create_commit_comment(
    owner: str,
    repo: str,
    ref: str,
    body: str,
    path: Optional[str] = None,
    position: Optional[int] = None,
    line: Optional[int] = None,
) -> Dict[str, Any]:
    """Create a comment on a commit.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        ref: Commit SHA
        body: Comment text
        path: Relative path of the file to comment on
        position: Line index in the diff to comment on
        line: Line number in the file to comment on

    Returns:
        Created comment details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "body": body,
        "path": path,
        "position": position,
        "line": line,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.post(
            build_url(f"repos/{owner}/{repo}/commits/{ref}/comments"),
            json=data,
        )
        return process_response(response)


def get_commit_status(owner: str, repo: str, ref: str) -> Dict[str, Any]:
    """Get the combined status for a specific commit.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        ref: Commit SHA

    Returns:
        Combined status details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/commits/{ref}/status")
        )
        return process_response(response)


def list_commit_statuses(
    owner: str,
    repo: str,
    ref: str,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """List all statuses for a specific commit.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        ref: Commit SHA
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        List of status details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(page=page, per_page=per_page)

    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/commits/{ref}/statuses"),
            params=params,
        )
        return process_response(response)


def create_commit_status(
    owner: str,
    repo: str,
    ref: str,
    state: str,
    target_url: Optional[str] = None,
    description: Optional[str] = None,
    context: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a status for a specific commit.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        ref: Commit SHA
        state: The state (error, failure, pending, success)
        target_url: URL to associate with this status
        description: Short description of the status
        context: Label to differentiate this status from others

    Returns:
        Created status details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "state": state,
        "target_url": target_url,
        "description": description,
        "context": context,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.post(
            build_url(f"repos/{owner}/{repo}/statuses/{ref}"),
            json=data,
        )
        return process_response(response)
