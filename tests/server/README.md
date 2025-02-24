# Server Tests

This directory contains tests specifically for the FastMCP server implementation. These tests verify the server's ability to handle GitHub API operations through MCP tools.

## Organization

- `test_server.py`: Tests for server initialization, tool registration, and tool implementations
- `conftest.py`: Server-specific test fixtures

## Available Fixtures

### From `conftest.py` (server-specific)

- `mock_fastmcp`: Mocks the FastMCP server while tracking tool decorator usage
- `mock_tool_response`: Creates standardized tool responses matching server implementation

### From `../conftest.py` (inherited global fixtures)

- `mock_auth`: GitHub authentication mocking
- `mock_github_class`: GitHub client mocking
- `mock_environment`: Environment setup
- `mock_repo`, `mock_issue`, etc.: Common GitHub object mocks

## Testing Patterns

1. Server Initialization
   - Verify correct server creation
   - Check tool registration
   - Validate server configuration

2. Tool Implementation
   - Test successful operations
   - Verify error handling
   - Check response formatting

3. GitHub Integration
   - Test interaction with GitHub API
   - Verify proper error propagation
   - Check rate limit handling

## Future Considerations

As the server grows to handle more GitHub operations, consider:

1. Subgrouping Tests
   - Group tests by operation type (issues, repos, etc.)
   - Create subdirectories for complex feature sets
   - Maintain clear naming conventions

2. Fixture Evolution
   - Keep fixtures focused and minimal
   - Move new specialized fixtures here
   - Document fixture relationships

3. Response Patterns
   - Maintain consistent error handling
   - Document response formats
   - Version response schemas if needed
