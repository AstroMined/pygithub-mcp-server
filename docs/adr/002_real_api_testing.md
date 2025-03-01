# ADR 002: Real API Testing

## Status
Accepted (Updated 2/28/2025)

## Context
The server's test suite has been relying on mock fixtures that attempt to replicate GitHub API behavior. This has led to:
- 24/25 tests failing
- Complex mock implementations
- Brittle test fixtures
- Difficulty maintaining mock parity with API changes
- Significant time spent debugging mock behavior rather than actual code

Recent experience has shown that even with careful implementation, mocks often fail to accurately represent the behavior of the real GitHub API. This leads to tests that pass with mocks but fail with the real API, or vice versa, undermining confidence in the test suite.

## Decision
We will completely eliminate mock-based testing in favor of real GitHub API testing:

1. Test Philosophy:
   - Eliminate all mocking from the test suite
   - Create realistic fixtures using real schemas, converters, and operations
   - Test actual behaviors with real API interactions
   - Focus on testing behavior and outcomes rather than implementation details
   - Accept the trade-offs of real API testing (network dependency, rate limits) for the benefit of higher confidence

2. Test Organization:
   - Replace all existing mock-based tests with real API tests
   - Separate unit tests and integration tests into distinct directories
   - Mark all integration tests with @pytest.mark.integration
   - Use environment variables for test credentials
   - Organize tests by domain (issues, repositories, users)

3. Test Infrastructure:
   - Maintain a dedicated test repository rather than creating/deleting for each test run
   - Use test-specific GitHub token with appropriate permissions
   - Implement thorough cleanup mechanisms that run after each test
   - Tag all test-created resources for easy identification
   - Implement rate limit handling with exponential backoff
   - Use unique identifiers for all test resources
   - Clear setup documentation

4. Implementation Strategy:
   - Build a robust unit test suite first to ensure internal components work correctly
   - Implement integration tests that test full resource lifecycles
   - Document patterns for future additions
   - Create helper functions for common test operations

## Consequences

### Positive
- Tests verify actual API behavior with high confidence
- Complete elimination of complex mock maintenance
- Real error responses and rate limits
- Tests serve as documentation of actual API behavior
- Higher confidence in functionality and compatibility
- No time spent debugging mock behavior
- Tests that pass locally will be more likely to pass in CI
- Easier onboarding for new contributors without mock complexity

### Negative
- Requires test token and repository with appropriate permissions
- Network dependency for all tests that verify external behavior
- Rate limit considerations for test execution
- Slower test execution compared to mock-based tests
- Potential for flakiness due to network issues or API changes
- Need for robust cleanup mechanisms to prevent test pollution
- More complex CI/CD setup for handling credentials and network access

### Mitigations
- Implement robust retry mechanisms for network issues with exponential backoff
- Use test tagging to allow running unit tests separately from integration tests
- Implement thorough cleanup routines that run after each test
- Use conditional requests with ETags to reduce rate limit impact
- Implement request batching where possible to minimize API calls
- Use unique identifiers and resource tagging for reliable cleanup
- Consider caching strategies for frequently accessed data

## Implementation Plan

1. Phase 1: Infrastructure Setup
   - Create dedicated test repository and token
   - Configure environment variables for test credentials
   - Implement rate limit handling with exponential backoff
   - Set up test directory structure with unit/integration separation
   - Create test fixtures and helper functions

2. Phase 2: Core Test Patterns
   - Develop lifecycle test patterns for each resource type
   - Create setup/teardown mechanisms for test isolation
   - Implement resource tagging and cleanup
   - Document test patterns and best practices
   - Create helper functions for common test operations

3. Phase 3A: Unit Test Suite
   - Schema Validation Tests: Ensure all schema models validate correctly
   - Converter Function Tests: Verify object conversion logic works properly
   - Utility Function Tests: Test helper functions and utilities
   - Error Handling Tests: Validate error detection and formatting

3. Phase 3B: Integration Tests
   - Issue Lifecycle Tests: Test full issue lifecycle with real API
   - Repository Operation Tests: Test repository operations
   - User-Related Tests: Test user-related functionality
   - Advanced API Feature Tests: Test more complex API interactions

4. Phase 4: Optimization & Refinement
   - Implement request batching and conditional requests
   - Add caching strategies for frequently accessed data
   - Optimize test execution time
   - Enhance CI/CD integration
   - Regular maintenance of test infrastructure

## Guidance for Future Development

1. New Features:
   - Always implement real API tests for new features
   - Document any assumptions about API behavior
   - Include both success and error scenarios
   - Test full resource lifecycles

2. Bug Fixes:
   - Reproduce bugs with real API tests before fixing
   - Add regression tests using real API
   - Never add mocks to work around API behavior

3. Refactoring:
   - Use real API tests as a safety net for refactoring
   - Focus on maintaining behavior, not implementation details
   - Update tests to reflect API changes, not code changes

4. Test Organization:
   - Keep unit tests and integration tests separate
   - Organize tests by domain (issues, repositories, users)
   - Use descriptive test names that reflect the behavior being tested
   - Implement proper setup and teardown for each test

5. Test Repository Management:
   - Tag all test-created resources for easy identification
   - Clean up resources after each test
   - Use unique identifiers for test resources
   - Implement thorough cleanup mechanisms

## Directory Structure

```
tests/
├── unit/                  # Fast tests with no external dependencies
│   ├── schemas/           # Schema validation tests
│   ├── converters/        # Object conversion tests
│   └── utils/             # Utility function tests
├── integration/           # Tests that hit the GitHub API
│   ├── issues/            # Issue-related integration tests
│   ├── repositories/      # Repository-related integration tests
│   └── users/             # User-related integration tests
└── conftest.py            # Shared test fixtures and configuration
```

## References
- [PyGithub Testing Documentation](https://pygithub.readthedocs.io/en/latest/testing.html)
- [GitHub API Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [Testing Microservices: Martin Fowler](https://martinfowler.com/articles/microservice-testing/)
- [Test Doubles: Martin Fowler](https://martinfowler.com/bliki/TestDouble.html)
- [Integration Tests: Kent C. Dodds](https://kentcdodds.com/blog/write-tests)
- [Testing Without Mocks: James Shore](https://www.jamesshore.com/v2/blog/2018/testing-without-mocks)
