# Milestone

Examples of working with GitHub Milestones using PyGithub.

## Get Milestone list

Get a list of milestones from a repository, filtered by state:

```python
repo = g.get_repo('PyGithub/PyGithub')
open_milestones = repo.get_milestones(state='open')
for milestone in open_milestones:
    print(milestone)

# Output:
# Milestone(number=1)
# Milestone(number=2)
```

Parameters for `get_milestones`:
- `state`: Filter milestones by state ('open', 'closed', 'all')
- `sort`: Sort milestones by ('due_on', 'completeness')
- `direction`: Sort direction ('asc' or 'desc')

## Get specific Milestone

Retrieve a specific milestone by its number:

```python
repo = g.get_repo('PyGithub/PyGithub')
repo.get_milestone(number=1)
# Output: Milestone(number=1)
```

## Create Milestone

### Basic milestone

Create a simple milestone with just a title:

```python
repo = g.get_repo('PyGithub/PyGithub')
repo.create_milestone(title='New Milestone')
# Output: Milestone(number=1)
```

### Detailed milestone

Create a milestone with additional details:

```python
repo = g.get_repo('PyGithub/PyGithub')
repo.create_milestone(
    title='New Milestone',
    state='open',
    description='Milestone description'
)
# Output: Milestone(number=1)
```

Parameters for `create_milestone`:
- `title`: The name of the milestone
- `state`: The state of the milestone ('open' or 'closed')
- `description`: A description of the milestone
- `due_on`: The milestone due date (datetime object)

## Common Operations

Milestones can be used to:
- Group related issues and pull requests
- Track progress towards a feature release or deadline
- Filter issues and pull requests in GitHub's interface
- Organize project planning and tracking

Note: Milestones are particularly useful for project management when used in combination with issues and pull requests. They help track progress towards specific goals or releases.
