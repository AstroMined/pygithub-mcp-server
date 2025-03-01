# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-02-28

### Added
- Common module reorganization (ADR 005):
  - Created domain-specific directories for converters (issues, repositories, users)
  - Established dedicated modules for error handling, client management, and utilities
  - Improved code organization and maintainability
  - Standardized on PyGithub for API interactions
  - Consolidated data transformation functions into logical groups

### Changed
- Moved converter functions to domain-specific files
- Relocated error handling to dedicated modules
- Transferred GitHub client functionality to client directory
- Consolidated datetime conversion in common/datetime.py
- Enhanced separation of concerns across all modules
- Removed deprecated common module files entirely
- Updated test imports to use the new module structure
- Eliminated technical debt by removing deprecated code instead of just marking it as deprecated

## [0.3.1] - 2025-02-28

### Fixed
- Schema validation issues:
  - Added strict=True to field definitions in CreateIssueParams and GetIssueParams to prevent automatic type coercion
  - Fixed validation for empty content lists in ToolResponse
  - Improved type checking for numeric and string fields
  - Fixed test assertions for datetime comparisons
  - Addressed specific test failures in schema validation tests
  - Ensured consistent validation across all schema models

### Added
- New implementation lessons in documentation:
  - Documented Pydantic v2 type coercion behavior differences
  - Added guidance on using strict=True for field-level validation
  - Updated schema validation best practices

## [0.3.0] - 2025-02-27

### Added
- Schema reorganization (ADR 003):
  - Created dedicated schemas directory with domain-specific files
  - Separated schemas by domain: base, repositories, issues, pull_requests, search, responses
  - Implemented backward compatibility through re-exports
  - Added deprecation warnings to original types.py module
  - Established foundation for schema-first development approach

- Enhanced schema validation (ADR 004):
  - Added field validators to prevent empty strings in critical fields
  - Implemented validation for owner, repo, path, title, body, and label fields
  - Improved error messages for validation failures
  - Aligned schema validation with PyGithub expectations

- Comprehensive schema test suite:
  - Created tests for base schemas (RepositoryRef, FileContent)
  - Added tests for issue-related schemas
  - Implemented tests for response schemas
  - Ensured tests cover both valid and invalid inputs

## [Unreleased]
### Added
- Updated ADR 002 (Real API Testing):
  - Shifted focus to prioritize real API testing over mock-based testing
  - Documented challenges with maintaining complex mocks
  - Added detailed implementation plan for transitioning to real API tests
  - Added guidance for future development
  - Expanded consequences and mitigation strategies
  - Added references to testing best practices

- Real GitHub API integration testing:
  - Environment-based configuration
  - Automatic test resource cleanup
  - Rate limit protection
  - Integration test documentation
  - create_issue integration tests
  - Dedicated test infrastructure in tests/server/

### Changed
- Enhanced error handling and message formatting:
  - Added 'permission' word to permission error messages for better clarity
  - Included status code in unknown error messages for easier debugging
  - Fixed rate limit error handling in issues.py to properly propagate errors
  - Improved error message formatting across all error types
  - All error-related tests now passing

- Improved rate limit error handling:
  - Enhanced RateLimitExceededException handling in GitHubClient
  - Added proper data formatting for rate limit errors
  - Fixed mock fixtures for rate limit testing
  - Improved error message formatting with rate details
  - Added rate limit information (remaining/limit) to error messages
  - Enhanced test coverage for rate limit scenarios

### Fixed
- Rate limit test fixtures now properly mock PyGithub's exception structure
- Error handling in GitHubClient now properly formats rate limit messages
- Mock objects now correctly handle rate limit attributes
- Mock object attribute naming to match PyGithub:
  - Changed issue_number to number in mock objects
  - Updated mock object edit() method to properly update state
  - Fixed attribute access in test assertions
  - Improved test stability by aligning with PyGithub conventions

### Changed
- Improved error handling in utils.py:
  - Enhanced rate limit detection logic
  - Fixed permission error vs rate limit error classification
  - Improved error message pattern matching

