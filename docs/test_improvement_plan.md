# Comprehensive Test Improvement Plan

## Current Status

As of March 8, 2025, we have:
- 100% of tests passing with 88% overall coverage (up from 86%)
- Completed Phase 1 of our test improvement plan:
  - Fixed TestGitHubClient warning by using underscore-prefixed class and proper fixture pattern
  - Improved datetime.py coverage from 54% to 95%+ with comprehensive test cases
  - Added tests for each datetime conversion function with proper edge cases
- Standardized fixtures in `tests/integration/conftest.py`
- Created comprehensive documentation for test patterns in `tests/integration/README.md`

## Implementation Progress (March 8, 2025)

We've made significant progress implementing the test improvement plan:

1. Created targeted unit tests for `tools/repositories/tools.py` (High Priority):
   - Created `tests/unit/tools/repositories/test_repositories_tools_edge_cases.py` with specific tests for:
     - Repository creation error handling (lines 57-58)
     - Fork repository errors (lines 111-112)
     - Repository search edge cases (lines 151-167)
     - File contents parameter validation (lines 210-214)
     - File update error cases (lines 246-262)
     - Push files validation (lines 297-313)
     - Branch creation edge cases (lines 346-362)
     - Commit list parameter validation (lines 395-396, 401-402)
     - User repository listing (lines 443-459)

2. Added integration tests in `tests/integration/tools/repositories/test_repositories_tools_integration.py`:
   - Repository search with empty results (lines 151-167)
   - Repository retrieval with real API
   - Commit listing with real API
   - File contents retrieval with real API
   - Repository search with real API

3. Key implementation approaches:
   - Used dataclasses instead of mocks (per project preferences)
   - Leveraged existing fixtures for integration tests
   - Used `with_retry` decorator for handling rate limiting
   - Created targeted tests for each missing coverage area
   - Followed project patterns for test structure

## Current Coverage Analysis

Based on the latest coverage report:

```
Name                                                              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------------------------------------
src/pygithub_mcp_server/__init__.py                                   4      0      0      0   100%
src/pygithub_mcp_server/__main__.py                                   4      0      0      0   100%
src/pygithub_mcp_server/client/__init__.py                            3      0      0      0   100%
src/pygithub_mcp_server/client/client.py                             61      6     10      3    87%   60, 91, 94, 122-124
src/pygithub_mcp_server/client/rate_limit.py                         53      3     18      1    94%   32-34, 46->49
src/pygithub_mcp_server/config/__init__.py                            2      0      0      0   100%
src/pygithub_mcp_server/config/settings.py                           33      1     16      2    94%   54->62, 59
src/pygithub_mcp_server/converters/__init__.py                        9      0      0      0   100%
src/pygithub_mcp_server/converters/common/__init__.py                 2      0      0      0   100%
src/pygithub_mcp_server/converters/common/datetime.py                49      0     30      3    96%   66->81, 76->81, 130->128
src/pygithub_mcp_server/converters/common/pagination.py              52      9     10      0    85%   41-43, 95-101
src/pygithub_mcp_server/converters/issues/__init__.py                 3      0      0      0   100%
src/pygithub_mcp_server/converters/issues/comments.py                 6      0      0      0   100%
src/pygithub_mcp_server/converters/issues/issues.py                  16      0      2      0   100%
src/pygithub_mcp_server/converters/parameters.py                     70      0     52      0   100%
src/pygithub_mcp_server/converters/repositories/__init__.py           3      0      0      0   100%
src/pygithub_mcp_server/converters/repositories/contents.py           4      0      0      0   100%
src/pygithub_mcp_server/converters/repositories/repositories.py       4      0      0      0   100%
src/pygithub_mcp_server/converters/responses.py                      16      1      8      1    92%   38
src/pygithub_mcp_server/converters/users/__init__.py                  2      0      0      0   100%
src/pygithub_mcp_server/converters/users/users.py                     6      0      2      0   100%
src/pygithub_mcp_server/errors/__init__.py                            4      0      0      0   100%
src/pygithub_mcp_server/errors/exceptions.py                         21      0      0      0   100%
src/pygithub_mcp_server/errors/formatters.py                         22      0     14      1    97%   33->47
src/pygithub_mcp_server/errors/handlers.py                          106     13     48      6    88%   57->64, 61-62, 65->71, 68-70, 95, 97, 99, 118-121, 143-145
src/pygithub_mcp_server/operations/__init__.py                        2      0      0      0   100%
src/pygithub_mcp_server/operations/issues.py                        196     21     36      1    91%   77, 214-226, 239-241, 245-246, 402-404
src/pygithub_mcp_server/operations/repositories.py                  150     32     26      9    77%   53-55, 81->83, 83->85, 85->89, 92-94, 116->120, 123-125, 153-155, 193-195, 225, 244-246, 277->271, 279-281, 294->297, 309-311, 337, 352-354, 377, 396-398
src/pygithub_mcp_server/schemas/__init__.py                           8      0      0      0   100%
src/pygithub_mcp_server/schemas/base.py                              27      0      6      0   100%
src/pygithub_mcp_server/schemas/issues.py                           176      0     44      1    99%   259->264
src/pygithub_mcp_server/schemas/pull_requests.py                     10      0      0      0   100%
src/pygithub_mcp_server/schemas/repositories.py                     138      2     38      4    97%   122->127, 124, 218->223, 220
src/pygithub_mcp_server/schemas/responses.py                         21      0      2      0   100%
src/pygithub_mcp_server/schemas/search.py                            14      0      0      0   100%
src/pygithub_mcp_server/server.py                                    25      1      2      1    93%   20
src/pygithub_mcp_server/tools/__init__.py                            68     11     24      3    80%   57->54, 68-76, 127, 130-131
src/pygithub_mcp_server/tools/issues/__init__.py                      2      0      0      0   100%
src/pygithub_mcp_server/tools/issues/tools.py                       183     39      2      0    79%   75-79, 112-113, 152-156, 193-197, 229-233, 304-308, 340-344, 376-380, 425-426
src/pygithub_mcp_server/tools/repositories/__init__.py                5      0      0      0   100%
src/pygithub_mcp_server/tools/repositories/tools.py                 182     68      0      0    63%   57-58, 111-112, 151-167, 210-214, 246-262, 297-313, 346-362, 395-396, 401-402, 443-459
src/pygithub_mcp_server/utils/__init__.py                             2      0      0      0   100%
src/pygithub_mcp_server/utils/environment.py                         52      6     30      6    83%   29, 34-37, 44->exit, 109, 112, 114->121
src/pygithub_mcp_server/version.py                                   10      2      0      0    80%   48, 56
-------------------------------------------------------------------------------------------------------------
TOTAL                                                              1826    215    420     42    88%
```

