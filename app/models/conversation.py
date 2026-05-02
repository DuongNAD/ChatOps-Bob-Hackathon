"""
Conversation database management using async SQLite.

This module provides database operations for storing and retrieving
conversation history across different chat sessions.
"""

import logging
from pathlib import Path
from typing import List, Tuple
import aiosqlite

from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)


def get_db_path() -> str:
    """
    Extract the database file path from DATABASE_URL.
    
    Removes the 'sqlite:///' prefix and returns the actual file path.
    
    Returns:
        str: The database file path
    """
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
        # Handle relative paths starting with ./
        if db_path.startswith("./"):
            db_path = db_path[2:]
        return db_path
    return db_url


async def init_db() -> None:
    """
    Initialize the database and create the messages table if it doesn't exist.
    
    Creates the 'messages' table with columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - session_id: TEXT (conversation session identifier)
    - role: TEXT (user or assistant)
    - content: TEXT (message content)
    - timestamp: TEXT (ISO format timestamp, defaults to current time)
    
    Raises:
        Exception: If database initialization fails
    """
    db_path = get_db_path()
    
    # Ensure the directory exists
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        async with aiosqlite.connect(db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index on session_id for faster queries
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_id 
                ON messages(session_id)
            """)
            
            await db.commit()
            logger.info(f"Database initialized successfully at {db_path}")
            
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


class SessionManager:
    """
    Manages conversation sessions and message history in the database.
    
    Provides async methods for saving messages and retrieving conversation history.
    """
    
    def __init__(self):
        """Initialize the SessionManager with database path from settings."""
        self.db_path = get_db_path()
    
    async def save_message(self, session_id: str, role: str, content: str) -> None:
        """
        Save a message to the database.
        
        Args:
            session_id: Unique identifier for the conversation session
            role: Role of the message sender (e.g., 'user', 'assistant')
            content: The message content
            
        Raises:
            Exception: If saving the message fails
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """
                    INSERT INTO messages (session_id, role, content)
                    VALUES (?, ?, ?)
                    """,
                    (session_id, role, content)
                )
                await db.commit()
                logger.debug(f"Saved message for session {session_id}: {role}")
                
        except Exception as e:
            logger.error(f"Failed to save message for session {session_id}: {e}")
            raise
    
    async def get_history(self, session_id: str, limit: int = 5) -> str:
        """
        Retrieve the most recent messages for a session.
        
        Args:
            session_id: Unique identifier for the conversation session
            limit: Maximum number of messages to retrieve (default: 5)
            
        Returns:
            str: Formatted conversation history as "role: content\n" for each message
            
        Raises:
            Exception: If retrieving history fails
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Set row factory to return rows as tuples
                db.row_factory = aiosqlite.Row
                
                cursor = await db.execute(
                    """
                    SELECT role, content
                    FROM messages
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (session_id, limit)
                )
                
                rows = await cursor.fetchall()
                
                # Reverse to get chronological order (oldest first)
                rows = list(reversed(rows))
                
                # Format as "role: content\n"
                history = "\n".join([f"{row['role']}: {row['content']}" for row in rows])
                
                logger.debug(f"Retrieved {len(rows)} messages for session {session_id}")
                return history
                
        except Exception as e:
            logger.error(f"Failed to retrieve history for session {session_id}: {e}")
            raise


# Made with Bob