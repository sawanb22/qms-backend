#!/usr/bin/env python3
"""
Development server startup script with SQLite initialization
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        return False

def main():
    """Main setup and startup function"""
    print("🚀 Starting QMS Backend with SQLite...")
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Check if virtual environment exists
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        if not run_command("python -m venv venv", "Virtual environment creation"):
            sys.exit(1)
    
    # Determine activation script based on OS
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
        pip_cmd = str(venv_path / "Scripts" / "pip.exe")
        python_cmd = str(venv_path / "Scripts" / "python.exe")
        uvicorn_cmd = str(venv_path / "Scripts" / "uvicorn.exe")
    else:  # Unix-like
        activate_script = venv_path / "bin" / "activate"
        pip_cmd = str(venv_path / "bin" / "pip")
        python_cmd = str(venv_path / "bin" / "python")
        uvicorn_cmd = str(venv_path / "bin" / "uvicorn")
    
    # Install dependencies
    if not run_command(f'"{pip_cmd}" install -r requirements.txt', "Installing dependencies"):
        sys.exit(1)
    
    # Initialize database
    if not run_command(f'"{python_cmd}" init_db.py', "Initializing SQLite database"):
        sys.exit(1)
    
    # Run Alembic migrations
    alembic_cmd = str(venv_path / "Scripts" / "alembic.exe") if os.name == 'nt' else str(venv_path / "bin" / "alembic")
    run_command(f'"{alembic_cmd}" upgrade head', "Running database migrations")
    
    # Start the server
    print("\n🌟 Starting development server...")
    print("   Server will be available at: http://localhost:8000")
    print("   API documentation: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([uvicorn_cmd, "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
