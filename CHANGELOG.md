# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.26] - 2025-03-12

### Fixed
- Fixed `test_update_file_integration` failure:
  - Modified `create_or_update_file()` to properly distinguish between creating and updating files
  - Now uses `repository.update_file()` when a SHA is provided (for updates)
  - Continues to use `repository.create_file()` when no SHA is provided (for new files)
- Fixed `test_push_files_error_handling` failure:
  - Added proper content validation to the `push_files()` function
  - Implemented early validation for empty file content before attempting GitHub API calls
  - Improved error handling with explicit GitHubError for invalid content
- Enhanced defensive coding practices for the repository operation module:
  - Added input validation before making API calls
  - Improved error propagation from PyGithub to GitHubError instances

## [0.5.25] - 2025-03-12

### Added
- Created comprehensive test migration plan to replace brittle mocked unit tests with integration tests:
  - Developed docs/test_migration_plan.md with detailed migration approach
  - Created specialized coverage analysis tool in scripts/coverage/test_coverage_analyzer.py
  - Implemented initial integration tests following ADR-002 principles:
    - Added test_files_operations_integration.py for file operations
    - Created test_branch_operations_integration.py for branch operations
  - Established standard patterns for integration test development
  - Documented risks and mitigation strategies for the migration process

### Changed
- Enhanced testing strategy to follow ADR-002 more consistently:
  - Moved away from brittle mock-based testing approach
  - Standardized on real API testing with robust fixtures and cleanup
  - Established test patterns for future development
  - Updated Memory Bank documents to reflect new testing approach
  - Set clear priorities and migration path for test improvements

## [0.5.24] - 2025-03-11

### Added
- Added robust error handling for GitHub API responses in repository operations
- Implemented defensive coding practices for handling variations in API response structures
- Added detailed logging of API response structures for better debugging
- Created comprehensive integration tests for error cases in repository tools

### Fixed
- Fixed bug in `create_or_update_file` where commit message couldn't be accessed correctly
- Fixed potential NoneType attribute errors when processing GitHub API responses
- Improved robustness of `push_files` operation with better error handling
- Enhanced error extraction from GitHub API responses with graceful fallbacks

## [0.5.23] - 2025-03-09

### Added
- Added Jinja2 to test dependencies to support HTML coverage report generation

### Fixed
- Fixed coverage analysis tool accuracy issue:
  - Improved test grouping logic to handle nested directory structures properly
  - Added support for deeper test paths like `tests/unit/schemas/repositories/`
  - Fixed grouping logic to use full path for module keys
  - Created fallback group for tests that don't match the expected structure
  - Added diagnostic output to show test grouping information
  - Improved test collection consistency to include all tests

## [0.5.22] - 2025-03-09

### Added
- Completely refactored coverage analysis tool into a proper Python package:
  - Reorganized analyze_coverage.py into scripts/coverage/ package
  - Created modular components with dedicated responsibilities:
    - models.py: Data classes for coverage information
    - runner.py: Test execution and collection
    - parser.py: Coverage output parsing
    - reports.py: Report generation (HTML, JSON, XML)
    - cli.py: Command-line interface
  - Implemented proper Python package structure
  - Added direct module execution via __main__.py
  - Created comprehensive package exports in __init__.py

### Changed
- Enhanced coverage analysis architecture:
  - Separated concerns with dedicated modules
  - Improved object model for coverage data
  - Created cleaner interfaces between components
  - Removed redundant duplicate code
  - Enhanced error handling and reporting
  - Fixed --run-integration flag handling in test collection
  - Improved maintainability with modular design

### Fixed
- Fixed redundant --run-integration flag in test collection command

## [0.5.21] - 2025-03-09

### Added
- Improved analyze_coverage.py script to better support test execution:
  - Fixed test collection and execution for both unit and integration tests
  - Simplified test execution by running all tests at once instead of module-by-module
  - Enhanced debugging output for test execution commands
  - Added elapsed time reporting for better visibility into test performance
  - Improved failure parsing and reporting
  - Enhanced script reliability by removing complex module-level test collection

