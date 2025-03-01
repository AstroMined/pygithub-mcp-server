"""Response formatting utilities.

This module provides functions for formatting responses for MCP tools.
"""

from typing import Any, Dict, Union

from pygithub_mcp_server.schemas.responses import (
    ResponseContent,
    TextContent,
    ToolResponse,
)


def create_tool_response(
    data: Any, is_error: bool = False
) -> Dict[str, Union[list, bool]]:
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
    else:
        content = TextContent(type="text", text=str(data))

    return ToolResponse(
        content=[content.model_dump()],
        is_error=is_error,
    ).model_dump()
