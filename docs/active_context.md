# Active Context

## Current Focus
Implementing the modular tool architecture (ADR-006) and improving the overall codebase organization. We've shifted from a monolithic server design to a modular, configurable architecture that supports selective enabling/disabling of tool groups.

Our current focus is on:
1. Implementing the modular tool architecture as defined in ADR-006
2. Creating a flexible configuration system for MCP server tools
3. Implementing effective testing strategies for the new architecture
4. Reorganizing the codebase for better maintainability and extensibility
5. Establishing patterns for future tool group implementations
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

- Fixed integration test issues:
  - Enhanced tool() decorator to automatically convert dictionary parameters to Pydantic models
  - Fixed inconsistencies between field names ("number" vs "issue_number") in tests and converters
  - Added proper timezone designation to ISO datetime strings in tests
  - Made Pydantic an explicit dependency in pyproject.toml

- Implemented ADR-006 Modular Tool Architecture:
  - Created a configuration system in dedicated `config/` package
  - Implemented a decorator-based tool registration system in `tools/` package
  - Migrated issue tools from server.py to `tools/issues/tools.py`
  - Refactored server.py to use a factory pattern with `create_server()`
  - Added support for selectively enabling/disabling tool groups via configuration
  - Added configuration file and environment variable override support
  - Created example configuration file (pygithub_mcp_config.json.example)
  - Updated package exports to match the new architecture

- Created comprehensive testing strategy for modular architecture:
  - Added unit tests for configuration system without mocks
  - Added unit tests for tool registration system
  - Created integration tests for issue tools following ADR-002
  - Established patterns for testing new tool groups
  - Created testing documentation in docs/testing/modular_architecture_testing.md

- Improved code organization and maintainability:
  - Established clear separation of concerns with modular design
  - Created consistent patterns for tool registration
  - Added proper error handling in tool modules
  - Improved logging throughout the system
  - Enhanced configuration flexibility for different deployment scenarios

- PyGithub Integration Lessons:
  - Discovered PyGithub's `get_issues()` doesn't directly accept per_page parameter
  - Need to handle pagination through PaginatedList objects instead
  - API behavior differs from documentation in some cases, particularly for filtering
  - Tests need to be resilient to real-world repository state

## Next Steps

1. Expand Modular Architecture:
   - Implement additional tool groups (repositories, pull_requests, etc.)
   - Create consistent patterns for new tool groups
   - Develop configuration templates for different usage scenarios
   - Enhance modularity with pluggable architecture

2. Testing Strategy Enhancement:
   - Expand test coverage for configuration system
   - Add real API tests for all tool modules
   - Develop efficient testing patterns for tool groups
   - Implement automated config validation tests

3. Performance Optimization:
   - Optimize tool loading based on configuration
   - Implement lazy loading for tool groups
   - Add caching strategies for frequently accessed data
   - Improve memory usage for large number of tools

4. User Experience Improvements:
   - Add in-tool documentation
   - Create more configuration examples
   - Add configuration validation
   - Enhance error messages for configuration issues

5. Documentation:
   - Create detailed guide for adding new tool groups
   - Document configuration best practices
   - Add examples for common configuration scenarios
   - Create architectural diagrams for better understanding

## Active Decisions

1. Modular Architecture Approach:
   - Use decorator-based registration for tools
   - Organize tools by domain (issues, repositories, etc.)
   - Support selective enabling/disabling of tool groups
   - Maintain backward compatibility during transition

2. Configuration System Design:
   - Support both file-based and environment variable configuration
   - Establish clear precedence rules for configuration sources
   - Provide sensible defaults for all settings
   - Document all configuration options clearly

3. Testing Strategy:
   - Follow ADR-002's real API testing approach
   - Test configuration components without mocks
   - Create integration tests for tool functionality
   - Ensure proper cleanup of test resources

4. Code Organization:
   - Group related tools in dedicated modules
   - Keep tool implementations separate from registration
   - Maintain clear separation between configuration and execution
   - Establish consistent patterns across all modules

## Current Considerations

1. Tool Group Granularity:
   - Determining the right level of granularity for tool groups
   - Balancing flexibility with simplicity in configuration
   - Considering interdependencies between tool groups
   - Planning for future expansion with new GitHub API features

2. Configuration Complexity:
   - Managing growing number of configuration options
   - Ensuring clear documentation for all configuration options
   - Providing sensible defaults that work for most users
   - Balancing flexibility with simplicity

3. Testing Approach:
   - Testing with various configuration combinations
   - Ensuring proper cleanup of test resources
   - Testing dynamic loading of tool groups
   - Verifying configuration precedence rules

4. Performance Considerations:
   - Optimizing tool loading based on configuration
   - Minimizing startup time with large number of tools
   - Reducing memory footprint with selective loading
   - Balancing modularity with performance

## Implementation Lessons

1. Modular Tool Architecture:
   - Decorator-based registration simplifies tool management
   - Dynamic import provides flexibility but requires careful error handling
   - Clear separation of concerns improves maintainability
   - Configuration-driven loading enables customization without code changes
   - Factory pattern in server.py centralizes server creation and configuration

2. Configuration Management:
   - Environment variables provide deployment flexibility
   - JSON configuration files offer more complex configuration options
   - Clear precedence rules prevent confusion
   - Sensible defaults reduce configuration burden
   - Validation prevents common misconfigurations

3. Testing Strategies:
   - Real API testing provides higher confidence than mocked tests
   - Test fixtures with proper cleanup prevent test pollution
   - Configuration can be tested without mocks
   - Integration tests should follow the real API approach
   - Unit tests should verify component behavior in isolation

4. Code Organization:
   - Logical grouping improves code navigation
   - Consistent patterns simplify maintenance
   - Clear separation of responsibilities reduces complexity
   - Proper error handling improves reliability
   - Comprehensive logging aids debugging

5. System Design:
   - Factory pattern simplifies server initialization
   - Decorator pattern streamlines tool registration
   - Strategy pattern in configuration system provides flexibility
   - Observer pattern could enhance future event handling
   - Command pattern is implicit in tool implementation
