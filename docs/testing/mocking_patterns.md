# Mocking Patterns Guide

This guide covers common mocking patterns and challenges in the PyGithub MCP Server project, with a focus on correctly mocking imported modules while preserving type checking.

## Introduction

### Common Mocking Challenges

When testing Python code that interacts with external libraries like PyGithub, we often face several challenges:
- Mocking imported modules and classes
- Preserving type checking functionality
- Ensuring mocks track method calls correctly
- Balancing realistic behavior with test isolation

### Python's Import System Behavior

Understanding Python's import system is crucial for effective mocking:
- Import statements bind names in the module's namespace at import time
- These bindings are not affected by later changes to the global module
- Mocking must target the specific namespace where the code uses the imported names

## Module Import Patching

### How Imports Bind Names

When you write:
```python
from github import Auth, Github
```

Python:
1. Imports the `github` module
2. Binds `Auth` and `Github` names in your module's namespace
3. These bindings are independent of the original module

### Why Global Patching Fails

Consider this common mistake:
```python
# This won't work as expected
monkeypatch.setattr('github.Auth', mock_auth)

# Because your module already has its own reference to Auth
from github import Auth  # This binding is unaffected by the patch
```

The patch changes the global module, but your code uses the already-bound name.

### Correct Patching Strategy

Instead, patch where the code actually uses the imported names:
```python
# This works correctly
monkeypatch.setattr('your_module.Auth', mock_auth)
# Or more specifically
monkeypatch.setattr('pygithub_mcp_server.common.github.Auth', mock_auth)
```

## Type Preservation

### Working with isinstance() Checks

Many libraries use `isinstance()` checks for type validation. For example, PyGithub's Github class:
```python
assert isinstance(auth, github.Auth.Auth)
```

To make this work:
1. The real type must be available for the check
2. Mock instances must be properly typed

### Using spec Parameter

The `spec` parameter helps create properly typed mocks:
```python
# Create instance that passes type checks
mock_token_instance = Mock(spec=Auth.Auth)

# Create factory that returns typed instance
mock_token = Mock(return_value=mock_token_instance)
```

### Balancing Mocking and Type Checking

Sometimes you need both mocking behavior and type checking:
```python
@pytest.fixture
def mock_auth(monkeypatch):
    """Mock Github Auth.Token while preserving type checking."""
    # Create properly typed instance
    mock_token_instance = Mock(spec=Auth.Auth)
    
    # Create factory that returns typed instance
    mock_token = Mock(return_value=mock_token_instance)
    
    # Patch at point of use
    monkeypatch.setattr('pygithub_mcp_server.common.github.Auth.Token', mock_token)
    
    return mock_token
```

## Real-World Examples

### PyGithub Auth Mocking

Our GitHubClient uses PyGithub's authentication:
```python
def _init_client(self) -> None:
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    auth = Auth.Token(token)
    self._github = Github(auth=auth)
```

To test this, we need:
1. A mock Token factory that tracks calls
2. A mock token instance that passes type checks
3. Proper patching at the point of use

Complete fixture:
```python
@pytest.fixture
def mock_auth(monkeypatch):
    """Mock Github Auth.Token while preserving module structure."""
    # Create token instance that will pass isinstance(auth, Auth.Auth)
    mock_token_instance = Mock(spec=Auth.Auth, name="mock_auth_token")
    
    # Create Token factory mock that returns our instance
    mock_token = Mock(return_value=mock_token_instance)
    
    # Patch only the Token method, preserving Auth.Auth type
    monkeypatch.setattr("pygithub_mcp_server.common.github.Auth.Token", mock_token)
    
    return mock_token
```

This allows tests to:
- Verify Token was called with correct arguments
- Pass PyGithub's type checks
- Track method calls on the token instance

### Other Common Scenarios

Similar patterns apply when mocking other imported modules:

1. Database Connections:
```python
# In your code
from database import Connection

# In tests
monkeypatch.setattr('your_module.Connection', mock_connection)
```

2. External APIs:
```python
# In your code
from external_api import Client

# In tests
monkeypatch.setattr('your_module.Client', mock_client)
```

## Best Practices

1. **Identify Import Points**
   - Look for import statements in the code under test
   - Note exactly which names are imported
   - Determine where those names are used

2. **Preserve Types**
   - Use `spec` parameter when type checking is needed
   - Keep real types available for isinstance() checks
   - Mock only the behavior, not the type system

3. **Patch Carefully**
   - Target the specific module namespace
   - Patch at the point of use
   - Verify your patches affect the right code

4. **Track Calls**
   - Ensure mocks can track method calls
   - Return consistent mock instances
   - Make assertions about how code uses dependencies

5. **Document Patterns**
   - Add successful patterns to .clinerules
   - Update testing documentation
   - Share learnings with the team
