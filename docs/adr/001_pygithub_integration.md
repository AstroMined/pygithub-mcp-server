# ADR 001: PyGithub Integration

## Status
Accepted

## Context
The GitHub MCP Server currently uses direct REST API calls via the requests library for GitHub API interactions. This approach requires manual handling of:
- HTTP requests and responses
- JSON parsing and serialization
- URL construction
- Session management
- Rate limiting
- Error handling

While functional, this leads to more complex code that needs to handle many low-level concerns. The implementation is more prone to errors and requires significant maintenance effort.

## Decision
We will refactor the codebase to use PyGithub's object-oriented interface instead of direct API calls. This change involves:

1. Core Architecture Changes:
   - Implement a singleton GitHubClient class to manage PyGithub instances
   - Replace direct HTTP calls with PyGithub object interactions
   - Update schemas to align with PyGithub's object model
   - Maintain FastMCP interface stability

2. Implementation Approach:
   - Start with list_issues as proof of concept
   - Phase implementation of additional features
   - Focus on stability and reliability
   - Comprehensive documentation updates

3. Schema Evolution:
   - Align Pydantic models with PyGithub objects
   - Add PyGithub-specific fields and relationships
   - Implement proper type validation
   - Maintain backward compatibility where possible

## Consequences

### Positive
- Reduced code complexity by leveraging PyGithub's object model
- Better error handling through PyGithub's exception system
- Improved maintainability with less boilerplate code
- Built-in support for GitHub API best practices
- Automatic rate limit handling
- Simplified authentication management
- Rich object model with proper relationships
- Better type safety and validation
- More robust pagination handling

### Negative
- Additional dependency on PyGithub
- Need to adapt to PyGithub's object model
- Potential learning curve for contributors
- May need to wrap some PyGithub functionality to maintain MCP interfaces
- Initial effort required for schema updates
- Migration period for existing functionality

## Implementation Plan

1. Phase 1: Foundation
   - Add PyGithub dependency
   - Create GitHubClient singleton
   - Update schema definitions
   - Implement conversion utilities

2. Phase 2: Proof of Concept
   - Refactor list_issues operation
   - Document new patterns
   - Validate approach
   - Gather feedback

3. Phase 3: Full Implementation
   - Refactor remaining operations
   - Update all schemas
   - Expand test coverage
   - Update documentation

4. Phase 4: Enhancement
   - Add new PyGithub capabilities
   - Optimize performance
   - Improve error handling
   - Expand feature set

## References
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
