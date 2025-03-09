"""Integration tests for repository tools.

This module contains integration tests for repository tools to improve coverage
and verify behavior with the real GitHub API.
"""

import json
import pytest
import uuid
from datetime import datetime

from pygithub_mcp_server.tools.repositories.tools import (
    get_repository,
    search_repositories,
    list_commits,
    get_file_contents
)

# Test for repository search with empty results, targeting lines 151-167
@pytest.mark.integration
def test_search_repositories_empty_results(test_owner, with_retry):
    """Test repository search with no results (lines 151-167)."""
    # Generate a unique search term that won't match any repositories
    unique_search = f"nonexistent-repo-{uuid.uuid4().hex[:12]}"
    
    # Execute the function with retry to handle potential rate limiting
    result = with_retry(lambda: search_repositories({"query": unique_search}))
    
    # Verify results - this should return an empty array, not an error
    assert not result.get("is_error", False)
    assert isinstance(result["content"], list)
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"
    
    # Parse the JSON and verify it's an empty array
    content = json.loads(result["content"][0]["text"])
    assert isinstance(content, list)
    assert len(content) == 0

# Test for repository retrieval with real API
@pytest.mark.integration
def test_get_repository_integration(test_owner, test_repo_name, with_retry):
    """Test getting repository details with real GitHub API."""
    # Call the tool with actual repository
    result = with_retry(lambda: get_repository({
        "owner": test_owner,
        "repo": test_repo_name
    }))
    
    # Verify successful response
    assert not result.get("is_error", False)
    assert result["content"][0]["type"] == "text"
    
    # Parse content and verify basic repository properties
    content = json.loads(result["content"][0]["text"])
    assert content["name"] == test_repo_name
    assert content["owner"] == test_owner
    assert "html_url" in content

# Test for commit listing with real API
@pytest.mark.integration
def test_list_commits_integration(test_owner, test_repo_name, with_retry):
    """Test listing commits with real GitHub API."""
    # Call the tool with limited results
    result = with_retry(lambda: list_commits({
        "owner": test_owner,
        "repo": test_repo_name,
        "per_page": 2  # Limit to 2 results for faster tests
    }))
    
    # Verify successful response
    assert not result.get("is_error", False)
    assert result["content"][0]["type"] == "text"
    
    # Parse content and verify commits structure
    content = json.loads(result["content"][0]["text"])
    assert isinstance(content, list)
    
    # If repository has commits, verify their structure
    if content:
        assert "sha" in content[0]
        assert "html_url" in content[0]
        assert "message" in content[0]

# Test for file contents retrieval with real API
@pytest.mark.integration
def test_get_file_contents_integration(test_owner, test_repo_name, with_retry):
    """Test getting file contents with real GitHub API."""
    # Try to get README.md which exists in most repositories
    result = with_retry(lambda: get_file_contents({
        "owner": test_owner,
        "repo": test_repo_name,
        "path": "README.md"
    }))
    
    # Check if we got a successful response
    if not result.get("is_error", False):
        # Successful file retrieval
        assert result["content"][0]["type"] == "text"
        content = json.loads(result["content"][0]["text"])
        assert content["name"] == "README.md"
        assert "content" in content
    else:
        # File might not exist, try root directory
        result = with_retry(lambda: get_file_contents({
            "owner": test_owner,
            "repo": test_repo_name,
            "path": ""
        }))
        
        # This should at least return directory contents
        assert not result.get("is_error", False)
        assert result["content"][0]["type"] == "text"
        content = json.loads(result["content"][0]["text"])
        assert "is_directory" in content
        assert content["is_directory"] is True

# Test for repository search with real API
@pytest.mark.integration
def test_search_repositories_integration(with_retry):
    """Test searching repositories with real GitHub API."""
    # Search for a common topic that should return results
    result = with_retry(lambda: search_repositories({
        "query": "topic:python",
        "per_page": 3  # Limit results for faster tests
    }))
    
    # Verify successful response
    assert not result.get("is_error", False)
    assert result["content"][0]["type"] == "text"
    
    # Parse content and verify results
    content = json.loads(result["content"][0]["text"])
    assert isinstance(content, list)
    assert len(content) > 0
    
    # Check first result has expected properties
    repo = content[0]
    assert "name" in repo
    assert "full_name" in repo
    assert "owner" in repo
    assert "html_url" in repo
