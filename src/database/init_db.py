"""
Database initialization script
"""
import sqlite3
from pathlib import Path
import os
from loguru import logger


def initialize_database():
    """Initialize the SQLite database with required tables"""
    db_path = os.getenv('DATABASE_PATH', 'data/linkedin_automation.db')
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Initializing database: {db_path}")
    
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    
    # Create posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_title TEXT NOT NULL,
            source_name TEXT,
            source_url TEXT,
            summary TEXT,
            content TEXT NOT NULL,
            hashtags TEXT,
            suggested_posting_time TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL,
            posted_at TEXT,
            linkedin_post_id TEXT
        )
    """)
    
    # Create engagements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS engagements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            impressions INTEGER DEFAULT 0,
            checked_at TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    """)
    
    # Create articles table (for tracking scraped articles)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            summary TEXT,
            source TEXT,
            published_at TEXT,
            scraped_at TEXT NOT NULL,
            category TEXT,
            relevance_score REAL
        )
    """)
    
    conn.commit()
    conn.close()
    
    logger.info("✅ Database initialized successfully")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    initialize_database()