### Expected Coverage Improvements

After implementing the planned tests, we expect to see:

1. For `tools/repositories/tools.py`:
   - Current: 63% coverage (68 missing lines)
   - Expected: 85-90% coverage (reduced to ~20 missing lines)
   - Key areas addressed: all identified missing ranges (57-58, 111-112, 151-167, etc.)

2. Additional integration tests will indirectly improve coverage in:
   - `operations/repositories.py`: expected to reach 85%+
   - Other modules through shared code paths

### Priority Areas (Updated)

1. **High Priority (Coverage < 70%)**
   - ~~`tools/repositories/tools.py` (63%)~~ - **In Progress**: Implemented targeted tests, awaiting new coverage report

2. **Medium Priority (Coverage 70-85%)**
   - `tools/issues/tools.py` (79%)
   - `operations/repositories.py` (77%)
   - `tools/__init__.py` (80%) 
   - `utils/environment.py` (83%)
   - `converters/common/pagination.py` (85%)

3. **Low Priority (Coverage > 85%)**
   - `client/client.py` (87%)
   - `errors/handlers.py` (88%)
   - All others with minor coverage gaps

## Comprehensive Improvement Strategy

Our test improvement strategy covers three key dimensions:

1. **Coverage Improvements** - Targeting specific code paths in priority modules
2. **Test Pattern Standardization** - Creating reusable patterns and fixtures
3. **Test Infrastructure** - Building tooling to support maintainable tests

### Phase 1: Coverage-Driven Improvements (In Progress)

#### 1. Repository Tools Module (High Priority)

**Target:** `tools/repositories/tools.py` (63% → 80%+)

Missing lines analysis shows we need tests for:
- ✅ Lines 57-58: Create repository error handling
- ✅ Lines 111-112: Fork repository error paths
- ✅ Lines 151-167: Repository search edge cases
- ✅ Lines 210-214: File contents parameter validation
- ✅ Lines 246-262: File update error cases
- ✅ Lines 297-313: Push files validation
- ✅ Lines 346-362: Branch creation edge cases
- ✅ Lines 395-396, 401-402: Commit list parameter validation
- ✅ Lines 443-459: User repository listing

