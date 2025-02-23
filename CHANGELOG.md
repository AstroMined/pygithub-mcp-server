# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Comprehensive test suite implementation:
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
