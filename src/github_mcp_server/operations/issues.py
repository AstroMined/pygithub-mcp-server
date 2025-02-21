"""GitHub issue operations.

This module provides functions for working with issues in GitHub repositories,
including creation, updates, comments, and listing.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from ..common.errors import GitHubError
from ..common.utils import get_session, format_query_params, process_response, build_url


def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: Optional[str] = None,
    assignees: Optional[List[str]] = None,
    labels: Optional[List[str]] = None,
    milestone: Optional[int] = None,
) -> Dict[str, Any]:
    """Create a new issue in a repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        title: Issue title
        body: Issue description
        assignees: List of usernames to assign
        labels: List of labels to add
        milestone: Milestone number to assign

    Returns:
        Created issue details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "title": title,
        "body": body,
        "assignees": assignees,
        "labels": labels,
        "milestone": milestone,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.post(
            build_url(f"repos/{owner}/{repo}/issues"), json=data
        )
        return process_response(response)


def get_issue(owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
    """Get details about a specific issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number

    Returns:
        Issue details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/issues/{issue_number}")
        )
        return process_response(response)


def update_issue(
    owner: str,
    repo: str,
    issue_number: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    state: Optional[str] = None,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None,
    milestone: Optional[Union[int, None]] = None,
) -> Dict[str, Any]:
    """Update an existing issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number to update
        title: New title
        body: New description
        state: New state (open or closed)
        labels: New labels
        assignees: New assignees
        milestone: New milestone number (None to clear)

    Returns:
        Updated issue details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "title": title,
        "body": body,
        "state": state,
        "labels": labels,
        "assignees": assignees,
        "milestone": milestone,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.patch(
            build_url(f"repos/{owner}/{repo}/issues/{issue_number}"), json=data
        )
        return process_response(response)


def list_issues(
    owner: str,
    repo: str,
    state: Optional[str] = None,
    labels: Optional[List[str]] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    since: Optional[datetime] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """List issues in a repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        state: Issue state (open, closed, all)
        labels: Filter by labels
        sort: Sort field (created, updated, comments)
        direction: Sort direction (asc, desc)
        since: Filter by date
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        List of issues from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(
        state=state,
        labels=labels,
        sort=sort,
        direction=direction,
        since=since,
        page=page,
        per_page=per_page,
    )

    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/issues"), params=params
        )
        return process_response(response)


def add_issue_comment(
    owner: str, repo: str, issue_number: int, body: str
) -> Dict[str, Any]:
    """Add a comment to an issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number to comment on
        body: Comment text

    Returns:
        Created comment details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {"body": body}

    with get_session() as session:
        response = session.post(
            build_url(f"repos/{owner}/{repo}/issues/{issue_number}/comments"), json=data
        )
        return process_response(response)


def list_issue_comments(
    owner: str,
    repo: str,
    issue_number: int,
    since: Optional[datetime] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """List comments on an issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number
        since: Filter by date
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        List of comments from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(since=since, page=page, per_page=per_page)

    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/issues/{issue_number}/comments"),
            params=params,
        )
        return process_response(response)


def update_issue_comment(
    owner: str, repo: str, comment_id: int, body: str
) -> Dict[str, Any]:
    """Update an issue comment.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        comment_id: Comment ID to update
        body: New comment text

    Returns:
        Updated comment details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {"body": body}

    with get_session() as session:
        response = session.patch(
            build_url(f"repos/{owner}/{repo}/issues/comments/{comment_id}"), json=data
        )
        return process_response(response)


def delete_issue_comment(owner: str, repo: str, comment_id: int) -> None:
    """Delete an issue comment.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        comment_id: Comment ID to delete

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.delete(
            build_url(f"repos/{owner}/{repo}/issues/comments/{comment_id}")
        )
        process_response(response)


def add_issue_labels(
    owner: str, repo: str, issue_number: int, labels: List[str]
) -> List[Dict[str, Any]]:
    """Add labels to an issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number
        labels: Labels to add

    Returns:
        Updated list of labels from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.post(
            build_url(f"repos/{owner}/{repo}/issues/{issue_number}/labels"),
            json={"labels": labels},
        )
        return process_response(response)


def remove_issue_label(
    owner: str, repo: str, issue_number: int, label: str
) -> None:
    """Remove a label from an issue.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        issue_number: Issue number
        label: Label to remove

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.delete(
            build_url(f"repos/{owner}/{repo}/issues/{issue_number}/labels/{label}")
        )
        process_response(response)