### Changed
- Modified test execution approach for improved reliability:
  - Replaced module-by-module approach with a more reliable full test execution
  - Added better debug logging for test commands and collection
  - Enhanced handling of test failures for more detailed reporting
  - Improved test execution with better parameter handling
  - Standardized on a simpler and more reliable test execution pattern

## [0.5.20] - 2025-03-08

### Changed
- Improved coverage reporting workflow:
  - Removed redundant HTML coverage reporting from pytest-cov configuration
  - Consolidated all coverage reporting through the analyze_coverage.py script
  - Eliminated duplication between pytest-cov HTML reports and analyzer reports
  - Enhanced documentation for viewing and using coverage reports
- Documentation improvements:
  - Added "Viewing Generated Reports" section to scripts/README.md with clear instructions 
  - Enhanced test_improvement_plan.md with comprehensive coverage analysis workflow
  - Added step-by-step guidance for using reports to improve coverage
  - Provided examples of coverage report usage patterns
  - Documented browser-based report viewing without web server requirements

## [0.5.19] - 2025-03-08

### Added
- Implemented comprehensive test infrastructure:
  - Created `scripts/analyze_coverage.py` to identify high-priority modules for testing
  - Developed `scripts/generate_tool_tests.py` for generating standardized tests
  - Added test templates that follow ADR-002 principles with dataclasses instead of mocks
  - Created detailed HTML and JSON coverage reports with module prioritization
  - Implemented CLI argument support for including integration tests in coverage analysis
- Enhanced test improvement plan with:
  - Comprehensive coverage analysis for all modules
  - Detailed implementation strategies for priority modules
  - Standardized test patterns using dataclasses instead of mocks
  - Templates for unit and integration tests following ADR-002
  - Implementation timeline and completion criteria

### Changed
- Improved development workflow with:
  - Developer-friendly colored console output for coverage reports
  - Interactive HTML reports for exploring test coverage gaps
  - Support for automatically generating both unit and integration tests
  - Better visibility into which code paths need testing

## [0.5.18] - 2025-03-07

### Added
- Enhanced datetime testing for all edge cases:
  - Added tests for timezone-naive datetime handling
  - Created tests for date-only formats
  - Added tests specifically for ensure_utc_datetime function
  - Improved test coverage for with_utc_datetimes decorator

### Fixed
- Fixed TestGitHubClient warning by prefixing class with underscore and using proper fixture
- Updated datetime testing to match actual function behavior rather than assumed behavior
- Clarified the difference between convert_iso_string_to_datetime and ensure_utc_datetime
- Improved understanding of timezone handling in the datetime conversion utilities

### Changed
- Improved test clarity with detailed docstrings explaining expected behavior
- Enhanced test coverage by adding separate test cases for each behavior variant
- Added proper assertions to clarify the expected behavior of datetime functions

## [0.5.17] - 2025-03-07

### Added
- Created comprehensive test improvement plan in `docs/test_improvement_plan.md`
- Developed detailed guidelines for integration tests in `tests/integration/README.md`
- Implemented robust `test_cleanup` fixture with proper resource tracking
- Added standardized `with_retry` mechanism for all GitHub API calls

### Changed
- Standardized integration test fixtures (test_owner, test_repo_name, unique_id)
- Updated environment variable handling in tests to use early loading approach
- Improved error handling in tests to use string matching instead of status code
- Fixed TestGitHubClient warning by replacing dataclass with regular class

### Fixed
- Resolved skipped repository integration tests by standardizing environment variable handling
- Fixed inconsistent fixture usage across integration tests
- Improved test retry logic for rate limit handling
- Enhanced error message checking in tests for better reliability

## [0.5.16] - 2025-03-07

### Changed
- Enhanced repository schema validation with strict mode and field validators
- Added schema validators for path, branch, and other critical string fields
- Updated system_patterns.md to include maintainable test strategies section
- Improved documentation on matching mock function signatures to real implementations

