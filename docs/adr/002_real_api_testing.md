# ADR 002: Real API Testing

## Status
Accepted (Updated 2/27/2025)

## Context
The server's test suite has been relying on mock fixtures that attempt to replicate GitHub API behavior. This has led to:
- 24/25 tests failing
- Complex mock implementations
- Brittle test fixtures
- Difficulty maintaining mock parity with API changes
- Significant time spent debugging mock behavior rather than actual code

Recent experience has shown that even with careful implementation, mocks often fail to accurately represent the behavior of the real GitHub API. This leads to tests that pass with mocks but fail with the real API, or vice versa, undermining confidence in the test suite.

## Decision
We will transition to real GitHub API testing as our primary testing strategy, with minimal mocking only where absolutely necessary:

1. Test Philosophy:
   - Prioritize real API testing over mock-based testing
   - Use mocks only for edge cases that cannot be reliably reproduced with the real API
   - Focus on testing behavior and outcomes rather than implementation details
   - Accept the trade-offs of real API testing (network dependency, rate limits) for the benefit of higher confidence

2. Test Organization:
   - Phase out most existing mock-based tests in favor of real API tests
   - Mark all real API tests with @pytest.mark.integration
   - Isolate integration test config to tests/server/
   - Use environment variables for test credentials

3. Test Infrastructure:
   - Dedicated test repository
   - Test-specific GitHub token
   - Automatic resource cleanup
   - Rate limit protection and backoff strategies
   - Clear setup documentation

4. Implementation Strategy:
   - Start with issue lifecycle (create → update → close) as proof of concept
   - Replace failing mock-based tests with real API tests
   - Document patterns for future additions
   - Maintain minimal mock tests only for edge cases

## Consequences

### Positive
- Tests verify actual API behavior
- Elimination of complex mock maintenance
- Real error responses and rate limits
- Tests serve as documentation
- Higher confidence in functionality
- Less time spent debugging mock behavior
- Tests that pass locally will be more likely to pass in CI

### Negative
- Requires test token and repository
- Network dependency for tests
- Rate limit considerations
- Slightly slower test execution
- Potential for flakiness due to network issues
- Need for cleanup mechanisms to prevent test pollution

### Mitigations
- Implement robust retry mechanisms for network issues
- Use test tagging to allow skipping integration tests when appropriate
- Implement thorough cleanup routines to prevent resource accumulation
- Consider caching strategies for frequently accessed data

## Implementation Plan

1. Phase 1: Infrastructure Refinement
   - Review and update environment configuration
   - Ensure test repository is properly configured
   - Implement robust token management
   - Develop rate limit handling with exponential backoff

2. Phase 2: Core Implementation
   - Replace issue lifecycle tests with real API tests
   - Implement thorough cleanup mechanisms
   - Document patterns for real API testing
   - Develop helper functions for common test operations

3. Phase 3: Comprehensive Transition
   - Systematically replace mock-based tests with real API tests
   - Identify and document any edge cases that still require mocking
   - Update documentation to reflect new testing approach
   - Train team members on new testing patterns

4. Phase 4: Optimization
   - Implement caching strategies where appropriate
   - Optimize test execution time
   - Refine CI/CD pipeline for efficient test execution
   - Regular maintenance of test infrastructure

## Guidance for Future Development

1. New Features:
   - Always implement real API tests for new features
   - Document any assumptions about API behavior
   - Include both success and error scenarios

2. Bug Fixes:
   - Reproduce bugs with real API tests before fixing
   - Add regression tests using real API
   - Avoid adding new mocks

3. Refactoring:
   - Use real API tests as a safety net for refactoring
   - Focus on maintaining behavior, not implementation details
   - Update tests to reflect API changes, not code changes

4. Mocking Guidelines:
   - Only mock when absolutely necessary (e.g., rate limit errors, rare error conditions)
   - Keep mocks as simple as possible
   - Document why mocking is necessary for each case
   - Regularly review mocked tests to see if they can be replaced with real API tests

## References
- [PyGithub Testing Documentation](https://pygithub.readthedocs.io/en/latest/testing.html)
- [GitHub API Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [Testing Microservices: Martin Fowler](https://martinfowler.com/articles/microservice-testing/)
- [Test Doubles: Martin Fowler](https://martinfowler.com/bliki/TestDouble.html)
