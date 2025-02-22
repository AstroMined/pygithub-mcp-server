# GithubIntegration Class

The `GithubIntegration` class is used to manage GitHub App integrations and obtain installation tokens.

## Constructor

```python
GithubIntegration(
    integration_id: int | str | None = None,
    private_key: str | None = None,
    base_url: str = 'https://api.github.com',
    *,
    timeout: int = 15,
    user_agent: str = 'PyGithub/Python',
    per_page: int = 30,
    verify: bool | str = True,
    retry: int | Retry | None = None,
    pool_size: int | None = None,
    seconds_between_requests: float | None = 0.25,
    seconds_between_writes: float | None = 1.0,
    jwt_expiry: int = 300,
    jwt_issued_at: int = -60,
    jwt_algorithm: str = 'RS256',
    auth: AppAuth | None = None,
    lazy: bool = False
)
```

### Parameters

- **auth**: Authentication method (preferred way to authenticate)
- **base_url**: API endpoint URL
- **timeout**: Request timeout in seconds
- **user_agent**: Custom user agent string
- **per_page**: Items per page in paginated results
- **verify**: SSL verification
- **retry**: Retry configuration for failed requests
- **pool_size**: Connection pool size
- **seconds_between_requests**: Delay between API requests
- **seconds_between_writes**: Delay between write operations
- **lazy**: Enable lazy loading of objects

### Deprecated Parameters
- **integration_id**: Use `auth=github.Auth.AppAuth()` instead
- **private_key**: Use `auth=github.Auth.AppAuth()` instead
- **jwt_expiry**: Use `auth=github.Auth.AppAuth()` instead
- **jwt_issued_at**: Use `auth=github.Auth.AppAuth()` instead
- **jwt_algorithm**: Use `auth=github.Auth.AppAuth()` instead

## Core Methods

### Authentication

```python
# Create a JWT token
jwt = integration.create_jwt(expiration=300)  # 5 minutes expiry

# Get an installation access token
token = integration.get_access_token(
    installation_id,
    permissions={"contents": "read", "issues": "write"}
)
```

### Installation Management

```python
# List all installations
installations = integration.get_installations()

# Get specific installation
repo_install = integration.get_repo_installation("owner", "repo")
org_install = integration.get_org_installation("org-name")
user_install = integration.get_user_installation("username")
app_install = integration.get_app_installation(installation_id)
```

### App Information

```python
# Get authenticated app information
app = integration.get_app()
```

## Context Manager Usage

The GithubIntegration instance can be used as a context manager to automatically close connections:

```python
with GithubIntegration(auth=auth) as gi:
    # do something
    installations = gi.get_installations()
```

## Common Installation Workflows

### 1. Getting an Installation Token

```python
# First, get the installation ID
installation = integration.get_repo_installation("owner", "repo")

# Then get an access token for that installation
token = integration.get_access_token(
    installation.id,
    permissions={
        "contents": "read",
        "issues": "write",
        "pull_requests": "write"
    }
)

# Use the token to create a Github instance
gh = Github(auth=Auth.Token(token.token))
```

### 2. Managing Multiple Installations

```python
# List all installations
installations = integration.get_installations()

# Get tokens for each installation
for installation in installations:
    token = integration.get_access_token(installation.id)
    gh = Github(auth=Auth.Token(token.token))
    # Do something with this installation's token
```

## Best Practices

1. Always use the `auth` parameter with `github.Auth.AppAuth()` instead of deprecated parameters
2. Store sensitive information (private keys, tokens) securely
3. Cache installation tokens until they expire (usually 1 hour)
4. Use appropriate permission scopes when requesting tokens
5. Handle rate limits and token expiration appropriately
6. Close connections when done using context manager or `close()` method

## Error Handling

The GithubIntegration class may raise these exceptions:
- `GithubException`: Base exception class
- `BadCredentialsException`: Invalid credentials
- `RateLimitExceededException`: Rate limit exceeded
- `InvalidJwtException`: Invalid JWT token
- `InstallationNotFound`: Installation not found

Example error handling:

```python
try:
    token = integration.get_access_token(installation_id)
except GithubException as e:
    if e.status == 404:
        print("Installation not found")
    elif e.status == 401:
        print("Invalid credentials")
    else:
        print(f"Unexpected error: {e}")
