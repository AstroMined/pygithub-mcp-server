# Project Objects

GitHub Projects provide a flexible way to organize and track work. The Project and ProjectColumn objects allow you to manage project boards programmatically.

## Project Object

The Project object represents a GitHub project board that can contain multiple columns of cards.

### Getting a Project

Projects can be created and accessed through a Repository or Organization:

```python
# Get specific project
project = repo.get_project(project_id)

# Get all repository projects
projects = repo.get_projects()

# Create new project
project = repo.create_project(
    name="Q1 Roadmap",
    body="First quarter planning board"
)
```

### Project Properties

#### Basic Information
- `name`: Project name
- `body`: Project description
- `number`: Project number
- `state`: Project state ("open" or "closed")
- `url`: API URL for this project
- `html_url`: Web URL for this project

#### Metadata
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `creator`: User who created the project
- `organization`: Organization if project belongs to one
- `private`: Whether the project is private

### Project Methods

```python
# Edit project
project.edit(
    name="Updated Project Name",
    body="Updated description",
    state="closed",  # or "open"
    organization_permission="write",  # or "read", "admin"
    private=True
)

# Delete project
project.delete()

# Get columns
columns = project.get_columns()

# Create new column
column = project.create_column("To Do")
```

## ProjectColumn Object

The ProjectColumn object represents a column in a project board that can contain cards representing issues, pull requests, or notes.

### Getting Columns

```python
# Get all columns in a project
columns = project.get_columns()

# Create new column
column = project.create_column("In Progress")
```

### Column Properties

- `name`: Column name
- `url`: API URL for this column
- `project_url`: URL of the parent project
- `cards_url`: URL for cards in this column

### Column Methods

```python
# Edit column
column.edit(name="Updated Column Name")

# Delete column
column.delete()

# Move column
column.move("first")  # or "last", or "after:column_id"

# Get cards
cards = column.get_cards()

# Create card from note
card = column.create_card(note="Task: Update documentation")

# Create card from issue or pull request
card = column.create_card(
    content_id=issue.id,
    content_type="Issue"  # or "PullRequest"
)
```

## Common Patterns

### Setting Up Project Board

```python
# Create project board
project = repo.create_project(
    name="Feature Development",
    body="""
## Project Goals
Track development of new features

## Board Structure
- Backlog: Planned features
- In Progress: Currently in development
- Review: Ready for code review
- Done: Completed features
"""
)

# Create standard columns
backlog = project.create_column("Backlog")
in_progress = project.create_column("In Progress")
review = project.create_column("Review")
done = project.create_column("Done")

# Add existing issues
for issue in repo.get_issues(labels=["feature"]):
    backlog.create_card(
        content_id=issue.id,
        content_type="Issue"
    )
```

### Managing Sprint Board

```python
# Create sprint board
sprint = repo.create_project(
    name=f"Sprint {sprint_number}",
    body=f"""
## Sprint Details
- Start: {sprint_start}
- End: {sprint_end}
- Story Points: {story_points}

## Sprint Goals
{sprint_goals}
"""
)

# Create sprint columns
todo = sprint.create_column("To Do")
in_progress = sprint.create_column("In Progress")
review = sprint.create_column("Review")
done = sprint.create_column("Done")

# Add sprint issues
for issue in repo.get_issues(milestone=sprint_milestone):
    todo.create_card(
        content_id=issue.id,
        content_type="Issue"
    )
```

### Project Automation

```python
# Move issues based on labels
for column in project.get_columns():
    for card in column.get_cards():
        if hasattr(card, "content") and card.content:
            issue = card.content
            if "urgent" in [label.name for label in issue.labels]:
                priority_column.create_card(
                    content_id=issue.id,
                    content_type="Issue"
                )
                card.delete()
```

## Best Practices

1. Project Structure
   - Use consistent column names
   - Define clear project goals
   - Document board usage
   - Consider automation needs
   - Keep boards focused

2. Column Management
   - Order columns logically
   - Limit work in progress
   - Archive completed cards
   - Review column contents
   - Update column names clearly

3. Card Organization
   - Use descriptive notes
   - Link related items
   - Add context to cards
   - Keep cards updated
   - Move cards promptly

4. Project Maintenance
   - Archive completed projects
   - Clean up old cards
   - Update project descriptions
   - Review project access
   - Document changes

5. Automation
   - Automate routine moves
   - Use labels effectively
   - Monitor card flow
   - Track project metrics
   - Review automation rules

## Error Handling

```python
try:
    project.edit(state="closed")
except github.GithubException as e:
    if e.status == 404:
        print("Project not found")
    elif e.status == 403:
        print("Permission denied")
    else:
        print(f"Error: {e.status} - {e.data}")
```

## Project Templates

### Development Board

```python
dev_board = repo.create_project(
    name="Development Tracking",
    body="""
## Board Purpose
Track development tasks and progress

## Columns
- Backlog: Upcoming work
- Ready: Ready for development
- In Progress: Currently being worked on
- Review: Ready for code review
- Testing: In QA testing
- Done: Completed work
"""
)

columns = [
    "Backlog",
    "Ready",
    "In Progress",
    "Review",
    "Testing",
    "Done"
]

for column in columns:
    dev_board.create_column(column)
```

### Bug Tracking Board

```python
bug_board = repo.create_project(
    name="Bug Tracking",
    body="""
## Board Purpose
Track and prioritize bug fixes

## Priority Levels
- Critical: System-breaking issues
- High: Major functionality issues
- Medium: Non-critical bugs
- Low: Minor issues

## Columns
- Reported: New bug reports
- Triaged: Assessed and prioritized
- In Progress: Being fixed
- Verification: Fix being verified
- Resolved: Fixed and verified
"""
)

columns = [
    "Reported",
    "Triaged",
    "In Progress",
    "Verification",
    "Resolved"
]

for column in columns:
    bug_board.create_column(column)
