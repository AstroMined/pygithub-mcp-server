"""Response formatting utilities.

This module provides functions for formatting responses for MCP tools.
"""

import json
from typing import Any, Dict, Union, List, Optional

from pygithub_mcp_server.schemas.responses import (
    ResponseContent,
    TextContent,
    ToolResponse,
)


def create_tool_response(
    data: Any, is_error: bool = False
) -> Dict[str, Union[List[Dict[str, str]], bool]]:
    """Create a standardized tool response.

    Args:
        data: Response data to format
        is_error: Whether this is an error response

    Returns:
        Formatted tool response
    """
    content: ResponseContent
    if isinstance(data, str):
        content = TextContent(type="text", text=data)
    elif isinstance(data, dict) or isinstance(data, list):
        # Convert dict/list to JSON string
        content = TextContent(type="text", text=json.dumps(data, indent=2))
    elif data is None:
        # Convert None to JSON null
        content = TextContent(type="text", text=json.dumps(None))
    else:
        content = TextContent(type="text", text=str(data))

    return ToolResponse(
        content=[content.model_dump()],
        is_error=is_error,
    ).model_dump()


def create_error_response(error: Any) -> Dict[str, Union[List[Dict[str, str]], bool]]:
    """Create a standardized error response.

    Args:
        error: Error to format (string, exception, or dict)

    Returns:
        Formatted error response
    """
    # Convert exception to string if needed
    if not isinstance(error, (str, dict, list)):
        error = str(error)
    
    return create_tool_response(error, is_error=True)
