import os
import uuid
import logging
import pytest

from pygithub_mcp_server.tools.issues.tools import update_issue


# Configure logging
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def test_repo_info():
    """Get test repository information from environment variables."""
    owner = os.environ.get("GITHUB_TEST_OWNER")
    repo = os.environ.get("GITHUB_TEST_REPO")
    
    if not owner or not repo:
        pytest.skip("GITHUB_TEST_OWNER and GITHUB_TEST_REPO environment variables required")
    
    return {
        "owner": owner,
        "repo": repo
    }


@pytest.fixture
def unique_id():
    """Generate a unique ID for test resources to prevent test interference."""
    return f"test-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def issue_cleanup(test_repo_info):
    """Clean up test issues after the test."""
    created_issues = []
    
    yield created_issues
    
    # Clean up all issues created during the test
    for issue_number in created_issues:
        try:
            params = {
                "owner": test_repo_info["owner"],
                "repo": test_repo_info["repo"],
                "issue_number": issue_number,
                "state": "closed"
            }
            logger.debug(f"Cleaning up test issue #{issue_number}")
            update_issue(params)
        except Exception as e:
            logger.warning(f"Failed to clean up issue #{issue_number}: {e}")
