"""GitHub pull request operations.

This module provides functions for working with pull requests in GitHub repositories,
including creation, updates, reviews, and merging.
"""

from typing import Any, Dict, List, Optional

from ..common.errors import GitHubError
from ..common.types import CreatePullRequestParams
from ..common.utils import get_session, format_query_params, process_response, build_url


def create_pull_request(params: CreatePullRequestParams) -> Dict[str, Any]:
    """Create a new pull request.

    Args:
        params: Pull request creation parameters

    Returns:
        Created pull request details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "title": params.title,
        "head": params.head,
        "base": params.base,
        "body": params.body,
        "draft": params.draft,
        "maintainer_can_modify": params.maintainer_can_modify,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.post(
            build_url(f"repos/{params.owner}/{params.repo}/pulls"), json=data
        )
        return process_response(response)


def get_pull_request(
    owner: str, repo: str, pull_number: int
) -> Dict[str, Any]:
    """Get details about a specific pull request.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        pull_number: Pull request number

    Returns:
        Pull request details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/pulls/{pull_number}")
        )
        return process_response(response)


def update_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    state: Optional[str] = None,
    base: Optional[str] = None,
    maintainer_can_modify: Optional[bool] = None,
) -> Dict[str, Any]:
    """Update a pull request.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        pull_number: Pull request number
        title: New title
        body: New description
        state: New state (open or closed)
        base: New base branch
        maintainer_can_modify: Allow maintainer modifications

    Returns:
        Updated pull request details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "title": title,
        "body": body,
        "state": state,
        "base": base,
        "maintainer_can_modify": maintainer_can_modify,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.patch(
            build_url(f"repos/{owner}/{repo}/pulls/{pull_number}"), json=data
        )
        return process_response(response)


def list_pull_requests(
    owner: str,
    repo: str,
    state: Optional[str] = None,
    head: Optional[str] = None,
    base: Optional[str] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """List pull requests in a repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        state: PR state (open, closed, all)
        head: Filter by head user/branch
        base: Filter by base branch
        sort: Sort field (created, updated, popularity, long-running)
        direction: Sort direction (asc, desc)
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        List of pull requests from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = format_query_params(
        state=state,
        head=head,
        base=base,
        sort=sort,
        direction=direction,
        page=page,
        per_page=per_page,
    )

    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/pulls"), params=params
        )
        return process_response(response)


def merge_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
    commit_title: Optional[str] = None,
    commit_message: Optional[str] = None,
    merge_method: Optional[str] = None,
    sha: Optional[str] = None,
) -> Dict[str, Any]:
    """Merge a pull request.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        pull_number: Pull request number
        commit_title: Title for merge commit
        commit_message: Extra detail for merge commit
        merge_method: Merge method (merge, squash, rebase)
        sha: SHA that pull request head must match

    Returns:
        Merge result from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "commit_title": commit_title,
        "commit_message": commit_message,
        "merge_method": merge_method,
        "sha": sha,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.put(
            build_url(f"repos/{owner}/{repo}/pulls/{pull_number}/merge"), json=data
        )
        return process_response(response)


def create_review(
    owner: str,
    repo: str,
    pull_number: int,
    body: Optional[str] = None,
    event: Optional[str] = None,
    comments: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Create a review on a pull request.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        pull_number: Pull request number
        body: Review comment text
        event: Review action (APPROVE, REQUEST_CHANGES, COMMENT)
        comments: Line-specific review comments

    Returns:
        Created review details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "body": body,
        "event": event,
        "comments": comments,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.post(
            build_url(f"repos/{owner}/{repo}/pulls/{pull_number}/reviews"),
            json=data,
        )
        return process_response(response)


def get_review(
    owner: str, repo: str, pull_number: int, review_id: int
) -> Dict[str, Any]:
    """Get a specific review.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        pull_number: Pull request number
        review_id: Review ID

    Returns:
        Review details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}")
        )
        return process_response(response)


def list_reviews(
    owner: str, repo: str, pull_number: int
) -> List[Dict[str, Any]]:
    """List reviews on a pull request.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        pull_number: Pull request number

    Returns:
        List of reviews from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/pulls/{pull_number}/reviews")
        )
        return process_response(response)


def dismiss_review(
    owner: str,
    repo: str,
    pull_number: int,
    review_id: int,
    message: str,
) -> Dict[str, Any]:
    """Dismiss a pull request review.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        pull_number: Pull request number
        review_id: Review ID to dismiss
        message: Reason for dismissing the review

    Returns:
        Updated review details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {"message": message}

    with get_session() as session:
        response = session.put(
            build_url(f"repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/dismissals"),
            json=data,
        )
        return process_response(response)


def update_branch(
    owner: str,
    repo: str,
    pull_number: int,
    expected_head_sha: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a pull request branch.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        pull_number: Pull request number
        expected_head_sha: SHA that pull request head must match

    Returns:
        Update result from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {}
    if expected_head_sha:
        data["expected_head_sha"] = expected_head_sha

    with get_session() as session:
        response = session.put(
            build_url(f"repos/{owner}/{repo}/pulls/{pull_number}/update-branch"),
            json=data,
        )
        return process_response(response)
