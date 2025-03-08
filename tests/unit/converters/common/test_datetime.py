"""Tests for datetime conversion functions.

This module tests the datetime conversion functions used to convert between
datetime objects and ISO format strings.
"""

import pytest
import functools
from datetime import datetime, timezone, timedelta

from pygithub_mcp_server.converters.common.datetime import (
    convert_datetime,
    convert_iso_string_to_datetime,
    ensure_utc_datetime,
    with_utc_datetimes
)


class TestConvertDatetime:
    """Tests for convert_datetime function."""

    def test_convert_datetime_with_datetime(self):
        """Test converting a datetime to ISO string."""
        dt = datetime(2023, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        result = convert_datetime(dt)
        assert result == "2023-01-15T12:30:45+00:00"
    
    def test_convert_datetime_with_none(self):
        """Test converting None to ISO string."""
        result = convert_datetime(None)
        assert result is None


class TestConvertIsoStringToDatetime:
    """Tests for convert_iso_string_to_datetime function."""

    def test_with_datetime_object(self):
        """Test with datetime object (should return as-is)."""
        dt = datetime(2023, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        result = convert_iso_string_to_datetime(dt)
        assert result is dt
    
    def test_with_z_timezone(self):
        """Test with Z timezone format."""
        result = convert_iso_string_to_datetime("2023-01-15T12:30:45Z")
        expected = datetime(2023, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        assert result == expected
    
    def test_with_offset_timezone_with_colon(self):
        """Test with standard offset timezone with colon."""
        result = convert_iso_string_to_datetime("2023-01-15T12:30:45+02:00")
        expected = datetime(2023, 1, 15, 12, 30, 45, 
                           tzinfo=timezone(timedelta(hours=2)))
        assert result.year == expected.year
        assert result.month == expected.month
        assert result.day == expected.day
        assert result.hour == expected.hour
        assert result.minute == expected.minute
        assert result.second == expected.second
        assert result.tzinfo is not None
        assert result.utcoffset() == expected.utcoffset()
    
    def test_with_offset_timezone_without_colon(self):
        """Test with offset timezone without colon."""
        result = convert_iso_string_to_datetime("2023-01-15T12:30:45-0500")
        expected = datetime(2023, 1, 15, 12, 30, 45, 
                           tzinfo=timezone(timedelta(hours=-5)))
        assert result.utcoffset() == expected.utcoffset()
    
    def test_with_short_timezone(self):
        """Test with short timezone format (hours only)."""
        result = convert_iso_string_to_datetime("2023-01-15T12:30:45+05")
        expected = datetime(2023, 1, 15, 12, 30, 45, 
                           tzinfo=timezone(timedelta(hours=5)))
        assert result.utcoffset() == expected.utcoffset()
    
    def test_with_single_digit_timezone(self):
        """Test with single digit timezone format."""
        result = convert_iso_string_to_datetime("2023-01-15T12:30:45+5")
        expected = datetime(2023, 1, 15, 12, 30, 45, 
                           tzinfo=timezone(timedelta(hours=5)))
        assert result.utcoffset() == expected.utcoffset()

    def test_invalid_type(self):
        """Test with invalid type (not string or datetime)."""
        with pytest.raises(ValueError) as exc_info:
            convert_iso_string_to_datetime(123)
        assert "Expected string or datetime" in str(exc_info.value)
    
    def test_short_string(self):
        """Test with too short string that can't be a date."""
        with pytest.raises(ValueError) as exc_info:
            convert_iso_string_to_datetime("abc")
        assert "Invalid date format" in str(exc_info.value)
    
    def test_datetime_without_timezone_handling(self):
        """Test that datetime without timezone remains naive."""
        result = convert_iso_string_to_datetime("2023-01-15T12:30:45")
        # Verify it keeps the time components
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 12
        assert result.minute == 30
        assert result.second == 45
        # For convert_iso_string_to_datetime, the result should stay naive
        assert result.tzinfo is None
    
    def test_date_only_format_handling(self):
        """Test that date-only format is handled as naive datetime."""
        result = convert_iso_string_to_datetime("2023-01-15")
        # Verify it creates a valid datetime with default time values
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 15
        # Default time should be midnight
        assert result.hour == 0
        assert result.minute == 0 
        assert result.second == 0
        # Should be a naive datetime
        assert result.tzinfo is None
    
    def test_malformed_datetime(self):
        """Test with malformed datetime string."""
        with pytest.raises(ValueError) as exc_info:
            convert_iso_string_to_datetime("2023-13-40T99:99:99Z")
        assert "Invalid isoformat string" in str(exc_info.value)


class TestEnsureUtcDatetime:
    """Tests for ensure_utc_datetime function."""
    
    def test_with_string(self):
        """Test with ISO format string."""
        result = ensure_utc_datetime("2023-01-15T12:30:45Z")
        expected = datetime(2023, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        assert result == expected
        assert result.tzinfo == timezone.utc
    
    def test_ensure_utc_with_naive_datetime_string(self):
        """Test that ensure_utc_datetime adds UTC timezone to naive datetime string."""
        # Pass a naive datetime string directly to ensure_utc_datetime
        result = ensure_utc_datetime("2023-01-15T12:30:45")
        
        # Should have UTC timezone
        assert result.tzinfo is not None
        assert result.tzinfo == timezone.utc
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 12
        assert result.minute == 30
        assert result.second == 45
    
    def test_ensure_utc_with_naive_datetime(self):
        """Test that ensure_utc_datetime adds UTC timezone to naive datetime object."""
        # Create a naive datetime using convert_iso_string_to_datetime
        naive_dt = convert_iso_string_to_datetime("2023-01-15T12:30:45")
        assert naive_dt.tzinfo is None  # Verify it's naive
        
        # Now pass to ensure_utc_datetime
        result = ensure_utc_datetime(naive_dt)
        
        # Should now have UTC timezone
        assert result.tzinfo is not None
        assert result.tzinfo == timezone.utc
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 12
        assert result.minute == 30
        assert result.second == 45
    
    def test_ensure_utc_with_date_only_string(self):
        """Test that ensure_utc_datetime handles date-only strings correctly."""
        # Pass a date-only string to ensure_utc_datetime
        result = ensure_utc_datetime("2023-01-15")
        
        # Should have UTC timezone and midnight time
        assert result.tzinfo is not None
        assert result.tzinfo == timezone.utc
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0
    
    def test_with_naive_datetime(self):
        """Test with naive datetime object (no timezone)."""
        dt = datetime(2023, 1, 15, 12, 30, 45)
        result = ensure_utc_datetime(dt)
        assert result.tzinfo == timezone.utc
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 12
        assert result.minute == 30
        assert result.second == 45
    
    def test_with_non_utc_timezone(self):
        """Test with non-UTC timezone."""
        # Create a datetime with non-UTC timezone
        non_utc_tz = timezone(timedelta(hours=5))
        dt = datetime(2023, 1, 15, 12, 30, 45, tzinfo=non_utc_tz)
        
        # Ensure UTC conversion
        result = ensure_utc_datetime(dt)
        
        # Should be converted to UTC (5 hours earlier)
        assert result.tzinfo == timezone.utc
        assert result.hour == 7  # 12 - 5 = 7
    
    def test_microseconds_truncation(self):
        """Test that microseconds are truncated."""
        dt = datetime(2023, 1, 15, 12, 30, 45, 123456, tzinfo=timezone.utc)
        result = ensure_utc_datetime(dt)
        assert result.microsecond == 0


class TestWithUtcDatetimes:
    """Tests for with_utc_datetimes decorator."""
    
    def test_all_datetime_params(self):
        """Test decorator with all params conversion."""
        @with_utc_datetimes()
        def test_func(dt1, dt2=None, regular_param="value"):
            return {
                "dt1": dt1,
                "dt2": dt2,
                "regular_param": regular_param
            }
        
        # Call with datetime string and datetime object
        result = test_func(
            dt1="2023-01-15T12:30:45Z", 
            dt2=datetime(2023, 1, 15, 10, 0, 0)
        )
        
        # Both should be converted to UTC timezone-aware datetimes
        assert isinstance(result["dt1"], datetime)
        assert result["dt1"].tzinfo == timezone.utc
        assert isinstance(result["dt2"], datetime)
        assert result["dt2"].tzinfo == timezone.utc
        
        # Regular param should be untouched
        assert result["regular_param"] == "value"
    
    def test_specific_param_names(self):
        """Test decorator with specific param names."""
        @with_utc_datetimes(param_names=["only_this_param"])
        def test_func(only_this_param, not_this_param=None):
            return {
                "only_this_param": only_this_param,
                "not_this_param": not_this_param
            }
        
        # Call with both params as datetime strings
        result = test_func(
            only_this_param="2023-01-15T12:30:45Z",
            not_this_param="2023-01-15T12:30:45Z"
        )
        
        # Only the specified param should be converted
        assert isinstance(result["only_this_param"], datetime)
        assert result["only_this_param"].tzinfo == timezone.utc
        
        # The other param should remain a string
        assert isinstance(result["not_this_param"], str)
    
    def test_original_function_name_and_docs(self):
        """Test that decorator preserves function name and docstring."""
        def original_func(dt_param):
            """Test docstring."""
            return dt_param
        
        decorated_func = with_utc_datetimes()(original_func)
        
        assert decorated_func.__name__ == original_func.__name__
        assert decorated_func.__doc__ == original_func.__doc__
