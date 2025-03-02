"""Tests for datetime conversion functions.

This module tests the datetime conversion functions used to convert between
datetime objects and ISO format strings.
"""

import pytest
from datetime import datetime, timezone, timedelta

from pygithub_mcp_server.converters.common.datetime import (
    convert_datetime,
    convert_iso_string_to_datetime
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