### Fixed
- Fixed DEFAULT_CONFIG usage in configuration tests
- Made tests more maintainable by using dynamic config validation instead of hardcoded values
- Updated GitHubError constructor pattern in .clinerules documentation
- Fixed repository tools tests to match operation function signatures
- Eliminated all test failures with clean test suite

## [0.5.15] - 2025-03-07

### Added
- Implemented Repository Tools Group (ADR-006):
  - Created operations/repositories.py with comprehensive repository operations
  - Implemented tools/repositories/ module following modular architecture
  - Added support for repository management, file operations, and branch operations
  - Created extensive unit tests using dataclasses instead of mocks (ADR-002)
  - Added safe integration tests for read operations
- Enhanced test suite:
  - Added schema validation tests for repository-related schemas
  - Created unit tests for repository operations using dataclasses
  - Implemented tool tests with proper error handling scenarios

## [0.5.14] - 2025-03-05

### Changed
- Updated test framework to fully align with ADR-007 (Pydantic-First Architecture):
  - Modified parameter validation tests to expect ValidationError directly from Pydantic
  - Updated test assertions to check for appropriate Pydantic validation error messages
  - Improved test reliability by matching exception types with actual implementation behavior
  - Completed test alignment with the Pydantic-First Architecture principles

### Fixed
- Fixed integration test failures in parameter validation tests:
  - Fixed test_list_issues_invalid_state and similar validation tests
  - Updated expected error assertions in all validation tests
  - Improved error message testing to match Pydantic's actual error format
  - Enhanced test maintainability by removing unnecessary error conversion

## [0.5.13] - 2025-03-05

### Added
- Implemented robust pagination utility:
  - Created unified pagination approach in converters/common/pagination.py
  - Added get_paginated_items and get_paginated_slice functions for safe PaginatedList handling
  - Implemented comprehensive error handling for index errors and empty results
  - Created unit tests using dataclasses instead of mocks following ADR-002
  - Added integration tests using real GitHub API
  - Made list_issues and list_issue_comments use the pagination utility consistently

### Changed
- Improved test organization:
  - Fixed Python module name collisions between unit and integration test files
  - Renamed test files to prevent import conflicts (test_pagination_unit.py and test_pagination_integration.py)
  - Replaced mock-based testing with dataclass fixtures for cleaner, type-safe tests
  - Enhanced test maintenance by eliminating unittest.mock dependencies
  - Enhanced error handling for PageinatedList edge cases
  - Improved consistency in API pagination approach across operations

## [0.5.12] - 2025-03-05

### Fixed
- Resolved issues with tests hanging on large repositories:
  - Fixed tests that were failing when accessing repositories with many issues (481+ closed issues)
  - Added pagination parameters (per_page and page) to all list_issues calls in tests
  - Improved test reliability and performance with repositories of any size
  - Enhanced test lifecycle management to avoid exhaustive data retrieval

### Added
- New test best practices:
  - Added documentation on pagination best practices in testing_strategy.md
  - Created guidelines for handling large data sets in tests
  - Updated implementation_status.md with lessons learned about GitHub API pagination
  - Added examples of proper pagination parameter usage in tests

## [0.5.11] - 2025-03-05

### Added
- Implemented ADR-007 (Pydantic-First Architecture):
  - Refactored all issue operations to accept Pydantic models directly
  - Updated all issue tools to pass models directly to operations
  - Leveraged Pydantic's built-in validation instead of custom decorators
  - Simplified error handling across all layers
  - Updated ADR-007 documentation to reflect implementation discoveries
  - Streamlined data flow between all layers with improved type safety

### Changed
- Improved architecture by removing unnecessary validation decorators
- Simplified code by leveraging Pydantic's built-in validation capabilities
- Enhanced type safety throughout the issue operations and tools
- Reduced code duplication by eliminating parameter unpacking/repacking

## [0.5.10] - 2025-03-04

### Added
- Documentation and architecture improvements:
  - Created ADR-007 for Pydantic-First Architecture
  - Updated system_patterns.md with Pydantic-First implementation patterns
  - Added new section on validation error handling
  - Enhanced documentation of data flow between layers
  - Improved system diagrams showing architecture

