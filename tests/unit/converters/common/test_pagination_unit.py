"""Unit tests for pagination utilities.

This module contains tests for the pagination utility functions without using mocks,
following the approach outlined in ADR-002: Real API Testing.
"""

import pytest
from dataclasses import dataclass
from typing import List, Optional, Any, Union

from pygithub_mcp_server.converters.common.pagination import get_paginated_slice, get_paginated_items


@dataclass
class MockPaginatedItem:
    """Simple dataclass for items in a paginated list."""
    id: int
    name: str


class PaginatedListFixture:
    """A dataclass-based PaginatedList substitute for testing.
    
    This adheres to the ADR-002 guidance on using dataclasses instead of mocks.
    """
    
    def __init__(self, items: Optional[List[Any]] = None, total_count: Optional[int] = None):
        """Initialize the test paginated list.
        
        Args:
            items: Optional list of items
            total_count: Optional total count (defaults to len(items))
        """
        self.items = items or []
        self.totalCount = total_count if total_count is not None else len(self.items)
    
    def __getitem__(self, index: Union[int, slice]) -> Union[Any, List[Any]]:
        """Implement getitem to simulate PaginatedList behavior.
        
        Args:
            index: Integer index or slice
            
        Returns:
            Item or list of items
            
        Raises:
            IndexError: If index is out of range
        """
        if isinstance(index, slice):
            start = index.start or 0
            stop = index.stop or len(self.items)
            # Simulate IndexError for invalid ranges
            if start >= len(self.items):
                raise IndexError("list index out of range")
            return self.items[start:stop]
        else:
            if index >= len(self.items):
                raise IndexError("list index out of range")
            return self.items[index]
    
    def get_page(self, page_index: int) -> List[Any]:
        """Simulate PyGithub's get_page method.
        
        Args:
            page_index: 0-based page index
            
        Returns:
            List of items for the requested page
            
        Raises:
            IndexError: If page index is out of range
        """
        # PyGithub uses 0-based indexing for get_page
        start = page_index * 30  # Default per_page is 30
        if start >= len(self.items):
            raise IndexError("Page index out of range")
        return self.items[start:start+30]


class TestPaginationUtilities:
    """Tests for the pagination utility functions."""

    def test_get_paginated_slice_normal_case(self):
        """Test get_paginated_slice with a normal case."""
        # Create test items
        items = [MockPaginatedItem(id=i, name=f"Item {i}") for i in range(5)]
        paginated_list = PaginatedListFixture(items)
        
        # Call the function
        result = get_paginated_slice(paginated_list, 0, 3)
        
        # Verify the result
        assert len(result) == 3
        assert result[0].id == 0
        assert result[1].id == 1
        assert result[2].id == 2

    def test_get_paginated_slice_empty_list(self):
        """Test get_paginated_slice with an empty list."""
        # Create an empty paginated list
        paginated_list = PaginatedListFixture([], total_count=0)
        
        # Call the function
        result = get_paginated_slice(paginated_list, 0, 3)
        
        # Verify the result is an empty list
        assert result == []

    def test_get_paginated_slice_index_error(self):
        """Test get_paginated_slice with an index error."""
        # Create a paginated list where accessing invalid indices raises IndexError
        items = [MockPaginatedItem(id=i, name=f"Item {i}") for i in range(3)]
        paginated_list = PaginatedListFixture(items)
        
        # Call the function with start index > list length
        result = get_paginated_slice(paginated_list, 5, 8)
        
        # Verify the result is an empty list
        assert result == []

    def test_get_paginated_items_with_page_and_per_page(self):
        """Test get_paginated_items with page and per_page."""
        # Create test items
        items = [MockPaginatedItem(id=i, name=f"Item {i}") for i in range(10)]
        paginated_list = PaginatedListFixture(items)
        
        # Call the function with page=2, per_page=3
        # This should get items 3,4,5 (0-indexed, page 2 starts at index 3)
        result = get_paginated_items(paginated_list, page=2, per_page=3)
        
        # Verify the result
        assert len(result) == 3
        assert result[0].id == 3
        assert result[1].id == 4
        assert result[2].id == 5

    def test_get_paginated_items_with_page_only(self):
        """Test get_paginated_items with page parameter only."""
        # Create test items - enough for multiple pages
        items = [MockPaginatedItem(id=i, name=f"Item {i}") for i in range(40)]
        paginated_list = PaginatedListFixture(items)
        
        # Call the function with page=2 only (should use default per_page=30)
        result = get_paginated_items(paginated_list, page=2)
        
        # Verify the result (page 2 should start at index 30)
        assert len(result) == 10  # Only 10 items left after page 1
        assert result[0].id == 30

    def test_get_paginated_items_with_per_page_only(self):
        """Test get_paginated_items with per_page parameter only."""
        # Create test items
        items = [MockPaginatedItem(id=i, name=f"Item {i}") for i in range(10)]
        paginated_list = PaginatedListFixture(items)
        
        # Call the function with per_page=5 only
        result = get_paginated_items(paginated_list, per_page=5)
        
        # Verify the result (should get first 5 items)
        assert len(result) == 5
        assert result[0].id == 0
        assert result[4].id == 4

    def test_get_paginated_items_no_parameters(self):
        """Test get_paginated_items with no pagination parameters."""
        # Create test items
        items = [MockPaginatedItem(id=i, name=f"Item {i}") for i in range(10)]
        paginated_list = PaginatedListFixture(items)
        
        # Call the function with no parameters
        result = get_paginated_items(paginated_list)
        
        # Verify the result (should get all items)
        assert len(result) == 10
        assert result[0].id == 0
        assert result[9].id == 9

    def test_get_paginated_items_empty_list(self):
        """Test get_paginated_items with an empty list."""
        # Create an empty paginated list
        paginated_list = PaginatedListFixture([], total_count=0)
        
        # Call the function
        result = get_paginated_items(paginated_list)
        
        # Verify the result is an empty list
        assert result == []

    def test_get_paginated_items_out_of_range_page(self):
        """Test get_paginated_items with a page that's out of range."""
        # Create test items
        items = [MockPaginatedItem(id=i, name=f"Item {i}") for i in range(10)]
        paginated_list = PaginatedListFixture(items)
        
        # Call the function with a page that's out of range
        result = get_paginated_items(paginated_list, page=100)
        
        # Verify the result is an empty list
        assert result == []
