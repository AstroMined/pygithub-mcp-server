# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Improved parameter handling for PyGithub method calls
- Updated README with accurate setup and usage instructions
- PyGithub integration for object-oriented GitHub API interactions
- GitHubClient singleton for centralized client management
- Object conversion utilities for GitHub types
- Comprehensive error mapping between PyGithub and our error types
- Proper pagination handling using PyGithub's built-in capabilities
- New documentation for PyGithub patterns and usage

### Changed
- Refactored issues module to use PyGithub (proof of concept)
- Updated project dependencies to include PyGithub
- Improved error handling with PyGithub's exception system
- Enhanced project structure with new utility modules
- Fixed list_issues parameter handling to match PyGithub requirements
- Updated documentation to reflect correct setup and usage patterns

### Removed
- Direct REST API calls in issues module
- Request-specific utility functions for GitHub API

## [0.1.0] - Initial Release

### Added
- Basic GitHub MCP Server implementation
- Issue management operations
- Error handling and validation
- Documentation and setup guides
- Local development environment with UV
