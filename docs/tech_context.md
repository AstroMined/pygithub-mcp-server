# Technical Context

## Technology Stack

### Core Dependencies
- Python 3.10+
- MCP Python SDK
- Pydantic for schema validation
- requests for HTTP operations
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
github/
  ├── __init__.py
  ├── server.py           # Main server implementation
  ├── common/
  │   ├── errors.py      # Custom error classes
  │   ├── types.py       # Pydantic models and types
  │   ├── utils.py       # Utility functions
  │   └── version.py     # Version information
  └── operations/
      ├── branches.py    # Branch operations
      ├── commits.py     # Commit operations
      ├── files.py       # File operations
      ├── issues.py      # Issue operations
      ├── pulls.py       # Pull request operations
      ├── repository.py  # Repository operations
      └── search.py      # Search operations
```

### Key Technical Decisions

1. Schema Validation
- Using Pydantic for input/output schema validation
- Replacing Zod schemas with Pydantic models
- Maintaining JSON Schema compatibility

2. Synchronous Implementation
- Using synchronous requests for GitHub API calls
- requests library for HTTP operations
- Simple session management with context managers
- Improved reliability and error handling

3. Error Handling
- Custom exception hierarchy matching TypeScript version
- Improved error messages and context
- Straightforward synchronous error handling
- Clear request/response error tracking

4. Type System
- Extensive use of Python type hints
- mypy for static type checking
- Runtime type validation via Pydantic

## Development Setup

1. Environment Setup
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
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
- Proper error handling for auth issues
- Session-based authentication management

2. Rate Limiting
- Respects GitHub API rate limits
- Implements exponential backoff
- Clear rate limit error messages
- Session-level rate limit tracking

3. API Versioning
- Uses GitHub API v3
- Maintains compatibility with API changes
- Version-specific error handling

## Testing Strategy

1. Unit Tests
- Individual operation testing
- Error case coverage
- Schema validation testing

2. Integration Tests
- Full API interaction tests
- Rate limit handling
- Error recovery testing
- Session management testing

3. Mock Testing
- GitHub API response mocking
- Error condition simulation
- Network failure handling

## Documentation

1. Code Documentation
- Google style docstrings
- Type hints throughout
- Clear function/class purposes

2. API Documentation
- Tool interface documentation
- Schema documentation
- Error handling documentation

3. Usage Examples
- Basic usage examples
- Common patterns
- Error handling examples
