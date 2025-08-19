from app import launch_app
from db.database_setup import initialize_database

if __name__ == "__main__":
    initialize_database()
    launch_app()
