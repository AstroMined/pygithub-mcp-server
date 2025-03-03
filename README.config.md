# PyGithub MCP Server Configuration Guide

This guide explains how to configure the PyGithub MCP Server to enable or disable specific tool groups.

## Configuration Options

The PyGithub MCP Server supports a modular architecture that allows you to enable or disable specific tool groups based on your needs. By default, only the `issues` tool group is enabled.

## Configuration Methods

You can configure the server using either of these methods:

### 1. Configuration File

Create a JSON configuration file (e.g., `pygithub_mcp_config.json`) with your desired settings:

```json
{
  "tool_groups": {
    "issues": {"enabled": true},
    "repositories": {"enabled": true},
    "pull_requests": {"enabled": false},
    "discussions": {"enabled": false},
    "search": {"enabled": true},
    "users": {"enabled": false},
    "organizations": {"enabled": false},
    "teams": {"enabled": false},
    "webhooks": {"enabled": false},
    "gists": {"enabled": false}
  },
  "logging": {
    "level": "INFO",
    "file_level": "DEBUG"
  }
}
```

Then set the environment variable `PYGITHUB_MCP_CONFIG` to point to your configuration file:

```bash
export PYGITHUB_MCP_CONFIG=/path/to/pygithub_mcp_config.json
```

### 2. Environment Variables

You can also use environment variables to enable or disable specific tool groups:

```bash
# Enable repositories tools
export PYGITHUB_ENABLE_REPOSITORIES=true

# Disable issues tools
export PYGITHUB_ENABLE_ISSUES=false

# Enable pull requests tools
export PYGITHUB_ENABLE_PULL_REQUESTS=true
```

Use values like `true`, `1`, `yes`, or `on` to enable a tool group, and `false`, `0`, `no`, or `off` to disable it.

## Available Tool Groups

The following tool groups are available:

| Tool Group     | Description                                     | Default |
|----------------|-------------------------------------------------|---------|
| issues         | GitHub issue operations (create, list, update)  | Enabled |
| repositories   | Repository operations                           | Disabled |
| pull_requests  | Pull request operations                         | Disabled |
| discussions    | Discussions operations                          | Disabled |
| search         | GitHub search operations                        | Disabled |
| users          | User management operations                      | Disabled |
| organizations  | Organization operations                         | Disabled |
| teams          | Team management operations                      | Disabled |
| webhooks       | Webhook management operations                   | Disabled |
| gists          | Gist operations                                 | Disabled |

## Logging Configuration

You can also configure logging levels through the configuration file:

```json
{
  "logging": {
    "level": "INFO",    # Console logging level
    "file_level": "DEBUG"  # File logging level
  }
}
```

Valid logging levels are: `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

## Example: Minimal Configuration

To only enable issue tools (the default):

```json
{
  "tool_groups": {
    "issues": {"enabled": true}
  }
}
```

## Example: Development Configuration

A configuration suitable for development:

```json
{
  "tool_groups": {
    "issues": {"enabled": true},
    "repositories": {"enabled": true},
    "pull_requests": {"enabled": true}
  },
  "logging": {
    "level": "DEBUG",
    "file_level": "DEBUG"
  }
}
```

## Adding New Tool Groups

When implementing new tool groups, follow the existing pattern:

1. Create a new directory under `src/pygithub_mcp_server/tools/` for your tool group
2. Implement tool functions using the `@tool()` decorator
3. Create a `register()` function that registers all tools
4. Add your tool group to the default configuration in `settings.py`

## Troubleshooting

If tools aren't loading as expected:

1. Check the server logs for registration messages
2. Ensure your configuration file is valid JSON
3. Verify the `PYGITHUB_MCP_CONFIG` environment variable is set correctly
4. Check that the tool group is enabled in your configuration
