"""
Application entry point.

- Initializes the local database (creates tables if needed)
- Launches the GUI application
"""

from app import launch_app
from db.database_setup import initialize_database

if __name__ == "__main__":
    # Prepare the database before starting the UI
    initialize_database()

    # Start the main application loop
    launch_app()
