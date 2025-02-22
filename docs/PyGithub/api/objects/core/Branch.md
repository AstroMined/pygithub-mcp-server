# Branch Object

The Branch object represents a Git branch in a GitHub repository and provides access to branch-related operations, with a particular focus on branch protection rules.

## Getting a Branch

Branches are typically obtained through a Repository object:

```python
# Get specific branch
branch = repo.get_branch("main")

# Get all branches
branches = repo.get_branches()
```

## Properties

- `name`: Branch name
- `commit`: Latest commit on the branch
- `protected`: Whether the branch has protection rules enabled
- `protection_url`: URL for branch protection API endpoints

## Branch Protection

### Basic Protection Management

```python
# Get branch protection settings
protection = branch.get_protection()

# Edit branch protection
branch.edit_protection(
    # Status checks
    strict=True,
    contexts=["continuous-integration"],
    
    # Review requirements
    dismiss_stale_reviews=True,
    require_code_owner_reviews=True,
    required_approving_review_count=2,
    
    # Admin enforcement
    enforce_admins=True,
    
    # Push restrictions
    user_push_restrictions=["user1", "user2"],
    team_push_restrictions=["team1", "team2"],
    
    # Branch settings
    required_linear_history=True,
    allow_force_pushes=False,
    allow_deletions=False,
    required_conversation_resolution=True,
    lock_branch=False
)

# Remove branch protection
branch.remove_protection()
```

### Status Check Protection

```python
# Get required status checks
status_checks = branch.get_required_status_checks()

# Edit required status checks
branch.edit_required_status_checks(
    strict=True,
    contexts=["ci/travis", "security/snyk"]
)

# Remove required status checks
branch.remove_required_status_checks()
```

### Pull Request Review Protection

```python
# Get pull request review requirements
review_protection = branch.get_required_pull_request_reviews()

# Edit pull request review requirements
branch.edit_required_pull_request_reviews(
    dismissal_users=["user1", "user2"],
    dismissal_teams=["team1", "team2"],
    dismiss_stale_reviews=True,
    require_code_owner_reviews=True,
    required_approving_review_count=2,
    require_last_push_approval=True
)

# Remove pull request review requirements
branch.remove_required_pull_request_reviews()
```

### Admin Enforcement

```python
# Check if admins are bound by restrictions
is_admin_enforced = branch.get_admin_enforcement()

# Enable admin enforcement
branch.set_admin_enforcement()

# Disable admin enforcement
branch.remove_admin_enforcement()
```

### Push Restrictions

```python
# Get user push restrictions
user_restrictions = branch.get_user_push_restrictions()

# Get team push restrictions
team_restrictions = branch.get_team_push_restrictions()

# Add user push restrictions
branch.add_user_push_restrictions("user1", "user2")

# Add team push restrictions
branch.add_team_push_restrictions("team1", "team2")

# Replace user push restrictions
branch.replace_user_push_restrictions("user1", "user2")

# Replace team push restrictions
branch.replace_team_push_restrictions("team1", "team2")

# Remove user push restrictions
branch.remove_user_push_restrictions("user1", "user2")

# Remove team push restrictions
branch.remove_team_push_restrictions("team1", "team2")

# Remove all push restrictions
branch.remove_push_restrictions()
```

### Required Signatures

```python
# Check if signatures are required
requires_signatures = branch.get_required_signatures()

# Require signatures
branch.add_required_signatures()

# Remove signature requirement
branch.remove_required_signatures()
```

### Branch Deletion Protection

```python
# Check if branch deletion is allowed
allows_deletion = branch.get_allow_deletions()

# Allow branch deletion
branch.set_allow_deletions()

# Prevent branch deletion
branch.remove_allow_deletions()
```

## Best Practices

1. Branch Protection
   - Enable appropriate protection rules for important branches
   - Require status checks for critical integrations
   - Set meaningful review requirements
   - Consider requiring signed commits for security

2. Access Control
   - Use team push restrictions over individual user restrictions
   - Keep admin enforcement enabled when possible
   - Regularly review and update access permissions

3. Code Review
   - Set appropriate number of required reviewers
   - Enable stale review dismissal
   - Require conversation resolution
   - Consider requiring code owner reviews

4. Status Checks
   - Enable strict status checks for important branches
   - Keep status check contexts up to date
   - Monitor status check performance

5. Error Handling
   - Handle protection rule changes carefully
   - Verify protection rules after changes
   - Consider impacts on CI/CD pipelines

## Error Handling

```python
try:
    branch.edit_protection(
        strict=True,
        contexts=["ci/travis"]
    )
except github.GithubException as e:
    if e.status == 404:
        print("Branch not found")
    elif e.status == 403:
        print("Permission denied")
    else:
        print(f"Error: {e.status} - {e.data}")
```

## Common Scenarios

### Setting up Main Branch Protection

```python
main = repo.get_branch("main")
main.edit_protection(
    # Require status checks
    strict=True,
    contexts=["ci/travis", "security/snyk"],
    
    # Require reviews
    dismiss_stale_reviews=True,
    require_code_owner_reviews=True,
    required_approving_review_count=1,
    
    # Enforce for admins
    enforce_admins=True,
    
    # Additional protections
    required_linear_history=True,
    allow_force_pushes=False,
    allow_deletions=False,
    required_conversation_resolution=True
)
```

### Setting up Development Branch Protection

```python
develop = repo.get_branch("develop")
develop.edit_protection(
    # Lighter status checks
    strict=False,
    contexts=["ci/travis"],
    
    # Basic review requirements
    dismiss_stale_reviews=False,
    required_approving_review_count=1,
    
    # More permissive settings
    enforce_admins=False,
    allow_force_pushes=True,
    required_linear_history=False
)
