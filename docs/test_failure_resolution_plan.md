# Test Failure Resolution Plan

This document outlines the comprehensive plan to resolve all integration test failures in the PyGitHub MCP Server. The plan breaks down issues into categories and provides specific solutions for each problem.

## 1. Datetime Handling Issues

### Problems
- **Timezone inconsistency**: Mixing aware and naive datetime objects when comparing
- In `client/rate_limit.py`, `datetime.now()` returns a naive datetime but is compared with GitHub API's timezone-aware datetimes
- Test failures: `test_check_rate_limit`, `test_handle_rate_limit_with_backoff`, `test_list_issue_comments_since`

### Solutions

- [x] **Make datetime.now() timezone-aware consistently**
  ```python
  # Before
  now = datetime.now()
  
  # After - make consistently timezone-aware
  now = datetime.now().astimezone()
  ```

- [x] **Fix wait_for_rate_limit_reset function**
  ```python
  def wait_for_rate_limit_reset(reset_time: datetime, buffer_seconds: int = 5) -> None:
      """Wait until rate limit resets."""
      # Ensure both are timezone-aware for comparison
      now = datetime.now().astimezone()
      if reset_time.tzinfo is None:
          reset_time = reset_time.astimezone()  # Local timezone if none specified
          
      if reset_time > now:
          # Rest of the function remains unchanged
  ```

- [x] **Fix issue_comments_since parameter in operations/issues.py**
  ```python
  # In list_issue_comments function
  if since is not None:
      if isinstance(since, str):
          # Convert ISO string to datetime object
          since = convert_iso_string_to_datetime(since)
      kwargs["since"] = since
  ```

## 2. Update Issue Operation Returning None

### Problem
- PyGithub's `issue.edit()` returns None, not the updated issue
- After edit, we're trying to access `updated_issue.title` but updated_issue is None

### Solution

- [x] **Modify the update_issue function**
  ```python
  # In operations/issues.py update_issue function
  # Replace:
  updated_issue = issue.edit(**kwargs)
  print(f"After edit, updated_issue.title: {updated_issue.title}")
  
  # With:
  issue.edit(**kwargs)
  # Get fresh issue data to ensure we have the latest state
  updated_issue = repository.get_issue(issue_number)
  print(f"After edit, updated_issue.title: {updated_issue.title}")  
  ```

## 3. Error Handling Mechanism

### Problems
- Inconsistent error handling methods:
  - `GitHubClient.get_instance()._handle_github_exception(e)` vs `handle_github_exception(e)`
- `GitHubRateLimitError` missing `reset_timestamp` attribute

### Solutions

- [x] **Standardize error handling**
  ```python
  # In client.py, add a method to the GitHubClient class
  def _handle_github_exception(self, exception):
      """Forward to the module-level handler for consistent handling."""
      from ..errors import handle_github_exception
      return handle_github_exception(exception)
  ```

- [x] **Add reset_timestamp to GitHubRateLimitError**
  ```python
  # In errors/exceptions.py, update GitHubRateLimitError
  class GitHubRateLimitError(GitHubError):
      """GitHub API rate limit error."""
      
      def __init__(self, message, reset_at=None, reset_timestamp=None, data=None):
          super().__init__(message, data)
          self.reset_at = reset_at
          # Add this line
          self.reset_timestamp = reset_timestamp if reset_timestamp else reset_at
  ```

## 4. Test Expectations vs. API Behavior

### Problems
- Pagination expectations don't match actual behavior
- Sort order tests failing due to implementation or API behavior
- Tests making assumptions about repository state
- `test_list_issues_sort_and_direction` has sort order issues
- `test_list_issues_since` expects filtering that doesn't match actual API behavior

### Solutions

- [ ] **Fix dynamic test expectations for pagination**
  ```python
  # Instead of hardcoded expectations:
  assert len(page1) <= 1  # BAD - assumes repo state
  
  # Get actual count first:
  all_issues = list_issues(owner, repo, state="all")
  total_count = len(all_issues)
  
  # Or directly check pagination works correctly:
  page1 = list_issues(owner, repo, per_page=5, page=1)
  page2 = list_issues(owner, repo, per_page=5, page=2)
  assert len(page1) <= 5  # Should respect per_page
  assert page1 != page2 if len(all_issues) > 5 else True  # Different pages if enough issues
  ```

- [ ] **Improve test isolation**
  ```python
  # Create a controlled test environment:
  # 1. Create exactly the resources needed for the test
  # 2. Run the test with those resources
  # 3. Clean up all created resources
  ```

- [ ] **Implement test resource tagging**
  ```python
  # Tag all test-created resources with unique test ID
  # Filter by tags when listing to ensure test data isolation
  ```

- [ ] **Address sort order test issues**
  - Check that sort parameters are correctly passed to the API
  - Verify the test's assertions match the expected API behavior
  - Add debug logging to verify actual sort behavior

- [ ] **Fix since parameter filtering**
  ```python
  # Ensure proper datetime conversion before passing to API
  # Validate filtering logic in the test matches GitHub's behavior
  ```

## 5. Exponential Backoff Testing

### Problem
- Test expects a specific backoff behavior that might not match implementation
- Rate limit tests take 30+ minutes to run due to waiting for real API rate limit reset times

### Solution

- [x] **Fix exponential backoff test**
  ```python
  # Added deterministic mode for testing
  def exponential_backoff(
      attempt: int, max_attempts: int = 5, base_delay: float = 2.0, deterministic: bool = False
  ):
      # ... existing code ...
      
      # Add test mode without jitter
      if deterministic:
          return base_delay * (2 ** attempt)
  ```

- [x] **Add test_mode parameter to handle_rate_limit_with_backoff**
  ```python
  def handle_rate_limit_with_backoff(
      github: Github, 
      exception: RateLimitExceededException,
      attempt: int = 0,
      max_attempts: int = 5,
      deterministic: bool = False,
      test_mode: bool = False
  ):
      # In test mode, use short delays instead of waiting for real reset times
      if test_mode:
          delay = exponential_backoff(attempt, max_attempts, base_delay=0.1, deterministic=deterministic)
          logger.info(f"Test mode: Using short delay instead of waiting for reset: {delay:.1f} seconds.")
          time.sleep(delay)
          return
  ```

## 6. Implementation Phases

### Phase 1: Fix Core Infrastructure ✅
- [x] Standardize datetime handling
- [x] Implement consistent error handling 
- [x] Fix GitHubRateLimitError class
- [x] Add test mode for rate limit tests

### Phase 2: Fix Issue Operations ✅
- [x] Fix update_issue function to properly get updated issue state
- [x] Address all NoneType object attribute errors

### Phase 3: Fix Test Expectations 🚧
- [ ] Adjust test expectations to match actual API behavior
- [ ] Fix pagination, sorting, and filtering issues
- [ ] Implement dynamic test expectations

### Phase 4: Comprehensive Testing 🚧
- [ ] Run full test suite to verify fixes
- [ ] Address any remaining edge cases
- [ ] Document patterns to avoid similar issues in future

## 8. Remaining Test Failures

