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

        # Lightweight migrations
        try:
            cols = {
                r[1] for r in conn.execute("PRAGMA table_info(exercices)").fetchall()
            }
            if "movement_category" not in cols:
                print(
                    "INFO: Migration: ajout de la colonne movement_category dans 'exercices'."
                )
                conn.execute("ALTER TABLE exercices ADD COLUMN movement_category TEXT")
            # Provenance/licence (pour imports externes comme wger)
            provenance_cols = [
                ("source", "TEXT"),
                ("source_uuid", "TEXT"),
                ("source_url", "TEXT"),
                ("license_name", "TEXT"),
                ("license_url", "TEXT"),
            ]
            for col, ctype in provenance_cols:
                if col not in cols:
                    print(
                        f"INFO: Migration: ajout de la colonne {col} ({ctype}) dans 'exercices'."
                    )
                    conn.execute(f"ALTER TABLE exercices ADD COLUMN {col} {ctype}")
            # Canonicalisation des données pour réduire les redondances
            # 1) pattern: map 'Plyo' -> 'Jump'
            conn.execute(
                "UPDATE exercices SET movement_pattern='Jump' WHERE LOWER(movement_pattern) IN ('plyo','saut','jump')"
            )
            # 2) category: ne garder que valeurs reconnues, sinon NULL
            allowed = {"Polyarticulaire", "Isolation", "Gainage"}
            try:
                rows = conn.execute(
                    "SELECT id, movement_category FROM exercices WHERE movement_category IS NOT NULL"
                ).fetchall()
                for r in rows:
                    val = r[1]
                    if val not in allowed:
                        conn.execute(
                            "UPDATE exercices SET movement_category = NULL WHERE id = ?",
                            (r[0],),
                        )
            except Exception:
                pass
            # 3) tags: remplacer 'Plyo' par 'Explosif', normaliser Isometrie
            conn.execute(
                "UPDATE exercices SET tags=REPLACE(tags, 'Plyo', 'Explosif') WHERE tags LIKE '%Plyo%'"
            )
            conn.execute(
                "UPDATE exercices SET tags=REPLACE(tags, 'Isometrie', 'Isométrie') WHERE tags LIKE '%Isometrie%'"
            )
            conn.commit()
        except Exception as e:
            print(f"WARN: Migration partielle non appliquee: {e}")

        # Ensure sessions table has course_type and intensity columns
        try:
            if _table_exists(conn, "sessions"):
                s_cols = {
                    r[1] for r in conn.execute("PRAGMA table_info(sessions)").fetchall()
                }
                if "course_type" not in s_cols:
                    print(
                        "INFO: Migration: ajout de la colonne course_type dans 'sessions'."
                    )
                    conn.execute("ALTER TABLE sessions ADD COLUMN course_type TEXT")
                if "intensity" not in s_cols:
                    print(
                        "INFO: Migration: ajout de la colonne intensity dans 'sessions'."
                    )
                    conn.execute("ALTER TABLE sessions ADD COLUMN intensity TEXT")
                conn.commit()
        except Exception as e:
            print(f"WARN: Migration 'sessions' non appliquee: {e}")

        if _is_exercices_empty(conn):
            print("INFO: Table 'exercices' vide. Import des donnees...")
            seed_data()
            print("INFO: Exercices importes avec succes.")
            return

    # Otherwise, nothing to do
    # Ensure pdf_templates table exists for customizable PDF styles
    try:
        _ensure_pdf_templates_table()
        # Ensure a default PDF template entry exists
        try:
            from services.pdf_template_service import PdfTemplateService

            PdfTemplateService().ensure_all_defaults_exist()
        except Exception:
            pass
    except Exception:
        pass
    return


def _ensure_pdf_templates_table() -> None:
    with db_manager.get_connection() as conn:
        try:
            if not _table_exists(conn, "pdf_templates"):
                conn.execute(
                    """
                    CREATE TABLE pdf_templates (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE,
                        type TEXT NOT NULL,
                        style_json TEXT NOT NULL,
                        is_default INTEGER NOT NULL DEFAULT 0,
                        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                conn.commit()
        except Exception as e:
            print(f"WARN: Could not ensure pdf_templates table: {e}")
