from pathlib import Path

from db.database_manager import db_manager
from db.seed import create_schema, seed_data


def initialize_database() -> None:
    db_path = Path(db_manager.db_path)
    if db_path.exists():
        return

    print("INFO: Base de données non trouvée. Initialisation en cours...")
    with db_manager._get_connection() as conn:
        create_schema(conn)
        seed_data(conn)
    print("INFO: Base de données initialisée avec succès.")

