#!/usr/bin/env python3
"""
Database initialization script for SQLite
Run this script to create the database and tables
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path so we can import our modules
sys.path.append(str(Path(__file__).parent))

from database import engine, Base
from models.event import Event

def init_db():
    """Initialize the database by creating all tables"""
    print("Initializing SQLite database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database initialized successfully!")
    print(f"Database file: {os.path.abspath('qms2.db')}")

if __name__ == "__main__":
    init_db()
