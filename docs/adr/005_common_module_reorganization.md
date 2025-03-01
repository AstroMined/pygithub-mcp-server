# ADR 005: Common Module Reorganization and API Interaction Strategy

## Status
Accepted

## Context
The PyGithub MCP Server currently has a mix of direct GitHub API interactions via the `requests` library in `utils.py` alongside the PyGithub library abstraction. Additionally, data transformation functions are spread across multiple files (`converters.py` and `utils.py`) with some overlapping responsibilities. This creates several issues:

1. **Redundant API Interaction Methods**: We have two ways to interact with the GitHub API - directly via `requests` and through PyGithub.
2. **Unclear Responsibility Boundaries**: The distinction between converters and formatters is not well-defined.
3. **Monolithic Files**: Several files in the `common` directory handle multiple responsibilities.
4. **Maintenance Challenges**: The current structure makes it difficult to maintain and extend the codebase.

Following our successful schema reorganization (ADR 003), we need to address these issues to improve code organization and maintainability.

## Decision
We will:

1. **Standardize on PyGithub for API Interactions**: Eliminate redundant direct API calls using `requests` where PyGithub provides equivalent functionality.

2. **Reorganize Data Transformation Functions**:
   - Create a `converters` directory with domain-specific modules
   - Consolidate all data transformation functions (both converters and formatters) into this directory
   - Organize by transformation direction and domain

3. **Create a Minimal Utils Module**: Retain only truly general utilities that don't fit elsewhere

4. **Maintain Backward Compatibility**: Use re-exports and deprecation warnings during transition

### New Directory Structure
```
src/
  pygithub_mcp_server/
    converters/                  # All data transformations
      __init__.py                # Re-exports all converters
      issues/                    # Issue-related converters
        __init__.py              # Re-exports issue converters
        issues.py                # Issue converters
        comments.py              # Issue comment converters
      repositories/              # Repository-related converters
        __init__.py              # Re-exports repository converters
        repositories.py          # Repository converters
        contents.py              # Repository content converters
      users/                     # User-related converters
        __init__.py              # Re-exports user converters
        users.py                 # User converters
      common/                    # Common converters used across domains
        __init__.py              # Re-exports common converters
        datetime.py              # Date/time conversions
      responses.py               # Tool response formatting
      parameters.py              # Parameter formatting
    
    utils/                       # Minimal general utilities
      __init__.py                # Re-exports utilities
      environment.py             # Environment utilities
      general.py                 # General-purpose utilities
    
    errors/                      # Error handling
      __init__.py                # Re-exports errors
      exceptions.py              # Custom exceptions
      formatters.py              # Error formatting
      handlers.py                # Error handling
    
    client/                      # GitHub client
      __init__.py                # Re-exports client
      client.py                  # Core GitHub client
      rate_limit.py              # Rate limit handling
```

## Consequences

### Positive
- **Clearer Responsibility Boundaries**: Each module has a well-defined purpose
- **Reduced Redundancy**: Elimination of duplicate API interaction methods
- **Improved Maintainability**: Easier to find and update specific functionality
- **Better Testability**: More focused modules are easier to test
- **Scalability**: Structure supports future growth and feature additions
- **Consistency**: Follows the same principles as our schema reorganization

### Negative
- **Initial Refactoring Effort**: Requires updating imports and function calls
- **Learning Curve**: Developers need to learn the new organization
- **Transition Period**: Temporary complexity during migration
- **Potential for Regression**: Risk of introducing bugs during refactoring

## Implementation Plan

### Phase 1: Audit Current Usage
1. Identify which `utils.py` functions are still needed
2. Map dependencies between functions
3. Identify where PyGithub can replace direct API calls

### Phase 2: Create New Directory Structure
1. Create the new directories
2. Set up `__init__.py` files for re-exports

### Phase 3: Migrate Functions
1. Move converter functions to appropriate files
2. Move formatter functions to appropriate files
3. Consolidate overlapping functionality
4. Update function signatures and documentation

### Phase 4: Update Imports and References
1. Update imports in operations modules
2. Update any other files that import from original locations
3. Add deprecation warnings to original files
4. Run tests to verify functionality

### Phase 5: Documentation and Cleanup
1. Update developer documentation
2. Add inline documentation explaining the new structure
3. Remove redundant code after transition period

## Implementation Status

As of February 28, 2025, this ADR has been fully implemented with the following components:

1. **Directory Structure Creation**:
   - Created all directories as specified in the new directory structure
   - Set up __init__.py files with appropriate re-exports
   - Organized files according to domain and responsibility

2. **Function Migration**:
   - Moved converter functions to domain-specific files
   - Consolidated datetime conversion in common/datetime.py
   - Relocated error handling to dedicated modules
   - Transferred GitHub client functionality to client directory
   - Moved utility functions to appropriate locations

3. **Backward Compatibility**:
   - Added deprecation warnings to all original files
   - Implemented re-exports from new locations
   - Ensured all public APIs remain accessible

4. **Documentation**:
   - Updated inline documentation
   - Added explanatory comments
   - Clarified module purposes and relationships

The implementation follows the plan outlined in this ADR and maintains backward compatibility while improving code organization and maintainability.

## References
- [ADR 003: Schema Reorganization](003_schema_reorganization.md)
- [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Python Package Structure Best Practices](https://docs.python-guide.org/writing/structure/)
