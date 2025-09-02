import sqlite3
from pathlib import Path

from db.database_manager import db_manager
from db.seed import create_schema, seed_data


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (name,),
    )
    return cur.fetchone() is not None


def _is_exercices_empty(conn: sqlite3.Connection) -> bool:
    try:
        cur = conn.execute("SELECT COUNT(*) AS n FROM exercices")
        row = cur.fetchone()
        return (row[0] if row else 0) == 0
    except sqlite3.Error:
        # If the table is missing or query fails, treat as empty
        return True


def initialize_database() -> None:
    db_path = Path(db_manager.db_path)

    # Case 1: DB file missing -> create schema and seed
    if not db_path.exists():
        print("INFO: Base de donnees non trouvee. Initialisation en cours...")
        create_schema()
        seed_data()
        print("INFO: Base de donnees initialisee avec succes.")
        return

    # Case 2: DB file exists -> ensure essential tables and seed if empty
    with db_manager.get_connection() as conn:
        if not _table_exists(conn, "exercices"):
            print("INFO: Schema manquant. Reconstruction et remplissage des donnees...")
            create_schema()
            seed_data()
            print("INFO: Base de donnees reconstruite et renseignee.")
            return

        if _is_exercices_empty(conn):
            print("INFO: Table 'exercices' vide. Import des donnees...")
            seed_data()
            print("INFO: Exercices importes avec succes.")
            return

    # Otherwise, nothing to do
    return
