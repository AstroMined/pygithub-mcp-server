# Active Context

## Current Focus
Improving test coverage for schema validation, with a focus on achieving 100% branch coverage for all schema files. We've successfully improved the coverage for issues.py from 90% to 100%, addressing specific branch coverage gaps in datetime validation logic.

Our current focus is on:
1. Comprehensive testing of datetime validation with various timezone formats
2. Testing edge cases in schema validation methods
3. Ensuring all branches in complex conditional logic are covered
4. Expanding test coverage to other schema files (base.py, responses.py)

We've fixed the test failures in `test_issues.py` by adding comprehensive tests for timezone formats. Specifically, we addressed branch coverage gaps in:
- The `validate_since` method for both `ListIssuesParams` and `ListIssueCommentsParams`, ensuring all timezone format variations are properly tested
- The `validate_title` method in `UpdateIssueParams` with `None` value

These improvements are part of our broader schema validation expansion effort, ensuring that our Pydantic models properly validate input data before it reaches PyGithub methods.

We're also continuing our transition to real GitHub API testing as our primary testing strategy, with minimal mocking only where absolutely necessary. This approach will:
- Verify actual API behavior with high confidence
- Eliminate complex mock maintenance
- Provide real error responses and rate limits
- Serve as API documentation
- Reduce time spent debugging mock behavior

Current test status:
- Schema validation tests: Significantly improved, with issues.py at 100% coverage
- Mock-based tests: 24/25 failing due to brittle mock implementations
- Integration tests: Initial implementation with create_issue
- Coverage gaps remain in:
  - base.py (73% coverage)
  - responses.py (78% coverage)
  - utils.py (17% coverage)
  - server.py (23% coverage)
  - operations/issues.py (71% coverage)
  - __main__.py (0% coverage)

We've updated our testing strategy (ADR 002) to prioritize real API testing over mock-based testing, focusing on behavior and outcomes rather than implementation details.

## Recent Changes
- Reorganized common module (ADR 005):
  - Created domain-specific directories for converters (issues, repositories, users)
  - Established dedicated modules for error handling, client management, and utilities
  - Implemented backward compatibility through re-exports and deprecation warnings
  - Improved code organization and maintainability
  - Standardized on PyGithub for API interactions
  - Consolidated data transformation functions into logical groups
  - Enhanced separation of concerns across all modules

- Improved schema test coverage:
  - Added comprehensive tests for datetime validation with various timezone formats
  - Added dedicated test methods for timezone format validation
  - Expanded test coverage for all schema classes in issues.py
  - Addressed specific branch coverage gap in the validate_since method
  - Improved test coverage from 90% to 99-100% for issues.py
  - Added tests for edge cases in all validation methods

- Fixed schema validation issues:
  - Added strict=True to field definitions in CreateIssueParams and GetIssueParams
  - Fixed validation for empty content lists in ToolResponse
  - Improved type checking for numeric and string fields
  - Ensured consistent validation across all schema models
  - Fixed test assertions for datetime comparisons
  
- Fixed schema test failures:
  - Fixed indentation issues in tests/schemas/test_issues.py
  - Removed redundant test file tests/schemas/test_issues_complete.py
  - Resolved NameError in test_invalid_page_values method
  - Improved test structure and organization
  - Fixed truncated test methods

- Enhanced schema validation (ADR 004):
  - Added field validators to prevent empty strings in critical fields
  - Implemented validation for owner, repo, path, title, body, and label fields
  - Improved error messages for validation failures
  - Aligned schema validation with PyGithub expectations
  - Added comprehensive tests for validation rules
  - Created ADR 004 to document validation approach

- Reorganized schema models (ADR 003):
  - Created dedicated schemas directory with domain-specific files
  - Separated schemas by domain: base, repositories, issues, pull_requests, search, responses
  - Implemented backward compatibility through re-exports
  - Added deprecation warnings to original types.py module
  - Created comprehensive test suite for schema validation
  - Improved maintainability and discoverability of schema models
  - Established foundation for schema-first development approach

