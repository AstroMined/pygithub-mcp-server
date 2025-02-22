# PyGithub MCP Server

A Model Context Protocol server that provides tools for interacting with the GitHub API through PyGithub. This server enables AI assistants to perform GitHub operations like managing issues, repositories, and pull requests.

## Features

- List, create, update, and manage GitHub issues
- Handle issue comments and labels
- Object-oriented GitHub API interactions via PyGithub
- Centralized GitHub client management
- Proper error handling and rate limit management
- Clean API abstraction through MCP tools
- Robust pagination handling
- Smart parameter handling and validation for PyGithub methods

## Installation

1. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install --no-build-isolation -e .
```

## Configuration

1. Set up environment variables:
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your-token-here"
```

2. Add the server to your MCP settings (e.g., `claude_desktop_config.json` or `cline_mcp_settings.json`):
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

## Development

### Testing with MCP Inspector
Test MCP tools during development using the MCP Inspector:
```bash
source .venv/bin/activate  # Ensure venv is activated
npx @modelcontextprotocol/inspector uv run pygithub-mcp-server
```

Use the MCP Inspector's Web UI to:
- Experiment with available tools
- Test with real GitHub repositories
- Verify success and error cases
- Document working payloads

### Project Structure

```
src/
└── pygithub_mcp_server/
    ├── __init__.py
    ├── __main__.py
    ├── server.py
    ├── common/
    │   ├── __init__.py
    │   ├── errors.py
    │   ├── github.py      # GitHub client singleton
    │   ├── converters.py  # Object conversion utilities
    │   ├── types.py
    │   ├── utils.py
    │   └── version.py
    └── operations/
        ├── __init__.py
        └── issues.py
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