**Implementation Complete:** Created targeted tests for all identified missing coverage areas in:
- `tests/unit/tools/repositories/test_repositories_tools_edge_cases.py`
- `tests/integration/tools/repositories/test_repositories_tools_integration.py`

**Implementation Approach:**

1. Created a test file structure that mirrors the tool structure:
   - Separate test modules for edge cases and integration tests
   - Clear naming convention for test functions targeting specific coverage gaps

2. Implemented a standard test matrix for each tool function:
   - Success path test
   - Validation error test
   - API error test
   - Parameter edge case tests

3. Leveraged existing fixtures:
   - Used `with_retry` for handling GitHub API rate limits
   - Used `test_owner`, `test_repo_name` for integration tests
   - Created targeted test fixtures for specific test scenarios

#### 2. Repository Operations Module (Medium Priority - Next Focus)

**Target:** `operations/repositories.py` (77% → 90%+)

Missing lines analysis shows we need tests for:
- Lines 53-55: Get repository error handling
- Lines 81-89: Repository creation branching logic
- Lines 92-94: Repository creation error handling
- Lines 123-125: Fork repository error handling
- Lines 153-155: Search repositories error handling
- Lines 193-195: File contents error handling
- Lines 244-246: File update error handling
- Lines 279-281: Push files error handling
- Lines 309-311: Branch creation error handling
- Lines 352-354: Commit listing error handling
- Lines 396-398: User repositories error handling

**Implementation Plan:**

1. Create comprehensive test classes for each operation group:
   - Follow the same approach used for repository tools
   - Create targeted tests for each missing coverage area
   - Leverage existing integration test fixtures

2. Focus on error conditions with appropriate error types:
   - 400-level errors (Not Found, Unauthorized, etc.)
   - Rate limiting errors
   - Validation errors
   - Network errors

3. Address conditional logic and edge cases:
   - Test parameter handling paths
   - Test branching logic through specific inputs

#### 3. Issues Tools Module (Medium Priority - Upcoming Focus)

**Target:** `tools/issues/tools.py` (79% → 90%+)

Missing lines analysis shows we need tests for:
- Lines 75-79: Create issue error handling
- Lines 112-113: Get issue error handling
- Lines 152-156: Update issue error handling
- Lines 193-197: List issues error handling
- Lines 229-233: Add comment error handling
- Lines 304-308: List comments error handling
- Lines 340-344: Update comment error handling
- Lines 376-380: Delete comment error handling
- Lines 425-426: Add labels error handling

**Implementation Plan:**

Apply the same comprehensive testing matrix as for repository tools, focusing on:
1. Success path tests
2. Validation error tests
3. API error tests
4. Parameter edge cases

### Phase 2: Test Pattern Standardization

Building on our coverage improvements, we'll create standardized patterns for all tests:

#### 1. Layer-specific Test Patterns

**Schema Layer Tests**
```python
def test_schema_validation():
    """Test schema field validation."""
    # Valid data test
    valid_data = {"owner": "test", "repo": "test-repo"}
    params = RepositoryParams(**valid_data)
    assert params.owner == "test"
    
    # Invalid data test
    with pytest.raises(ValidationError) as exc_info:
        RepositoryParams(owner="", repo="test-repo")
    assert "owner cannot be empty" in str(exc_info.value)
    
    # Field validator test
    with pytest.raises(ValidationError) as exc_info:
        IssueParams(owner="test", repo="test-repo", state="invalid")
    assert "invalid state" in str(exc_info.value)
```

**Operations Layer Tests**
```python
def test_operation_success(mock_github_client):
    """Test successful operation."""
    # Setup
    params = OperationParams(param1="value1", param2="value2")
    
    # Execute
    result = operation_function(params)
    
    # Verify
    assert result["key"] == "expected_value"
    mock_github_client.method.assert_called_once_with("value1", "value2")

def test_operation_error(mock_github_client_with_error):
    """Test operation error handling."""
    # Setup
    params = OperationParams(param1="value1", param2="value2")
    
    # Execute and verify
    with pytest.raises(GitHubError) as exc_info:
        operation_function(params)
    assert "error message" in str(exc_info.value)
```

