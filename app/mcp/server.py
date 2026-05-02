"""
MCP (Model Context Protocol) Server for ChatOps Gateway.

This module provides an MCP server that exposes tools for querying
conversation data from the ChatOps database.
"""

import json
import sqlite3
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Database path
DB_PATH = "data/chatops.db"

# Create MCP server instance
app = Server("chatops-gateway")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available MCP tools.
    
    Returns:
        list[Tool]: List of available tools
    """
    return [
        Tool(
            name="fetch_recent_conversations",
            description="Fetch the 5 most recent user messages from the ChatOps database",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool execution requests.
    
    Args:
        name: The name of the tool to execute
        arguments: Tool arguments (not used for fetch_recent_conversations)
        
    Returns:
        list[TextContent]: Tool execution results
    """
    if name == "fetch_recent_conversations":
        return await fetch_recent_conversations()
    else:
        raise ValueError(f"Unknown tool: {name}")


async def fetch_recent_conversations() -> list[TextContent]:
    """
    Fetch the 5 most recent user messages from the database.
    
    Connects to the SQLite database and retrieves recent user messages
    with their session_id, content, and timestamp.
    
    Returns:
        list[TextContent]: JSON string containing recent conversations
    """
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query for 5 most recent user messages
        cursor.execute("""
            SELECT session_id, content, timestamp
            FROM messages
            WHERE role = 'user'
            ORDER BY timestamp DESC
            LIMIT 5
        """)
        
        # Fetch results
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        conversations = []
        for row in rows:
            conversations.append({
                "session_id": row["session_id"],
                "content": row["content"],
                "timestamp": row["timestamp"]
            })
        
        # Close connection
        conn.close()
        
        # Return as JSON string
        result_json = json.dumps(conversations, indent=2, ensure_ascii=False)
        
        return [
            TextContent(
                type="text",
                text=result_json
            )
        ]
        
    except sqlite3.Error as e:
        error_message = f"Database error: {str(e)}"
        return [
            TextContent(
                type="text",
                text=json.dumps({"error": error_message})
            )
        ]
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        return [
            TextContent(
                type="text",
                text=json.dumps({"error": error_message})
            )
        ]


async def main():
    """
    Main entry point for the MCP server.
    
    Runs the server using stdio transport.
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


# Run the server
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


# Made with Bob