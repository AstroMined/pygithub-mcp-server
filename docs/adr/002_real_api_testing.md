# ADR 002: Real API Testing

## Status
Accepted (Updated 3/4/2025)

## Context
The server's test suite has been relying on mock fixtures that attempt to replicate PyGithub's behavior with the GitHub API.  
This has led to:
- Complex mock implementations that are difficult to maintain
- Brittle test fixtures that break with minor API changes
- Difficulty maintaining mock parity with GitHub API through PyGithub's abstraction layer
- Significant time spent debugging mock behavior rather than actual code
- Lower confidence in test results and their applicability to real-world use

Recent experience has shown that even with careful implementation, mocks often fail to accurately represent the behavior of the real GitHub API. This leads to tests that pass with mocks but fail with the real API, or vice versa, undermining confidence in the test suite.

## Decision
We will completely eliminate mock-based testing in favor of real GitHub API testing through PyGithub's abstraction layer for integration tests, and use alternative approaches to eliminate tradinional `MagicMock` style mocking in unit tests:

1. **Test Philosophy**:
   - Eliminate all mocking for integration tests in favor of real API interactions
   - Test actual behaviors and outcomes rather than implementation details
   - Use dataclasses and minimal test objects instead of MagicMock for unit tests
   - Focus on testing what functions do, not how they do it
   - Accept the trade-offs of real API testing (network dependency, rate limits) for higher confidence

2. **Test Organization**:
   - Organize tests in a layer-based structure mirroring the application architecture
   - Separate unit tests and integration tests into distinct directories
   - Mark all integration tests with @pytest.mark.integration
   - Use environment variables for test credentials
   - Create clear directory structure that maps to application modules

3. **Test Infrastructure**:
   - Maintain a dedicated test repository rather than creating/deleting for each test run
   - Use test-specific GitHub repo and token with appropriate permissions
   - Implement thorough cleanup mechanisms that run after each test
   - Tag all test-created resources for easy identification
   - Implement rate limit handling with exponential backoff
   - Use unique identifiers for all test resources
   - Provide clear setup documentation

4. **Implementation Approach**:
   - Prioritize modules based on coverage gaps and criticality
   - Build a robust unit test suite using dataclasses and dependency injection
   - Implement integration tests that test full resource lifecycles
   - Use pytest fixtures for test data and environment setup
   - Create helper functions for common test operations
   - Implement phased approach to gradually improve coverage

## Implementation Details

### Directory Structure

We will organize tests in a layer-based structure that mirrors the application architecture:

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

### Unit Testing Without Mocks

While our integration tests will interact with the real GitHub API through PyGithub's abstraction layer, we've also refined our unit testing approach to eliminate dependency on mocking frameworks:

#### Using Dataclasses Instead of Mock Objects

Python's standard library `dataclasses` provide a superior alternative to `unittest.mock.MagicMock`:

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

This approach provides several benefits:
- Type safety - IDE autocomplete works properly
- No unexpected attribute creation
- Clear structure that mirrors the real objects
- Better representation in test failure output
- More maintainable test code
- Prevents hidden bugs from typos in attribute names

#### Pytest Fixtures and Dependency Injection

We use pytest fixtures to create and inject test objects:

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

#### Context Managers for Test Environment

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

### Testing Approach by Module Priority

Based on current coverage and criticality, we've prioritized testing efforts:

#### High Priority Modules

1. **Tools Module** (Currently 50% for tools/issues/tools.py)
   - Create comprehensive integration tests for each tool function
   - Test both success and error paths
   - Cover parameter validation
   - Test edge cases (rate limiting, permissions)

2. **Server Module** (Currently 67%)
   - Test server initialization with various configurations
   - Test tool registration/deregistration
   - Test server error handling
   - Test connection/disconnection processes

3. **Client and Rate Limit Module** (Currently 69% for rate_limit.py)
   - Test backoff calculations with various inputs
   - Test rate limit detection from different response types
   - Test different rate limit types (core, search, etc.)

4. **Operations Module** (Currently 75% for operations/issues.py)
   - Focus on untested functions and branches
   - Create comprehensive lifecycle tests
   - Test error conditions extensively

#### Medium Priority Modules

1. **Tools Registration Framework** (Currently 77% for tools/__init__.py)
   - Test tool decorator functionality
   - Test registration mechanisms
   - Test tool discovery
   - Test configuration-based enabling/disabling