**Tools Layer Tests**
```python
@pytest.mark.integration
def test_tool_success(test_owner, test_repo):
    """Test successful tool execution with real PyGithub client."""
    # Set up test data
    params = {"params": {"owner": test_owner, "repo": test_repo}}
    
    # Call tool with real parameters
    result = get_repository(params)
    
    # Verify
    assert not result.get("is_error", False)
    assert isinstance(result["content"], list)
    assert result["content"][0]["type"] == "text"
    # Verify actual content reflects the real repository

@pytest.mark.integration
def test_tool_error():
    """Test tool error handling with non-existent repository."""
    # Set up test data with non-existent repository
    params = {"params": {"owner": "non-existent-user-12345", "repo": "non-existent-repo-12345"}}
    
    # Call tool with invalid parameters
    result = get_repository(params)
    
    # Verify error response
    assert result.get("is_error", False) is True
    assert "not found" in result["content"][0]["text"].lower()
```

#### 2. Test Fixture Templates

**Unit Test Fixtures**
```python
# tests/unit/conftest.py

@pytest.fixture
def test_github_objects():
    """Create test objects using dataclasses for unit tests."""
    owner = RepositoryOwner(login="test-owner", id=12345)
    repo = Repository(
        id=98765,
        name="test-repo",
        full_name="test-owner/test-repo",
        owner=owner,
        html_url="https://github.com/test-owner/test-repo"
    )
    
    issue = Issue(
        number=1,
        title="Test Issue",
        body="Test issue body",
        state="open",
        user=owner,
        html_url="https://github.com/test-owner/test-repo/issues/1"
    )
    
    return {
        "owner": owner,
        "repository": repo,
        "issue": issue
    }

@pytest.fixture
def github_exceptions():
    """Create GitHub exceptions for testing error paths."""
    return {
        "not_found": GithubException(404, {"message": "Not found"}),
        "rate_limit": GithubException(403, {"message": "API rate limit exceeded"}),
        "validation": GithubException(422, {"message": "Validation failed", "errors": [
            {"resource": "Issue", "field": "title", "code": "missing_field"}
        ]})
    }
```

**Integration Test Fixtures**
```python
# tests/integration/conftest.py

@pytest.fixture
def test_owner():
    """Get the GitHub owner for integration tests."""
    return os.environ.get("GITHUB_TEST_OWNER", "test-owner")

@pytest.fixture
def test_repo():
    """Get the GitHub repository for integration tests."""
    return os.environ.get("GITHUB_TEST_REPO", "test-repo")

@pytest.fixture
def unique_id():
    """Generate a unique identifier for test resources."""
    return f"test-{str(uuid.uuid4())[:8]}"

@pytest.fixture
def test_cleanup():
    """Fixture to track and clean up test resources."""
    cleanup = TestCleanup()
    yield cleanup
    cleanup.cleanup_all()

class TestCleanup:
    """Resource tracking and cleanup helper."""
    
    def __init__(self):
        self.issues = []
        self.comments = []
        self.repositories = []
        self.branches = []
        
    def add_issue(self, owner, repo, issue_number):
        """Track an issue for cleanup."""
        self.issues.append((owner, repo, issue_number))
    
    def add_comment(self, owner, repo, issue_number, comment_id):
        """Track a comment for cleanup."""
        self.comments.append((owner, repo, issue_number, comment_id))
        
    def add_repository(self, owner, repo):
        """Track a repository for cleanup."""
        self.repositories.append((owner, repo))
        
    def add_branch(self, owner, repo, branch):
        """Track a branch for cleanup."""
        self.branches.append((owner, repo, branch))
        
    def cleanup_all(self):
        """Clean up all tracked resources."""
        client = GitHubClient.get_instance()
        
        # Clean up in reverse order of dependencies
        self._cleanup_comments(client)
        self._cleanup_issues(client)
        self._cleanup_branches(client)
        self._cleanup_repositories(client)
```

**Test Retry Mechanism**
```python
# tests/integration/utils/retry.py

def with_retry(func, max_retries=3, initial_wait=2):
    """
    Execute a function with retry logic for rate limit handling.
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        initial_wait: Initial wait time in seconds (doubles each retry)
        
    Returns:
        The result of the function if successful
        
    Raises:
        The last exception if all retries fail
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return func()
        except GitHubError as e:
            if "rate limit exceeded" in str(e).lower() and attempt < max_retries - 1:
                wait_time = initial_wait * (2 ** attempt)
                logging.warning(f"Rate limited, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                last_exception = e
            else:
                raise
    
    if last_exception:
        raise last_exception
```

