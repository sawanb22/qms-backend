# qms-backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import the router from the api directory
from api import routes

# Load environment variables from .env file at the start
load_dotenv()

# Initialize the main FastAPI application
app = FastAPI(
    title="QMS Event Management API",
    description="A modular API for creating and managing QMS events with AI assistance.",
    version="3.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows our React frontend to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174", "http://localhost:5175", "http://127.0.0.1:5175"],  # Allow both frontend ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes from the api/routes.py file
# All routes in the router will be prefixed with /api
app.include_router(routes.router, prefix="/api")

# A simple root endpoint to confirm the API is running
@app.get("/")
def read_root():
    return {"status": "QMS API is running"}
