"""Test fixtures and utilities for schema tests.

This module provides fixtures and helper functions for testing Pydantic schema models
against PyGithub's expectations.
"""

import pytest
from pydantic import ValidationError

# Base fixtures

@pytest.fixture
def valid_repository_ref_data():
    """Valid data for RepositoryRef schema."""
    return {
        "owner": "octocat",
        "repo": "hello-world"
    }

@pytest.fixture
def valid_file_content_data():
    """Valid data for FileContent schema."""
    return {
        "path": "README.md",
        "content": "# Hello World\n\nThis is a test repository."
    }

# Repository fixtures

@pytest.fixture
def valid_create_repository_data():
    """Valid data for CreateRepositoryParams schema."""
    return {
        "name": "hello-world",
        "description": "This is a test repository",
        "private": True,
        "auto_init": True
    }

@pytest.fixture
def valid_create_or_update_file_data(valid_repository_ref_data):
    """Valid data for CreateOrUpdateFileParams schema."""
    return {
        **valid_repository_ref_data,
        "path": "README.md",
        "content": "# Hello World\n\nThis is a test repository.",
        "message": "Initial commit",
        "branch": "main",
        "sha": "abc123"  # Optional for updates
    }

@pytest.fixture
def valid_push_files_data(valid_repository_ref_data, valid_file_content_data):
    """Valid data for PushFilesParams schema."""
    return {
        **valid_repository_ref_data,
        "branch": "main",
        "files": [valid_file_content_data],
        "message": "Add README.md"
    }

@pytest.fixture
def valid_search_repositories_data():
    """Valid data for SearchRepositoriesParams schema."""
    return {
        "query": "org:octocat language:python",
        "page": 1,
        "per_page": 30
    }

@pytest.fixture
def valid_get_file_contents_data(valid_repository_ref_data):
    """Valid data for GetFileContentsParams schema."""
    return {
        **valid_repository_ref_data,
        "path": "README.md",
        "branch": "main"  # Optional
    }

@pytest.fixture
def valid_fork_repository_data(valid_repository_ref_data):
    """Valid data for ForkRepositoryParams schema."""
    return {
        **valid_repository_ref_data,
        "organization": "my-org"  # Optional
    }

@pytest.fixture
def valid_create_branch_data(valid_repository_ref_data):
    """Valid data for CreateBranchParams schema."""
    return {
        **valid_repository_ref_data,
        "branch": "feature-branch",
        "from_branch": "main"  # Optional
    }

@pytest.fixture
def valid_list_commits_data(valid_repository_ref_data):
    """Valid data for ListCommitsParams schema."""
    return {
        **valid_repository_ref_data,
        "page": 1,
        "per_page": 30,
        "sha": "main"  # Optional
    }

# Issue fixtures

@pytest.fixture
def valid_create_issue_data(valid_repository_ref_data):
    """Valid data for CreateIssueParams schema."""
    return {
        **valid_repository_ref_data,
        "title": "Found a bug",
        "body": "I'm having a problem with this.",
        "assignees": ["octocat"],
        "labels": ["bug", "help wanted"],
        "milestone": 1
    }

@pytest.fixture
def valid_list_issues_data(valid_repository_ref_data):
    """Valid data for ListIssuesParams schema."""
    return {
        **valid_repository_ref_data,
        "state": "open",
        "labels": ["bug"],
        "sort": "created",
        "direction": "desc",
        "since": "2020-01-01T00:00:00Z",
        "page": 1,
        "per_page": 30
    }

@pytest.fixture
def valid_get_issue_data(valid_repository_ref_data):
    """Valid data for GetIssueParams schema."""
    return {
        **valid_repository_ref_data,
        "issue_number": 1
    }

@pytest.fixture
def valid_update_issue_data(valid_repository_ref_data):
    """Valid data for UpdateIssueParams schema."""
    return {
        **valid_repository_ref_data,
        "issue_number": 1,
        "title": "Updated bug report",
        "body": "I've found more details about this bug.",
        "state": "closed",
        "labels": ["bug", "fixed"],
        "assignees": ["octocat", "other-user"],
        "milestone": 2
    }