### Added
- Comprehensive test suite for utils.py:
  - Increased coverage from 17% to 95%
  - Added parameter validation tests
  - Enhanced error handling tests
  - Added rate limit handling tests
  - Improved response processing tests

### Changed
- Removed test mode functionality from GitHubClient
- Simplified test environment by removing test-specific code paths
- Optimized update_issue to avoid unnecessary API calls when no changes provided

### Added
- Comprehensive test suite implementation:
  - Added pytest configuration with coverage reporting
  - Created test fixtures for GitHub objects
  - Added unit tests for error handling
  - Added unit tests for operations layer
  - Added test utilities and helper functions

### Fixed
- Mock object implementations:
  - Fixed protected attribute access in MockNamedUser (_login)
  - Fixed protected attribute access in MockIssueComment (_id)
  - Fixed protected attribute access in MockLabel (_id)
  - Fixed protected attribute access in MockMilestone (_id)
  - Fixed protected attribute access in MockRepository (_name)
  - Resolved circular dependencies between mock_repo and mock_issue fixtures
  - Improved fixture organization with autouse configuration
  - Separated object creation from configuration

### Added
  - Added pytest configuration with coverage reporting
  - Created test fixtures for GitHub objects
  - Added unit tests for error handling
  - Added unit tests for operations layer
  - Added test utilities and helper functions
- New testing documentation:
  - Added mocking_patterns.md guide for handling imported modules
  - Added detailed examples of type-safe mocking
  - Added best practices for module patching

### Changed
- Improved test mocking implementation:
  - Removed test-specific code from GitHubClient class
  - Enhanced mock classes with proper PyGithub attribute handling
  - Added _completeIfNotSet support in mock objects
  - Fixed property access patterns in mock classes
  - Improved test mode detection
- Updated project structure to include tests directory
- Enhanced documentation with testing information
- Improved mock object implementations
- Added mocking patterns to .clinerules
- Updated active_context.md with new testing insights
- Enhanced mock implementations to preserve type checking
- Fixed GitHubClient singleton implementation:
  - Added _created_via_get_instance flag for better instantiation control
  - Improved direct instantiation prevention
  - Enhanced resource type detection for repository operations
  - Fixed rate limit error handling for missing headers
  - All tests in test_github_client.py now pass

### Known Issues
- Test coverage could be improved further
- Some mock objects may need refinement

## [0.2.1] - 2025-02-22

### Added
- New documentation guides:
  - error-handling.md: Comprehensive error handling documentation
  - security.md: Security best practices and considerations
  - tool-reference.md: Detailed tool reference with examples
- Enhanced error handling with resource type detection
- Improved validation error formatting

### Changed
- Standardized error handling across all operations
- Improved error message clarity and usefulness
- Enhanced error response formatting

## [0.2.0] - 2025-02-22

### Added
- Complete set of GitHub issue operations:
  - get_issue: Get issue details
  - update_issue: Modify existing issues
  - add_issue_comment: Add comments to issues
  - list_issue_comments: List comments on an issue
  - update_issue_comment: Update existing comments
  - delete_issue_comment: Remove comments
  - add_issue_labels: Add labels to issues
  - remove_issue_label: Remove labels from issues
- Improved parameter handling for all operations using kwargs pattern
- Comprehensive docstrings and type hints for all functions
- Additional examples in README for all issue operations
- Enhanced error handling for comment operations

### Changed
- Fixed comment operations to use issue.get_comment instead of repository.get_issue_comment
- Updated parameter models to include issue_number for comment operations
- Improved error messages for invalid parameters
- Enhanced logging for better debugging
- Updated documentation with complete usage examples

### Fixed
- Comment operations now properly access comments through parent issues
- Optional parameter handling in update_issue and list_issue_comments
- Parameter validation for datetime fields

## [0.1.0] - Initial Release

### Added

### Added
- Basic GitHub MCP Server implementation
- Issue management operations
- Error handling and validation
- Documentation and setup guides
- Local development environment with UV
