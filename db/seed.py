import csv
from pathlib import Path
from typing import Optional

from db.database_manager import db_manager

SCHEMA_PATH = "db/schema.sql"
CSV_PATH = Path("data/base_aliments_enrichie_bloc4.csv")


def create_schema():
    with db_manager.get_connection() as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())


def seed_data():
    with db_manager.get_connection() as conn:
        exercices = [
            ("Squat", "Jambes", "Barre", "Force", 1.0, 1),
            ("Fente avant", "Jambes", "Haltères", "Hypertrophie", 0.8, 1),
            ("Développé couché", "Pectoraux", "Barre", "Force", 1.0, 1),
            ("Tractions", "Dos", "Barre fixe", "Hypertrophie", 1.0, 1),
            ("Rowing haltère", "Dos", "Haltère", "Hypertrophie", 0.8, 1),
            ("Planche", "Abdominaux", "Tapis", "Stabilité", 0.5, 0),
            ("Burpees", "Full body", "Poids du corps", "Cardio", 1.2, 0),
            ("Saut en hauteur", "Jambes", "Poids du corps", "Pliométrie", 1.0, 0),
            ("Course à pied", "Jambes", "Tapis", "Endurance", 1.0, 0),
            ("Développé militaire", "Épaules", "Barre", "Force", 0.9, 1),
            ("Élévation latérale", "Épaules", "Haltères", "Hypertrophie", 0.3, 1),
            ("Crunch", "Abdominaux", "Poids du corps", "Hypertrophie", 0.4, 0),
        ]
        conn.executemany(
            """
            INSERT INTO exercices (
                nom, groupe_musculaire_principal, equipement,
                type_effort, coefficient_volume, est_chargeable
            ) VALUES (?,?,?,?,?,?)
            """,
            exercices,
        )

        clients = [
            ("Doe", "John", "john@example.com", "1990-01-01"),
            ("Smith", "Anna", "anna@example.com", "1985-05-12"),
            ("Martin", "Lucas", "lucas@example.com", "1995-07-23"),
            ("Durand", "Sophie", "sophie@example.com", "1992-11-05"),
        ]
        conn.executemany(
            "INSERT INTO clients (nom, prenom, email, date_naissance) VALUES (?,?,?,?)",
            clients,
        )

        seances = [
            (1, "Individuel", "Séance jambes"),
            (2, "Individuel", "Séance haut du corps"),
            (None, "Collectif", "Cours HIIT"),
            (None, "Collectif", "Yoga matinal"),
        ]
        conn.executemany(
            "INSERT INTO seances (client_id, type_seance, titre) VALUES (?,?,?)",
            seances,
        )

        def get_exercice_id(nom: str) -> int:
            cur = conn.execute("SELECT id FROM exercices WHERE nom = ?", (nom,))
            return cur.fetchone()[0]

        resultats = [
            (1, get_exercice_id("Squat"), 4, 8, 100, "Difficile"),
            (1, get_exercice_id("Fente avant"), 3, 10, 40, "Brûlant"),
            (2, get_exercice_id("Développé couché"), 4, 8, 80, "Facile"),
            (2, get_exercice_id("Tractions"), 3, 6, 0, "Difficile"),
        ]
        conn.executemany(
            """
            INSERT INTO resultats_exercices (
                seance_id, exercice_id, series_effectuees,
                reps_effectuees, charge_utilisee, feedback_client
            ) VALUES (?,?,?,?,?,?)
            """,
            resultats,
        )

        conn.commit()

        if not CSV_PATH.exists():
            print(f"Fichier introuvable: {CSV_PATH}")
            return

        def parse_float(value: str) -> Optional[float]:
            try:
                value = value.strip()
                if not value:
                    return None
                return float(value.replace(",", "."))
            except Exception:
                return None

        def parse_int(value: str) -> Optional[int]:
            try:
                value = value.strip()
                if not value:
                    return None
                return int(value)
            except Exception:
                return None

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nom = row.get("Aliment", "").strip()
                if not nom:
                    continue

                categorie = row.get("Catégorie", "").strip() or None
                kcal = parse_float(row.get("Kcal", "")) or 0.0
                prot = parse_float(row.get("Protéines (g)", "")) or 0.0
                gluc = parse_float(row.get("Glucides (g)", "")) or 0.0
                lip = parse_float(row.get("Lipides (g)", "")) or 0.0
                ind_healthy = parse_int(row.get("Healthy (Indice)", ""))
                ind_commun = parse_int(row.get("Commun (Indice)", ""))

                try:
                    cur = conn.execute(
                        (
                            "INSERT OR IGNORE INTO aliments "
                            "(nom, categorie, type_alimentation, kcal_100g, proteines_100g, "
                            "glucides_100g, lipides_100g, fibres_100g, unite_base, indice_healthy, indice_commun) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'g', ?, ?)"
                        ),
                        (
                            nom,
                            categorie,
                            None,
                            kcal,
                            prot,
                            gluc,
                            lip,
                            None,
                            ind_healthy,
                            ind_commun,
                        ),
                    )

                    if cur.rowcount == 0:
                        continue

                    aliment_id = cur.lastrowid
                    conn.execute(
                        "INSERT INTO portions (aliment_id, description, grammes_equivalents) VALUES (?, ?, ?)",
                        (aliment_id, "100g", 100),
                    )
                except Exception as e:
                    print(f"Erreur lors de l'insertion de {nom}: {e}")

        conn.commit()


if __name__ == "__main__":
    create_schema()
    print("Base de données recréée.")
    seed_data()
    print("Données insérées.")