## [0.5.9] - 2025-03-04

### Fixed
- Resolved remaining test failures in GitHub issue tools:
  - Fixed create_issue parameter validation to properly handle missing required fields
  - Improved empty string handling in update_issue for body parameter
  - Enhanced pagination in list_issue_comments and list_issues functions
  - Updated error handling in remove_nonexistent_label while maintaining descriptive messages
  - Fixed tool parameter validation and error propagation throughout tools

### Changed
- Improved test assertions to accept more user-friendly error message formats
- Enhanced error handling philosophy to prioritize descriptive error messages
- Completed all test failure resolutions from the test failure resolution plan

## [0.5.8] - 2025-03-03

### Added
- Comprehensive test coverage improvements:
  - Added integration tests for GitHub issue tools error cases
  - Created unit tests for server initialization and configuration
  - Expanded test coverage for rate limit handling
  - Added parameter validation tests for operations/issues.py
  - Implemented tests for main module without using mocks
  - Created tests for repository converters with dataclasses instead of mocks

### Changed
- Improved unit testing approach:
  - Used dataclasses to create test objects instead of unittest.mock
  - Leveraged pytest fixtures for test data preparation
  - Implemented context managers for test environment control
  - Enhanced test infrastructure for GitHub API integration testing
  - Updated test organization for better maintainability
  - Focused on testing behaviors rather than implementation details

### Documentation
- Enhanced active_context.md with improved testing strategies
- Updated progress.md with completed test coverage items
- Added new implementation lessons for unit testing without mocks
- Added insights about using dataclasses for cleaner, type-safe tests

## [0.5.6] - 2025-03-02

### Added
- Modular Tool Architecture (ADR-006):
  - Implemented configurable tool architecture with selective tool group enabling
  - Created dedicated `config/` package with flexible configuration system
  - Implemented decorator-based tool registration in `tools/` package
  - Added support for configuration via file or environment variables
  - Created comprehensive testing strategy for modular architecture
  - Added example configuration file (pygithub_mcp_config.json.example)
  - Added detailed documentation in README.config.md

### Changed
- Refactored server.py to use factory pattern with `create_server()`
- Migrated issue tools from server.py to `tools/issues/tools.py`
- Updated package exports to match the new architecture
- Enhanced documentation to reflect the new modular design
- Improved test organization with separate unit and integration test directories
- Improved code organization with clearer separation of concerns

### Documentation
- Created testing documentation in docs/testing/modular_architecture_testing.md
- Updated README.md to showcase the new configurable architecture
- Created configuration guide in README.config.md
- Added example configuration file (pygithub_mcp_config.json.example)
- Updated ADR-006 status to "Accepted"

## [0.5.5] - 2025-03-02

### Added
- Improved implementation lessons documentation for PyGithub parameter handling
- Added extended testing guidance for datetime handling in active_context.md

### Changed
- Updated test_failure_resolution_plan with completion status for all previously failing tests
- Enhanced datetime handling with microsecond truncation for improved consistency

### Fixed
- Fixed labels parameter handling in list_issues to use list of strings rather than comma-separated string
- Resolved 'since' parameter filtering by using appropriate future date buffer (24h vs 1h)
- Fixed datetime handling inconsistencies in filtering operations
- Eliminated all remaining test failures from the test failure resolution plan

## [0.5.4] - 2025-03-02

### Added
- Enhanced test failure resolution plan with detailed status tracking
- Added implementation lessons on PyGithub's pagination handling
- Improved documentation for test robustness strategy

### Changed
- Updated pagination test to be resilient to repository state
- Modified test expectations to focus on behavior rather than exact counts
- Enhanced datetime handling documentation in active_context.md

### Fixed
- Fixed rate limit error handler to properly extract reset times from response headers
- Fixed test approach for pagination to avoid making assumptions about repository state
- Resolved datetime module scoping issues in error handler

## [0.5.3] - 2025-03-02

