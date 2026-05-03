"""
MCP (Model Context Protocol) Server for ChatOps Gateway.

This module provides an MCP server that exposes tools for querying
conversation data and system health from the ChatOps database.
"""

import json
from datetime import datetime
from pathlib import Path

import aiosqlite
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
        ),
        Tool(
            name="search_conversations",
            description="Search conversations by keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for in conversation messages"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["keyword"]
            }
        ),
        Tool(
            name="get_session_stats",
            description="Get statistics about conversation sessions (total sessions, messages, active sessions)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_system_health",
            description="Check overall system health including database status and configuration",
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
        arguments: Tool arguments
        
    Returns:
        list[TextContent]: Tool execution results
    """
    handlers = {
        "fetch_recent_conversations": fetch_recent_conversations,
        "search_conversations": search_conversations,
        "get_session_stats": get_session_stats,
        "get_system_health": get_system_health,
    }
    
    handler = handlers.get(name)
    if handler:
        return await handler(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def fetch_recent_conversations(arguments: dict) -> list[TextContent]:
    """
    Fetch the 5 most recent user messages from the database.
    Uses async SQLite for non-blocking database access.
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT session_id, content, timestamp
                FROM messages
                WHERE role = 'user'
                ORDER BY timestamp DESC
                LIMIT 5
            """)
            rows = await cursor.fetchall()
            
            conversations = [
                {
                    "session_id": row["session_id"],
                    "content": row["content"],
                    "timestamp": row["timestamp"]
                }
                for row in rows
            ]
        
        return [TextContent(type="text", text=json.dumps(conversations, indent=2, ensure_ascii=False))]
        
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def search_conversations(arguments: dict) -> list[TextContent]:
    """
    Search conversations by keyword using async SQLite.
    """
    keyword = arguments.get("keyword", "")
    limit = arguments.get("limit", 10)
    
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT session_id, role, content, timestamp
                FROM messages
                WHERE content LIKE ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (f"%{keyword}%", limit))
            rows = await cursor.fetchall()
            
            results = [
                {
                    "session_id": row["session_id"],
                    "role": row["role"],
                    "content": row["content"],
                    "timestamp": row["timestamp"]
                }
                for row in rows
            ]
        
        return [TextContent(type="text", text=json.dumps({
            "keyword": keyword,
            "results_count": len(results),
            "results": results
        }, indent=2, ensure_ascii=False))]
        
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def get_session_stats(arguments: dict) -> list[TextContent]:
    """
    Get statistics about conversation sessions.
    """
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Total messages
            cursor = await db.execute("SELECT COUNT(*) FROM messages")
            total_messages = (await cursor.fetchone())[0]
            
            # Total sessions
            cursor = await db.execute("SELECT COUNT(DISTINCT session_id) FROM messages")
            total_sessions = (await cursor.fetchone())[0]
            
            # Messages by role
            cursor = await db.execute("""
                SELECT role, COUNT(*) as count 
                FROM messages 
                GROUP BY role
            """)
            role_counts = {row[0]: row[1] for row in await cursor.fetchall()}
            
            # Most active sessions
            cursor = await db.execute("""
                SELECT session_id, COUNT(*) as msg_count, 
                       MIN(timestamp) as first_msg, MAX(timestamp) as last_msg
                FROM messages
                GROUP BY session_id
                ORDER BY msg_count DESC
                LIMIT 5
            """)
            active_sessions = [
                {
                    "session_id": row[0],
                    "message_count": row[1],
                    "first_message": row[2],
                    "last_message": row[3]
                }
                for row in await cursor.fetchall()
            ]
        
        stats = {
            "total_messages": total_messages,
            "total_sessions": total_sessions,
            "messages_by_role": role_counts,
            "most_active_sessions": active_sessions
        }
        
        return [TextContent(type="text", text=json.dumps(stats, indent=2, ensure_ascii=False))]
        
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def get_system_health(arguments: dict) -> list[TextContent]:
    """
    Check overall system health.
    """
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # Check database
    try:
        db_exists = Path(DB_PATH).exists()
        if db_exists:
            async with aiosqlite.connect(DB_PATH) as db:
                cursor = await db.execute("SELECT COUNT(*) FROM messages")
                count = (await cursor.fetchone())[0]
                health["components"]["database"] = {
                    "status": "healthy",
                    "path": DB_PATH,
                    "total_records": count
                }
        else:
            health["components"]["database"] = {
                "status": "not_initialized",
                "path": DB_PATH
            }
    except Exception as e:
        health["components"]["database"] = {
            "status": "error",
            "error": str(e)
        }
        health["status"] = "degraded"
    
    # Check screenshots directory
    screenshots_dir = Path("data/screenshots")
    if screenshots_dir.exists():
        screenshot_count = len(list(screenshots_dir.glob("*.png")))
        health["components"]["screenshots"] = {
            "status": "healthy",
            "directory": str(screenshots_dir),
            "file_count": screenshot_count
        }
    else:
        health["components"]["screenshots"] = {
            "status": "not_initialized"
        }
    
    return [TextContent(type="text", text=json.dumps(health, indent=2, ensure_ascii=False))]


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