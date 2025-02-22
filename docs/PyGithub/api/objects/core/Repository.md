# Repository Object

The Repository object is one of the core objects in PyGithub, representing a GitHub repository and providing access to all repository-related operations.

## Getting a Repository

```python
# From Github instance
repo = g.get_repo("owner/repo")  # By full name
repo = g.get_repo(123456)        # By ID

# From authenticated user
repo = g.get_user().get_repo("repo-name")

# From organization
repo = g.get_organization("org-name").get_repo("repo-name")
```

## Properties

### Basic Information
- `name`: Repository name
- `full_name`: Full repository name (owner/repo)
- `description`: Repository description
- `homepage`: Homepage URL
- `language`: Primary repository language
- `private`: Whether the repository is private
- `fork`: Whether the repository is a fork
- `archived`: Whether the repository is archived
- `disabled`: Whether the repository is disabled
- `visibility`: Repository visibility (public/private/internal)

### Statistics
- `size`: Repository size in KB
- `stargazers_count`: Number of stars
- `watchers_count`: Number of watchers
- `forks_count`: Number of forks
- `open_issues_count`: Number of open issues
- `subscribers_count`: Number of subscribers
- `network_count`: Number of network members

### Settings
- `default_branch`: Default branch name
- `has_issues`: Whether issues are enabled
- `has_projects`: Whether projects are enabled
- `has_wiki`: Whether wiki is enabled
- `has_downloads`: Whether downloads are enabled
- `has_discussions`: Whether discussions are enabled

### Merge Settings
- `allow_merge_commit`: Whether merge commits are allowed
- `allow_squash_merge`: Whether squash merging is allowed
- `allow_rebase_merge`: Whether rebase merging is allowed
- `allow_auto_merge`: Whether auto-merge is enabled
- `delete_branch_on_merge`: Whether to delete head branches after merging

### Timestamps
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `pushed_at`: Last push timestamp

### Related Objects
- `owner`: Repository owner (NamedUser)
- `organization`: Organization if repo belongs to one
- `parent`: Parent repository if this is a fork
- `source`: Source repository if this is a fork
- `permissions`: Current user's permissions

## Methods

### Repository Management

```python
# Edit repository settings
repo.edit(
    name="new-name",
    description="New description",
    homepage="https://example.com",
    private=True,
    has_issues=True,
    has_wiki=True,
    has_downloads=True,
    default_branch="main"
)

# Delete repository
repo.delete()

# Transfer ownership
repo.transfer_ownership("new-owner")

# Get repository topics
topics = repo.get_topics()

# Update repository topics
repo.replace_topics(["python", "api", "github"])
```

### Content Management

```python
# Get file contents
contents = repo.get_contents("path/to/file.txt")
contents = repo.get_contents("")  # Root directory

# Create file
repo.create_file(
    path="path/to/file.txt",
    message="Create file",
    content="File content",
    branch="main"  # Optional
)

# Update file
repo.update_file(
    path="path/to/file.txt",
    message="Update file",
    content="New content",
    sha=file.sha,
    branch="main"  # Optional
)

# Delete file
repo.delete_file(
    path="path/to/file.txt",
    message="Delete file",
    sha=file.sha,
    branch="main"  # Optional
)

# Get README
readme = repo.get_readme()

# Get archive link
archive_url = repo.get_archive_link("zipball", "main")
```

### Branch Operations

```python
# Get branches
branches = repo.get_branches()

# Get specific branch
branch = repo.get_branch("main")

# Rename branch
repo.rename_branch("master", "main")

# Compare branches/commits
comparison = repo.compare("base", "head")
```

### Commit Operations

```python
# Get commits
commits = repo.get_commits()

# Get specific commit
commit = repo.get_commit("sha")

# Create git blob
blob = repo.create_git_blob("content", "utf-8")

# Create git tree
tree = repo.create_git_tree([tree_element])

# Create git commit
commit = repo.create_git_commit(
    message="Commit message",
    tree=tree,
    parents=[parent_commit]
)

# Merge branches
repo.merge(
    base="main",
    head="feature",
    commit_message="Merge feature into main"
)
```

### Issue Management

```python
# Get issues
issues = repo.get_issues(state="open")

# Create issue
issue = repo.create_issue(
    title="Issue title",
    body="Issue description",
    assignee="username",
    labels=["bug"]
)

# Get specific issue
issue = repo.get_issue(number=1)

# Get labels
labels = repo.get_labels()

# Create label
label = repo.create_label(
    name="bug",
    color="f29513",
    description="Bug reports"
)
```

### Pull Request Operations

```python
# Get pull requests
pulls = repo.get_pulls(state="open")

# Create pull request
pr = repo.create_pull(
    title="Pull request title",
    body="Description",
    base="main",
    head="feature-branch"
)

# Get specific pull request
pr = repo.get_pull(number=1)
```

### Release Management

```python
# Get releases
releases = repo.get_releases()

# Create release
release = repo.create_git_release(
    tag="v1.0",
    name="Version 1.0",
    message="Release notes",
    draft=False,
    prerelease=False
)

# Get latest release
latest = repo.get_latest_release()
```

### Collaboration

```python
# Get collaborators
collaborators = repo.get_collaborators()

# Add collaborator
repo.add_to_collaborators(
    "username",
    permission="push"  # or "pull", "admin", "maintain", "triage"
)

# Remove collaborator
repo.remove_from_collaborators("username")

# Get teams
teams = repo.get_teams()

# Get contributors
contributors = repo.get_contributors()
```

### Security

```python
# Get code scanning alerts
alerts = repo.get_codescan_alerts()

# Get Dependabot alerts
alerts = repo.get_dependabot_alerts()

# Enable/disable vulnerability alerts
repo.enable_vulnerability_alert()
repo.disable_vulnerability_alert()

# Enable/disable automated security fixes
repo.enable_automated_security_fixes()
repo.disable_automated_security_fixes()
```

### Statistics and Traffic

```python
# Get statistics
contributors = repo.get_stats_contributors()
commit_activity = repo.get_stats_commit_activity()
code_frequency = repo.get_stats_code_frequency()
participation = repo.get_stats_participation()
punch_card = repo.get_stats_punch_card()

# Get traffic data
referrers = repo.get_top_referrers()
paths = repo.get_top_paths()
views = repo.get_views_traffic()
clones = repo.get_clones_traffic()
```

## Error Handling

Repository operations can raise various exceptions:

```python
try:
    repo = g.get_repo("owner/repo")
    repo.create_file(...)
except github.GithubException as e:
    if e.status == 404:
        print("Repository not found")
    elif e.status == 403:
        print("Permission denied")
    else:
        print(f"Error: {e.status} - {e.data}")
```

## Best Practices

1. Content Operations
   - Always provide meaningful commit messages
   - Handle file encoding appropriately
   - Check file existence before operations
   - Use appropriate branches for changes

2. Rate Limiting
   - Monitor API rate limits
   - Use conditional requests when possible
   - Batch operations when possible
   - Implement exponential backoff for retries

3. Security
   - Use minimal required permissions
   - Handle sensitive data carefully
   - Enable security features
   - Keep dependencies updated

4. Error Handling
   - Implement proper error handling
   - Handle rate limits gracefully
   - Log API errors appropriately
   - Use try/except blocks around API calls

5. Resource Management
   - Close connections when done
   - Use pagination efficiently
   - Clean up temporary resources
   - Monitor resource usage