2. **Converters** (77% for parameters.py, 75% for repositories/*)
   - Test conversion of different object types
   - Test error handling during conversion
   - Test edge cases with unusual data

3. **Main Module** (Currently 0%)
   - Test command-line entry points
   - Test environment variable handling
   - Test configuration loading

### Implementation Timeline

We will implement the testing strategy in phases:

1. **Phase 1 (High Priority Modules):**
   - Implement tests for tools/issues/tools.py
   - Add server.py tests
   - Improve rate_limit.py coverage
   - Enhance operations/issues.py tests

2. **Phase 2 (Medium Priority Modules):**
   - Add tests for __main__.py
   - Improve converters coverage
   - Enhance tools registration tests

3. **Phase 3 (Low Priority Modules):**
   - Fill specific gaps in high-coverage modules
   - Final coverage report and assessment

### Test Infrastructure Improvements

To support this effort, we will also:

1. Create robust test helpers for:
   - Resource creation and cleanup
   - Test identification/tagging
   - Rate limit handling
   - Retryable test decorators

2. Enhance test fixtures for:
   - Repository setup/teardown
   - Issue lifecycle management
   - Comment/label management

## Consequences

### Positive
- Tests verify actual API behavior with high confidence
- Complete elimination of complex mock maintenance
- Higher confidence in functionality and compatibility
- No time spent debugging mock behavior
- Tests that pass locally will be more likely to pass in CI
- Easier onboarding for new contributors without mock complexity
- More maintainable test code with clearer structure
- Better type safety with dataclasses instead of MagicMock
- Improved ability to test edge cases and error conditions

### Negative
- Requires test token and repository with appropriate permissions
- Network dependency for all tests that verify external behavior
- Rate limit considerations for test execution
- Slower test execution compared to mock-based tests
- Potential for flakiness due to network issues or API changes
- Need for robust cleanup mechanisms to prevent test pollution
- More complex CI/CD setup for handling credentials and network access

### Mitigations
- Implement robust retry mechanisms for network issues with exponential backoff
- Use test tagging to allow running unit tests separately from integration tests
- Implement thorough cleanup routines that run after each test
- Use conditional requests with ETags to reduce rate limit impact
- Implement request batching where possible to minimize API calls
- Use unique identifiers and resource tagging for reliable cleanup
- Consider caching strategies for frequently accessed data

## Best Practices & Standards

1. **No Mocks Policy for Integration Tests**
   - Eliminate all mocking for integration tests
   - Use real API interactions for testing behavior
   - Accept the trade-offs of real API testing for higher confidence

2. **Alternative Approaches to Mocking for Unit Tests**
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
   - Use pytest fixtures for test data and environment setup

5. **Resource Management**
   - Use unique identifiers for test resources
   - Tag all test-created resources for easy identification
   - Always clean up test resources
   - Implement thorough cleanup mechanisms that run after each test

6. **Rate Limit Handling**
   - Implement exponential backoff with retry
   - Use conditional requests where possible
   - Consider resource-specific rate limits
   - Use test-specific token with appropriate limits

7. **Error Testing**
   - Test both success and error scenarios
   - Test edge cases and boundary conditions
   - Verify error messages and codes
   - Test rate limit handling and recovery

## CI/CD Configuration

For CI/CD, configure:

```bash
# Run only unit tests (fast)
pytest tests/unit/ -v

# Run integration tests (requires credentials)
pytest tests/integration/ -v --run-integration
```

## Guidance for Future Development

1. **New Features:**
   - Always implement real API tests for new features
   - Document any assumptions about API behavior
   - Include both success and error scenarios
   - Test full resource lifecycles

2. **Bug Fixes:**
   - Reproduce bugs with real API tests before fixing
   - Add regression tests using real API
   - Never add mocks to work around API behavior

3. **Refactoring:**
   - Use real API tests as a safety net for refactoring
   - Focus on maintaining behavior, not implementation details
   - Update tests to reflect API changes, not code changes

4. **Test Organization:**
   - Keep unit tests and integration tests separate
   - Organize tests by application layer, then by domain
   - Use descriptive test names that reflect the behavior being tested
   - Implement proper setup and teardown for each test

5. **Test Repository Management:**
   - Tag all test-created resources for easy identification
   - Clean up resources after each test
   - Use unique identifiers for test resources
   - Implement thorough cleanup mechanisms

## References
- [PyGithub Testing Documentation](https://pygithub.readthedocs.io/en/latest/testing.html)
- [GitHub API Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [Testing Microservices: Martin Fowler](https://martinfowler.com/articles/microservice-testing/)
- [Test Doubles: Martin Fowler](https://martinfowler.com/bliki/TestDouble.html)
- [Integration Tests: Kent C. Dodds](https://kentcdodds.com/blog/write-tests)
- [Testing Without Mocks: James Shore](https://www.jamesshore.com/v2/blog/2018/testing-without-mocks)
- [Python Dataclasses Documentation](https://docs.python.org/3/library/dataclasses.html)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
