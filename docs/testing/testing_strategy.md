# PyGithub MCP Server Testing Strategy

This comprehensive document outlines the testing strategy for the PyGithub MCP Server, incorporating both the modular tool architecture (ADR-006) and test coverage improvement plans aligned with real API testing (ADR-002).

## Introduction & Overview

The PyGithub MCP Server testing strategy is guided by two key architectural decisions:
- [ADR-002: Real API Testing](../adr/002_real_api_testing.md) - Using real GitHub API calls instead of mocks
- [ADR-006: Modular Tool Architecture](../adr/006_modular_tool_architecture.md) - Implementing configurable tool architecture

Our core testing principles include:
1. Using real API calls instead of mocks
2. Testing behavior rather than implementation details
3. Implementing thorough resource cleanup
4. Using unique identifiers for test resources
5. Handling rate limits with exponential backoff

## Test Organization

Tests are organized into two main categories with a consistent layer-based structure:

```
tests/
├── unit/                  # Fast tests with minimal or no external dependencies
│   ├── client/            # Tests for client module
│   ├── config/            # Tests for configuration
│   ├── converters/        # Tests for converters
│   ├── errors/            # Tests for error handling
│   ├── schemas/           # Tests for schema validation
│   ├── tools/             # Tests for tool registration and functionality
│   └── utils/             # Tests for utility functions
└── integration/           # Tests that use the real GitHub API
    ├── client/            # Tests for client module with real API
    ├── config/            # Tests for configuration with real settings
    ├── converters/        # Tests for converters with real data
    ├── errors/            # Tests for error handling with real API errors
    ├── operations/        # Tests for API operations with real GitHub endpoints
    │   ├── issues/        # Tests for issue operations
    │   ├── repositories/  # Tests for repository operations
    │   └── users/         # Tests for user operations
    ├── schemas/           # Tests for schema validation with real data
    ├── tools/             # Tests for MCP tools with real API
    │   ├── issues/        # Tests for issue tools
    │   ├── repositories/  # Tests for repository tools
    │   └── users/         # Tests for user tools
    └── utils/             # Tests for utilities with real environments
```

## Current Coverage Status

As of March 2025, the overall test coverage is at 83%, with several modules having significant gaps:

| Module | Coverage | Priority |
|--------|----------|----------|
| tools/issues/tools.py | 50% | High |
| server.py | 67% | High |
| client/rate_limit.py | 69% | High |
| operations/issues.py | 75% | High |
| __main__.py | 0% | Medium |
| converters/parameters.py | 77% | Medium |
| converters/repositories/* | 75% | Medium |
| tools/__init__.py | 77% | Medium |
| errors/handlers.py | 87% | Low |
| utils/environment.py | 83% | Low |
| version.py | 80% | Low |

## Testing Approach by Module

### 1. Tools Module

#### Coverage Priority: High (Currently 50% for tools/issues/tools.py)

**Approach:**
- Create comprehensive integration tests for each tool function
- Test both success and error paths
- Cover parameter validation
- Test edge cases (rate limiting, permissions)

**Specific Tests to Add:**
- Missing error conditions for each tool
- Various parameter combinations
- Rate limit handling
- Authentication issues
- Permission errors

**Sample Test Implementation:**
```python
# Example: tests/integration/tools/issues/test_issue_tools.py
@pytest.mark.integration
def test_create_issue_lifecycle():
    """Test the complete lifecycle of an issue using the MCP tool."""
    # Implementation for all stages of issue lifecycle
```

### 2. Config Package

**Approach:**
- Test configuration loading from various sources
- Test environment variable overrides
- Test default configurations
- Test validation logic

**Sample Test Implementation:**
```python
# Example: tests/unit/config/test_settings.py
def test_default_configuration():
    """Test default configuration is loaded correctly."""
    config = load_config()
    assert "tool_groups" in config
    assert config["tool_groups"]["issues"]["enabled"] is True
    assert config["tool_groups"]["repositories"]["enabled"] is False

def test_environment_variable_override():
    """Test environment variables override default configuration."""
    with patch.dict(os.environ, {"PYGITHUB_ENABLE_REPOSITORIES": "true"}):
        config = load_config()
        assert config["tool_groups"]["repositories"]["enabled"] is True
```

### 3. Server Module

#### Coverage Priority: High (Currently 67%)

**Approach:**
- Test server initialization with various configurations
- Test tool registration/deregistration
- Test server error handling
- Test connection/disconnection processes

**Specific Tests to Add:**
- Server initialization with different configs
- Error handling for invalid tool registrations
- Server lifecycle events

**Sample Test Implementation:**
```python
# Example: tests/unit/test_server_init.py
def test_create_server():
    """Test that create_server returns a properly configured FastMCP instance."""
    server = create_server()
    assert server is not None
    # Additional assertions
```

### 4. Client and Rate Limit Module

#### Coverage Priority: High (Currently 69% for rate_limit.py)

**Approach:**
- Test backoff calculations with various inputs
- Test rate limit detection from different response types
- Test different rate limit types (core, search, etc.)

**Specific Tests to Add:**
- Exponential backoff with different retry counts
- Rate limit header parsing
- Secondary rate limit handling
- Different rate limit types

### 5. Operations Module

#### Coverage Priority: High (Currently 75% for operations/issues.py)

**Approach:**
- Focus on untested functions and branches
- Create comprehensive lifecycle tests
- Test error conditions extensively

**Specific Tests to Add:**
- Error handling for all operations
- Parameter validation
- Edge cases like empty lists, large payloads
- Rate limit handling during operations

**Sample Test Implementation:**
```python
# Example: tests/integration/operations/issues/test_lifecycle.py
@pytest.mark.integration
def test_issue_lifecycle():
    """Test the complete lifecycle of an issue."""
    # Using the real GitHub API:
    # 1. Create an issue
    # 2. Get the issue
    # 3. Update the issue
    # 4. Add comments, labels, etc.
    # 5. Clean up
```

### 6. Tools Registration Framework

#### Coverage Priority: Medium (Currently 77% for tools/__init__.py)

**Approach:**
- Test tool decorator functionality
- Test registration mechanisms
- Test tool discovery
- Test configuration-based enabling/disabling

**Sample Test Implementation:**
```python
# Example: tests/unit/tools/test_registration.py
def test_tool_decorator():
    """Test tool decorator registers functions correctly."""
    # Implementation

def test_load_tools_with_config():
    """Test tool loading based on configuration."""
    # Implementation
```

### 7. Converters

#### Coverage Priority: Medium (77% for parameters.py, 75% for repositories/*)

**Approach:**
- Test conversion of different object types
- Test error handling during conversion
- Test edge cases with unusual data
- Test validation logic

### 8. Main Module

#### Coverage Priority: Medium (Currently 0%)

**Approach:**
- Test command-line entry points
- Test environment variable handling
- Test configuration loading

## Testing New Tool Groups

As new tool groups are added, follow these guidelines:

1. Create a matching integration test directory structure
2. Test each tool function with the real GitHub API
3. Implement lifecycle tests that cover the full resource lifecycle
4. Test both success and error cases
5. Follow established patterns for test setup and cleanup

## Implementation Timeline

1. **Phase 1 (Week 1-2):** High priority modules
   - Implement tests for tools/issues/tools.py
   - Add server.py tests
   - Improve rate_limit.py coverage
   - Enhance operations/issues.py tests

2. **Phase 2 (Week 3-4):** Medium priority modules
   - Add tests for __main__.py
   - Improve converters coverage
   - Enhance tools registration tests

3. **Phase 3 (Week 5):** Low priority modules
   - Fill specific gaps in high-coverage modules
   - Final coverage report and assessment

## Testing Infrastructure Improvements

To support this effort, we should also:

1. Create robust test helpers for:
   - Resource creation and cleanup
   - Test identification/tagging
   - Rate limit handling
   - Retryable test decorators

2. Enhance test fixtures for:
   - Repository setup/teardown
   - Issue lifecycle management
   - Comment management
   - Label management

## Unit Testing Without Mocks

While our integration tests follow the real API approach from ADR-002, we've also refined our unit testing strategy to minimize dependency on mocking frameworks. This approach has several benefits:

### Using Dataclasses Instead of Mock Objects

We've found that Python's standard library `dataclasses` provide a superior alternative to `unittest.mock.MagicMock` for creating test objects:

```python
# Instead of this:
mock_repo = MagicMock()
mock_repo.id = 12345
mock_repo.name = "test-repo"
mock_repo.full_name = "test-owner/test-repo"
mock_repo.owner.login = "test-owner"

# Prefer this:
@dataclass
class RepositoryOwner:
    login: str

@dataclass
class Repository:
    id: int
    name: str
    full_name: str
    owner: RepositoryOwner
    private: bool
    html_url: str
    description: str = None
    
repo = Repository(
    id=12345,
    name="test-repo",
    full_name="test-owner/test-repo",
    owner=RepositoryOwner(login="test-owner"),
    private=False,
    html_url="https://github.com/test-owner/test-repo",
    description="Test repository description"
)
```

**Benefits:**
- Type safety - IDE autocomplete works properly
- No unexpected attribute creation
- Clear structure that mirrors the real objects
- Better representation in test failure output
- More maintainable test code
- Prevents hidden bugs from typos in attribute names

### Pytest Fixtures and Dependency Injection

Use pytest fixtures to create and inject test objects:

```python
@pytest.fixture
def test_repository():
    """Create a test repository object."""
    return Repository(
        id=12345,
        name="test-repo",
        # other attributes...
    )

def test_convert_repository(test_repository):
    """Test repository conversion function."""
    result = convert_repository(test_repository)
    assert result["id"] == 12345
    # other assertions...
```

### Context Managers for Test Environment

For environment-dependent code like `__main__.py`:

```python
@contextmanager
def capture_stdout():
    """Capture stdout for testing."""
    new_stdout = StringIO()
    old_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield new_stdout
    finally:
        sys.stdout = old_stdout
```

### Testing __main__.py and Module Loading

For testing modules that use `if __name__ == "__main__"` logic:

```python
def test_module_execution(monkeypatch):
    # Keep track if main was called
    main_called = False
    
    # Define a function to track if main is called
    def track_main():
        nonlocal main_called
        main_called = True
    
    # Patch the main function
    monkeypatch.setattr('module.__main__.main', track_main)
    
    # Simulate module execution with __name__ == "__main__"
    tmp_name = __main__.__name__
    __main__.__name__ = "__main__"
    
    try:
        # This should execute the if __name__ == "__main__" block
        importlib.reload(__main__)
        
        # Verify main was called
        assert main_called is True
    finally:
        # Restore original module name
        __main__.__name__ = tmp_name
```

## Best Practices & Standards

1. **No Mocks Policy**
   - Eliminate all mocking for integration tests
   - Use real API interactions for testing behavior
   - Accept the trade-offs of real API testing for higher confidence

2. **Alternative Approaches to Mocking**
   - Use dataclasses for test objects instead of MagicMock
   - Define minimal, focused classes that match expected interfaces
   - Use default values to simplify test creation
   - Leverage standard library tools (contextmanager, StringIO, importlib.reload)
   - Consider using types.SimpleNamespace for simple attribute containers
   - Apply dependency injection for easier test parameterization
   - Design functions to accept dependencies rather than create them

3. **Focus on Behavior Testing**
   - Test what a function does, not how it does it
   - Verify inputs and outputs, not implementation details
   - Create equivalence classes of test cases
   - Focus on high-level outcomes rather than internal steps
   - Test edge cases thoroughly (None values, empty lists, etc.)
   - Verify error conditions as carefully as success paths

4. **Test Isolation**
   - Each test should be independent and isolated from others
   - Implement proper setup and teardown

5. **Resource Management**
   - Use unique identifiers for test resources
   - Tag all test-created resources for easy identification
   - Always clean up test resources

6. **Pagination in Tests**
   - Always add pagination limits when testing list operations
   - Use reasonable page sizes (20-30 items) to avoid performance issues
   - Be aware that repositories can grow to contain hundreds or thousands of items
   - Testing examples:
     ```python
     # Good - Using pagination limits
     issues = list_issues(ListIssuesParams(
         owner=owner,
         repo=repo,
         state="closed",
         per_page=20,   # Limit results to avoid hanging
         page=1         # Only get first page
     ))
     
     # Problematic - No pagination limits (will try to fetch all items)
     issues = list_issues(ListIssuesParams(
         owner=owner,
         repo=repo,
         state="closed"
     ))
     ```
   - For operations that need to find specific items:
     - Create test items with unique identifiers
     - Place test items at the beginning of lists (e.g., with naming that sorts first)
     - Use targeted queries where possible (labels, state filters, etc.)
   - Consider time limits for tests that could potentially run long

6. **Rate Limit Handling**
   - Implement exponential backoff
   - Use conditional requests where possible
   - Consider resource-specific rate limits

7. **Error Testing**
   - Test both success and error scenarios
   - Test edge cases and boundary conditions
   - Verify error messages and codes

## CI/CD Configuration

For CI/CD, configure:

1. Environment variables for test credentials
2. Test repository access
3. Pytest marks to separate unit and integration tests
4. Rate limit handling

Example CI commands:

```bash
# Run only unit tests (fast)
pytest tests/unit/ -v

# Run integration tests (requires credentials)
pytest tests/integration/ -v --run-integration
```

## Tracking Progress

We'll track progress by:
1. Running regular coverage reports
2. Documenting new tests in test report documents
3. Updating this plan as new gaps are identified

## Conclusion

By following this comprehensive testing strategy, we aim to:
1. Increase overall test coverage to >90%
2. Maintain our commitment to real API testing (ADR-002)
3. Ensure thorough testing of the modular tool architecture (ADR-006)
4. Provide robust test coverage for all layers of the application

This will result in higher confidence in our code, better reliability, and easier maintenance and extension of the PyGithub MCP Server.

## References

- [ADR-002: Real API Testing](../adr/002_real_api_testing.md)
- [ADR-006: Modular Tool Architecture](../adr/006_modular_tool_architecture.md)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [PyTest Documentation](https://docs.pytest.org/)
