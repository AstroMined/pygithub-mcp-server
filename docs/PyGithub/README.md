# PyGithub Documentation

This documentation provides comprehensive coverage of the PyGithub library, focusing on the most commonly used objects and operations for GitHub automation.

## Documentation Structure

```
docs/PyGithub/
├── README.md               # This file
├── api/                    # API documentation
│   ├── index.md           # API overview and navigation
│   └── objects/           # Object-specific documentation
│       ├── core/          # Core GitHub objects
│       │   ├── Repository.md
│       │   └── Branch.md
│       ├── issues/        # Issue tracking
│       │   ├── Issue.md
│       │   └── Milestone.md
│       ├── projects/      # Project management
│       │   └── Project.md
│       └── pulls/         # Code review
│           └── PullRequest.md
```

## Getting Started

### Installation

```bash
pip install PyGithub
```

### Basic Usage

```python
from github import Github

# Create a GitHub instance
g = Github("your-access-token")

# Get a repository
repo = g.get_repo("owner/repo")

# Perform operations
issues = repo.get_issues(state="open")
pulls = repo.get_pulls(state="open")
branches = repo.get_branches()
```

## Documentation Overview

### [API Documentation](api/index.md)

Comprehensive documentation of PyGithub objects and their usage:

- **Core Objects**: Repository, Branch
- **Issue Tracking**: Issue, Milestone
- **Project Management**: Project, ProjectColumn
- **Code Review**: PullRequest, PullRequestReview

Each object's documentation includes:
- Properties and methods
- Code examples
- Common patterns
- Best practices
- Error handling

### Key Features

1. **Repository Management**
   - Create and configure repositories
   - Manage branches and protection rules
   - Handle collaborators and teams

2. **Issue Tracking**
   - Create and manage issues
   - Organize with labels and milestones
   - Track progress and assignments

3. **Project Management**
   - Create project boards
   - Manage columns and cards
   - Automate workflows

4. **Code Review**
   - Create and manage pull requests
   - Review code changes
   - Handle merging and branch management

## Best Practices

### Authentication

Always use tokens over username/password:

```python
# Using environment variable (recommended)
import os
g = Github(os.getenv("GITHUB_TOKEN"))

# Using personal access token directly
g = Github("your-token")
```

### Error Handling

Implement proper error handling:

```python
try:
    repo = g.get_repo("owner/repo")
except GithubException as e:
    if e.status == 404:
        print("Repository not found")
    elif e.status == 403:
        print("Permission denied")
```

### Rate Limiting

Monitor and handle rate limits:

```python
def check_rate_limit():
    rate = g.get_rate_limit()
    if rate.core.remaining < 100:
        print(f"Warning: {rate.core.remaining} calls remaining")
        print(f"Reset time: {rate.core.reset}")
```

## Common Use Cases

### Automation Scripts

```python
# Auto-label issues
def label_new_issues():
    for issue in repo.get_issues(state="open", labels=[]):
        if "bug" in issue.title.lower():
            issue.add_to_labels("bug")
        elif "feature" in issue.title.lower():
            issue.add_to_labels("enhancement")

# Auto-merge pull requests
def merge_approved_pulls():
    for pull in repo.get_pulls(state="open"):
        reviews = pull.get_reviews()
        if all(review.state == "APPROVED" for review in reviews):
            pull.merge()
```

### Project Management

```python
# Create sprint board
def create_sprint_board(sprint_number):
    board = repo.create_project(
        f"Sprint {sprint_number}",
        body="Sprint planning board"
    )
    
    # Create columns
    todo = board.create_column("To Do")
    in_progress = board.create_column("In Progress")
    review = board.create_column("Review")
    done = board.create_column("Done")
    
    return board
```

### Code Review

```python
# Review pull requests
def review_pull_request(pull):
    files = pull.get_files()
    comments = []
    
    for file in files:
        if file.filename.endswith('.py'):
            comments.append({
                'path': file.filename,
                'position': file.changes,
                'body': 'Please add docstring'
            })
    
    if comments:
        pull.create_review(
            body="Please address comments",
            event="REQUEST_CHANGES",
            comments=comments
        )
```

## Contributing

Contributions to this documentation are welcome! Please:

1. Follow the established format
2. Include practical examples
3. Test code snippets
4. Update relevant diagrams
5. Maintain cross-references

## Additional Resources

- [PyGithub Repository](https://github.com/PyGithub/PyGithub)
- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)

## License

This documentation is licensed under the MIT License. See the LICENSE file for details.