Based on the latest test run, the following tests still fail:

1. `test_handle_github_exception_rate_limit`: 
   - Issue: Reset times not being properly set in the `GitHubRateLimitError` object.
   - Solution: Fix the `handle_github_exception` function to properly set reset timestamps.

2. `test_list_issue_comments_since`:
   - Issue: Comments with future "since" filter still appear in results.
   - Solution: Improve datetime handling and filtering.

3. `test_list_issues_pagination`:
   - Issue: Pagination returning 19 items despite requesting per_page=1.
   - Solution: Fix pagination parameter handling.

4. `test_list_issues_labels_filter`:
   - Issue: Issue is found with non-existent label filter.
   - Solution: Fix label filtering or test expectations.

5. `test_list_issues_since`:
   - Issue: Issue is found with future "since" filter.
   - Solution: Fix datetime handling for filtering by updated time.

## 7. Long-term Improvements

- [ ] **Timezone Handling Policy**
  - Document whether the system uses aware or naive datetimes
  - Add converter utilities that enforce the chosen approach
  - Add validation to catch timezone inconsistencies early

- [ ] **API Behavior Documentation**
  - Document GitHub API behaviors that might be unexpected
  - Create test fixtures that match real API responses

- [ ] **Error Handling Standardization**
  - Create a single, consistent pattern for error handling
  - Add comprehensive tests specifically for error scenarios

- [ ] **Test Pattern Improvements**
  - Update test helpers to ensure consistent state
  - Add better cleanup mechanisms for test resources
  - Implement more robust test isolation

## Appendix: Actual Status of Integration Tests  

