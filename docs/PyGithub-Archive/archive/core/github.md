# Github Main Class

The `Github` class is the primary entry point for the PyGithub library. It provides access to all GitHub API v3 functionality.

## Constructor

```python
Github(
    login_or_token: str | None = None,
    password: str | None = None,
    jwt: str | None = None,
    app_auth: AppAuthentication | None = None,
    base_url: str = 'https://api.github.com',
    timeout: int = 15,
    user_agent: str = 'PyGithub/Python',
    per_page: int = 30,
    verify: bool | str = True,
    retry: int | Retry | None = GithubRetry(total=10),
    pool_size: int | None = None,
    seconds_between_requests: float | None = 0.25,
    seconds_between_writes: float | None = 1.0,
    auth: github.Auth.Auth | None = None,
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
- **login_or_token**: Use `auth=github.Auth.Login()` or `auth=github.Auth.Token()` instead
- **password**: Use `auth=github.Auth.Login()` instead
- **jwt**: Use `auth=github.Auth.AppAuth()` instead
- **app_auth**: Use `auth=github.Auth.AppInstallationAuth()` instead

## Core Methods

### Authentication & Rate Limiting

```python
# Get rate limit status
rate_limit = g.get_rate_limit()

# Get remaining/limit as tuple
remaining, limit = g.rate_limiting

# Get rate limit reset time
reset_time = g.rate_limiting_resettime

# Get OAuth scopes
scopes = g.oauth_scopes
```

### User Operations

```python
# Get authenticated user
user = g.get_user()

# Get user by username
user = g.get_user("username")

# Get user by ID
user = g.get_user_by_id(123456)

# List all users
users = g.get_users()
```

### Repository Operations

```python
# Get repository by full name
repo = g.get_repo("owner/repo")

# Get repository by ID
repo = g.get_repo(123456)

# List public repositories
repos = g.get_repos()

# Search repositories
repos = g.search_repositories("language:python stars:>1000")
```

### Organization Operations

```python
# Get organization
org = g.get_organization("org-name")

# List organizations
orgs = g.get_organizations()
```

### Search Operations

```python
# Search repositories
repos = g.search_repositories("python", sort="stars")

# Search users
users = g.search_users("location:london", sort="followers")

# Search issues
issues = g.search_issues("is:open label:bug", sort="created")

# Search code
code = g.search_code("filename:README.md")

# Search commits
commits = g.search_commits("fix bug", sort="author-date")

# Search topics
topics = g.search_topics("machine-learning")
```

### Content Operations

```python
# Render markdown
html = g.render_markdown("# Hello World")

# Get gitignore templates
templates = g.get_gitignore_templates()
template = g.get_gitignore_template("Python")

# Get emojis
emojis = g.get_emojis()
```

### Webhook Operations

```python
# Get webhook
hook = g.get_hook("web")

# List webhooks
hooks = g.get_hooks()

# Get webhook delivery
delivery = g.get_hook_delivery(hook_id, delivery_id)

# List webhook deliveries
deliveries = g.get_hook_deliveries(hook_id)
```

## Context Manager Usage

The Github instance can be used as a context manager to automatically close connections:

```python
with Github(auth=auth) as gh:
    # do something
    repo = gh.get_repo("owner/repo")
```

## Best Practices

1. Always use the `auth` parameter for authentication instead of deprecated parameters
2. Monitor rate limits using `get_rate_limit()`
3. Use appropriate delays between requests to avoid hitting rate limits
4. Enable retries for better reliability
5. Use lazy loading for better performance when dealing with large datasets
6. Close connections when done using context manager or `close()` method

## Error Handling

The Github class will raise exceptions for various error conditions:
- `GithubException`: Base exception class
- `BadCredentialsException`: Authentication failure
- `RateLimitExceededException`: Rate limit exceeded
- `BadAttributeException`: Invalid parameter values
- `TwoFactorException`: 2FA required
- `BadUserAgentException`: Invalid user agent

Always wrap API calls in appropriate try/except blocks to handle these exceptions.
