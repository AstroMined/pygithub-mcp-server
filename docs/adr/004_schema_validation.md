# ADR 004: Enhanced Schema Validation

## Status

Accepted

## Context

During the reorganization of our schema models, we identified a potential issue with the validation of string fields. The original Pydantic models allowed empty strings for fields like `owner`, `repo`, `title`, `body`, and `label`, which could lead to runtime errors when these values are passed to PyGithub methods.

PyGithub expects non-empty strings for these fields, and passing empty strings could result in:

1. Malformed API requests (e.g., `owner/` or `/repo` instead of `owner/repo`)
2. Validation errors from the GitHub API
3. Unexpected behavior in PyGithub methods

While Pydantic's default validation ensures that required string fields are present, it does not validate that they contain non-empty values.

## Decision

We have decided to enhance our schema validation by adding custom field validators that check for empty strings in critical fields. Specifically:

1. Add `field_validator` decorators to validate that string fields contain non-whitespace characters
2. Implement validation for:
   - `owner` and `repo` in `RepositoryRef`
   - `path` in `FileContent`
   - `title` in `CreateIssueParams`
   - `body` in `IssueCommentParams` and `UpdateIssueCommentParams`
   - `label` in `RemoveIssueLabelParams`

The validation logic checks if the string, after stripping whitespace, is empty, and raises a clear error message if it is.

## Consequences

### Positive

1. **Improved Error Messages**: Users will receive clear error messages when they provide empty strings, rather than cryptic errors from PyGithub or the GitHub API.
2. **Earlier Validation**: Errors are caught during schema validation rather than during API calls, providing faster feedback.
3. **Alignment with PyGithub**: Our schema validation now better aligns with PyGithub's expectations.
4. **Consistent Behavior**: All critical string fields now have consistent validation rules.

### Negative

1. **Backward Compatibility**: Any existing code that relied on empty strings being accepted will now fail validation.
2. **Maintenance Overhead**: We need to ensure that all new schema models follow the same validation pattern.

## Implementation

The implementation uses Pydantic's `field_validator` decorator to add custom validation logic:

```python
@field_validator('owner')
@classmethod
def validate_owner(cls, v):
    """Validate that owner is not empty."""
    if not v.strip():
        raise ValueError("owner cannot be empty")
    return v
```

This pattern is applied to all critical string fields that should not be empty.

## Alternatives Considered

1. **Rely on PyGithub Validation**: We could have relied on PyGithub to validate inputs, but this would result in less clear error messages and later feedback.
2. **Use Regex Patterns**: We could have used regex patterns in the field definitions, but this would be less explicit and harder to maintain.
3. **Add Validation in Operations Layer**: We could have added validation in the operations layer, but this would duplicate logic and potentially allow invalid data to pass through the schema layer.

## References

- [Pydantic Field Validators Documentation](https://docs.pydantic.dev/latest/usage/validators/)
- [PyGithub Repository](https://github.com/PyGithub/PyGithub)