@pytest.fixture
def valid_issue_comment_data(valid_repository_ref_data):
    """Valid data for IssueCommentParams schema."""
    return {
        **valid_repository_ref_data,
        "issue_number": 1,
        "body": "This is a comment on the issue."
    }

@pytest.fixture
def valid_list_issue_comments_data(valid_repository_ref_data):
    """Valid data for ListIssueCommentsParams schema."""
    return {
        **valid_repository_ref_data,
        "issue_number": 1,
        "since": "2020-01-01T00:00:00Z",
        "page": 1,
        "per_page": 30
    }

@pytest.fixture
def valid_update_issue_comment_data(valid_repository_ref_data):
    """Valid data for UpdateIssueCommentParams schema."""
    return {
        **valid_repository_ref_data,
        "issue_number": 1,
        "comment_id": 123456,
        "body": "Updated comment text."
    }

@pytest.fixture
def valid_delete_issue_comment_data(valid_repository_ref_data):
    """Valid data for DeleteIssueCommentParams schema."""
    return {
        **valid_repository_ref_data,
        "issue_number": 1,
        "comment_id": 123456
    }

@pytest.fixture
def valid_add_issue_labels_data(valid_repository_ref_data):
    """Valid data for AddIssueLabelsParams schema."""
    return {
        **valid_repository_ref_data,
        "issue_number": 1,
        "labels": ["bug", "help wanted"]
    }

@pytest.fixture
def valid_remove_issue_label_data(valid_repository_ref_data):
    """Valid data for RemoveIssueLabelParams schema."""
    return {
        **valid_repository_ref_data,
        "issue_number": 1,
        "label": "help wanted"
    }

# Pull request fixtures

@pytest.fixture
def valid_create_pull_request_data(valid_repository_ref_data):
    """Valid data for CreatePullRequestParams schema."""
    return {
        **valid_repository_ref_data,
        "title": "Amazing new feature",
        "head": "feature-branch",
        "base": "main",
        "body": "Please pull these awesome changes in!",
        "draft": False,
        "maintainer_can_modify": True
    }

# Search fixtures

@pytest.fixture
def valid_search_params_data():
    """Valid data for SearchParams schema."""
    return {
        "q": "repo:octocat/hello-world is:issue is:open",
        "sort": "created",
        "order": "desc",
        "per_page": 30,
        "page": 1
    }

@pytest.fixture
def valid_search_code_data():
    """Valid data for SearchCodeParams schema."""
    return {
        "q": "repo:octocat/hello-world language:python",
        "sort": "indexed",
        "order": "desc",
        "per_page": 30,
        "page": 1
    }

@pytest.fixture
def valid_search_issues_data():
    """Valid data for SearchIssuesParams schema."""
    return {
        "q": "repo:octocat/hello-world is:issue is:open",
        "sort": "created",
        "order": "desc",
        "per_page": 30,
        "page": 1
    }

@pytest.fixture
def valid_search_users_data():
    """Valid data for SearchUsersParams schema."""
    return {
        "q": "type:user language:python location:san-francisco",
        "sort": "followers",
        "order": "desc",
        "per_page": 30,
        "page": 1
    }

# Response fixtures

@pytest.fixture
def valid_tool_response_data():
    """Valid data for ToolResponse schema."""
    return {
        "content": [
            {
                "type": "text",
                "text": "Operation completed successfully."
            }
        ],
        "is_error": False
    }

@pytest.fixture
def valid_text_content_data():
    """Valid data for TextContent schema."""
    return {
        "type": "text",
        "text": "Operation completed successfully."
    }

@pytest.fixture
def valid_error_content_data():
    """Valid data for ErrorContent schema."""
    return {
        "type": "error",
        "text": "An error occurred: Resource not found."
    }

# Helper functions

def assert_validation_error(schema_class, data, expected_error_substring):
    """Assert that validation fails with an error containing the expected substring."""
    with pytest.raises(ValidationError) as exc_info:
        schema_class(**data)
    error_str = str(exc_info.value).lower()
    assert expected_error_substring.lower() in error_str, f"Expected '{expected_error_substring}' in '{error_str}'"
