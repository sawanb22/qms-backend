@echo off
echo Setting up SQLite database for QMS Backend...

:: Change to backend directory
cd /d "%~dp0"

:: Create and activate virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Initialize database
echo Initializing SQLite database...
python init_db.py

:: Run Alembic migrations (if needed)
echo Running database migrations...
alembic upgrade head

echo Setup complete! You can now run the server with:
echo uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
