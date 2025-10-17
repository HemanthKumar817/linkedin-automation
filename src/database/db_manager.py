"""
Database Manager - handles all database operations
"""
import sqlite3
from typing import Dict, List, Optional
from loguru import logger
from pathlib import Path
import os


class DatabaseManager:
    """Manages SQLite database operations"""
    
    def __init__(self):
        """Initialize database manager"""
        db_path = os.getenv('DATABASE_PATH', 'data/linkedin_automation.db')
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._init_connection()
    
    def _init_connection(self):
        """Initialize database connection"""
        try:
            self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            logger.info(f"✅ Database connected: {self.db_path}")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise
    
    def save_post(self, post: Dict) -> int:
        """Save a post to database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO posts (
                    topic_title, source_name, source_url, summary,
                    content, hashtags, suggested_posting_time,
                    status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                post.get('topic_title'),
                post.get('source_name'),
                post.get('source_url'),
                post.get('summary'),
                post.get('content'),
                post.get('hashtags'),
                post.get('suggested_posting_time'),
                post.get('status', 'pending'),
                post.get('created_at')
            ))
            self.conn.commit()
            return cursor.lastrowid
        
        except Exception as e:
            logger.error(f"Error saving post: {str(e)}")
            return -1
    
    def get_pending_posts(self) -> List[Dict]:
        """Get all pending posts"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM posts WHERE status = 'pending'")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        
        except Exception as e:
            logger.error(f"Error fetching pending posts: {str(e)}")
            return []
    
    def update_post_status(self, post_id: int, status: str) -> bool:
        """Update post status"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE posts SET status = ? WHERE id = ?",
                (status, post_id)
            )
            self.conn.commit()
            return True
        
        except Exception as e:
            logger.error(f"Error updating post status: {str(e)}")
            return False
    
    def save_engagement(self, engagement: Dict) -> bool:
        """Save engagement metrics"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO engagements (
                    post_id, likes, comments, shares, impressions, checked_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                engagement.get('post_id'),
                engagement.get('likes', 0),
                engagement.get('comments', 0),
                engagement.get('shares', 0),
                engagement.get('impressions', 0),
                engagement.get('checked_at')
            ))
            self.conn.commit()
            return True
        
        except Exception as e:
            logger.error(f"Error saving engagement: {str(e)}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