#### 3. Test Helper Functions

```python
# tests/helpers/repository_helpers.py

def create_test_repository(owner, repo_name, test_cleanup=None):
    """
    Create a test repository and register for cleanup.
    
    Args:
        owner: GitHub username or organization
        repo_name: Repository name
        test_cleanup: Optional TestCleanup instance
        
    Returns:
        Created repository details
    """
    params = CreateRepositoryParams(
        name=repo_name,
        description=f"Test repository created by automated tests",
        private=True,
        auto_init=True
    )
    
    result = with_retry(lambda: repositories.create_repository(params))
    
    if test_cleanup:
        test_cleanup.add_repository(owner, repo_name)
        
    return result
```

### Phase 3: Test Infrastructure Enhancements

#### 1. Test Generator for New Tools

To facilitate rapid test development for new tool groups, we'll create a test generator utility:

```python
# scripts/generate_tool_tests.py

import argparse
import os
import re
from pathlib import Path

TEMPLATE = """
import pytest
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from pygithub_mcp_server.tools.{module} import {tool_name}
from pygithub_mcp_server.errors import GitHubError
from pygithub_mcp_server.schemas.{schema_module} import {schema_name}

# Dataclasses representing PyGithub objects
@dataclass
class RepositoryOwner:
    login: str
    id: int = 12345
    html_url: str = "https://github.com/test-owner"
    
@dataclass
class Repository:
    id: int
    name: str
    full_name: str
    owner: RepositoryOwner
    private: bool = False
    html_url: str = "https://github.com/test-owner/test-repo"
    description: Optional[str] = None
    
# Unit tests with dataclasses
def test_{tool_func}_success():
    \"\"\"Test successful {tool_name} execution using dataclasses.\"\"\"
    # Create test data using dataclasses
    owner = RepositoryOwner(login="test-owner")
    repo = Repository(
        id=98765,
        name="test-repo",
        full_name="test-owner/test-repo",
        owner=owner
    )
    
    # Test parameters
    params = {{"params": {params}}}
    
    # Patch PyGithub interactions to return our dataclass objects
    with pytest.MonkeyPatch.context() as monkeypatch:
        # Configure to return our test objects
        monkeypatch.setattr(
            "pygithub_mcp_server.client.GitHubClient.get_instance().get_repo",
            lambda _: repo
        )
        
        # Execute the tool
        result = {tool_func}(params)
        
        # Verify success result
        assert not result.get("is_error", False)
        assert isinstance(result["content"], list)
        assert result["content"][0]["type"] == "text"

# Integration test
@pytest.mark.integration
def test_{tool_func}_integration(test_owner, test_repo, test_cleanup):
    \"\"\"Test {tool_name} with real PyGithub client.\"\"\"
    # Test parameters with real repo
    params = {{"params": {{"owner": test_owner, "repo": test_repo}}}}
    
    # Execute the tool with real parameters
    result = {tool_func}(params)
    
    # Verify the tool executed successfully with real data
    assert not result.get("is_error", False)
    assert isinstance(result["content"], list)
    assert "text" in result["content"][0]
    # Additional assertions based on the specific tool

def test_{tool_func}_validation_error():
    \"\"\"Test {tool_name} with validation errors.\"\"\"
    # Test with invalid parameters
    with pytest.raises(ValueError):
        # This should fail during Pydantic validation
        {schema_name}(**{invalid_params})
    
    # Test the tool itself with invalid parameters
    params = {{"params": {invalid_params}}}
    
    # Execute the tool
    result = {tool_func}(params)
    
    # Verify error result
    assert result.get("is_error", True)
    assert "validation" in result["content"][0]["text"].lower()

def test_{tool_func}_github_error():
    \"\"\"Test {tool_name} with GitHub API errors.\"\"\"
    # Test parameters
    params = {{"params": {params}}}
    
    # Simulate GitHub API error without mocks
    with pytest.MonkeyPatch.context() as monkeypatch:
        # Configure to raise a GitHub exception
        def raise_github_exception(*args, **kwargs):
            from github import GithubException
            raise GithubException(404, {{"message": "Not Found"}})
            
        monkeypatch.setattr(
            "pygithub_mcp_server.client.GitHubClient.get_instance().get_repo",
            raise_github_exception
        )
        
        # Execute the tool
        result = {tool_func}(params)
        
        # Verify error result
        assert result.get("is_error", True)
        assert "not found" in result["content"][0]["text"].lower()
"""

def generate_tool_tests(module, tool_name, tool_func, schema_module, schema_name, params, invalid_params):
    """Generate standardized tests for a tool function."""
    # Create test directory if it doesn't exist
    test_dir = Path(f"tests/unit/tools/{module}")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Create test file
    test_file = test_dir / f"test_{tool_func}.py"
    
    # Fill template
    content = TEMPLATE.format(
        module=module,
        tool_name=tool_name,
        tool_func=tool_func,
        schema_module=schema_module,
        schema_name=schema_name,
        params=params,
        invalid_params=invalid_params
    )
    
    # Write to file
    with open(test_file, "w") as f:
        f.write(content)
        
    print(f"Generated tests for {tool_name} at {test_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate tool tests")
    parser.add_argument("--module", required=True, help="Tool module name (e.g., issues)")
    parser.add_argument("--tool-name", required=True, help="Tool name (e.g., create_issue)")
    parser.add_argument("--schema-module", required=True, help="Schema module name (e.g., issues)")
    parser.add_argument("--schema-name", required=True, help="Schema class name (e.g., CreateIssueParams)")
    
    args = parser.parse_args()
    
    # Convert CamelCase to snake_case
    tool_func = re.sub(r'(?<!^)(?=[A-Z])', '_', args.tool_name).lower()
    
    # Example parameters
    params = {"param1": "value1", "param2": "value2"}
    invalid_params = {"param1": "", "param2": 123}  # Invalid types/values
    
    generate_tool_tests(
        args.module,
        args.tool_name,
        tool_func,
        args.schema_module,
        args.schema_name,
        params,
        invalid_params
    )
```

