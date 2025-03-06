"""Pagination utilities for PyGithub API responses.

This module provides functions for safely handling pagination of PyGithub
PaginatedList objects with proper error handling and bounds checking.
"""

import logging
from typing import Any, List, Optional, TypeVar, Generic, Dict, Union

from github.PaginatedList import PaginatedList

logger = logging.getLogger(__name__)

T = TypeVar('T')


def get_paginated_slice(paginated_list: PaginatedList, start: int, end: int) -> List[Any]:
    """Safely retrieve a slice of items from a PyGithub PaginatedList.
    
    Args:
        paginated_list: PyGithub PaginatedList object
        start: Start index (0-based)
        end: End index (exclusive)
        
    Returns:
        List of items from the paginated list
    """
    try:
        # Get total count if available to check bounds
        total_count = getattr(paginated_list, "totalCount", None)
        if total_count is not None and total_count == 0:
            logger.debug("Paginated list is empty (totalCount=0)")
            return []
            
        # Try to get the slice
        result = list(paginated_list[start:end])
        return result
    except IndexError:
        logger.debug(f"IndexError with slice {start}:{end}, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error retrieving slice {start}:{end}: {str(e)}")
        return []


def get_paginated_items(
    paginated_list: PaginatedList,
    page: Optional[int] = None,
    per_page: Optional[int] = None
) -> List[Any]:
    """Get items from a paginated list with flexible pagination options.
    
    Args:
        paginated_list: PyGithub PaginatedList object
        page: Page number (1-based, optional)
        per_page: Items per page (optional)
        
    Returns:
        List of items from the paginated list
    """
    logger.debug(f"Getting paginated items with page={page}, per_page={per_page}")
    
    try:
        if page is not None and per_page is not None:
            # Use both page and per_page for precise pagination
            start = (page - 1) * per_page  # Convert to 0-based indexing
            end = start + per_page
            logger.debug(f"Getting items for page {page} with {per_page} per page (indices {start}-{end})")
            return get_paginated_slice(paginated_list, start, end)
        elif page is not None:
            # Use default per_page value (30) with specified page
            try:
                items = paginated_list.get_page(page - 1)  # PyGithub uses 0-based indexing
                logger.debug(f"Getting items for page {page} with default items per page")
                return items
            except IndexError:
                logger.debug(f"IndexError with page {page}, returning empty list")
                return []
        elif per_page is not None:
            # Get just the first per_page items
            logger.debug(f"Getting first {per_page} items")
            return get_paginated_slice(paginated_list, 0, per_page)
        else:
            # No pagination, get all items (but handle empty lists)
            try:
                # Check if there are any items first
                total_count = getattr(paginated_list, "totalCount", None)
                if total_count is not None and total_count == 0:
                    logger.debug("No items found (totalCount=0)")
                    return []
                else:
                    items = list(paginated_list)
                    logger.debug(f"Got {len(items)} items")
                    return items
            except Exception as e:
                logger.error(f"Error retrieving all items: {str(e)}")
                return []
    except Exception as e:
        # Catch any unexpected errors to prevent crashes
        logger.error(f"Unexpected error in pagination: {str(e)}")
        return []
