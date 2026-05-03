"""
Dashboard and API endpoints for conversations and system stats.
"""

import logging
from pathlib import Path
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

import aiosqlite
from app.models.conversation import get_db_path

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/conversations", tags=["conversations"])
async def get_conversations(
    limit: int = Query(default=20, ge=1, le=100, description="Number of messages to return"),
    session_id: str = Query(default=None, description="Filter by session ID")
):
    """
    Retrieve recent conversation messages.
    
    Returns:
        dict: List of messages with metadata
    """
    try:
        async with aiosqlite.connect(get_db_path()) as db:
            db.row_factory = aiosqlite.Row
            
            if session_id:
                cursor = await db.execute(
                    """SELECT session_id, role, content, timestamp 
                       FROM messages WHERE session_id = ?
                       ORDER BY timestamp DESC LIMIT ?""",
                    (session_id, limit)
                )
            else:
                cursor = await db.execute(
                    """SELECT session_id, role, content, timestamp 
                       FROM messages ORDER BY timestamp DESC LIMIT ?""",
                    (limit,)
                )
            
            rows = await cursor.fetchall()
            messages = [
                {
                    "session_id": row["session_id"],
                    "role": row["role"],
                    "content": row["content"],
                    "timestamp": row["timestamp"]
                }
                for row in rows
            ]
        
        return {"messages": messages, "count": len(messages)}
        
    except Exception as e:
        logger.error(f"Failed to fetch conversations: {e}")
        return {"messages": [], "count": 0, "error": str(e)}


@router.get("/stats", tags=["stats"])
async def get_stats():
    """
    Get system statistics.
    
    Returns:
        dict: Statistics about conversations, sessions, and message counts
    """
    try:
        async with aiosqlite.connect(get_db_path()) as db:
            # Total messages
            cursor = await db.execute("SELECT COUNT(*) FROM messages")
            total_messages = (await cursor.fetchone())[0]
            
            # Total sessions
            cursor = await db.execute("SELECT COUNT(DISTINCT session_id) FROM messages")
            total_sessions = (await cursor.fetchone())[0]
            
            # User messages
            cursor = await db.execute("SELECT COUNT(*) FROM messages WHERE role = 'user'")
            user_messages = (await cursor.fetchone())[0]
            
            # AI responses
            cursor = await db.execute("SELECT COUNT(*) FROM messages WHERE role = 'assistant'")
            ai_responses = (await cursor.fetchone())[0]
        
        return {
            "total_messages": total_messages,
            "total_sessions": total_sessions,
            "user_messages": user_messages,
            "ai_responses": ai_responses
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch stats: {e}")
        return {
            "total_messages": 0,
            "total_sessions": 0,
            "user_messages": 0,
            "ai_responses": 0,
            "error": str(e)
        }
