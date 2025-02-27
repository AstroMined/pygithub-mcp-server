# ADR 002: Real API Testing

## Status
Accepted

## Context
The server's test suite has been relying on mock fixtures that attempt to replicate GitHub API behavior. This has led to:
- 24/25 tests failing
- Complex mock implementations
- Brittle test fixtures
- Difficulty maintaining mock parity with API changes

## Decision
We will implement real GitHub API testing alongside existing mock-based tests:

1. Test Organization:
   - Keep existing mock-based tests for quick feedback
   - Add integration tests marked with @pytest.mark.integration
   - Isolate integration test config to tests/server/
   - Use environment variables for test credentials

2. Test Infrastructure:
   - Dedicated test repository
   - Test-specific GitHub token
   - Automatic resource cleanup
   - Rate limit protection
   - Clear setup documentation

3. Implementation Strategy:
   - Start with create_issue as proof of concept
   - Gradually add integration tests for other operations
   - Document patterns for future additions
   - Maintain separation from mock-based tests

## Consequences

### Positive
- Tests verify actual API behavior
- No need to maintain complex mocks
- Real error responses and rate limits
- Tests serve as documentation
- Higher confidence in functionality

### Negative
- Requires test token and repository
- Network dependency for tests
- Rate limit considerations
- Slightly slower test execution

## Implementation Plan
1. Phase 1: Infrastructure
   - Environment configuration
   - Test repository setup
   - Token management
   - Rate limit handling

2. Phase 2: Initial Implementation
   - create_issue integration tests
   - Basic success/error scenarios
   - Resource cleanup

3. Phase 3: Expansion
   - Additional operation tests
   - Complex scenarios
   - Documentation updates

## References
- [PyGithub Testing Documentation](https://pygithub.readthedocs.io/en/latest/testing.html)
- [GitHub API Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