#### 2. Test Coverage Report Analyzer

To help prioritize test efforts, we'll create a coverage report analyzer:

```python
# scripts/analyze_coverage.py

import os
import re
import json
import subprocess
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ModuleCoverage:
    """Coverage information for a module."""
    name: str
    statements: int
    missing: int
    branches: int
    branch_missing: int
    coverage: float
    missing_lines: List[str]
    
    @property
    def priority(self):
        """Determine testing priority based on coverage."""
        if self.coverage < 70:
            return "High"
        elif self.coverage < 85:
            return "Medium"
        else:
            return "Low"

def run_coverage():
    """Run pytest coverage and return the output."""
    result = subprocess.run(
        ["pytest", "--cov=src/pygithub_mcp_server", "--cov-report=term-missing"],
        capture_output=True,
        text=True
    )
    return result.stdout

def parse_coverage_output(output):
    """Parse coverage output into structured data."""
    modules = []
    
    # Extract module lines
    pattern = r"(src/pygithub_mcp_server/[^\s]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+%)\s*(.*)"
    for line in output.split("\n"):
        match = re.match(pattern, line)
        if match:
            name, stmts, miss, branch, bpart, cover, missing = match.groups()
            coverage = int(cover.strip("%"))
            
            module = ModuleCoverage(
                name=name,
                statements=int(stmts),
                missing=int(miss),
                branches=int(branch),
                branch_missing=int(bpart),
                coverage=coverage,
                missing_lines=missing.strip() if missing else ""
            )
            modules.append(module)
    
    return modules

def generate_report(modules):
    """Generate a prioritized test coverage report."""
    # Sort by priority and coverage
    sorted_modules = sorted(
        modules, 
        key=lambda m: (0 if m.priority == "High" else 1 if m.priority == "Medium" else 2, m.coverage)
    )
    
    # Generate report
    report = {
        "summary": {
            "total_modules": len(modules),
            "high_priority": len([m for m in modules if m.priority == "High"]),
            "medium_priority": len([m for m in modules if m.priority == "Medium"]),
            "low_priority": len([m for m in modules if m.priority == "Low"]),
            "average_coverage": sum(m.coverage for m in modules) / len(modules) if modules else 0,
        },
        "modules": [
            {
                "name": m.name,
                "priority": m.priority,
                "coverage": m.coverage,
                "missing_statements": m.missing,
                "missing_branches": m.branch_missing,
                "missing_lines": m.missing_lines
            }
            for m in sorted_modules
        ]
    }
    
    return report

if __name__ == "__main__":
    # Run coverage
    output = run_coverage()
    
    # Parse output
    modules = parse_coverage_output(output)
    
    # Generate report
    report = generate_report(modules)
    
    # Write report to file
    with open("coverage_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"Generated coverage report with {len(modules)} modules.")
    print(f"High priority modules: {report['summary']['high_priority']}")
    print(f"Medium priority modules: {report['summary']['medium_priority']}")
    print(f"Low priority modules: {report['summary']['low_priority']}")
    print(f"Average coverage: {report['summary']['average_coverage']:.2f}%")
```

