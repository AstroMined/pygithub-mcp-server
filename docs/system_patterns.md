# System Patterns

## Core Patterns

### 1. Tool Registration
```python
@server.tool()
async def tool_name(params: ToolParams) -> ToolResult:
    """Tool documentation following Google style.
    
    Args:
        params: Validated parameters for the tool
        
    Returns:
        Tool execution result
        
    Raises:
        GitHubError: If GitHub API operation fails
    """
    # Implementation
```

### 2. Schema Definition
```python
class ToolParams(BaseModel):
    """Parameters for tool operation.
    
    Attributes:
        param1: Description of first parameter
        param2: Description of second parameter
    """
    param1: str
    param2: Optional[int] = None
```

### 3. Error Handling
```python
try:
    result = await github_api_call()
except aiohttp.ClientError as e:
    raise GitHubError(f"API request failed: {e}") from e
except ValidationError as e:
    raise GitHubValidationError(str(e)) from e
```

### 4. API Response Processing
```python
async def process_github_response(response: aiohttp.ClientResponse) -> Any:
    """Process GitHub API response with proper error handling.
    
    Args:
        response: Raw API response
        
    Returns:
        Processed response data
        
    Raises:
        GitHubError: For various GitHub API errors
    """
    if response.status == 404:
        raise GitHubResourceNotFoundError(await response.text())
    # ... other status code handling
```

## Design Patterns

### 1. Repository Pattern
- Operations modules encapsulate GitHub API endpoints
- Clean separation of concerns
- Consistent error handling
- Type-safe interfaces

### 2. Factory Pattern
- Tool registration via decorators
- Automatic schema validation
- Consistent interface generation

### 3. Strategy Pattern
- Pluggable transport layer (stdio)
- Extensible error handling
- Configurable API client

## Implementation Patterns

### 1. Async Context Management
```python
class GitHubClient:
    """Async context manager for GitHub API operations."""
    
    async def __aenter__(self) -> "GitHubClient":
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, *exc_info) -> None:
        await self.session.close()
```

### 2. Schema Validation
```python
class CreateIssueParams(BaseModel):
    """Parameters for creating an issue.
    
    All fields are validated according to GitHub API requirements.
    """
    owner: str
    repo: str
    title: str
    body: Optional[str] = None
    assignees: List[str] = Field(default_factory=list)
    labels: List[str] = Field(default_factory=list)
```

### 3. Response Transformation
```python
def transform_api_response(data: Dict[str, Any]) -> ToolResult:
    """Transform GitHub API response to tool result format.
    
    Args:
        data: Raw API response data
        
    Returns:
        Formatted tool result
    """
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(data, indent=2)
            }
        ]
    }
```

## Testing Patterns

### 1. Fixture Pattern
```python
@pytest.fixture
async def github_client():
    """Provide configured GitHub client for tests."""
    async with GitHubClient() as client:
        yield client
```

### 2. Mock Pattern
```python
@pytest.mark.asyncio
async def test_create_issue(mock_github_api):
    """Test issue creation with mocked API."""
    mock_github_api.post.return_value = mock_response(
        status=201,
        payload={"number": 1, "title": "Test Issue"}
    )
    result = await create_issue(owner="test", repo="test", title="Test")
    assert result["number"] == 1
```

### 3. Integration Pattern
```python
@pytest.mark.integration
async def test_real_api_call():
    """Test against real GitHub API.
    
    Requires valid GitHub token in environment.
    """
    result = await create_repository(name="test-repo")
    assert result["name"] == "test-repo"
```

## Error Handling Patterns

### 1. Custom Exceptions
```python
class GitHubError(Exception):
    """Base exception for GitHub API errors."""
    pass

class GitHubRateLimitError(GitHubError):
    """Raised when GitHub API rate limit is exceeded."""
    def __init__(self, reset_at: datetime):
        self.reset_at = reset_at
        super().__init__(f"Rate limit exceeded, resets at {reset_at}")
```

### 2. Error Recovery
```python
async def with_retry(func: Callable, *args, max_retries: int = 3) -> Any:
    """Execute function with exponential backoff retry.
    
    Args:
        func: Async function to execute
        args: Function arguments
        max_retries: Maximum number of retry attempts
        
    Returns:
        Function result
        
    Raises:
        GitHubError: If all retries fail
    """
    for attempt in range(max_retries):
        try:
            return await func(*args)
        except GitHubError as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

## Documentation Patterns

### 1. Module Documentation
```python
"""GitHub MCP Server operations module.

This module implements GitHub API operations following the MCP protocol.
Each operation is exposed as a tool with proper validation and error handling.

Typical usage example:

    server = FastMCP("github")
    server.add_tool(create_issue)
    server.run()
"""
```

### 2. Class Documentation
```python
class GitHubClient:
    """GitHub API client with proper error handling.
    
    This class manages the HTTP session and provides methods for
    making authenticated requests to the GitHub API.
    
    Attributes:
        base_url: GitHub API base URL
        session: aiohttp ClientSession instance
    """
```

### 3. Function Documentation
```python
async def create_issue(
    owner: str,
    repo: str,
    title: str,
    **kwargs: Any
) -> Dict[str, Any]:
    """Create a new issue in a GitHub repository.
    
    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        title: Issue title
        **kwargs: Additional issue parameters (body, labels, etc.)
        
    Returns:
        Created issue data from GitHub API
        
    Raises:
        GitHubError: If issue creation fails
        GitHubValidationError: If parameters are invalid
    """
