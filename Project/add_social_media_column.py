#!/usr/bin/env python3
"""
Script to add social_media column to SurveyResponse table
"""

import sqlite3
import os

def add_social_media_column():
    """Add social_media column to SurveyResponse table"""
    db_path = 'instance/site.db'
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(survey_response)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'social_media' not in columns:
            # Add the social_media column
            cursor.execute("ALTER TABLE survey_response ADD COLUMN social_media TEXT")
            conn.commit()
            print("Successfully added social_media column to survey_response table")
        else:
            print("social_media column already exists")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(survey_response)")
        columns = cursor.fetchall()
        print("\nCurrent table structure:")
        for column in columns:
            print(f"  {column[1]} ({column[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_social_media_column() 