# Integration Testing Guidelines

This directory contains integration tests for the PyGithub MCP Server that interact with the real GitHub API. Following ADR-002, these tests use real API interactions instead of mocks to ensure proper behavior.

## Getting Started

### Environment Setup

Tests require the following environment variables to be set:
- `GITHUB_PERSONAL_ACCESS_TOKEN`: Your GitHub Personal Access Token
- `GITHUB_TEST_OWNER`: GitHub username/organization for test operations
- `GITHUB_TEST_REPO`: Repository name for test operations

These can be set in the `.env.test` file in the project root.

### Running Tests

Run integration tests with:

```bash
# Run all integration tests
pytest tests/integration/ --run-integration

# Run specific test modules
pytest tests/integration/operations/repositories/ --run-integration -v
```

## Standardized Fixtures

The following standardized fixtures are available for all integration tests:

### Repository Access

- `test_owner` - Provides the GitHub owner name from environment variables
- `test_repo_name` - Provides the GitHub repository name from environment variables
- `test_repo_obj` - Provides a PyGithub Repository object for the test repository

### Testing Utilities

- `github_client` - Singleton GitHubClient instance for API interactions
- `unique_id` - Generates a unique identifier for test resources
- `with_retry` - Decorator for retrying operations during rate limiting
- `test_cleanup` - Helper for tracking and cleaning up test resources

## Using Fixtures Properly

### Basic Pattern

```python
@pytest.mark.integration
def test_something(test_owner, test_repo_name, with_retry):
    """Test description."""
    # Create parameters
    params = SomeParams(
        owner=test_owner,
        repo=test_repo_name,
        # ...other parameters
    )
    
    # Call operation with retry
    @with_retry
    def operation_with_retry():
        return some_operation(params)
    
    result = operation_with_retry()
    
    # Assert expected results
    assert some_condition(result)
```

### Resource Cleanup

```python
@pytest.mark.integration
def test_resource_creation(test_owner, test_repo_name, unique_id, test_cleanup, with_retry):
    """Test that creates resources requiring cleanup."""
    # Create resource
    resource_name = f"test-resource-{unique_id}"
    
    @with_retry
    def create_resource_with_retry():
        return create_resource(resource_name)
    
    result = create_resource_with_retry()
    
    # Register for cleanup
    test_cleanup.add_issue(test_owner, test_repo_name, result["issue_number"])
    
    # Assert expected behavior
    assert resource_is_valid(result)
```

### Error Handling

```python
@pytest.mark.integration
def test_with_error_handling(test_owner, test_repo_name, with_retry):
    """Test with potential expected errors."""
    try:
        @with_retry
        def operation_with_retry():
            return some_operation()
        
        result = operation_with_retry()
        
        # Assert successful result
        assert is_valid(result)
    except GitHubError as e:
        # Handle expected errors
        error_msg = str(e).lower()
        if "expected error condition" not in error_msg:
            raise  # Re-raise unexpected errors
```

## Best Practices

1. **Always use standard fixtures** rather than redefining your own
2. **Apply retry mechanisms** to all GitHub API calls
3. **Clean up resources** created during tests
4. **Use unique identifiers** for all test resources
5. **Use appropriate pagination** in list operations to avoid long-running tests
6. **Handle expected errors** clearly and precisely
7. **Only use `pytest.skip`** within fixture functions, not in test functions
