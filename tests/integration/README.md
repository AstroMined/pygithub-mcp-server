# Integration Tests

This directory contains integration tests for the PyGithub MCP Server that use the real GitHub API. These tests verify that our operations work correctly with the actual GitHub API, providing high confidence in the functionality of our server.

## Test Structure

The integration tests are organized by domain:

- `issues/`: Tests for GitHub issue operations
  - `test_lifecycle.py`: Complete issue lifecycle tests
  - `test_create.py`: Tests for creating issues
  - `test_update.py`: Tests for updating issues
  - `test_list.py`: Tests for listing issues
  - `test_comments.py`: Tests for issue comment operations
  - `test_labels.py`: Tests for issue label operations
- `repositories/`: Tests for repository operations (future)
- `users/`: Tests for user operations (future)

## Test Fixtures

Common test fixtures are defined in `conftest.py`:

- `load_test_env`: Loads environment variables from `.env.test`
- `github_client`: Provides a GitHub client instance
- `test_repo`: Provides a test repository instance
- `test_owner`: Provides the test repository owner
- `test_repo_name`: Provides the test repository name
- `unique_id`: Generates a unique identifier for test resources
- `with_retry`: Provides a decorator for retrying operations on rate limit errors

## Running the Tests

### Prerequisites

1. Create a `.env.test` file in the project root with the following variables:
   ```
   GITHUB_PERSONAL_ACCESS_TOKEN=your-test-token
   GITHUB_TEST_OWNER=test-owner
   GITHUB_TEST_REPO=test-repo
   ```

2. Ensure the test token has appropriate permissions for the test repository.

### Running All Integration Tests

```bash
pytest tests/integration -v
```

### Running Specific Test Files

```bash
pytest tests/integration/issues/test_lifecycle.py -v
```

### Running Specific Test Functions

```bash
pytest tests/integration/issues/test_create.py::test_create_issue_required_params -v
```

## Test Design Principles

1. **Real API Testing**: All tests use the real GitHub API to verify behavior.
2. **Resource Cleanup**: Each test cleans up after itself, even if the test fails.
3. **Unique Resources**: Tests use unique identifiers to prevent conflicts.
4. **Rate Limit Handling**: Tests use exponential backoff to handle rate limits.
5. **Comprehensive Coverage**: Tests cover both success and error scenarios.
6. **Full Lifecycle Testing**: Tests cover the complete lifecycle of resources.

## Test Patterns

### Resource Creation and Cleanup

```python
@pytest.mark.integration
def test_example(test_owner, test_repo_name, unique_id, with_retry):
    # Setup
    owner = test_owner
    repo = test_repo_name
    title = f"Test Issue {unique_id}"
    
    # Create resource
    @with_retry
    def create_test_resource():
        return create_issue(owner, repo, title)
    
    resource = create_test_resource()
    
    try:
        # Test operations
        # ...
    finally:
        # Cleanup
        try:
            @with_retry
            def cleanup_resource():
                return update_issue(owner, repo, resource["issue_number"], state="closed")
            
            cleanup_resource()
        except Exception as e:
            print(f"Failed to clean up resource: {e}")
```

### Rate Limit Handling

```python
@with_retry
def operation_that_might_hit_rate_limits():
    return some_github_operation()
```

## Best Practices

1. Always use the `@pytest.mark.integration` decorator for integration tests.
2. Always use the `with_retry` decorator for operations that might hit rate limits.
3. Always clean up resources in a `finally` block to ensure cleanup even if the test fails.
4. Use unique identifiers for all test resources to prevent conflicts.
5. Verify both success and error scenarios.
6. Test the complete lifecycle of resources.
7. Keep tests focused on specific functionality.
8. Use descriptive test names that reflect the behavior being tested.
