# PyGithub MCP Server Test Organization

## Directory Structure

The tests are organized by:
1. Test type (unit vs integration)
2. Module layer (matching source code organization)

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

## Test Organization Pattern

- **Unit tests**: Focus on testing individual components in isolation
- **Integration tests**: Test interaction with the real GitHub API following ADR-002

### Tests are organized by application layer:

1. **Client**: GitHub API client and rate limiting
2. **Converters**: Object conversion between PyGithub and our schema
3. **Errors**: Error handling and formatting
4. **Operations**: Core GitHub API operations
5. **Schemas**: Data validation and modeling
6. **Tools**: MCP tool registration and implementation
7. **Utils**: Utility functions

For integration tests, within each layer (especially operations and tools), tests are further organized by GitHub object type (issues, repositories, users, etc.).
