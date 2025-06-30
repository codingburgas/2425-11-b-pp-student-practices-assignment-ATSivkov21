#!/usr/bin/env python3
"""
Comprehensive project cleanup and validation script
"""

import os
import sys
import sqlite3
import shutil
from pathlib import Path

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        'static/results',
        'static/ads',
        'instance',
        'migrations/versions'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_database():
    """Check and fix database issues"""
    db_path = 'instance/site.db'
    
    if not os.path.exists(db_path):
        print("⚠️  Database not found. It will be created when the app runs.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if social_media column exists
        cursor.execute("PRAGMA table_info(survey_response)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'social_media' not in columns:
            print("❌ social_media column missing from database")
            cursor.execute("ALTER TABLE survey_response ADD COLUMN social_media TEXT")
            conn.commit()
            print("✅ Added social_media column to database")
        else:
            print("✅ social_media column exists in database")
        
        # Check if share_results column exists in user table
        cursor.execute("PRAGMA table_info(user)")
        user_columns = [column[1] for column in cursor.fetchall()]
        
        if 'share_results' not in user_columns:
            print("❌ share_results column missing from user table")
            cursor.execute("ALTER TABLE user ADD COLUMN share_results BOOLEAN DEFAULT 0")
            conn.commit()
            print("✅ Added share_results column to user table")
        else:
            print("✅ share_results column exists in user table")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")

def check_static_files():
    """Check if required static files exist"""
    required_files = [
        'static/ads/ad1.jpg',
        'static/ads/ad2.jpg', 
        'static/ads/ad3.jpg'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"⚠️  Missing static file: {file_path}")
        else:
            print(f"✅ Static file exists: {file_path}")

def cleanup_cache():
    """Remove Python cache files"""
    cache_dirs = ['__pycache__', 'app/__pycache__', 'app/utils/__pycache__']
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"✅ Removed cache directory: {cache_dir}")

def validate_imports():
    """Test if all modules can be imported"""
    modules_to_test = [
        'app',
        'app.models',
        'app.forms', 
        'app.utils.ai_model',
        'app.utils.plot_utils',
        'app.utils.email_utils'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ Import successful: {module}")
        except ImportError as e:
            print(f"❌ Import failed: {module} - {e}")

def check_environment():
    """Check environment configuration"""
    print("\n🔧 Environment Check:")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
    else:
        print("⚠️  .env file not found. Create one based on .env.example")
    
    # Check Python version
    python_version = sys.version_info
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("⚠️  Python 3.8+ recommended")

def main():
    """Main cleanup function"""
    print("🧹 Project Cleanup and Validation")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("\n📁 Creating directories...")
    create_directories()
    
    print("\n🗄️  Checking database...")
    check_database()
    
    print("\n📁 Checking static files...")
    check_static_files()
    
    print("\n🧹 Cleaning cache...")
    cleanup_cache()
    
    print("\n📦 Testing imports...")
    validate_imports()
    
    print("\n🔧 Environment check...")
    check_environment()
    
    print("\n" + "=" * 50)
    print("🎉 Cleanup completed!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Create .env file with your configuration")
    print("3. Run the application: python run.py")

if __name__ == "__main__":
    main() 