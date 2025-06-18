"""
Database initialization script for the K-Beauty Analysis application.
"""

import os
import sqlite3
from pathlib import Path

def init_db():
    """Initialize the SQLite database with all required tables and columns."""
    # Use the same database name as in main.py
    db_path = "chromalyze.db"
    
    # Check if the database already exists
    db_exists = os.path.exists(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the main analysis_results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis_results
    (id TEXT PRIMARY KEY,
     status TEXT NOT NULL,
     faces_detected INTEGER,
     skin_tone TEXT,
     face_shape TEXT,
     color_season TEXT,
     error_detail TEXT,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)
    ''')
    
    # Add indexes for faster lookups
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_status ON analysis_results (status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_created_at ON analysis_results (created_at)')
    
    # Check if we need to add the error_detail column to an existing database
    if db_exists:
        # Check if error_detail column exists
        cursor.execute("PRAGMA table_info(analysis_results)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'error_detail' not in columns:
            print("Adding missing error_detail column to analysis_results table")
            cursor.execute("ALTER TABLE analysis_results ADD COLUMN error_detail TEXT")
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    init_db()