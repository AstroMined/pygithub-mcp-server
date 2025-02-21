"""GitHub branch operations.

This module provides functions for working with branches in GitHub repositories,
including creation, deletion, and protection rules.
"""

from typing import Any, Dict, List, Optional

from ..common.errors import GitHubError
from ..common.utils import get_session, process_response, build_url


def get_branch(owner: str, repo: str, branch: str) -> Dict[str, Any]:
    """Get information about a branch.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        branch: Branch name

    Returns:
        Branch information from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/branches/{branch}")
        )
        return process_response(response)


def list_branches(
    owner: str,
    repo: str,
    protected: Optional[bool] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """List branches in a repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        protected: Filter by protection status
        page: Page number for pagination
        per_page: Number of results per page (max 100)

    Returns:
        List of branches from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = {}
    if protected is not None:
        params["protected"] = "true" if protected else "false"
    if page:
        params["page"] = str(page)
    if per_page:
        params["per_page"] = str(per_page)

    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/branches"), params=params
        )
        return process_response(response)


def create_branch_from_ref(
    owner: str, repo: str, branch: str, from_branch: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new branch from a reference.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        branch: Name for the new branch
        from_branch: Source branch (defaults to default branch)

    Returns:
        Created branch information from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        # Get the SHA of the source branch
        if from_branch:
            ref_path = f"heads/{from_branch}"
        else:
            # Get default branch
            response = session.get(build_url(f"repos/{owner}/{repo}"))
            repo_info = process_response(response)
            ref_path = f"heads/{repo_info['default_branch']}"

        # Get the SHA of the source branch
        response = session.get(
            build_url(f"repos/{owner}/{repo}/git/ref/{ref_path}")
        )
        ref = process_response(response)
        sha = ref["object"]["sha"]

        # Create the new branch
        data = {
            "ref": f"refs/heads/{branch}",
            "sha": sha,
        }
        response = session.post(
            build_url(f"repos/{owner}/{repo}/git/refs"), json=data
        )
        return process_response(response)


def delete_branch(owner: str, repo: str, branch: str) -> None:
    """Delete a branch.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        branch: Branch to delete

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.delete(
            build_url(f"repos/{owner}/{repo}/git/refs/heads/{branch}")
        )
        process_response(response)


def update_branch_protection(
    owner: str,
    repo: str,
    branch: str,
    required_status_checks: Optional[Dict[str, Any]] = None,
    enforce_admins: bool = False,
    required_pull_request_reviews: Optional[Dict[str, Any]] = None,
    restrictions: Optional[Dict[str, Any]] = None,
    required_linear_history: bool = False,
    allow_force_pushes: bool = False,
    allow_deletions: bool = False,
    required_conversation_resolution: bool = False,
) -> Dict[str, Any]:
    """Update branch protection rules.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        branch: Branch to protect
        required_status_checks: Required status check settings
        enforce_admins: Enforce rules on repository administrators
        required_pull_request_reviews: Pull request review settings
        restrictions: Branch restriction settings
        required_linear_history: Require linear history
        allow_force_pushes: Allow force pushes
        allow_deletions: Allow branch deletion
        required_conversation_resolution: Require conversation resolution

    Returns:
        Updated branch protection settings from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "required_status_checks": required_status_checks,
        "enforce_admins": enforce_admins,
        "required_pull_request_reviews": required_pull_request_reviews,
        "restrictions": restrictions,
        "required_linear_history": required_linear_history,
        "allow_force_pushes": allow_force_pushes,
        "allow_deletions": allow_deletions,
        "required_conversation_resolution": required_conversation_resolution,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.put(
            build_url(f"repos/{owner}/{repo}/branches/{branch}/protection"),
            json=data,
        )
        return process_response(response)


def get_branch_protection(owner: str, repo: str, branch: str) -> Dict[str, Any]:
    """Get branch protection settings.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        branch: Branch name

    Returns:
        Branch protection settings from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/branches/{branch}/protection")
        )
        return process_response(response)


def remove_branch_protection(owner: str, repo: str, branch: str) -> None:
    """Remove branch protection.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        branch: Branch name

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        response = session.delete(
            build_url(f"repos/{owner}/{repo}/branches/{branch}/protection")
        )
        process_response(response)


def merge_branch(
    owner: str,
    repo: str,
    base: str,
    head: str,
    commit_message: Optional[str] = None,
) -> Dict[str, Any]:
    """Merge a branch.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        base: The name of the base branch to merge into
        head: The name of the head branch to merge from
        commit_message: Optional commit message for the merge

    Returns:
        Merge result from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "base": base,
        "head": head,
        "commit_message": commit_message,
    }
    # Remove None values
    data = {k: v for k, v in data.items() if v is not None}

    with get_session() as session:
        response = session.post(
            build_url(f"repos/{owner}/{repo}/merges"), json=data
        )
        return process_response(response)