- Updated ADR 002 (Real API Testing):
  - Shifted focus to prioritize real API testing over mock-based testing
  - Documented challenges with maintaining complex mocks
  - Added detailed implementation plan for transitioning to real API tests
  - Added guidance for future development
  - Expanded consequences and mitigation strategies
  - Added references to testing best practices

- Enhanced error handling and message formatting:
  - Added 'permission' word to permission error messages for clarity
  - Included status code in unknown error messages
  - Fixed rate limit error handling in issues.py
  - Improved error message formatting across all error types
  - Enhanced test coverage for error scenarios
  - All error-related tests now passing

- Improved rate limit error handling:
  - Enhanced RateLimitExceededException handling in GitHubClient
  - Added proper data formatting for rate limit errors
  - Fixed mock fixtures for rate limit testing
  - Improved error message formatting with rate details
  - Added rate limit information to error messages
  - Enhanced test coverage for rate limit scenarios

- Removed test mode functionality:
  - Eliminated test-specific code from GitHubClient
  - Deleted test_github_client_test_mode.py
  - Simplified test environment setup
  - Optimized update_issue operation for no-change cases

- Fixed mock object implementations:
  - Added proper attribute initialization for all mock classes
  - Implemented _completeIfNotSet consistently
  - Added missing property decorators
  - Fixed protected attribute access (_login, _id, etc.)
  - Resolved circular dependencies in fixtures

- Improved test mocking approach:
  - Removed test-specific code from GitHubClient
  - Enhanced mock classes with proper attribute initialization
  - Added _completeIfNotSet implementation for mock objects
  - Fixed property access in mock classes
  - Improved test mode detection and handling

- Fixed failing tests in GitHubClient implementation:
  - Improved singleton pattern to properly prevent direct instantiation
  - Added _created_via_get_instance flag for robust instantiation control
  - Enhanced resource type detection for repository operations
  - Fixed rate limit error handling for missing headers
  - All tests in test_github_client.py now pass

- Implemented comprehensive test suite:
  - Set up pytest configuration with coverage reporting
  - Created test fixtures for GitHub objects
  - Added unit tests for error handling
  - Added unit tests for operations layer
  - Added test utilities and helper functions
- Test suite revealed several issues that need attention
- Configured test coverage reporting

- Standardized error handling across all operations
- Added comprehensive error message formatting
- Created new documentation guides:
  - error-handling.md: Error types and handling patterns
  - security.md: Authentication and content security
  - tool-reference.md: Detailed tool documentation
- Improved resource type detection in error messages
- Enhanced validation error formatting

- Implemented all GitHub issue operations as MCP tools:
  - get_issue: Get details about a specific issue
  - update_issue: Update an existing issue
  - add_issue_comment: Add a comment to an issue
  - list_issue_comments: List comments on an issue
  - update_issue_comment: Update an issue comment
  - delete_issue_comment: Delete an issue comment
  - add_issue_labels: Add labels to an issue
  - remove_issue_label: Remove a label from an issue
- Added corresponding parameter models with Pydantic validation
- Implemented comprehensive error handling and logging
- Followed established patterns for tool registration and response formatting
- Renamed package from github-mcp-server to pygithub-mcp-server
- Created GitHub repository at github.com/AstroMined/pygithub-mcp-server
- Added LICENSE.md (MIT) and .gitignore
- Confirmed build works without --no-build-isolation flag
- Implemented PyGithub integration for issues module as proof of concept
- Created GitHubClient singleton for centralized PyGithub management
- Added comprehensive object conversion utilities
- Implemented proper pagination and error handling
- Updated documentation with PyGithub patterns
- Fixed list_issues parameter handling to match PyGithub requirements
- Improved error handling for PyGithub assertions

## Next Steps
1. Complete Schema Validation Fixes
   - Fix remaining test failures in schema validation
   - Update test_issues.py to properly compare datetime objects
   - Add strict=True to all fields that should reject type coercion
   - Ensure all validators are working correctly
   - Add additional tests for edge cases

2. Schema Validation Expansion
   - Review all schema models for validation opportunities
   - Add field validators for critical string fields
   - Implement enum validation for state, sort, and direction fields
   - Add range validation for numeric fields
   - Ensure consistent validation patterns across all schemas
   - Update tests to cover all validation rules

