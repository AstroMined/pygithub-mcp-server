# ADR 003: Schema Reorganization

## Status
Accepted

## Context
The PyGithub MCP Server currently defines all Pydantic schemas in a single `types.py` file within the `common` directory. As the project grows and plans for expansion, this monolithic approach presents several challenges:

1. **Maintainability Issues**: The file contains schemas spanning multiple domains (issues, repositories, pull requests, etc.), making it difficult to maintain and extend.

2. **Discoverability Problems**: Developers must search through a large file to find relevant schemas, reducing productivity.

3. **Coupling Concerns**: Changes to one domain's schemas risk affecting others due to their proximity in the same file.

4. **Development Process**: The current structure doesn't facilitate a "schema-first" development approach where data integrity is baked into the process from the start.

5. **Future Growth**: With plans for significant feature expansion, the current structure will become increasingly unwieldy.

The project needs a more organized and scalable approach to schema management that aligns with the single responsibility principle and facilitates future development.

## Decision
We will reorganize the schema definitions by:

1. Creating a dedicated `schemas` directory to replace schema definitions in `common/types.py`
2. Decomposing schemas into domain-specific files with single responsibilities
3. Maintaining backward compatibility through re-exports
4. Establishing a "schema-first" development process for new features

### New Directory Structure
```
src/
  pygithub_mcp_server/
    schemas/                  # New directory for all schemas
      __init__.py             # Re-exports all schemas for backward compatibility
      base.py                 # Base models used across multiple domains
      repositories.py         # Repository-related schemas
      issues.py               # Issue and issue comment related schemas
      pull_requests.py        # Pull request and PR comment schemas
      search.py               # Search-related schemas
      responses.py            # Response type schemas
```

### Schema Organization
Each schema file will focus on a specific domain:

- **base.py**: Common models like `RepositoryRef` used across domains
- **repositories.py**: Repository operations (create, search, fork, etc.)
- **issues.py**: Issue operations (create, update, list, etc.) and issue comments
- **pull_requests.py**: Pull request operations and PR comments
- **search.py**: Search operations across GitHub
- **responses.py**: Common response types and formatting

### Backward Compatibility
To maintain compatibility with existing code:
- The `__init__.py` file will re-export all schemas
- The original `types.py` will be updated to import and re-export from the new locations with deprecation warnings

## Consequences

### Positive
- **Improved Organization**: Clear separation of concerns with domain-specific files
- **Enhanced Maintainability**: Easier to update and extend schemas in isolation
- **Better Discoverability**: Developers can quickly find relevant schemas
- **Simplified Development**: New features can start with schema development first
- **Reduced Merge Conflicts**: Less chance of conflicts when multiple developers work on different domains
- **Future-Proof**: Structure scales well as new features are added
- **Documentation**: Domain organization makes it easier to document schema relationships

### Negative
- **Initial Refactoring Effort**: Requires updating imports across the codebase
- **Learning Curve**: Developers need to learn the new organization
- **Potential for Duplication**: Need to carefully manage cross-domain models
- **Migration Period**: Temporary complexity during transition

## Implementation Plan

### Phase 1: Create Schema Directory Structure
1. Create the `src/pygithub_mcp_server/schemas` directory
2. Create the initial schema files with appropriate imports
3. Set up `__init__.py` for re-exports

### Phase 2: Migrate Existing Schemas
1. Move base models to `base.py`
2. Move domain-specific schemas to their respective files
3. Ensure proper imports between schema files
4. Update docstrings and type hints

### Phase 3: Update Imports in Existing Code
1. Update imports in `server.py`
2. Update imports in operations modules
3. Update any other files that import from `types.py`
4. Run tests to verify functionality

### Phase 4: Deprecate Original types.py
1. Convert `types.py` to re-export from the new schema modules
2. Add deprecation warnings
3. Document the new schema organization
4. Update developer guidelines

## Future Schema Development Process
With this new structure in place, the process for adding new features would be:

1. Identify the domain for the new feature
2. Create or update the appropriate schema file
3. Implement the feature using the schema
4. Update tests and documentation

This approach ensures data integrity is baked into the development process from the start.

## References
- [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [Python Package Structure Best Practices](https://docs.python-guide.org/writing/structure/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
