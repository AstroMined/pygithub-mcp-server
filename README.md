# PyGithub MCP Server

A Model Context Protocol server that provides tools for interacting with the GitHub API through PyGithub. This server enables AI assistants to perform GitHub operations like managing issues, repositories, and pull requests.

## Features

- Modular Tool Architecture:
  - Configurable tool groups that can be enabled/disabled
  - Domain-specific organization (issues, repositories, etc.)
  - Flexible configuration via file or environment variables
  - Clear separation of concerns with modular design
  - Easy extension with consistent patterns

- Complete GitHub Issue Management:
  - Create and update issues
  - Get issue details and list repository issues
  - Add, list, update, and delete comments
  - Manage issue labels
  - Handle assignees and milestones

- Smart Parameter Handling:
  - Dynamic kwargs building for optional parameters
  - Proper type conversion for GitHub objects
  - Validation for all input parameters
  - Clear error messages for invalid inputs

- Robust Implementation:
  - Object-oriented GitHub API interactions via PyGithub
  - Centralized GitHub client management
  - Proper error handling and rate limiting
  - Clean API abstraction through MCP tools
  - Comprehensive pagination support
  - Detailed logging for debugging

## Documentation

Comprehensive guides are available in the docs/guides directory:

- error-handling.md: Error types, handling patterns, and best practices
- security.md: Authentication, access control, and content security
- tool-reference.md: Detailed tool documentation with examples

See these guides for detailed information about using the PyGithub MCP Server.

## Usage Examples

### Issue Operations

1. Creating an Issue
```json
{
  "owner": "username",
  "repo": "repository",
  "title": "Issue Title",
  "body": "Issue description",
  "assignees": ["username1", "username2"],
  "labels": ["bug", "help wanted"],
  "milestone": 1
}
```

2. Getting Issue Details
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1
}
```

3. Updating an Issue
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "title": "Updated Title",
  "body": "Updated description",
  "state": "closed",
  "labels": ["bug", "wontfix"]
}
```

### Comment Operations

1. Adding a Comment
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "body": "This is a comment"
}
```

2. Listing Comments
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "per_page": 10
}
```

3. Updating a Comment
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "comment_id": 123456789,
  "body": "Updated comment text"
}
```

### Label Operations

1. Adding Labels
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "labels": ["enhancement", "help wanted"]
}
```

2. Removing a Label
```json
{
  "owner": "username",
  "repo": "repository",
  "issue_number": 1,
  "label": "enhancement"
}
```

All operations handle optional parameters intelligently:
- Only includes provided parameters in API calls
- Converts primitive types to GitHub objects (e.g., milestone number to Milestone object)
- Provides clear error messages for invalid parameters
- Handles pagination automatically where applicable

## Installation

1. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install -e .
```

## Configuration

### Basic Configuration

Add the server to your MCP settings (e.g., `claude_desktop_config.json` or `cline_mcp_settings.json`):
```json
{
  "mcpServers": {
    "github": {
      "command": "/path/to/repo/.venv/bin/python",
      "args": ["-m", "pygithub_mcp_server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

### Tool Group Configuration

The server supports selectively enabling or disabling tool groups through configuration. You can configure this in two ways:

#### 1. Configuration File

Create a JSON configuration file (e.g., `pygithub_mcp_config.json`):
```json
{
  "tool_groups": {
    "issues": {"enabled": true},
    "repositories": {"enabled": true},
    "pull_requests": {"enabled": false},
    "discussions": {"enabled": false},
    "search": {"enabled": true}
  }
}
```

Then specify this file in your environment:
```bash
export PYGITHUB_MCP_CONFIG=/path/to/pygithub_mcp_config.json
```

#### 2. Environment Variables

Alternatively, use environment variables to configure tool groups:
```bash
export PYGITHUB_ENABLE_ISSUES=true
export PYGITHUB_ENABLE_REPOSITORIES=true
export PYGITHUB_ENABLE_PULL_REQUESTS=false
```

By default, only the `issues` tool group is enabled. See `README.config.md` for more detailed configuration options.

## Development

### Testing
The project includes a comprehensive test suite:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov

# Run specific test file
pytest tests/test_operations/test_issues.py

# Run tests matching a pattern
pytest -k "test_create_issue"
```

Note: Many tests are currently failing and under investigation. This is a known issue being actively worked on.

### Testing with MCP Inspector
Test MCP tools during development using the MCP Inspector:
```bash
source .venv/bin/activate  # Ensure venv is activated
npx @modelcontextprotocol/inspector -e GITHUB_PERSONAL_ACCESS_TOKEN=your-token-here uv run pygithub-mcp-server
```

Use the MCP Inspector's Web UI to:
- Experiment with available tools
- Test with real GitHub repositories
- Verify success and error cases
- Document working payloads

### Project Structure

```
tests/
├── unit/                # Fast tests without external dependencies
│   ├── config/          # Configuration tests
│   ├── tools/           # Tool registration tests
│   └── ...              # Other unit tests
└── integration/         # Tests with real GitHub API
    ├── issues/          # Issue tools tests
    └── ...              # Other integration tests
```

```
src/
└── pygithub_mcp_server/
    ├── __init__.py
    ├── __main__.py
    ├── server.py        # Server factory (create_server)
    ├── version.py
    ├── config/          # Configuration system
    │   ├── __init__.py
    │   └── settings.py  # Configuration management
    ├── tools/           # Modular tool system
    │   ├── __init__.py  # Tool registration framework
    │   └── issues/      # Issue tools
    │       ├── __init__.py
    │       └── tools.py # Issue tool implementations
    ├── client/          # GitHub client functionality
    │   ├── __init__.py
    │   ├── client.py    # Core GitHub client
    │   └── rate_limit.py # Rate limit handling
    ├── converters/      # Data transformation
    │   ├── __init__.py
    │   ├── parameters.py # Parameter formatting
    │   ├── responses.py # Response formatting
    │   ├── common/      # Common converters
    │   ├── issues/      # Issue-related converters
    │   ├── repositories/ # Repository converters
    │   └── users/       # User-related converters
    ├── errors/          # Error handling
    │   ├── __init__.py
    │   └── exceptions.py # Custom exceptions
    ├── operations/      # GitHub operations
    │   ├── __init__.py
    │   └── issues.py
    ├── schemas/         # Data models
    │   ├── __init__.py
    │   ├── base.py
    │   ├── issues.py
    │   └── ...
    └── utils/           # General utilities
        ├── __init__.py
        └── environment.py # Environment utilities
```

### Troubleshooting

1. Server fails to start:
   - Verify venv Python path in MCP settings
   - Ensure all requirements are installed in venv
   - Check GITHUB_PERSONAL_ACCESS_TOKEN is set and valid

2. Build errors:
   - Use --no-build-isolation flag with uv build
   - Ensure Python 3.10+ is being used
   - Verify all dependencies are installed

3. GitHub API errors:
   - Check token permissions and validity
   - Review pygithub_mcp_server.log for detailed error traces
   - Verify rate limits haven't been exceeded

## Dependencies
- Python 3.10+
- MCP Python SDK
- Pydantic
- PyGithub
- UV package manager

## License

MIT