3. Phase 1: Infrastructure Refinement
   - Review and update environment configuration
   - Ensure test repository is properly configured
   - Implement robust token management
   - Develop rate limit handling with exponential backoff

4. Phase 2: Core Implementation
   - Replace issue lifecycle tests with real API tests
   - Implement thorough cleanup mechanisms
   - Document patterns for real API testing
   - Develop helper functions for common test operations

5. Phase 3: Comprehensive Transition
   - Systematically replace mock-based tests with real API tests
   - Identify and document any edge cases that still require mocking
   - Update documentation to reflect new testing approach
   - Train team members on new testing patterns

6. Phase 4: Optimization
   - Implement caching strategies where appropriate
   - Optimize test execution time
   - Refine CI/CD pipeline for efficient test execution
   - Regular maintenance of test infrastructure

7. Phase 3: Coverage Improvements
   - Core Utilities (utils.py)
     * Parameter validation tests
     * Error handling coverage
     * Type conversion utilities
     * Target: 90%+ coverage
   
   - Issue Operations (issues.py)
     * Error scenarios
     * Resource lifecycle
     * Label management
     * Target: 95%+ coverage
   
   - Server Core (server.py)
     * Lifecycle events
     * Request/response handling
     * Tool registration
     * Target: 85%+ coverage
   
   - Entry Point (__main__.py)
     * Initialization flow
     * Argument handling
     * Target: 100% coverage

8. Testing Strategy
   - Test each tool with MCP Inspector
   - Verify with real GitHub repositories
   - Plan unit tests for operations
   - Plan integration tests with GitHub API

9. PyPI Publication
   - Verify package name availability
   - Prepare for PyPI release
   - Document installation process
   - Update badges in README.md

10. Schema Alignment
   - Update Pydantic models to match PyGithub objects
   - Document field mappings and relationships
   - Implement conversion utilities
   - Add validation for PyGithub-specific constraints

11. Client Implementation
   - Create singleton GitHubClient class
   - Implement PyGithub instance management
   - Add object conversion utilities
   - Handle pagination and rate limiting

12. Operation Refactoring
   - Convert list_issues as proof of concept
   - Document new patterns and approaches
   - Plan additional operation implementations
   - Maintain FastMCP interface stability

13. Testing Implementation
   - Set up pytest infrastructure
   - Create test fixtures and mocks
   - Implement unit tests for operations
   - Add integration tests for API calls

## Active Decisions
1. Schema Validation Approach
   - Use strict=True for fields that should reject type coercion
   - Add field-level validators for empty strings and other constraints
   - Ensure consistent validation patterns across all schemas
   - Balance between strict validation and usability

2. Schema Organization
   - Domain-specific schema files for better organization
   - Base schemas for common models (RepositoryRef, FileContent)
   - Backward compatibility through re-exports
   - Schema-first development approach for new features
   - Comprehensive validation with clear error messages

3. Testing Strategy
   - Prioritize real API testing over mock-based testing
   - Use mocks only for edge cases that cannot be reliably reproduced
   - Focus on testing behavior and outcomes rather than implementation details
   - Accept the trade-offs of real API testing for higher confidence
   - Implement thorough cleanup mechanisms to prevent test pollution

4. PyGithub Integration
   - Using singleton pattern for client management
   - Maintaining FastMCP interface stability
   - Aligning schemas with PyGithub objects
   - Leveraging PyGithub's built-in features

5. Schema Evolution
   - Moving from REST API schema to object model
   - Adding PyGithub-specific fields
   - Implementing proper type validation
   - Maintaining backward compatibility

6. Implementation Strategy
   - Starting with list_issues proof of concept
   - Phased approach to feature implementation
   - Focus on stability and reliability
   - Comprehensive documentation updates

## Current Considerations
1. Schema Validation Strategy
   - Field validators for critical string fields
   - Whitespace stripping for string validation
   - Clear error messages for validation failures
   - Consistent validation patterns across schemas
   - Balance between validation and flexibility
   - Strict type checking for fields that should reject coercion

