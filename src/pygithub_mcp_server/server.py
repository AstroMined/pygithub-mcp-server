"""PyGithub MCP Server implementation.

This module provides a FastMCP server that exposes GitHub API operations.
The server uses a modular architecture to organize tools into logical groups
that can be selectively enabled or disabled through configuration.
"""

import logging
import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from pygithub_mcp_server.config import load_config
from pygithub_mcp_server.tools import load_tools
from pygithub_mcp_server.version import VERSION

# Set up logging
log_dir = Path(__file__).parent.parent.parent / 'logs'
if not log_dir.exists():
    os.makedirs(log_dir)

log_file = log_dir / 'pygithub_mcp_server.log'
logger = logging.getLogger()  # Get root logger
logger.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stderr)
    ],
    force=True
)
logger = logging.getLogger(__name__)
logger.debug("Logging initialized")

def create_server():
    """Create and configure the MCP server.
    
    Returns:
        FastMCP: The configured MCP server instance
    """
    # Create FastMCP server instance
    mcp = FastMCP(
        "pygithub-mcp-server",
        version=VERSION,
        description="GitHub API operations via MCP"
    )
    
    # Load configuration
    config = load_config()
    logger.info(f"Loaded configuration: {len(config['tool_groups'])} tool groups defined")
    
    # Log which tool groups are enabled
    enabled_groups = [name for name, cfg in config["tool_groups"].items() if cfg.get("enabled", False)]
    logger.info(f"Enabled tool groups: {', '.join(enabled_groups) or 'none'}")
    
    # Load and register tools based on configuration
    load_tools(mcp, config)
    
    return mcp


if __name__ == "__main__":
    server = create_server()
    server.run()