```
$ pytest tests/unit tests/integration/ --run-integration --log-level=INFO
=========================================================================================================== test session starts ============================================================================================================
platform linux -- Python 3.10.12, pytest-8.3.4, pluggy-1.5.0 -- /code/python-mcp-servers/pygithub-mcp-server/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /code/python-mcp-servers/pygithub-mcp-server
configfile: pyproject.toml
plugins: mock-3.14.0, cov-6.0.0, anyio-4.8.0
collected 228 items                                                                                                                                                                                                                        

tests/unit/converters/common/test_datetime.py::TestConvertDatetime::test_convert_datetime_with_datetime PASSED                                                                                                                       [  0%]
tests/unit/converters/common/test_datetime.py::TestConvertDatetime::test_convert_datetime_with_none PASSED                                                                                                                           [  0%]
tests/unit/converters/common/test_datetime.py::TestConvertIsoStringToDatetime::test_with_datetime_object PASSED                                                                                                                      [  1%]
tests/unit/converters/common/test_datetime.py::TestConvertIsoStringToDatetime::test_with_z_timezone PASSED                                                                                                                           [  1%]
tests/unit/converters/common/test_datetime.py::TestConvertIsoStringToDatetime::test_with_offset_timezone_with_colon PASSED                                                                                                           [  2%]
tests/unit/converters/common/test_datetime.py::TestConvertIsoStringToDatetime::test_with_offset_timezone_without_colon PASSED                                                                                                        [  2%]
tests/unit/converters/common/test_datetime.py::TestConvertIsoStringToDatetime::test_with_short_timezone PASSED                                                                                                                       [  3%]
tests/unit/converters/common/test_datetime.py::TestConvertIsoStringToDatetime::test_with_single_digit_timezone PASSED                                                                                                                [  3%]
tests/unit/converters/issues/test_issues.py::TestConvertLabel::test_convert_label_full PASSED                                                                                                                                        [  3%]
tests/unit/converters/issues/test_issues.py::TestConvertLabel::test_convert_label_minimal PASSED                                                                                                                                     [  4%]
tests/unit/converters/issues/test_issues.py::TestConvertMilestone::test_convert_milestone_full PASSED                                                                                                                                [  4%]
tests/unit/converters/issues/test_issues.py::TestConvertMilestone::test_convert_milestone_minimal PASSED                                                                                                                             [  5%]
tests/unit/converters/issues/test_issues.py::TestConvertMilestone::test_convert_milestone_none PASSED                                                                                                                                [  5%]
tests/unit/converters/issues/test_issues.py::TestConvertIssue::test_convert_issue_full PASSED                                                                                                                                        [  6%]
tests/unit/converters/issues/test_issues.py::TestConvertIssue::test_convert_issue_minimal PASSED                                                                                                                                     [  6%]
tests/unit/converters/issues/test_issues.py::TestConvertIssue::test_convert_issue_closed PASSED                                                                                                                                      [  7%]
tests/unit/converters/issues/test_issues.py::TestConvertIssueList::test_convert_empty_list PASSED                                                                                                                                    [  7%]
tests/unit/converters/issues/test_issues.py::TestConvertIssueList::test_convert_issue_list PASSED                                                                                                                                    [  7%]
tests/unit/converters/test_parameters.py::TestBuildIssueKwargs::test_with_all_parameters PASSED                                                                                                                                      [  8%]
tests/unit/converters/test_parameters.py::TestBuildIssueKwargs::test_with_minimal_parameters PASSED                                                                                                                                  [  8%]
tests/unit/converters/test_parameters.py::TestBuildIssueKwargs::test_with_none_values PASSED                                                                                                                                         [  9%]
tests/unit/converters/test_parameters.py::TestBuildListIssuesKwargs::test_with_all_parameters PASSED                                                                                                                                 [  9%]
tests/unit/converters/test_parameters.py::TestBuildListIssuesKwargs::test_with_minimal_parameters PASSED                                                                                                                             [ 10%]
tests/unit/converters/test_parameters.py::TestBuildListIssuesKwargs::test_with_none_values PASSED                                                                                                                                    [ 10%]
tests/unit/converters/test_parameters.py::TestBuildUpdateIssueKwargs::test_with_all_parameters PASSED                                                                                                                                [ 10%]
tests/unit/converters/test_parameters.py::TestBuildUpdateIssueKwargs::test_with_minimal_parameters PASSED                                                                                                                            [ 11%]
tests/unit/converters/test_parameters.py::TestBuildUpdateIssueKwargs::test_with_none_values PASSED                                                                                                                                   [ 11%]
tests/unit/converters/test_parameters.py::TestBuildUpdateIssueKwargs::test_with_partial_parameters PASSED                                                                                                                            [ 12%]
tests/unit/converters/test_responses.py::TestCreateToolResponse::test_with_string_content PASSED                                                                                                                                     [ 12%]
tests/unit/converters/test_responses.py::TestCreateToolResponse::test_with_dict_content PASSED                                                                                                                                       [ 13%]
tests/unit/converters/test_responses.py::TestCreateToolResponse::test_with_list_content PASSED                                                                                                                                       [ 13%]
tests/unit/converters/test_responses.py::TestCreateToolResponse::test_with_error_flag PASSED                                                                                                                                         [ 14%]
tests/unit/converters/test_responses.py::TestCreateToolResponse::test_with_none_content PASSED                                                                                                                                       [ 14%]
tests/unit/converters/test_responses.py::TestCreateErrorResponse::test_with_string_error PASSED                                                                                                                                      [ 14%]
tests/unit/converters/test_responses.py::TestCreateErrorResponse::test_with_exception PASSED                                                                                                                                         [ 15%]
tests/unit/converters/test_responses.py::TestCreateErrorResponse::test_with_dict_error PASSED                                                                                                                                        [ 15%]
tests/unit/converters/users/test_users.py::TestConvertUser::test_convert_user_full PASSED                                                                                                                                            [ 16%]
tests/unit/converters/users/test_users.py::TestConvertUser::test_convert_user_minimal PASSED                                                                                                                                         [ 16%]
tests/unit/converters/users/test_users.py::TestConvertUser::test_convert_organization PASSED                                                                                                                                         [ 17%]
tests/unit/converters/users/test_users.py::TestConvertUser::test_convert_site_admin PASSED                                                                                                                                           [ 17%]
tests/unit/converters/users/test_users.py::TestConvertUser::test_convert_user_none PASSED                                                                                                                                            [ 17%]
tests/unit/errors/test_formatters.py::TestFormatGitHubError::test_base_github_error PASSED                                                                                                                                           [ 18%]
tests/unit/errors/test_formatters.py::TestFormatGitHubError::test_validation_error PASSED                                                                                                                                            [ 18%]
tests/unit/errors/test_formatters.py::TestFormatGitHubError::test_resource_not_found_error PASSED                                                                                                                                    [ 19%]
tests/unit/errors/test_formatters.py::TestFormatGitHubError::test_authentication_error PASSED                                                                                                                                        [ 19%]
tests/unit/errors/test_formatters.py::TestFormatGitHubError::test_permission_error PASSED                                                                                                                                            [ 20%]
tests/unit/errors/test_formatters.py::TestFormatGitHubError::test_rate_limit_error_with_reset_time PASSED                                                                                                                            [ 20%]
tests/unit/errors/test_formatters.py::TestFormatGitHubError::test_rate_limit_error_without_reset_time PASSED                                                                                                                         [ 21%]
tests/unit/errors/test_formatters.py::TestFormatGitHubError::test_conflict_error PASSED                                                                                                                                              [ 21%]
tests/unit/errors/test_formatters.py::TestIsGitHubError::test_with_github_errors PASSED                                                                                                                                              [ 21%]
tests/unit/errors/test_formatters.py::TestIsGitHubError::test_with_non_github_errors PASSED                                                                                                                                          [ 22%]
tests/unit/errors/test_formatters.py::TestIsGitHubError::test_with_non_errors PASSED                                                                                                                                                 [ 22%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_rate_limit_exceeded 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Rate limit exceeded (handlers.py:41)
PASSED                                                                                                                                                                                                                               [ 23%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_rate_limit_exceeded_without_rate 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Rate limit exceeded (handlers.py:41)
PASSED                                                                                                                                                                                                                               [ 23%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_authentication_error 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=401, data={'message': 'Bad credentials'} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Authentication error (handlers.py:90)
PASSED                                                                                                                                                                                                                               [ 24%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_permission_error 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=403, data={'message': 'Resource not accessible by integration'} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Permission denied (handlers.py:114)
PASSED                                                                                                                                                                                                                               [ 24%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_403_rate_limit 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=403, data={'message': 'API rate limit exceeded'} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Rate limit exceeded (handlers.py:96)
PASSED                                                                                                                                                                                                                               [ 25%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_not_found_with_hint 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=404, data={'message': 'Not Found'} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Resource not found (handlers.py:119)
PASSED                                                                                                                                                                                                                               [ 25%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_not_found_auto_detection 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=404, data={'message': 'Issue not found'} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Resource not found (handlers.py:119)
PASSED                                                                                                                                                                                                                               [ 25%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_not_found_with_resource_in_data 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=404, data={'message': 'Not Found', 'resource': 'pull_request'} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Resource not found (handlers.py:119)
PASSED                                                                                                                                                                                                                               [ 26%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_validation_error 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=422, data={'message': 'Validation Failed', 'errors': [{'resource': 'Issue', 'field': 'title', 'code': 'missing_field'}]} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Validation error (handlers.py:127)
PASSED                                                                                                                                                                                                                               [ 26%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_unknown_error 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=500, data={'message': 'Internal server error'} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Unknown GitHub error: 500 (handlers.py:130)
PASSED                                                                                                                                                                                                                               [ 27%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_string_data 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=400, data={'message': 'Bad request'} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Unknown GitHub error: 400 (handlers.py:130)
PASSED                                                                                                                                                                                                                               [ 27%]
tests/unit/errors/test_handlers.py::TestHandleGithubException::test_handle_plain_string_data 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:36 [   ERROR] Handling GitHub exception: status=400, data={'message': 'Something went wrong'} (handlers.py:70)
2025-03-02 10:45:36 [   ERROR] Unknown GitHub error: 400 (handlers.py:130)
PASSED                                                                                                                                                                                                                               [ 28%]
tests/unit/errors/test_handlers.py::TestFormatValidationError::test_format_validation_error_with_field_errors PASSED                                                                                                                 [ 28%]
tests/unit/errors/test_handlers.py::TestFormatValidationError::test_format_validation_error_without_field_errors PASSED                                                                                                              [ 28%]
tests/unit/errors/test_handlers.py::TestFormatValidationError::test_format_validation_error_without_errors PASSED                                                                                                                    [ 29%]
tests/unit/errors/test_handlers.py::TestFormatValidationError::test_format_validation_error_with_none_data PASSED                                                                                                                    [ 29%]
tests/unit/schemas/test_base.py::TestRepositoryRef::test_valid_data PASSED                                                                                                                                                           [ 30%]
tests/unit/schemas/test_base.py::TestRepositoryRef::test_minimal_valid_data PASSED                                                                                                                                                   [ 30%]
tests/unit/schemas/test_base.py::TestRepositoryRef::test_missing_required_fields PASSED                                                                                                                                              [ 31%]
tests/unit/schemas/test_base.py::TestRepositoryRef::test_invalid_field_types PASSED                                                                                                                                                  [ 31%]
tests/unit/schemas/test_base.py::TestRepositoryRef::test_empty_strings PASSED                                                                                                                                                        [ 32%]
tests/unit/schemas/test_base.py::TestRepositoryRef::test_none_values PASSED                                                                                                                                                          [ 32%]
tests/unit/schemas/test_base.py::TestRepositoryRef::test_extra_fields PASSED                                                                                                                                                         [ 32%]
tests/unit/schemas/test_base.py::TestFileContent::test_valid_data PASSED                                                                                                                                                             [ 33%]
tests/unit/schemas/test_base.py::TestFileContent::test_minimal_valid_data PASSED                                                                                                                                                     [ 33%]
tests/unit/schemas/test_base.py::TestFileContent::test_missing_required_fields PASSED                                                                                                                                                [ 34%]
tests/unit/schemas/test_base.py::TestFileContent::test_invalid_field_types PASSED                                                                                                                                                    [ 34%]
tests/unit/schemas/test_base.py::TestFileContent::test_empty_strings PASSED                                                                                                                                                          [ 35%]
tests/unit/schemas/test_base.py::TestFileContent::test_none_values PASSED                                                                                                                                                            [ 35%]
tests/unit/schemas/test_base.py::TestFileContent::test_extra_fields PASSED                                                                                                                                                           [ 35%]
tests/unit/schemas/test_base.py::TestFileContent::test_binary_content PASSED                                                                                                                                                         [ 36%]
tests/unit/schemas/test_issues.py::TestCreateIssueParams::test_valid_data PASSED                                                                                                                                                     [ 36%]
tests/unit/schemas/test_issues.py::TestCreateIssueParams::test_minimal_valid_data PASSED                                                                                                                                             [ 37%]
tests/unit/schemas/test_issues.py::TestCreateIssueParams::test_missing_required_fields PASSED                                                                                                                                        [ 37%]
tests/unit/schemas/test_issues.py::TestCreateIssueParams::test_invalid_field_types PASSED                                                                                                                                            [ 38%]
tests/unit/schemas/test_issues.py::TestCreateIssueParams::test_empty_strings PASSED                                                                                                                                                  [ 38%]
tests/unit/schemas/test_issues.py::TestCreateIssueParams::test_none_values PASSED                                                                                                                                                    [ 39%]
tests/unit/schemas/test_issues.py::TestCreateIssueParams::test_empty_lists PASSED                                                                                                                                                    [ 39%]
tests/unit/schemas/test_issues.py::TestCreateIssueParams::test_default_values PASSED                                                                                                                                                 [ 39%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_valid_data PASSED                                                                                                                                                      [ 40%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_minimal_valid_data PASSED                                                                                                                                              [ 40%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_valid_state_values PASSED                                                                                                                                              [ 41%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_invalid_state_values PASSED                                                                                                                                            [ 41%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_valid_sort_values PASSED                                                                                                                                               [ 42%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_invalid_sort_values PASSED                                                                                                                                             [ 42%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_valid_direction_values PASSED                                                                                                                                          [ 42%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_invalid_direction_values PASSED                                                                                                                                        [ 43%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_invalid_page_values PASSED                                                                                                                                             [ 43%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_invalid_per_page_values PASSED                                                                                                                                         [ 44%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_none_per_page_value PASSED                                                                                                                                             [ 44%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_datetime_parsing PASSED                                                                                                                                                [ 45%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_timezone_formats PASSED                                                                                                                                                [ 45%]
tests/unit/schemas/test_issues.py::TestListIssuesParams::test_invalid_datetime_format PASSED                                                                                                                                         [ 46%]
tests/unit/schemas/test_issues.py::TestGetIssueParams::test_valid_data PASSED                                                                                                                                                        [ 46%]
tests/unit/schemas/test_issues.py::TestGetIssueParams::test_missing_required_fields PASSED                                                                                                                                           [ 46%]
tests/unit/schemas/test_issues.py::TestGetIssueParams::test_invalid_issue_number_type PASSED                                                                                                                                         [ 47%]
tests/unit/schemas/test_issues.py::TestGetIssueParams::test_negative_issue_number PASSED                                                                                                                                             [ 47%]
tests/unit/schemas/test_issues.py::TestUpdateIssueParams::test_valid_data PASSED                                                                                                                                                     [ 48%]
tests/unit/schemas/test_issues.py::TestUpdateIssueParams::test_minimal_valid_data PASSED                                                                                                                                             [ 48%]
tests/unit/schemas/test_issues.py::TestUpdateIssueParams::test_partial_update PASSED                                                                                                                                                 [ 49%]
tests/unit/schemas/test_issues.py::TestUpdateIssueParams::test_valid_state_values PASSED                                                                                                                                             [ 49%]
tests/unit/schemas/test_issues.py::TestUpdateIssueParams::test_invalid_state_values PASSED                                                                                                                                           [ 50%]
tests/unit/schemas/test_issues.py::TestUpdateIssueParams::test_empty_title PASSED                                                                                                                                                    [ 50%]
tests/unit/schemas/test_issues.py::TestUpdateIssueParams::test_none_values PASSED                                                                                                                                                    [ 50%]
tests/unit/schemas/test_issues.py::TestUpdateIssueParams::test_title_validation_edge_cases PASSED                                                                                                                                    [ 51%]
tests/unit/schemas/test_issues.py::TestUpdateIssueParams::test_invalid_field_types PASSED                                                                                                                                            [ 51%]
tests/unit/schemas/test_issues.py::TestUpdateIssueCommentParams::test_valid_data PASSED                                                                                                                                              [ 52%]
tests/unit/schemas/test_issues.py::TestUpdateIssueCommentParams::test_missing_required_fields PASSED                                                                                                                                 [ 52%]
tests/unit/schemas/test_issues.py::TestUpdateIssueCommentParams::test_empty_body PASSED                                                                                                                                              [ 53%]
tests/unit/schemas/test_issues.py::TestUpdateIssueCommentParams::test_invalid_field_types PASSED                                                                                                                                     [ 53%]
tests/unit/schemas/test_issues.py::TestDeleteIssueCommentParams::test_valid_data PASSED                                                                                                                                              [ 53%]
tests/unit/schemas/test_issues.py::TestDeleteIssueCommentParams::test_missing_required_fields PASSED                                                                                                                                 [ 54%]
tests/unit/schemas/test_issues.py::TestDeleteIssueCommentParams::test_negative_issue_number PASSED                                                                                                                                   [ 54%]
tests/unit/schemas/test_issues.py::TestDeleteIssueCommentParams::test_invalid_field_types PASSED                                                                                                                                     [ 55%]
tests/unit/schemas/test_issues.py::TestAddIssueLabelsParams::test_valid_data PASSED                                                                                                                                                  [ 55%]
tests/unit/schemas/test_issues.py::TestAddIssueLabelsParams::test_missing_required_fields PASSED                                                                                                                                     [ 56%]
tests/unit/schemas/test_issues.py::TestAddIssueLabelsParams::test_empty_labels_list PASSED                                                                                                                                           [ 56%]
tests/unit/schemas/test_issues.py::TestAddIssueLabelsParams::test_negative_issue_number PASSED                                                                                                                                       [ 57%]
tests/unit/schemas/test_issues.py::TestAddIssueLabelsParams::test_invalid_field_types PASSED                                                                                                                                         [ 57%]
tests/unit/schemas/test_issues.py::TestRemoveIssueLabelParams::test_valid_data PASSED                                                                                                                                                [ 57%]
tests/unit/schemas/test_issues.py::TestRemoveIssueLabelParams::test_missing_required_fields PASSED                                                                                                                                   [ 58%]
tests/unit/schemas/test_issues.py::TestRemoveIssueLabelParams::test_empty_label PASSED                                                                                                                                               [ 58%]
tests/unit/schemas/test_issues.py::TestRemoveIssueLabelParams::test_invalid_field_types PASSED                                                                                                                                       [ 59%]
tests/unit/schemas/test_issues.py::TestIssueCommentParams::test_valid_data PASSED                                                                                                                                                    [ 59%]
tests/unit/schemas/test_issues.py::TestIssueCommentParams::test_missing_required_fields PASSED                                                                                                                                       [ 60%]
tests/unit/schemas/test_issues.py::TestIssueCommentParams::test_empty_body PASSED                                                                                                                                                    [ 60%]
tests/unit/schemas/test_issues.py::TestIssueCommentParams::test_invalid_field_types PASSED                                                                                                                                           [ 60%]
tests/unit/schemas/test_issues.py::TestListIssueCommentsParams::test_valid_data PASSED                                                                                                                                               [ 61%]
tests/unit/schemas/test_issues.py::TestListIssueCommentsParams::test_minimal_valid_data PASSED                                                                                                                                       [ 61%]
tests/unit/schemas/test_issues.py::TestListIssueCommentsParams::test_datetime_parsing PASSED                                                                                                                                         [ 62%]
tests/unit/schemas/test_issues.py::TestListIssueCommentsParams::test_timezone_formats PASSED                                                                                                                                         [ 62%]
tests/unit/schemas/test_issues.py::TestListIssueCommentsParams::test_invalid_datetime_format PASSED                                                                                                                                  [ 63%]
tests/unit/schemas/test_issues.py::TestListIssueCommentsParams::test_invalid_field_types PASSED                                                                                                                                      [ 63%]
tests/unit/schemas/test_issues.py::TestListIssueCommentsParams::test_invalid_page_values PASSED                                                                                                                                      [ 64%]
tests/unit/schemas/test_issues.py::TestListIssueCommentsParams::test_invalid_per_page_values PASSED                                                                                                                                  [ 64%]
tests/unit/schemas/test_responses.py::TestToolResponse::test_valid_data PASSED                                                                                                                                                       [ 64%]
tests/unit/schemas/test_responses.py::TestToolResponse::test_minimal_valid_data PASSED                                                                                                                                               [ 65%]
tests/unit/schemas/test_responses.py::TestToolResponse::test_missing_required_fields PASSED                                                                                                                                          [ 65%]
tests/unit/schemas/test_responses.py::TestToolResponse::test_invalid_content_type PASSED                                                                                                                                             [ 66%]
tests/unit/schemas/test_responses.py::TestToolResponse::test_empty_content_list PASSED                                                                                                                                               [ 66%]
tests/unit/schemas/test_responses.py::TestToolResponse::test_is_error_values PASSED                                                                                                                                                  [ 67%]
tests/unit/schemas/test_responses.py::TestTextContent::test_valid_data PASSED                                                                                                                                                        [ 67%]
tests/unit/schemas/test_responses.py::TestTextContent::test_missing_required_fields PASSED                                                                                                                                           [ 67%]
tests/unit/schemas/test_responses.py::TestTextContent::test_invalid_type_value PASSED                                                                                                                                                [ 68%]
tests/unit/schemas/test_responses.py::TestTextContent::test_empty_text PASSED                                                                                                                                                        [ 68%]
tests/unit/schemas/test_responses.py::TestErrorContent::test_valid_data PASSED                                                                                                                                                       [ 69%]
tests/unit/schemas/test_responses.py::TestErrorContent::test_missing_required_fields PASSED                                                                                                                                          [ 69%]
tests/unit/schemas/test_responses.py::TestErrorContent::test_invalid_type_value PASSED                                                                                                                                               [ 70%]
tests/unit/schemas/test_responses.py::TestErrorContent::test_empty_text PASSED                                                                                                                                                       [ 70%]
tests/unit/schemas/test_responses.py::TestResponseContent::test_text_content PASSED                                                                                                                                                  [ 71%]
tests/unit/schemas/test_responses.py::TestResponseContent::test_error_content PASSED                                                                                                                                                 [ 71%]
tests/unit/utils/test_environment.py::TestGetGithubToken::test_with_token_in_env PASSED                                                                                                                                              [ 71%]
tests/unit/utils/test_environment.py::TestGetGithubToken::test_without_token_in_env PASSED                                                                                                                                           [ 72%]
tests/unit/utils/test_environment.py::TestGetEnvVar::test_with_var_in_env PASSED                                                                                                                                                     [ 72%]
tests/unit/utils/test_environment.py::TestGetEnvVar::test_without_var_in_env_no_default PASSED                                                                                                                                       [ 73%]
tests/unit/utils/test_environment.py::TestGetEnvVar::test_without_var_in_env_with_default PASSED                                                                                                                                     [ 73%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[true-True] PASSED                                                                                                                               [ 74%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[True-True] PASSED                                                                                                                               [ 74%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[TRUE-True] PASSED                                                                                                                               [ 75%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[1-True] PASSED                                                                                                                                  [ 75%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[yes-True] PASSED                                                                                                                                [ 75%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[Yes-True] PASSED                                                                                                                                [ 76%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[YES-True] PASSED                                                                                                                                [ 76%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[false-False] PASSED                                                                                                                             [ 77%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[False-False] PASSED                                                                                                                             [ 77%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[FALSE-False] PASSED                                                                                                                             [ 78%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[0-False] PASSED                                                                                                                                 [ 78%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[no-False] PASSED                                                                                                                                [ 78%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[No-False] PASSED                                                                                                                                [ 79%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_valid_bool_values[NO-False] PASSED                                                                                                                                [ 79%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_with_invalid_bool_value PASSED                                                                                                                                         [ 80%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_without_var_in_env_no_default PASSED                                                                                                                                   [ 80%]
tests/unit/utils/test_environment.py::TestGetBoolEnvVar::test_without_var_in_env_with_default PASSED                                                                                                                                 [ 81%]
tests/integration/client/test_client.py::test_singleton_pattern PASSED                                                                                                                                                               [ 81%]
tests/integration/client/test_client.py::test_direct_instantiation PASSED                                                                                                                                                            [ 82%]
tests/integration/client/test_client.py::test_github_property PASSED                                                                                                                                                                 [ 82%]
tests/integration/client/test_client.py::test_get_repo_success PASSED                                                                                                                                                                [ 82%]
tests/integration/client/test_client.py::test_get_repo_not_found 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:37 [   ERROR] GitHub exception when getting repo AstroMined/nonexistent-repo-20250302104537: 404 {"message": "Not Found", "documentation_url": "https://docs.github.com/rest/repos/repos#get-a-repository", "status": "404"} (client.py:128)
2025-03-02 10:45:37 [   ERROR] Handling GitHub exception: status=404, data={'message': 'Not Found', 'documentation_url': 'https://docs.github.com/rest/repos/repos#get-a-repository', 'status': '404'} (handlers.py:70)
2025-03-02 10:45:37 [   ERROR] Resource not found (handlers.py:119)
PASSED                                                                                                                                                                                                                               [ 83%]
tests/integration/client/test_client.py::test_get_repo_invalid_name 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:38 [   ERROR] GitHub exception when getting repo invalid/repo/name: 404 {"message": "Not Found", "documentation_url": "https://docs.github.com/rest", "status": "404"} (client.py:128)
2025-03-02 10:45:38 [   ERROR] Handling GitHub exception: status=404, data={'message': 'Not Found', 'documentation_url': 'https://docs.github.com/rest', 'status': '404'} (handlers.py:70)
2025-03-02 10:45:38 [   ERROR] Resource not found (handlers.py:119)
PASSED                                                                                                                                                                                                                               [ 83%]
tests/integration/client/test_rate_limit.py::test_check_rate_limit PASSED                                                                                                                                                            [ 84%]
tests/integration/client/test_rate_limit.py::test_wait_for_rate_limit_reset 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:38 [    INFO] Rate limit reset time is in the past. Waiting 1 seconds. (rate_limit.py:55)
2025-03-02 10:45:39 [    INFO] Rate limit exceeded. Waiting 3.0 seconds until reset. (rate_limit.py:51)
PASSED                                                                                                                                                                                                                               [ 84%]
tests/integration/client/test_rate_limit.py::test_exponential_backoff PASSED                                                                                                                                                         [ 85%]
tests/integration/client/test_rate_limit.py::test_handle_rate_limit_with_backoff 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:42 [   ERROR] Maximum retry attempts (2) exceeded for rate limit (rate_limit.py:110)
2025-03-02 10:45:42 [    INFO] Test mode: Using short delay instead of waiting for reset: 0.1 seconds. (rate_limit.py:116)
2025-03-02 10:45:42 [    INFO] Test mode: Using short delay instead of waiting for reset: 0.2 seconds. (rate_limit.py:116)
2025-03-02 10:45:42 [    INFO] Test mode: Using short delay instead of waiting for reset: 0.4 seconds. (rate_limit.py:116)
PASSED                                                                                                                                                                                                                               [ 85%]
tests/integration/errors/test_handlers_integration.py::test_handle_github_exception_not_found 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:43 [   ERROR] Handling GitHub exception: status=404, data={'message': 'Not Found', 'documentation_url': 'https://docs.github.com/rest/repos/repos#get-a-repository', 'status': '404'} (handlers.py:70)
2025-03-02 10:45:43 [   ERROR] Resource not found (handlers.py:119)
PASSED                                                                                                                                                                                                                               [ 85%]
tests/integration/errors/test_handlers_integration.py::test_handle_github_exception_invalid_input 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:44 [   ERROR] Handling GitHub exception: status=422, data={'message': 'Validation Failed', 'errors': [{'resource': 'Issue', 'code': 'missing_field', 'field': 'title'}], 'documentation_url': 'https://docs.github.com/rest/issues/issues#create-an-issue', 'status': '422'} (handlers.py:70)
2025-03-02 10:45:44 [   ERROR] Validation error (handlers.py:127)
PASSED                                                                                                                                                                                                                               [ 86%]
tests/integration/errors/test_handlers_integration.py::test_handle_github_exception_rate_limit 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:45:44 [   ERROR] Rate limit exceeded (handlers.py:41)
FAILED                                                                                                                                                                                                                               [ 86%]
tests/integration/errors/test_handlers_integration.py::test_format_validation_error PASSED                                                                                                                                           [ 87%]
tests/integration/errors/test_handlers_integration.py::test_format_validation_error_no_errors PASSED                                                                                                                                 [ 87%]
tests/integration/errors/test_handlers_integration.py::test_format_validation_error_no_data PASSED                                                                                                                                   [ 88%]
tests/integration/issues/test_comments.py::test_add_issue_comment PASSED                                                                                                                                                             [ 88%]
tests/integration/issues/test_comments.py::test_list_issue_comments PASSED                                                                                                                                                           [ 89%]
tests/integration/issues/test_comments.py::test_update_issue_comment PASSED                                                                                                                                                          [ 89%]
tests/integration/issues/test_comments.py::test_delete_issue_comment PASSED                                                                                                                                                          [ 89%]
tests/integration/issues/test_comments.py::test_list_issue_comments_since FAILED                                                                                                                                                     [ 90%]
tests/integration/issues/test_comments.py::test_comment_lifecycle PASSED                                                                                                                                                             [ 90%]
tests/integration/issues/test_create.py::test_create_issue_required_params PASSED                                                                                                                                                    [ 91%]
tests/integration/issues/test_create.py::test_create_issue_all_params PASSED                                                                                                                                                         [ 91%]
tests/integration/issues/test_create.py::test_create_and_verify_issue PASSED                                                                                                                                                         [ 92%]
tests/integration/issues/test_labels.py::test_add_issue_labels PASSED                                                                                                                                                                [ 92%]
tests/integration/issues/test_labels.py::test_remove_issue_label PASSED                                                                                                                                                              [ 92%]
tests/integration/issues/test_labels.py::test_add_issue_labels_multiple_calls PASSED                                                                                                                                                 [ 93%]
tests/integration/issues/test_labels.py::test_remove_nonexistent_label 
-------------------------------------------------------------------------------------------------------------- live log call ---------------------------------------------------------------------------------------------------------------
2025-03-02 10:47:10 [ WARNING] Label 'nonexistent-test-20250302104707-01bdef0c' does not exist on issue #148 (issues.py:507)
PASSED                                                                                                                                                                                                                               [ 93%]
tests/integration/issues/test_labels.py::test_label_lifecycle PASSED                                                                                                                                                                 [ 94%]
tests/integration/issues/test_lifecycle.py::test_issue_lifecycle PASSED                                                                                                                                                              [ 94%]
tests/integration/issues/test_list.py::test_list_issues_basic PASSED                                                                                                                                                                 [ 95%]
tests/integration/issues/test_list.py::test_list_issues_state_filter PASSED                                                                                                                                                          [ 95%]
tests/integration/issues/test_list.py::test_list_issues_pagination FAILED                                                                                                                                                            [ 96%]
tests/integration/issues/test_list.py::test_list_issues_labels_filter FAILED                                                                                                                                                         [ 96%]
tests/integration/issues/test_list.py::test_list_issues_sort_and_direction PASSED                                                                                                                                                    [ 96%]
tests/integration/issues/test_list.py::test_list_issues_since FAILED                                                                                                                                                                 [ 97%]
tests/integration/issues/test_update.py::test_update_issue_title PASSED                                                                                                                                                              [ 97%]
tests/integration/issues/test_update.py::test_update_issue_body PASSED                                                                                                                                                               [ 98%]
tests/integration/issues/test_update.py::test_update_issue_state PASSED                                                                                                                                                              [ 98%]
tests/integration/issues/test_update.py::test_update_issue_labels PASSED                                                                                                                                                             [ 99%]
tests/integration/issues/test_update.py::test_update_issue_multiple_fields PASSED                                                                                                                                                    [ 99%]
tests/integration/issues/test_update.py::test_update_issue_no_changes PASSED                                                                                                                                                         [100%]

================================================================================================================= FAILURES =================================================================================================================
_________________________________________________________________________________________________ test_handle_github_exception_rate_limit __________________________________________________________________________________________________
tests/integration/errors/test_handlers_integration.py:90: in test_handle_github_exception_rate_limit
    assert error.reset_at is not None or error.reset_timestamp is not None
E   AssertionError: assert (None is not None or None is not None)
E    +  where None = GitHubRateLimitError('API rate limit exceeded (0/None calls remaining)').reset_at
E    +  and   None = GitHubRateLimitError('API rate limit exceeded (0/None calls remaining)').reset_timestamp
----------------------------------------------------------------------------------------------------------- Captured stderr call -----------------------------------------------------------------------------------------------------------
2025-03-02 10:45:44,071 - pygithub_mcp_server.errors.handlers - ERROR - Rate limit exceeded
------------------------------------------------------------------------------------------------------------ Captured log call -------------------------------------------------------------------------------------------------------------
ERROR    pygithub_mcp_server.errors.handlers:handlers.py:41 Rate limit exceeded
______________________________________________________________________________________________________ test_list_issue_comments_since ______________________________________________________________________________________________________
tests/integration/issues/test_comments.py:315: in test_list_issue_comments_since
    assert c["id"] != comment["id"], "Comment found with future since filter"
E   AssertionError: Comment found with future since filter
E   assert 2692788952 != 2692788952
----------------------------------------------------------------------------------------------------------- Captured stdout call -----------------------------------------------------------------------------------------------------------

update_issue called with title=None
Got issue with title: Test Issue (List Comments Since) test-20250302104612-0a2c07be
kwargs for edit: {'state': 'closed'}
After edit, updated_issue.title: Test Issue (List Comments Since) test-20250302104612-0a2c07be
Converted result: {'id': 2889625794, 'issue_number': 140, 'title': 'Test Issue (List Comments Since) test-20250302104612-0a2c07be', 'body': None, 'state': 'closed', 'state_reason': 'completed', 'locked': False, 'active_lock_reason': None, 'comments': 1, 'created_at': '2025-03-02T15:46:13+00:00', 'updated_at': '2025-03-02T15:46:19+00:00', 'closed_at': '2025-03-02T15:46:19+00:00', 'author_association': 'OWNER', 'user': {'login': 'AstroMined', 'id': 67924737, 'type': 'User', 'site_admin': False}, 'assignee': None, 'assignees': [], 'milestone': None, 'labels': [], 'url': 'https://api.github.com/repos/AstroMined/mcp-testing/issues/140', 'html_url': 'https://github.com/AstroMined/mcp-testing/issues/140', 'repository': {'full_name': 'AstroMined/mcp-testing', 'name': 'mcp-testing', 'owner': 'AstroMined'}}
_______________________________________________________________________________________________________ test_list_issues_pagination ________________________________________________________________________________________________________
tests/integration/issues/test_list.py:199: in test_list_issues_pagination
    assert len(page1) <= 1  # Should respect per_page=1
E   AssertionError: assert 19 <= 1
E    +  where 19 = len([{'active_lock_reason': None, 'assignee': None, 'assignees': [], 'author_association': 'OWNER', ...}, {'active_lock_reason': None, 'assignee': None, 'assignees': [], 'author_association': 'OWNER', ...}, {'active_lock_reason': None, 'assignee': None, 'assignees': [], 'author_association': 'OWNER', ...}, {'active_lock_reason': None, 'assignee': None, 'assignees': [], 'author_association': 'OWNER', ...}, {'active_lock_reason': None, 'assignee': None, 'assignees': [], 'author_association': 'OWNER', ...}, {'active_lock_reason': None, 'assignee': None, 'assignees': [], 'author_association': 'OWNER', ...}, ...])
----------------------------------------------------------------------------------------------------------- Captured stdout call -----------------------------------------------------------------------------------------------------------

update_issue called with title=None
Got issue with title: Test Issue (Pagination) test-20250302105213-c8d005b5
kwargs for edit: {'state': 'closed'}
After edit, updated_issue.title: Test Issue (Pagination) test-20250302105213-c8d005b5
Converted result: {'id': 2889628797, 'issue_number': 154, 'title': 'Test Issue (Pagination) test-20250302105213-c8d005b5', 'body': None, 'state': 'closed', 'state_reason': 'completed', 'locked': False, 'active_lock_reason': None, 'comments': 0, 'created_at': '2025-03-02T15:52:14+00:00', 'updated_at': '2025-03-02T15:54:34+00:00', 'closed_at': '2025-03-02T15:54:34+00:00', 'author_association': 'OWNER', 'user': {'login': 'AstroMined', 'id': 67924737, 'type': 'User', 'site_admin': False}, 'assignee': None, 'assignees': [], 'milestone': None, 'labels': [], 'url': 'https://api.github.com/repos/AstroMined/mcp-testing/issues/154', 'html_url': 'https://github.com/AstroMined/mcp-testing/issues/154', 'repository': {'full_name': 'AstroMined/mcp-testing', 'name': 'mcp-testing', 'owner': 'AstroMined'}}
______________________________________________________________________________________________________ test_list_issues_labels_filter ______________________________________________________________________________________________________
tests/integration/issues/test_list.py:292: in test_list_issues_labels_filter
    assert i["issue_number"] != issue["issue_number"], "Issue found with non-existent label"
E   AssertionError: Issue found with non-existent label
E   assert 155 != 155
----------------------------------------------------------------------------------------------------------- Captured stdout call -----------------------------------------------------------------------------------------------------------

update_issue called with title=None
Got issue with title: Test Issue (Labels Filter) test-20250302105435-4946c94d
kwargs for edit: {'labels': ['bug', 'test-label']}
After edit, updated_issue.title: Test Issue (Labels Filter) test-20250302105435-4946c94d
Converted result: {'id': 2889629958, 'issue_number': 155, 'title': 'Test Issue (Labels Filter) test-20250302105435-4946c94d', 'body': None, 'state': 'open', 'state_reason': None, 'locked': False, 'active_lock_reason': None, 'comments': 0, 'created_at': '2025-03-02T15:54:36+00:00', 'updated_at': '2025-03-02T15:54:38+00:00', 'closed_at': None, 'author_association': 'OWNER', 'user': {'login': 'AstroMined', 'id': 67924737, 'type': 'User', 'site_admin': False}, 'assignee': None, 'assignees': [], 'milestone': None, 'labels': [{'id': 8172388006, 'name': 'bug', 'description': "Something isn't working", 'color': 'd73a4a'}, {'id': 8224817342, 'name': 'test-label', 'description': None, 'color': 'ededed'}], 'url': 'https://api.github.com/repos/AstroMined/mcp-testing/issues/155', 'html_url': 'https://github.com/AstroMined/mcp-testing/issues/155', 'repository': {'full_name': 'AstroMined/mcp-testing', 'name': 'mcp-testing', 'owner': 'AstroMined'}}

update_issue called with title=None
Got issue with title: Test Issue (Labels Filter) test-20250302105435-4946c94d
kwargs for edit: {'state': 'closed'}
After edit, updated_issue.title: Test Issue (Labels Filter) test-20250302105435-4946c94d
Converted result: {'id': 2889629958, 'issue_number': 155, 'title': 'Test Issue (Labels Filter) test-20250302105435-4946c94d', 'body': None, 'state': 'closed', 'state_reason': 'completed', 'locked': False, 'active_lock_reason': None, 'comments': 0, 'created_at': '2025-03-02T15:54:36+00:00', 'updated_at': '2025-03-02T15:55:28+00:00', 'closed_at': '2025-03-02T15:55:28+00:00', 'author_association': 'OWNER', 'user': {'login': 'AstroMined', 'id': 67924737, 'type': 'User', 'site_admin': False}, 'assignee': None, 'assignees': [], 'milestone': None, 'labels': [{'id': 8172388006, 'name': 'bug', 'description': "Something isn't working", 'color': 'd73a4a'}, {'id': 8224817342, 'name': 'test-label', 'description': None, 'color': 'ededed'}], 'url': 'https://api.github.com/repos/AstroMined/mcp-testing/issues/155', 'html_url': 'https://github.com/AstroMined/mcp-testing/issues/155', 'repository': {'full_name': 'AstroMined/mcp-testing', 'name': 'mcp-testing', 'owner': 'AstroMined'}}
__________________________________________________________________________________________________________ test_list_issues_since __________________________________________________________________________________________________________
tests/integration/issues/test_list.py:443: in test_list_issues_since
    assert i["issue_number"] != issue["issue_number"], "Issue found with future since filter"
E   AssertionError: Issue found with future since filter
E   assert 158 != 158
----------------------------------------------------------------------------------------------------------- Captured stdout call -----------------------------------------------------------------------------------------------------------

update_issue called with title=None
Got issue with title: Test Issue (Since) test-20250302105611-9e18628a
kwargs for edit: {'state': 'closed'}
After edit, updated_issue.title: Test Issue (Since) test-20250302105611-9e18628a
Converted result: {'id': 2889630755, 'issue_number': 158, 'title': 'Test Issue (Since) test-20250302105611-9e18628a', 'body': None, 'state': 'closed', 'state_reason': 'completed', 'locked': False, 'active_lock_reason': None, 'comments': 0, 'created_at': '2025-03-02T15:56:12+00:00', 'updated_at': '2025-03-02T15:56:17+00:00', 'closed_at': '2025-03-02T15:56:17+00:00', 'author_association': 'OWNER', 'user': {'login': 'AstroMined', 'id': 67924737, 'type': 'User', 'site_admin': False}, 'assignee': None, 'assignees': [], 'milestone': None, 'labels': [], 'url': 'https://api.github.com/repos/AstroMined/mcp-testing/issues/158', 'html_url': 'https://github.com/AstroMined/mcp-testing/issues/158', 'repository': {'full_name': 'AstroMined/mcp-testing', 'name': 'mcp-testing', 'owner': 'AstroMined'}}

---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                                                              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------------------------------------
src/pygithub_mcp_server/__init__.py                                   4      0      0      0   100%
src/pygithub_mcp_server/__main__.py                                   3      3      0      0     0%   6-10
src/pygithub_mcp_server/client/__init__.py                            3      0      0      0   100%
src/pygithub_mcp_server/client/client.py                             54      3     10      3    91%   60, 91, 94
src/pygithub_mcp_server/client/rate_limit.py                         53     14     18      2    69%   32-34, 46->49, 121-137
src/pygithub_mcp_server/converters/__init__.py                        9      0      0      0   100%
src/pygithub_mcp_server/converters/common/__init__.py                 2      0      0      0   100%
src/pygithub_mcp_server/converters/common/datetime.py                20      0     14      2    94%   52->67, 62->67
src/pygithub_mcp_server/converters/issues/__init__.py                 3      0      0      0   100%
src/pygithub_mcp_server/converters/issues/comments.py                 6      0      0      0   100%
src/pygithub_mcp_server/converters/issues/issues.py                  16      0      2      0   100%
src/pygithub_mcp_server/converters/parameters.py                     59     11     46      1    79%   19-30, 45->49
src/pygithub_mcp_server/converters/repositories/__init__.py           3      0      0      0   100%
src/pygithub_mcp_server/converters/repositories/contents.py           4      1      0      0    75%   24
src/pygithub_mcp_server/converters/repositories/repositories.py       4      1      0      0    75%   24
src/pygithub_mcp_server/converters/responses.py                      16      1      8      1    92%   38
src/pygithub_mcp_server/converters/users/__init__.py                  2      0      0      0   100%
src/pygithub_mcp_server/converters/users/users.py                     6      0      2      0   100%
src/pygithub_mcp_server/errors/__init__.py                            4      0      0      0   100%
src/pygithub_mcp_server/errors/exceptions.py                         21      0      0      0   100%
src/pygithub_mcp_server/errors/formatters.py                         22      0     14      1    97%   33->47
src/pygithub_mcp_server/errors/handlers.py                           97     11     44      5    89%   56-58, 83, 85, 87, 107-110, 121->125, 132-134
src/pygithub_mcp_server/operations/__init__.py                        2      0      0      0   100%
src/pygithub_mcp_server/operations/issues.py                        221     59     68     15    74%   64-68, 76-77, 99-100, 155-159, 180-181, 221, 225, 229, 234, 238, 240, 245, 247, 273-285, 293-294, 306-313, 339-340, 376->380, 387, 389, 396-397, 425-426, 447-448, 480-481, 511-513
src/pygithub_mcp_server/schemas/__init__.py                           8      0      0      0   100%
src/pygithub_mcp_server/schemas/base.py                              27      0      6      0   100%
src/pygithub_mcp_server/schemas/issues.py                           176      0     44      1    99%   259->264
src/pygithub_mcp_server/schemas/pull_requests.py                     10      0      0      0   100%
src/pygithub_mcp_server/schemas/repositories.py                      34      0      0      0   100%
src/pygithub_mcp_server/schemas/responses.py                         21      0      2      0   100%
src/pygithub_mcp_server/schemas/search.py                            14      0      0      0   100%
src/pygithub_mcp_server/server.py                                   175    135      2      1    23%   32, 73-98, 122-149, 168-187, 212-237, 257-277, 299-321, 342-363, 383-403, 423-443, 463-483
src/pygithub_mcp_server/utils/__init__.py                             2      0      0      0   100%
src/pygithub_mcp_server/utils/environment.py                         52      6     30      6    83%   29, 34-37, 44->exit, 109, 112, 114->121
src/pygithub_mcp_server/version.py                                   10      2      0      0    80%   48, 56
-------------------------------------------------------------------------------------------------------------
TOTAL                                                              1163    247    310     38    79%
Coverage HTML written to dir coverage_html

========================================================================================================= short test summary info ==========================================================================================================
FAILED tests/integration/errors/test_handlers_integration.py::test_handle_github_exception_rate_limit - AssertionError: assert (None is not None or None is not None)
FAILED tests/integration/issues/test_comments.py::test_list_issue_comments_since - AssertionError: Comment found with future since filter
FAILED tests/integration/issues/test_list.py::test_list_issues_pagination - AssertionError: assert 19 <= 1
FAILED tests/integration/issues/test_list.py::test_list_issues_labels_filter - AssertionError: Issue found with non-existent label
FAILED tests/integration/issues/test_list.py::test_list_issues_since - AssertionError: Issue found with future since filter
================================================================================================ 5 failed, 223 passed in 687.73s (0:11:27)
```
