# Technical Context

## Technology Stack

### Core Dependencies
- Python 3.10+
- MCP Python SDK
- PyGithub for GitHub API interaction
- Pydantic for schema validation
- pytest for testing

### Development Tools
- UV for dependency management
- mypy for type checking
- black for code formatting
- isort for import sorting
- pylint for linting

## Architecture

### Component Structure
```
src/
└── pygithub_mcp_server/
    ├── __init__.py
    ├── server.py           # Main server implementation
    ├── common/
    │   ├── errors.py      # Custom error classes
    │   ├── types.py       # Pydantic models and types
    │   ├── utils.py       # Utility functions
    │   ├── version.py     # Version information
    │   └── github.py      # GitHub client singleton
    └── operations/
        ├── branches.py    # Branch operations
        ├── commits.py     # Commit operations
        ├── files.py       # File operations
        ├── issues.py      # Issue operations
        ├── pulls.py       # Pull request operations
        ├── repository.py  # Repository operations
        └── search.py      # Search operations

# Project Root
├── .gitignore            # Git ignore patterns
├── LICENSE.md            # MIT License
├── README.md            # Project documentation
├── pyproject.toml       # Project configuration
└── docs/               # Documentation directory
```

### Key Technical Decisions

1. PyGithub Integration
   - Object-oriented API interaction
   - Built-in pagination support
   - Automatic rate limiting
   - Rich object model
   - Singleton client pattern

2. Schema Design
   - PyGithub-aligned schemas
   - Strong type validation
   - Clear object relationships
   - Comprehensive field coverage
   - Conversion utilities

3. Error Handling
   - PyGithub exception mapping
   - Custom error hierarchy
   - Consistent error patterns
   - Clear error messages
   - Rate limit handling

## Development Setup

1. Environment Setup
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

2. Testing
```bash
pytest
pytest --cov=github tests/
```

3. Linting and Formatting
```bash
black .
isort .
pylint github tests
mypy github
```

## GitHub API Integration

1. Authentication
- Personal Access Token required
- Token passed via environment variable
- PyGithub authentication handling
- Session management via PyGithub

2. Rate Limiting
- Automatic handling by PyGithub
- Built-in retries and backoff
- Clear rate limit errors
- Rate limit tracking

3. API Versioning
- PyGithub version compatibility
- GitHub API v3 support
- Consistent version handling
- Automatic header management

## Testing Strategy

1. Unit Tests
- PyGithub object mocking
- Schema validation testing
- Conversion testing
- Error case coverage

2. Integration Tests
- Full PyGithub interaction
- Rate limit handling
- Error recovery
- Pagination testing

3. Mock Testing
- PyGithub response mocking
- Error simulation
- Rate limit testing
- Object conversion testing

## Documentation

1. Code Documentation
- Google style docstrings
- Type hints throughout
- PyGithub object mapping
- Clear function/class purposes

2. API Documentation
- Tool interface documentation
- Schema documentation
- PyGithub object relationships
- Error handling documentation

3. Usage Examples
- Basic usage examples
- PyGithub patterns
- Error handling examples
- Pagination examples

## Implementation Patterns

1. Client Usage
```python
from pygithub_mcp_server.common.github import GitHubClient

def operation():
    client = GitHubClient.get_instance()
    return client.operation()
```

2. Error Handling
```python
try:
    result = github_operation()
    return convert_to_schema(result)
except GithubException as e:
    raise GitHubError(str(e))
```

3. Schema Conversion
```python
def convert_to_schema(github_obj):
    """Convert PyGithub object to our schema."""
    return {
        "field": github_obj.field,
        # ... other fields
    }
```

4. Optional Parameter Handling
```python
def github_operation(required_param, **optional_params):
    # Build kwargs with required parameters
    kwargs = {"required": required_param}
    
    # Add optional parameters only if provided
    if optional_params.get("body"):
        kwargs["body"] = optional_params["body"]
    
    # Convert primitive types to PyGithub objects
    if optional_params.get("milestone"):
        kwargs["milestone"] = get_milestone_object(optional_params["milestone"])
    
    # Make API call with only provided parameters
    return client.operation(**kwargs)
```

## Best Practices

1. PyGithub Usage
- Use object-oriented interface
- Handle pagination properly
- Respect rate limits
- Convert objects consistently
- Build kwargs dynamically for optional parameters
- Only include non-None values in method calls
- Convert primitive types to PyGithub objects
- Handle object conversion errors explicitly

2. Error Management
- Map exceptions properly
- Provide clear messages
- Handle rate limits
- Log errors appropriately

3. Testing
- Mock PyGithub objects
- Test error cases
- Verify conversions
- Check pagination

4. Documentation
- Document object mappings
- Explain conversions
- Show usage examples
- Note limitations
