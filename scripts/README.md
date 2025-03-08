# Scripts for PyGithub MCP Server

This directory contains utility scripts for development, testing, and maintenance of the PyGithub MCP Server project.

## Available Scripts

### Coverage Analysis

The `analyze_coverage.py` script provides detailed analysis of test coverage with prioritized recommendations:

```bash
# Run unit tests and generate reports
python scripts/analyze_coverage.py --run-tests --html

# Run both unit and integration tests for coverage
python scripts/analyze_coverage.py --run-tests --include-integration --html

# Use existing .coverage file and generate reports
python scripts/analyze_coverage.py --html

# Set a minimum coverage threshold
python scripts/analyze_coverage.py --run-tests --threshold 85
```

#### Features:
- Identifies high, medium, and low priority modules based on coverage
- Shows exact line numbers that need testing
- Generates both JSON and HTML reports
- Colorful console output with summary statistics
- Can run tests or use existing .coverage file
- HTML report with interactive details for each module

### Test Generator

The `generate_tool_tests.py` script creates standardized test files for new PyGithub MCP Server tools:

```bash
# Create tests for a repository tool
python scripts/generate_tool_tests.py --module repositories --tool-name GetRepository

# Create tests for an issue tool with custom schema
python scripts/generate_tool_tests.py --module issues --tool-name CreateIssue --schema-module issues --schema-name CreateIssueParams

# Create only integration tests
python scripts/generate_tool_tests.py --module repositories --tool-name ListCommits --integration-only
```

#### Features:
- Generates both unit and integration tests
- Uses dataclasses instead of mocks (following ADR-002)
- Follows project's test patterns and conventions
- Includes templates for most common tools
- Customizable test parameters and schemas
- Option to generate only unit or integration tests

## Integration with Development Workflow

These scripts integrate with the project's development workflow to improve quality and maintainability:

1. **Test-Driven Development**:
   - Use the coverage analyzer to identify untested code
   - Focus testing efforts on high-priority modules
   - Track improvement in coverage metrics

2. **Adding New Tools**:
   - Use the test generator to create standardized tests
   - Follow the Pydantic-First Architecture (ADR-007)
   - Ensure proper test coverage from the start

3. **Continuous Integration**:
   - Set coverage thresholds for CI pipelines
   - Generate coverage reports as part of CI
   - Prevent coverage regression

4. **Documentation**:
   - Coverage reports help document the test status
   - Generated tests document expected behavior
   - Clear code examples show how tools should be used
