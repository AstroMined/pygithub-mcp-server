# Test Improvement Plan

## Current Status

As of March 7, 2025, we have:
- 354 tests passing with 86% overall coverage
- Fixed the skipped integration tests for repository operations
- Standardized fixtures in `tests/integration/conftest.py`
- Created comprehensive documentation for test patterns in `tests/integration/README.md`

## Remaining Issues

1. **TestGitHubClient Warning Persists**
   ```
   PytestCollectionWarning: cannot collect test class 'TestGitHubClient' because it has a __init__ constructor
   ```

2. **Low Coverage Areas**
   - `converters/common/datetime.py`: 54% coverage 
   - `tools/repositories/tools.py`: 55% coverage
   - `operations/repositories.py`: 77% coverage

## Improvement Plan

### Phase 1: Fix Warning & Immediate Issues

1. **Fix TestGitHubClient Warning**
   - Approach options:
     ```python
     # Option 1: Convert to fixture
     @pytest.fixture
     def test_github_client():
         """Test GitHub client fixture."""
         client = GitHub()
         return {
             "github": client,
             "get_repo": lambda full_name: create_test_repo(full_name, client)
         }

     # Helper function
     def create_test_repo(full_name, github):
         owner, repo = full_name.split("/")
         return Repository(
             id=54321,
             name=repo,
             full_name=full_name,
             owner=RepositoryOwner(login=owner),
             html_url=f"https://github.com/{full_name}"
         )
     ```
     - Alternative: Add a `pytest.mark.filterwarnings` marker to ignore this specific warning

2. **Improve datetime.py Coverage (54% → 80%+)**
   - Target missing lines: 47, 51, 62, 63->81, 66->81, 76->81, 102-115, 124-135
   - Add tests for:
     ```python
     def test_datetime_conversion_timezone_formats():
         """Test datetime conversion with various timezone formats."""
         # Test ISO format with Z
         assert convert_datetime("2021-01-01T00:00:00Z") == datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
         
         # Test ISO format with +00:00
         assert convert_datetime("2021-01-01T00:00:00+00:00") == datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
         
         # Test ISO format with -0500 (no colon)
         assert convert_datetime("2021-01-01T00:00:00-0500") is not None
         
         # Test invalid formats
         with pytest.raises(ValueError):
             convert_datetime("2021-01-01")  # Missing time component
             
         with pytest.raises(ValueError):
             convert_datetime("2021-01-01T00:00:00")  # Missing timezone
     ```

3. **Fix Error Handling Consistency**
   - Address GitHubError 'status' attribute issue in tests
   - Update error handling to use a consistent approach
   - Focus on handlers.py coverage gaps (lines 57->64, 61-62, 65->71, 68-70)

### Phase 2: Targeted Coverage Improvements

1. **Improve repositories.py Operations (77% → 90%+)**
   - Target missing lines: 53-55, 92-94, 123-125, 153-155, 193-195, etc.
   - Add tests for specific error conditions
   - Test edge cases and boundary conditions

2. **Focus on tools/repositories/tools.py (55% → 80%+)**
   - Target missing lines: 57-58, 68-72, 110-120, 151-167, etc.
   - Create specific tests for each tool function
   - Focus on error handling paths

3. **Standardize Remaining Tests**
   - Apply standardized fixture pattern to:
     - `tests/integration/operations/issues/`
     - `tests/integration/tools/`
   - Ensure consistent error handling and resource cleanup
   - Add proper retry mechanisms to all API calls

### Phase 3: Comprehensive Coverage

1. **Create Test Helpers**
   - Build reusable test helpers for common operations
   - Reduce duplication in test setup and cleanup
   - Create patterns for common assertions

2. **Add Test Pattern Verification**
   - Create linting rules to enforce fixture usage
   - Add test pattern guidelines to CI process
   - Document patterns for common test operations

3. **Conduct Testing Review**
   - Review all test files for adherence to patterns
   - Ensure consistent retry and cleanup mechanisms
   - Verify edge cases are covered

## Completion Criteria

- Overall coverage above 90%
- No modules below 75% coverage
- All tests passing without warnings
- Consistent fixture usage across all tests
- Comprehensive documentation for test patterns

## Timeline

- Phase 1: Immediate (Next Session)
- Phase 2: Medium Term (1-2 Sessions)
- Phase 3: Long Term (2-3 Sessions)
