# Milestone Object

The Milestone object represents a GitHub milestone, which is used to track progress on groups of issues and pull requests within a repository.

## Getting a Milestone

Milestones are typically obtained through a Repository object:

```python
# Get specific milestone
milestone = repo.get_milestone(number)

# Get all milestones
milestones = repo.get_milestones()

# Get milestones with filters
milestones = repo.get_milestones(
    state="open",  # or "closed"
    sort="due_date",  # or "completeness"
    direction="asc"  # or "desc"
)

# Create new milestone
milestone = repo.create_milestone(
    title="v1.0",
    state="open",
    description="First stable release",
    due_on=datetime(2024, 12, 31)
)
```

## Properties

### Basic Information
- `number`: Milestone number
- `title`: Milestone title
- `description`: Milestone description
- `state`: Milestone state ("open" or "closed")
- `due_on`: Due date for the milestone

### Progress Information
- `open_issues`: Number of open issues
- `closed_issues`: Number of closed issues
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `closed_at`: When the milestone was closed
- `url`: API URL for this milestone
- `html_url`: Web URL for this milestone

### Relationships
- `creator`: User who created the milestone
- `repository`: Parent repository

## Methods

### Basic Operations

```python
# Edit milestone
milestone.edit(
    title="Updated title",
    state="closed",  # or "open"
    description="Updated description",
    due_on=datetime(2024, 12, 31)
)

# Delete milestone
milestone.delete()

# Get associated labels
labels = milestone.get_labels()
```

## Common Patterns

### Creating Sprint Milestone

```python
# Create sprint milestone
sprint = repo.create_milestone(
    title="Sprint 23",
    description="""
## Sprint Goals
- Implement feature X
- Fix critical bugs
- Improve performance

## Dates
- Start: 2024-03-01
- End: 2024-03-15
""",
    due_on=datetime(2024, 3, 15)
)

# Add issues to sprint
for issue in repo.get_issues(state="open", labels=["sprint-ready"]):
    issue.edit(milestone=sprint)
```

### Creating Release Milestone

```python
# Create release milestone
release = repo.create_milestone(
    title="v2.0.0",
    description="""
## Release Goals
- Major feature additions
- Breaking changes
- Performance improvements

## Timeline
- Code Freeze: 2024-06-15
- Release: 2024-06-30
""",
    due_on=datetime(2024, 6, 30)
)

# Add planned features and bugs
repo.create_issue(
    title="Implement new API",
    body="Design and implement v2 API",
    milestone=release,
    labels=["feature", "breaking-change"]
)
```

### Managing Milestone Progress

```python
# Update milestone progress
milestone.edit(
    description=milestone.description + "\n\n## Progress\n- Feature X completed\n- Bug Y fixed",
)

# Close completed milestone
milestone.edit(
    state="closed",
    description=milestone.description + "\n\n## Completion\nAll goals achieved"
)

# Move incomplete issues to next milestone
next_milestone = repo.create_milestone(
    title="v2.1.0",
    description="Follow-up release"
)

for issue in repo.get_issues(milestone=milestone, state="open"):
    issue.edit(milestone=next_milestone)
```

## Error Handling

```python
try:
    milestone.edit(state="closed")
except github.GithubException as e:
    if e.status == 404:
        print("Milestone not found")
    elif e.status == 403:
        print("Permission denied")
    else:
        print(f"Error: {e.status} - {e.data}")
```

## Best Practices

1. Milestone Creation
   - Use clear, descriptive titles
   - Set realistic due dates
   - Provide detailed descriptions
   - Define clear goals and criteria
   - Consider using templates

2. Milestone Management
   - Keep descriptions up to date
   - Track progress regularly
   - Update status appropriately
   - Close completed milestones
   - Document completion status

3. Issue Organization
   - Group related issues together
   - Prioritize within milestones
   - Balance workload appropriately
   - Consider dependencies
   - Track blockers

4. Timeline Management
   - Set realistic due dates
   - Monitor progress regularly
   - Adjust dates if needed
   - Consider buffer time
   - Track delays and reasons

5. Project Planning
   - Use milestones for releases
   - Plan sprints effectively
   - Track long-term goals
   - Maintain roadmap alignment
   - Review milestone completion

## Common Use Cases

### Sprint Planning

```python
# Create sprint milestone
sprint = repo.create_milestone(
    title=f"Sprint {sprint_number}",
    description=f"""
## Sprint Goals
{sprint_goals}

## Dates
- Start: {sprint_start}
- End: {sprint_end}

## Planning Notes
- Story Points: {story_points}
- Team Capacity: {team_capacity}
- Focus Areas: {focus_areas}
""",
    due_on=sprint_end_date
)
```

### Release Planning

```python
# Create release milestone
release = repo.create_milestone(
    title=version,
    description=f"""
## Release Goals
{release_goals}

## Timeline
- Development: {dev_period}
- Testing: {test_period}
- Documentation: {doc_period}
- Release: {release_date}

## Features
{feature_list}

## Breaking Changes
{breaking_changes}
""",
    due_on=release_date
)
```

### Milestone Tracking

```python
# Get milestone progress
open_issues = len(list(repo.get_issues(milestone=milestone, state="open")))
closed_issues = len(list(repo.get_issues(milestone=milestone, state="closed")))
total_issues = open_issues + closed_issues
progress = (closed_issues / total_issues * 100) if total_issues > 0 else 0

# Update milestone description with progress
milestone.edit(
    description=f"""
{milestone.description}

## Progress Update ({datetime.now().strftime('%Y-%m-%d')})
- Completed: {closed_issues}/{total_issues} issues ({progress:.1f}%)
- Remaining: {open_issues} issues
- Status: {"On Track" if progress >= expected_progress else "Behind Schedule"}
"""
)