2. Testing Transition
   - Systematically replacing mock-based tests with real API tests
   - Identifying edge cases that still require mocking
   - Implementing robust cleanup mechanisms
   - Managing rate limits in test environments
   - Handling network dependencies in CI/CD pipelines

3. Schema Migration
   - Mapping between PyGithub objects and our schemas
   - Handling new PyGithub-specific fields
   - Maintaining type safety
   - Ensuring backward compatibility

4. Testing Strategy
   - Mocking PyGithub objects
   - Testing pagination
   - Error condition coverage
   - Integration test approach

5. Feature Expansion
   - Identifying useful PyGithub features
   - Planning feature implementation order
   - Maintaining consistent patterns
   - Documentation coverage

## Implementation Lessons
1. Pydantic v2 Type Coercion
   - Pydantic v2 has different type coercion behavior than v1
   - It attempts to convert types automatically (e.g., int to str)
   - Use strict=True to prevent automatic type coercion
   - Field-level strictness is more precise than model-level
   - Test both valid and invalid types to ensure proper validation
   - Be explicit about expected behavior in tests

2. Schema Validation
   - Empty strings can cause runtime errors in PyGithub
   - Pydantic's default validation doesn't check for empty strings
   - Field validators provide clear error messages
   - Validation at schema level prevents issues at runtime
   - Consistent validation patterns improve maintainability
   - Whitespace stripping catches spaces-only inputs
   - Balance validation with backward compatibility

3. Datetime Validation
   - ISO 8601 datetime validation requires careful testing
   - Timezone handling is particularly complex and error-prone
   - Test various timezone formats (Z, +00:00, -05:00, -0500)
   - Test edge cases like missing timezone, invalid timezone format
   - Ensure validation logic handles all branches in conditional statements
   - Negative timezone offsets need specific test cases
   - Python's datetime.fromisoformat() has specific format requirements

3. Testing Strategy
   - Real API testing provides higher confidence than mock-based testing
   - Mocks often fail to accurately represent API behavior
   - Time spent debugging mock behavior could be better spent on real tests
   - Focus on behavior and outcomes rather than implementation details
   - Implement thorough cleanup to prevent test pollution
   - Use test tagging to allow skipping integration tests when appropriate

4. Error Message Formatting
   - Include descriptive words in error messages (e.g., 'permission' in permission errors)
   - Add technical details like status codes for debugging
   - Format messages consistently across error types
   - Consider both user experience and debugging needs
   - Test error message content explicitly
   - Ensure error messages are actionable

5. Rate Limit Error Handling
   - Properly mock PyGithub's RateLimitExceededException structure
   - Include rate details (remaining/limit) in error messages
   - Handle missing rate attributes defensively
   - Format reset time consistently
   - Test both presence and absence of rate information
   - Consider user experience in error message formatting

6. Test Coverage Strategy
   - Focus on core utilities first to establish patterns
   - Build test coverage incrementally and systematically
   - Maintain existing test stability while expanding coverage
   - Use pytest.parametrize for comprehensive validation testing
   - Follow established mocking patterns from mocking_patterns.md
   - Balance between test coverage and maintainability

7. Production Code Purity
   - Avoid test-specific code paths in production code
   - Use proper mocking instead of test mode flags
   - Keep production code focused on real use cases
   - Maintain clear separation between test and production code

8. Operation Optimization
   - Check for no-op cases early
   - Avoid unnecessary API calls
   - Return early when no changes needed
   - Balance between fresh data and efficiency

9. Mock Object Design
  - Initialize all required attributes in __init__
  - Implement _completeIfNotSet for PyGithub compatibility
  - Use property decorators consistently
  - Handle lazy loading patterns properly
  - Keep mock classes focused on test requirements
  - Initialize protected attributes (_id, _login, etc.)
  - Follow PyGithub's attribute access patterns
  - Break circular dependencies in fixtures
  - Use autouse fixtures for configuration
  - Separate object creation from configuration

10. Singleton Pattern Testing
   - Use dedicated flag for instantiation control
   - Don't rely solely on instance state
   - Reset all singleton state between tests
   - Consider test fixture impact on patterns
   - Document singleton testing approach

