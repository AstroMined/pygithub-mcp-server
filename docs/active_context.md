# Active Context

## Current Focus
Resolving integration test failures with a focus on providing a robust test suite that properly interacts with the GitHub API. We've been addressing key issues related to timezone handling, error reporting, and test performance following our real API testing approach as outlined in ADR-002.

Our current focus is on:
1. Fixing integration test failures to ensure they are reliable and robust
2. Improving datetime handling for consistent timezone-aware operations
3. Enhancing error handling and reporting, particularly for rate limits
4. Optimizing test performance, especially for rate limit tests
5. Ensuring tests don't make assumptions about repository state
6. Maintaining and expanding our ADR-002 approach of real API testing

We've made several improvements to test coverage, fixed bugs, and enhanced error handling. Key enhancements include:

1. Fixed the handling of `None` values in the `create_tool_response` function by properly using `json.dumps(None)` to produce "null" rather than the string "None".

2. Implemented the `convert_issue_list` function in the issues converter, enhancing our ability to handle collections of issues.

3. Created comprehensive tests for converters using realistic data structures instead of mocks:
   - Implemented realistic classes in tests that match PyGithub's API
   - Created test fixtures with proper data structures for Issue, User, Label, etc.
   - Tested all edge cases without relying on mocks

4. Created integration tests following the ADR-002 approach:
   - Added client module tests using real GitHub API
   - Implemented rate limit handling tests
   - Added error handlers tests with real error conditions

## Recent Changes

- Fixed integration test failures:
  - Improved datetime handling with consistent timezone-aware operations
  - Enhanced rate limit testing with test_mode and deterministic options
  - Fixed `update_issue` function to properly handle PyGithub's edit() returning None
  - Added missing `_handle_github_exception` method to GitHubClient
  - Added missing reset_timestamp attribute to GitHubRateLimitError
  - Fixed error handling in the remove_issue_label function
  - Created comprehensive test failure resolution plan in docs/test_failure_resolution_plan.md
  - Updated pagination test to be resilient to repository state
  - Fixed rate limit handler to properly extract reset time from response headers

- Fixed rate limit test performance issues:
  - Added test_mode parameter to handle_rate_limit_with_backoff function
  - Implemented deterministic mode for backoff calculations
  - Eliminated long waits for real API rate limit reset times during testing
  - Fixed exponential backoff testing with predictable calculations

- Test Suite Robustness:
  - Modified tests to avoid making assumptions about repository state
  - Implemented more dynamic test expectations for pagination and filtering
  - Improved test reliability by focusing on behavior verification rather than strict counts
  - Added better error handling and reporting in test failures

- PyGithub Integration Lessons:
  - Discovered PyGithub's `get_issues()` doesn't directly accept per_page parameter
  - Need to handle pagination through PaginatedList objects instead
  - API behavior differs from documentation in some cases, particularly for filtering
  - Tests need to be resilient to real-world repository state

## Next Steps

1. Continue Fixing Integration Tests:
   - Fix underlying pagination implementation in list_issues
   - Address labels filtering in list_issues
   - Fix since parameter datetime handling in both list_issues and list_issue_comments
   - Run full suite to verify fixes

2. Optimize Test Performance:
   - Identify further test scenarios that could benefit from test_mode
   - Implement caching where appropriate to reduce API calls
   - Develop more efficient test pattern for common operations
   - Reduce overall test time by consolidating related tests

3. Improve Error Handling:
   - Enhance header extraction from GitHub exceptions
   - Create more detailed error messages with troubleshooting guidance
   - Add more robust handling for edge cases in rate limiting

4. Repository Management:
   - Develop strategy for test repository cleanup
   - Add script for periodic purging of old test resources
   - Implement tagging system for test resources to identify test-created items
   - Consider creating dedicated test repositories for different test domains

5. Documentation:
   - Update guides with lessons learned from testing
   - Document PyGithub integration patterns and gotchas
   - Create troubleshooting guide for common issues

## Active Decisions

1. Test Robustness Strategy:
   - Tests should be resilient to repository state variations
   - Focus on verifying behavior, not exact counts or states
   - Use dynamic assertions that adapt to actual conditions
   - Include comprehensive context in test failure messages

2. PyGithub Integration Pattern:
   - Handle pagination correctly using PaginatedList methods
   - Pass only supported parameters to PyGithub methods
   - Extract direct data when needed rather than relying on PyGithub conveniences
   - Always check documentation against actual behavior

3. Error Handling Approach:
   - Extract as much information as possible from exceptions
   - Provide clear, actionable error messages
   - Include context specific to the operation being performed
   - Follow consistent patterns across all error handling code

4. Testing Strategy:
   - Follow ADR-002's real API testing approach
   - Create isolated test resources that verify specific behaviors
   - Implement thorough cleanup to minimize repository pollution
   - Use test modes to speed up testing when possible

## Current Considerations

1. Rate Limit Impact:
   - Tests must be designed to minimize rate limit impact
   - Consider implementing conditional requests with ETags where appropriate
   - Optimize test sequencing to maximize parallelism while respecting rate limits
   - Add rate limit preservation measures in CI/CD pipeline

2. Test Repository Management:
   - Repository is getting cluttered with test resources
   - Need strategy for periodic cleanup without disrupting active tests
   - Consider dedicated test repositories for different testing domains
   - Implement resource tagging for easier management

3. Datetime Standardization:
   - Standardize on timezone-aware datetime objects throughout the codebase
   - Add validation to catch mixing of aware and naive datetimes
   - Document datetime handling policies for contributors
   - Create utilities to simplify correct datetime usage

4. Testing Patterns:
   - Develop standard patterns for creating, validating, and cleaning up test resources
   - Document best practices for resilient tests
   - Create helper functions for common test operations
   - Standardize test fixture organization

## Implementation Lessons

1. PyGithub Pagination:
   - PyGithub's PaginatedList doesn't directly accept per_page in get_issues()
   - Must handle pagination after getting the PaginatedList
   - Use PaginatedList methods or slicing to get specific pages
   - Example: `issues = paginated_issues.get_page(page - 1)` (0-indexed)

2. Datetime Handling:
   - Always use timezone-aware datetimes for consistency
   - Add timezone information to datetime objects with `.astimezone()`
   - Compare apples to apples: ensure all datetimes in comparisons have tz info
   - When accepting string dates, convert to datetime objects early
   - Truncate microseconds for consistency with API expectations (`.replace(microsecond=0)`)
   - Use sufficient buffer (24h+) for future date filtering tests to account for timezone handling differences
   - Store timezone-aware datetimes in all error objects that involve timestamps

3. Error Extraction:
   - GitHub exceptions contain valuable data in headers, not just the body
   - Extract rate limit information from headers when not available in the body
   - Always include multiple fallbacks for extracting error details
   - Log complete exception context for debugging

4. Test Repository Maintenance:
   - Test repository state impacts test reliability
   - Clean up test resources properly after each test
   - Use unique identifiers in test resource names
   - Don't assume clean repository state between test runs

5. Test Assumptions:
   - Don't assume empty repository or specific counts
   - Verify behavior rather than specific states
   - Add context when assertions fail to aid debugging
   - Use conditional assertions based on actual repository state

6. PyGithub Documentation vs. Reality:
   - PyGithub API doesn't always match GitHub REST API documentation
   - Some parameters must be transformed (e.g., list → comma-separated string)
   - Always verify parameter handling with simple tests
   - Document discrepancies for future reference
