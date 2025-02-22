# Repository Object

The Repository object represents a GitHub repository and provides access to all repository-related operations.

## Constructor

Repositories are typically obtained through the Github main class:

```python
# Get repository by full name
repo = g.get_repo("owner/repo")

# Get repository by ID
repo = g.get_repo(123456)
```

## Properties

- `name`: Repository name
- `full_name`: Full repository name (owner/repo)
- `description`: Repository description
- `private`: Whether the repository is private
- `fork`: Whether the repository is a fork
- `forks_count`: Number of forks
- `stargazers_count`: Number of stars
- `watchers_count`: Number of watchers
- `size`: Repository size in KB
- `default_branch`: Default branch name
- `language`: Primary repository language
- `has_issues`: Whether issues are enabled
- `has_wiki`: Whether wiki is enabled
- `has_downloads`: Whether downloads are enabled
- `archived`: Whether the repository is archived
- `disabled`: Whether the repository is disabled
- `visibility`: Repository visibility (public/private/internal)

## Methods

### Basic Operations

```python
# Edit repository settings
repo.edit(name="new-name", description="New description", private=True)

# Delete repository
repo.delete()

# Get repository topics
topics = repo.get_topics()

# Replace repository topics
repo.replace_topics(["python", "api", "github"])

# Transfer ownership
repo.transfer_ownership("new-owner")
```

### Content Operations

```python
# Get file contents
contents = repo.get_contents("path/to/file.txt")

# Get directory contents
contents = repo.get_contents("")  # Root directory

# Create file
repo.create_file(
    path="path/to/file.txt",
    message="Create file",
    content="File content"
)

# Update file
repo.update_file(
    path="path/to/file.txt",
    message="Update file",
    content="New content",
    sha=file.sha
)

# Delete file
repo.delete_file(
    path="path/to/file.txt",
    message="Delete file",
    sha=file.sha
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
```

### Commit Operations

```python
# Get commits
commits = repo.get_commits()

# Get specific commit
commit = repo.get_commit("sha")

# Compare commits
comparison = repo.compare("base", "head")

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
```

### Issue Operations

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

# Get issue
issue = repo.get_issue(number=1)

# Get labels
labels = repo.get_labels()

# Create label
label = repo.create_label(
    name="bug",
    color="f29513"
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

### Release Operations

```python
# Get releases
releases = repo.get_releases()

# Create release
release = repo.create_git_release(
    tag="v1.0",
    name="Version 1.0",
    message="Release notes"
)

# Get latest release
latest = repo.get_latest_release()
```

### Webhook Operations

```python
# Get webhooks
hooks = repo.get_hooks()

# Create webhook
hook = repo.create_hook(
    name="web",
    config={"url": "https://example.com/webhook"}
)

# Get webhook
hook = repo.get_hook(hook_id)
```

### Security Operations

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

### Collaboration

```python
# Get collaborators
collaborators = repo.get_collaborators()

# Add collaborator
repo.add_to_collaborators("username")

# Remove collaborator
repo.remove_from_collaborators("username")

# Get teams
teams = repo.get_teams()

# Get contributors
contributors = repo.get_contributors()
```

## Error Handling

Repository operations can raise various exceptions:

```python
try:
    repo = g.get_repo("owner/repo")
except github.UnknownObjectException:
    print("Repository not found")
except github.GithubException as e:
    print(f"Error: {e.status} - {e.data}")
```

## Best Practices

1. Content Operations
   - Always provide meaningful commit messages
   - Handle file encoding appropriately
   - Check file existence before operations

2. Rate Limiting
   - Monitor API rate limits
   - Use conditional requests when possible
   - Batch operations when possible

3. Security
   - Use minimal required permissions
   - Handle sensitive data carefully
   - Enable security features

4. Error Handling
   - Implement proper error handling
   - Handle rate limits gracefully
   - Log API errors appropriately