#### 3. CI/CD Integration

To ensure consistent test coverage over time, we'll add GitHub Actions workflows:

```yaml
# .github/workflows/coverage.yml
name: Test Coverage

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install uv
        uv venv
        uv pip install -e ".[dev]"
    
    - name: Run tests with coverage
      run: |
        pytest --cov=src/pygithub_mcp_server --cov-report=xml
      env:
        GITHUB_TEST_TOKEN: ${{ secrets.GITHUB_TEST_TOKEN }}
        GITHUB_TEST_OWNER: ${{ secrets.GITHUB_TEST_OWNER }}
        GITHUB_TEST_REPO: ${{ secrets.GITHUB_TEST_REPO }}
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
```

## Coverage Analysis Workflow

The project uses a two-part approach for managing and improving test coverage:

### 1. Coverage Data Collection

Coverage data is collected using pytest-cov when running tests:

```bash
# Run unit tests with coverage
pytest

# Include integration tests for more comprehensive coverage
pytest --run-integration
```

This generates a `.coverage` file at the project root containing raw coverage data.

### 2. Coverage Analysis and Reporting

For analyzing coverage data, we use our custom analyzer script:

```bash
# Analyze existing coverage data and generate HTML report
python scripts/analyze_coverage.py --html

# Run tests and analyze in a single step
python scripts/analyze_coverage.py --run-tests --html

# Include integration tests in analysis
python scripts/analyze_coverage.py --run-tests --include-integration --html
```

### Viewing Coverage Reports

The analyzer generates two files:
- `coverage_report.json` - Machine-readable JSON data
- `coverage_report.html` - Interactive HTML report (when using --html flag)

To view the HTML report, open `coverage_report.html` in any web browser:
```bash
# On Linux
xdg-open coverage_report.html

# On macOS
open coverage_report.html

# Or simply double-click the file in your file explorer
```

No web server is required - the HTML file can be viewed directly in a browser.

### Using Coverage Reports Effectively

1. **Identify Priority Areas**: Focus on "High Priority" modules first (coverage below 70%)
2. **Examine Missing Lines**: Each module shows exactly which lines need test coverage
3. **Implement Tests Strategically**: Address the most critical missing coverage first
4. **Track Progress**: Re-run the analyzer after adding tests to verify improvements
5. **Set Thresholds**: Use the `--threshold` parameter to enforce minimum coverage standards

## Implementation Timeline

### Phase 1 (Immediate)
- Create test dataclasses for PyGithub objects
- Implement core tests for repositories.tools.py
- Setup integration tests for high-priority modules
- Add test helpers for common operations

### Phase 2 (Next 1-2 Days)
- Implement tests for operations/repositories.py
- Add tests for tools/issues/tools.py
- Create test generator script
- Standardize test patterns across all components

### Phase 3 (Next 2-3 Days)
- Complete coverage for all remaining modules
- Create coverage analyzer script
- Implement CI/CD integration
- Document test patterns and best practices

## Test Coverage Report Example

Below is an example of what the analyzer's output for high-priority modules might look like:

```
=== High Priority Modules ===
src/pygithub_mcp_server/tools/repositories/tools.py: 63% coverage
  Missing lines: 57-58, 111-112, 151-167, 246-262, 297-313, 346-362
  Priority: Implement tests for repository creation, fork, and search functionality

src/pygithub_mcp_server/tools/issues/tools.py: 79% coverage
  Missing lines: 75-79, 112-113, 152-156, 193-197, 229-233
  Priority: Focus on error handling tests for issue operations
```

This format makes it clear which specific code sections need testing attention.

## Completion Criteria

- Overall coverage above 90%
- No modules below 75% coverage
- All tests passing without warnings
- Real PyGithub client usage in integration tests 
- Consistent use of dataclasses instead of mocks
- Comprehensive documentation for test patterns
- Automated tooling for test generation and analysis
