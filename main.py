"""
Entry point for uvicorn server.
Imports the FastAPI app from the app module.

Usage:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from app.main import app

__all__ = ["app"]
