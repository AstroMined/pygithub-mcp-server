"""GitHub file operations.

This module provides functions for working with files in GitHub repositories,
including creating, updating, and reading file contents.
"""

import base64
from typing import Any, Dict, List, Optional

from ..common.errors import GitHubError
from ..common.types import FileContent
from ..common.utils import get_session, process_response, build_url


def get_file_contents(
    owner: str, repo: str, path: str, branch: Optional[str] = None
) -> Dict[str, Any]:
    """Get contents of a file from a GitHub repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        path: Path to the file
        branch: Optional branch name (defaults to default branch)

    Returns:
        File content details from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    params = {}
    if branch:
        params["ref"] = branch

    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/contents/{path}"), params=params
        )
        return process_response(response)


def create_or_update_file(
    owner: str,
    repo: str,
    path: str,
    content: str,
    message: str,
    branch: str,
    sha: Optional[str] = None,
) -> Dict[str, Any]:
    """Create or update a file in a GitHub repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        path: Path where to create/update the file
        content: Content of the file
        message: Commit message
        branch: Branch to create/update the file in
        sha: SHA of file being replaced (required for updates)

    Returns:
        File creation/update result from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch,
    }
    if sha:
        data["sha"] = sha

    with get_session() as session:
        response = session.put(
            build_url(f"repos/{owner}/{repo}/contents/{path}"), json=data
        )
        return process_response(response)


def delete_file(
    owner: str, repo: str, path: str, message: str, branch: str, sha: str
) -> Dict[str, Any]:
    """Delete a file from a GitHub repository.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        path: Path to the file to delete
        message: Commit message
        branch: Branch containing the file
        sha: SHA of file to delete

    Returns:
        File deletion result from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    data = {
        "message": message,
        "sha": sha,
        "branch": branch,
    }

    with get_session() as session:
        response = session.delete(
            build_url(f"repos/{owner}/{repo}/contents/{path}"), json=data
        )
        return process_response(response)


def push_files(
    owner: str,
    repo: str,
    branch: str,
    files: List[FileContent],
    message: str,
) -> Dict[str, Any]:
    """Push multiple files to a GitHub repository in a single commit.

    This function handles the complexity of creating a new tree and commit
    to push multiple files at once, preserving Git history.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        branch: Branch to push to
        files: List of files to push, each with path and content
        message: Commit message

    Returns:
        Push result from GitHub API

    Raises:
        GitHubError: If the API request fails
    """
    with get_session() as session:
        # Get the reference to head
        response = session.get(
            build_url(f"repos/{owner}/{repo}/git/refs/heads/{branch}")
        )
        ref = process_response(response)
        base_tree = ref["object"]["sha"]

        # Create blobs for each file
        blobs = []
        for file in files:
            blob_data = {
                "content": file.content,
                "encoding": "utf-8",
            }
            response = session.post(
                build_url(f"repos/{owner}/{repo}/git/blobs"), json=blob_data
            )
            blob = process_response(response)
            blobs.append(
                {
                    "path": file.path,
                    "mode": "100644",
                    "type": "blob",
                    "sha": blob["sha"],
                }
            )

        # Create a new tree
        tree_data = {
            "base_tree": base_tree,
            "tree": blobs,
        }
        response = session.post(
            build_url(f"repos/{owner}/{repo}/git/trees"), json=tree_data
        )
        tree = process_response(response)

        # Create a new commit
        commit_data = {
            "message": message,
            "tree": tree["sha"],
            "parents": [base_tree],
        }
        response = session.post(
            build_url(f"repos/{owner}/{repo}/git/commits"), json=commit_data
        )
        commit = process_response(response)

        # Update the reference
        ref_data = {
            "sha": commit["sha"],
        }
        response = session.patch(
            build_url(f"repos/{owner}/{repo}/git/refs/heads/{branch}"), json=ref_data
        )
        return process_response(response)


def get_archive_link(
    owner: str, repo: str, archive_format: str = "tarball", ref: Optional[str] = None
) -> str:
    """Get a URL to download a repository archive.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        archive_format: Format of the archive (tarball or zipball)
        ref: Optional Git reference (branch, tag, or commit SHA)

    Returns:
        URL to download the archive

    Raises:
        GitHubError: If the API request fails
    """
    ref_part = f"/{ref}" if ref else ""
    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/{archive_format}{ref_part}"),
            allow_redirects=False,
        )
        if response.status_code == 302:  # GitHub returns a redirect to the archive
            return response.headers["Location"]
        else:
            process_response(response)
            raise GitHubError("Failed to get archive link")


def get_raw_content(owner: str, repo: str, path: str, ref: Optional[str] = None) -> str:
    """Get raw content of a file from a GitHub repository.

    This is different from get_file_contents as it returns the raw file content
    rather than the API response with metadata.

    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        path: Path to the file
        ref: Optional Git reference (branch, tag, or commit SHA)

    Returns:
        Raw file content as string

    Raises:
        GitHubError: If the API request fails
    """
    headers = {"Accept": "application/vnd.github.raw"}
    params = {}
    if ref:
        params["ref"] = ref

    with get_session() as session:
        response = session.get(
            build_url(f"repos/{owner}/{repo}/contents/{path}"),
            headers=headers,
            params=params,
        )
        if response.ok:
            return response.text
        else:
            process_response(response)