### Added
- Added test_mode parameter to rate limit functions to improve test performance
- Created comprehensive test failure resolution plan in docs/test_failure_resolution_plan.md
- Implemented deterministic mode for rate limit backoff calculations

### Changed
- Standardized error handling across operations with _handle_github_exception method
- Improved datetime handling with consistent timezone-aware operations
- Enhanced rate limit tests to use test_mode instead of waiting for real reset times

### Fixed
- Fixed update_issue function to properly handle PyGithub's edit() returning None
- Added missing reset_timestamp attribute to GitHubRateLimitError
- Fixed error handling in the remove_issue_label function for 404 errors
- Fixed issue with offset-naive and offset-aware datetime comparisons
- Improved list_issues and list_issue_comments to properly handle string ISO dates

## [0.5.2] - 2025-03-02

### Added
- Added comprehensive unit tests for error handlers module
- Improved test coverage for datetime converters
- Added tests with real PyGithub exception structures following ADR-002

### Changed
- Improved error handling consistency in handlers.py
- Enhanced snake_case resource name formatting in error messages

### Fixed
- Fixed inconsistent datetime handling in error handlers (timestamps → datetime)
- Fixed resource name formatting in error messages
- Ensured consistent error type mapping in handlers
- Improved error message clarity and consistency

## [0.5.1] - 2025-03-01

### Added
- Implemented `convert_issue_list` function in issues converter
- Added comprehensive unit tests for converters using realistic data structures
- Created integration tests for client module and error handlers following ADR-002

### Changed
- Removed mock-based tests in favor of real API testing approach (ADR-002)
- Improved test coverage for converter modules

### Fixed
- Fixed handling of `None` values in `create_tool_response` function

## [0.5.0] - 2025-03-01

### Added
- Implemented ADR-002 (Real API Testing):
  - Created integration test directory structure with domain-specific organization
  - Implemented test fixtures with retry mechanism for rate limits
  - Added comprehensive test suite for GitHub issue operations
  - Set up environment configuration for real API testing
  - Added test documentation with patterns and best practices
  - Successfully ran first real API test (test_list_issues_basic)
  - Established foundation for future integration tests

### Changed
- Updated pytest configuration for integration tests:
  - Added integration test marker
  - Configured test output formatting
  - Added logging settings for better debugging
- Enhanced test organization with separate integration test directory
- Improved test fixtures for real API testing
- Updated documentation to reflect new testing approach

### Fixed
- Security: Ensured .env.test is properly ignored by git
- Added explicit .env.test to .gitignore for better security

## [0.4.2] - 2025-03-01

### Added
- Enhanced datetime conversion to support more flexible timezone formats:
  - Added support for single-digit timezone offsets (e.g., "-5")
  - Improved handling of various timezone formats
  - Updated tests to verify support for all timezone formats
  - Fixed validation issues in ListIssuesParams and ListIssueCommentsParams

### Changed
- Improved datetime conversion following Single Responsibility Principle
- Enhanced test coverage for datetime validation
- Updated documentation to reflect datetime handling improvements

## [0.4.1] - 2025-03-01

### Added
- Environment configuration with .env file support:
  - Added .env.test file for test credentials
  - Implemented dotenv loading functionality in utils/environment.py
  - Added environment type support (test, dev, prod)
  - Improved test organization with unit test structure

### Changed
- Updated import paths to reflect module reorganization
- Fixed environment utility tests to expect GitHubError
- Added unit test conftest.py with test environment loading
- Established foundation for real API testing

### Fixed
- Fixed import issues after common module reorganization
- Updated GitHubError import in environment tests
- Fixed version import path in __init__.py

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
- Integration test improvements:
  - Enhanced tool() decorator to automatically convert dictionary parameters to Pydantic models
  - Fixed issues in test_issue_lifecycle and test_list_issues integration tests
  - Aligned field name conventions in tests and converters ("number" vs "issue_number")
  - Added proper timezone designation to ISO datetime strings in tests
  - Made Pydantic an explicit dependency in pyproject.toml

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
