# Testing Strategy for Modular Tool Architecture

This document outlines the testing strategy for the modular tool architecture implemented as part of ADR-006.

## Overview

The modular tool architecture introduces several new components that need testing:

1. Configuration system (`config/` package)
2. Tool registration framework (`tools/` package)
3. Tool modules (e.g., `tools/issues/`)
4. Refactored server initialization

Our testing strategy follows the principles established in [ADR-002: Real API Testing](../adr/002_real_api_testing.md), which emphasizes:

- Eliminating mock-based testing
- Testing with real GitHub API interactions
- Focusing on behavior and outcomes rather than implementation details
- Thorough test isolation and cleanup

## Test Organization

Tests are organized into two main categories:

```
tests/
├── unit/            # Fast tests with no external dependencies
│   ├── config/      # Tests for configuration system
│   ├── tools/       # Tests for tool registration framework
│   └── ...          # Existing unit tests
└── integration/     # Tests that use the real GitHub API
    ├── issues/      # Tests for issue-related tools
    ├── repositories/# Tests for repository-related tools (future)
    └── ...          # Existing integration tests
```

## Unit Testing Approach

For the new modular architecture components, we will create focused unit tests that validate core functionality without external dependencies.

### Config Package Testing

Test the configuration system in `src/pygithub_mcp_server/config/`:

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

### Tools Framework Testing

Test the tool registration system in `src/pygithub_mcp_server/tools/`:

```python
# Example: tests/unit/tools/test_registration.py
def test_tool_decorator():
    """Test tool decorator registers functions correctly."""
    # Implementation

def test_load_tools_with_config():
    """Test tool loading based on configuration."""
    # Implementation
```

## Integration Testing Approach

Following ADR-002, our integration tests will use the real GitHub API without mocks.

### Tool Module Integration Tests

For each tool module (e.g., `src/pygithub_mcp_server/tools/issues/tools.py`):

```python
# Example: tests/integration/issues/test_issue_tools.py
@pytest.mark.integration
def test_create_issue_lifecycle():
    """Test the complete lifecycle of an issue."""
    # Using the real GitHub API:
    # 1. Create an issue
    # 2. Get the issue
    # 3. Update the issue
    # 4. Add comments, labels, etc.
    # 5. Clean up
```

Key testing principles:

1. Test real API behavior with configured test credentials
2. Test full resource lifecycles
3. Test error scenarios (invalid inputs, permissions, etc.)
4. Implement proper cleanup to avoid test pollution
5. Use unique identifiers for test resources
6. Handle rate limits with exponential backoff

## Testing New Tool Groups

As new tool groups are added, follow these guidelines:

1. Create a matching integration test directory (e.g., `tests/integration/repositories/`)
2. Test each tool function with the real GitHub API
3. Implement lifecycle tests that cover the full resource lifecycle
4. Test both success and error cases
5. Follow established patterns for test setup and cleanup

Example test structure for a new tool group:

```python
# Example: tests/integration/repositories/test_repo_tools.py
@pytest.mark.integration
def test_create_repository_lifecycle():
    """Test the complete lifecycle of a repository."""
    # Implementation
```

## Server Testing

For the refactored server initialization:

```python
# Example: tests/unit/test_server_init.py
def test_create_server():
    """Test that create_server returns a properly configured FastMCP instance."""
    server = create_server()
    assert server is not None
    # Additional assertions
```

Integration tests for server initialization:

```python
# Example: tests/integration/test_server_integration.py
@pytest.mark.integration
def test_server_loads_configured_tools():
    """Test that server loads tools based on configuration."""
    # Implementation
```

## CI/CD Configuration

For CI/CD, configure:

1. Environment variables for test credentials
2. Test repository access
3. Pytest marks to separate unit and integration tests
4. Rate limit handling

Example CI command:

```bash
# Run only unit tests (fast)
pytest tests/unit/ -v

# Run integration tests (requires credentials)
pytest tests/integration/ -v --runintegration
```

## Best Practices

1. **Test Isolation**: Each test should be independent and isolated from others
2. **Cleanup**: Always clean up resources created during tests
3. **Unique Identifiers**: Use unique identifiers for test resources
4. **Resource Tagging**: Tag all test-created resources for easy identification
5. **Error Cases**: Test both success and error scenarios
6. **Rate Limits**: Implement rate limit handling with exponential backoff

## Avoiding Mocks

In accordance with ADR-002:

1. Eliminate all mocking for integration tests
2. Use real API interactions for testing behavior
3. Accept the trade-offs of real API testing for higher confidence
4. Implement robust retry mechanisms for network issues

## References

- [ADR-002: Real API Testing](../adr/002_real_api_testing.md)
- [ADR-006: Modular Tool Architecture](../adr/006_modular_tool_architecture.md)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [PyTest Documentation](https://docs.pytest.org/)