11. Error Handling Patterns
   - Handle optional datetime fields defensively
   - Use clear placeholder text for missing values
   - Consider edge cases in error formatting
   - Test both presence and absence of optional data
   - Document expected behavior for missing fields

12. Testing Strategy
   - Comprehensive test suite is essential
   - Mocking GitHub objects requires careful attention
   - Test fixtures improve test maintainability
   - Coverage reporting helps identify gaps
   - Unit tests reveal design issues early
   - Mock data should match real API responses
   - Patch imported modules at point of use, not globally
   - Preserve type checking when mocking external libraries
   - Consider module namespace binding when patching
   - Use Mock(spec=...) to maintain type safety
   - Create consistent mock instances for tracking calls
   - Balance realistic behavior with test isolation

13. Error Handling
   - Standardized error handling improves maintainability
   - Clear error messages help with debugging
   - Resource type detection provides better context
   - Validation errors should be actionable
   - Consistent patterns across operations
   - Security implications must be considered

14. Documentation
   - Comprehensive guides improve usability
   - Security considerations must be documented
   - Examples help clarify usage patterns
   - Tool reference must be detailed
   - Error handling deserves special attention

15. Project Structure
   - Singleton pattern benefits for client management
   - Clear separation of concerns in operations
   - Importance of schema documentation
   - Value of phased implementation
   - Match library requirements for parameter handling
   - Build isolation works fine without flags
   - Package naming important for PyPI publication

16. PyGithub Integration
   - Follow library examples for parameter patterns
   - Handle assertions properly
   - Use simpler parameter passing when possible
   - Validate parameters before API calls
   - Build kwargs dynamically for optional parameters
   - Only include non-None values in method calls
   - Convert primitive types to PyGithub objects
   - Handle object conversion errors explicitly

17. Environment Setup
   - PyGithub dependency management
   - Token-based authentication remains unchanged
   - Testing infrastructure needs
   - Documentation importance

18. Server Operation
   - FastMCP interface stability
   - Error handling improvements
   - Rate limiting benefits
   - Object model advantages

19. Test File Management
   - Avoid duplicate test files with similar names
   - Ensure test files are complete and properly formatted
   - Remove redundant test files to prevent confusion
   - Maintain consistent test structure across files
   - Fix indentation issues promptly to prevent syntax errors
   - Complete all test methods properly to avoid runtime errors

20. Module Organization Patterns
   - Domain-based decomposition improves maintainability
   - Re-exports with deprecation warnings ensure backward compatibility
   - Clear separation of concerns reduces code complexity
   - Consistent directory structures improve discoverability
   - Logical grouping of related functionality enhances readability
   - Deprecation warnings help guide users to new APIs
   - Granular modules are easier to test and maintain
   - Consistent naming conventions improve navigation

## Progress Tracking

### Completed
- Renamed package to pygithub-mcp-server
- Created and configured GitHub repository
- Added LICENSE.md and .gitignore
- Created ADR for PyGithub integration
- Designed high-level architecture
- Planned implementation phases
- Documented technical decisions
- Implemented GitHubClient singleton
- Created object conversion utilities
- Refactored issues module to use PyGithub
- Added PyGithub patterns to documentation

### In Progress
- Schema validation fixes for test failures
- Schema validation expansion
- Testing strategy development
- Documentation updates
- Schema migration for remaining modules
- Operation refactoring planning

### Recent Fixes
- Added strict=True to field definitions in CreateIssueParams and GetIssueParams
- Fixed validation for empty content lists in ToolResponse
- Fixed issue attribute name mismatch:
  - Changed issue_number access from issue.issue_number to issue.number in converters.py
  - Updated test_convert_issue to match our schema's issue_number field
  - Resolved AttributeError in list_issues operation
  - Aligned mock object attributes with PyGithub:
    - Changed issue_number to number in mock objects
    - Fixed mock object edit() method to properly update state
    - Updated test assertions to use correct attribute names

### Upcoming
- Fix remaining test failures in schema validation
- Expand schema validation to all models
- Refactor remaining operations to use PyGithub
- Expand test suite with PyGithub mocks
- Add integration tests
- Implement advanced PyGithub features
