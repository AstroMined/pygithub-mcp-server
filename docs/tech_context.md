# Technical Context

> **Note:** This document provides a high-level overview of the technology stack and architecture. For detailed implementation patterns, code examples, and best practices, please refer to [`system_patterns.md`](system_patterns.md).

## Technology Stack

### Core Dependencies
- Python 3.10+
- MCP Python SDK
- PyGithub for GitHub API interaction
- Pydantic for schema validation and data modeling
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
    ├── server.py           # Server factory implementation
    ├── schemas/            # Pydantic models organized by domain
    │   ├── __init__.py     # Re-exports all schemas for backward compatibility
    │   ├── base.py         # Base models used across multiple domains
    │   ├── repositories.py # Repository-related schemas
    │   ├── issues.py       # Issue and issue comment related schemas
    │   ├── pull_requests.py # Pull request and PR comment schemas
    │   ├── search.py       # Search-related schemas
    │   └── responses.py    # Response type schemas
    ├── tools/              # Tool implementations organized by domain
    │   ├── __init__.py     # Tool registration system
    │   ├── issues/         # Issue-related tools
    │   │   ├── __init__.py # Issue tools exports
    │   │   └── tools.py    # Issue tool implementations
    │   ├── repositories/   # Repository-related tools
    │   │   ├── __init__.py
    │   │   └── tools.py
    │   └── [other domains]
    ├── config/             # Configuration management
    │   ├── __init__.py     # Re-exports configuration functions
    │   └── settings.py     # Configuration system
    ├── operations/         # Domain operations (business logic)
    │   ├── issues.py       # Issue operations
    │   ├── repositories.py # Repository operations
    │   └── [other operations]
    ├── client/             # GitHub client
    │   ├── __init__.py     # Re-exports client
    │   ├── client.py       # Core GitHub client
    │   └── rate_limit.py   # Rate limit handling
    ├── errors/             # Error handling
    │   ├── __init__.py     # Re-exports errors
    │   ├── exceptions.py   # Custom exceptions
    │   ├── formatters.py   # Error formatting
    │   └── handlers.py     # Error handling
    ├── converters/         # Data transformation functions
    │   ├── __init__.py     # Re-exports all converters
    │   ├── issues/         # Issue-related converters
    │   ├── repositories/   # Repository-related converters
    │   ├── users/          # User-related converters
    │   ├── common/         # Common converters (datetime, pagination)
    │   ├── responses.py    # Tool response formatting
    │   └── parameters.py   # Parameter formatting
    └── utils/              # General utilities
        ├── __init__.py     # Re-exports utilities
        ├── environment.py  # Environment utilities
        └── general.py      # General-purpose utilities

# Project Root
├── .gitignore               # Git ignore patterns
├── LICENSE.md               # MIT License
├── README.md                # Project documentation
├── ROADMAP.md               # Development roadmap
├── pygithub_mcp_config.json.example  # Configuration example
├── pyproject.toml           # Project configuration
├── docs/                    # Documentation directory
│   ├── adr/                 # Architectural Decision Records
│   ├── guides/              # User guides
│   └── [other documentation]
└── tests/                   # Test suite
    ├── unit/                # Unit tests (no external dependencies)
    │   ├── client/          # Tests for client module
    │   ├── config/          # Tests for configuration
    │   └── [other unit tests]
    └── integration/         # Tests that use the real GitHub API
        ├── operations/      # Tests for API operations
        ├── tools/           # Tests for MCP tools
        └── [other integration tests]
```

### Key Technical Decisions

1. **Pydantic-First Architecture (ADR-007)**
   - Pydantic models as primary data interchange format between all layers
   - Operations layer accepts Pydantic models directly
   - No unpacking of models between layers
   - All validation logic lives in Pydantic models
   - Consistent error handling across all layers

2. **PyGithub Integration (ADR-001)**
   - Object-oriented API interaction via PyGithub
   - Built-in pagination support
   - Automatic rate limiting
   - Rich object model
   - Singleton client pattern

3. **Real API Testing (ADR-002)**
   - Elimination of mocks in favor of real API interactions
   - Test behavior rather than implementation details
   - Use dataclasses instead of MagicMock for unit tests
   - Test organization mirrors application architecture
   - Robust cleanup mechanisms for test resources

4. **Schema Organization (ADR-003)**
   - Domain-specific schema files
   - Clear separation of concerns
   - Re-exports for backward compatibility
   - Schema-first development approach

5. **Enhanced Schema Validation (ADR-004)**
   - Custom field validators for critical fields
   - Validation for non-empty strings
   - Improved error messages
   - Alignment with PyGithub expectations

6. **Module Reorganization (ADR-005)**
   - Converters directory with domain-specific modules
   - Minimal utils module with truly general utilities
   - Error handling in dedicated module
   - Client functionality in dedicated module

7. **Modular Tool Architecture (ADR-006)**
   - Tool modules organized by domain
   - Configuration-driven tool registration
   - Decorator-based tool system
   - Selectively enable/disable tool groups

## Development Setup

1. Environment Setup
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

2. Configuration
```bash
# Copy example configuration
cp pygithub_mcp_config.json.example pygithub_mcp_config.json
# Edit configuration file
# Set environment variable
export PYGITHUB_MCP_CONFIG=/path/to/pygithub_mcp_config.json
# Or set specific tool group environments
export PYGITHUB_ENABLE_REPOSITORIES=true
```

3. Testing
```bash
# Run unit tests (fast, no external dependencies)
pytest tests/unit/

# Run integration tests (requires credentials)
pytest tests/integration/ --run-integration
```

4. Linting and Formatting
```bash
black .
isort .
pylint src tests
mypy src
```

## GitHub API Integration

1. Authentication
- Personal Access Token required
- Token passed via environment variable (`GITHUB_TOKEN`)
- PyGithub authentication handling
- Session management via PyGithub

2. Rate Limiting
- Automatic handling by PyGithub
- Built-in retries and exponential backoff
- Clear rate limit errors
- Rate limit tracking

3. API Versioning
- PyGithub version compatibility
- GitHub API v3 support
- Consistent version handling
- Automatic header management

## Testing Strategy

The project follows a comprehensive testing strategy detailed in ADR-002:

1. **Unit Tests**
   - Python dataclasses for test objects instead of mocks
   - Focus on component behaviors in isolation
   - Test schema validation, conversion logic, and configuration
   - Fast execution without external dependencies

2. **Integration Tests**
   - Real GitHub API interactions
   - Test full feature workflows
   - Comprehensive cleanup mechanisms to prevent test pollution
   - Rate limit handling with exponential backoff

3. **Test Organization**
   - Mirrors application architecture for better maintainability
   - Separation of unit and integration tests
   - Clear test markers for selective execution
   - Environment-based configuration for test credentials

For detailed testing patterns including code examples, see the [System Patterns](system_patterns.md#testing-patterns) document.
