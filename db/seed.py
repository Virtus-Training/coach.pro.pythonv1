import csv
import os
from typing import Optional

from db.database_manager import db_manager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "db", "schema.sql")
EXERCISES_CSV = os.path.join(BASE_DIR, "data", "exercices_master.csv")
ALIMENTS_CSV = os.path.join(BASE_DIR, "data", "base_aliments_enrichie_bloc4.csv")


def create_schema():
    with db_manager.get_connection() as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())


def seed_data():
    with db_manager.get_connection() as conn:
        # Chargement des exercices depuis le CSV
        with open(EXERCISES_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            exercices = []
            for row in reader:
                nom = row.get("name", "").strip()
                if not nom:
                    continue
                groupe = row.get("primary_muscle", "").strip()
                equip_list = [
                    e.strip() for e in row.get("equipment", "").split(";") if e.strip()
                ]
                equipement = ", ".join(equip_list)
                tags = ", ".join(
                    e.strip() for e in row.get("tags", "").split(";") if e.strip()
                )
                movement_pattern = row.get("movement_pattern", "").strip() or None
                type_effort = row.get("category", "").strip() or ""
                est_chargeable = (
                    0 if equip_list and equip_list == ["Poids du corps"] else 1
                )
                exercices.append(
                    (
                        nom,
                        groupe,
                        equipement,
                        tags or None,
                        movement_pattern,
                        type_effort,
                        1.0,
                        est_chargeable,
                    )
                )

        conn.executemany(
            """
            INSERT INTO exercices (
                nom, groupe_musculaire_principal, equipement, tags, movement_pattern,
                type_effort, coefficient_volume, est_chargeable
            ) VALUES (?,?,?,?,?,?,?,?)
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

        def get_exercice_id(nom: str) -> Optional[int]:
            cur = conn.execute("SELECT id FROM exercices WHERE nom = ?", (nom,))
            row = cur.fetchone()
            return row[0] if row else None

        resultats = [
            (1, get_exercice_id("Air squat"), 4, 8, 0, "Difficile"),
            (1, get_exercice_id("Goblet squat"), 3, 10, 20, "Brûlant"),
            (2, get_exercice_id("Barbell bench press"), 4, 8, 80, "Facile"),
            (2, get_exercice_id("Pull-up"), 3, 6, 0, "Difficile"),
        ]
        resultats = [r for r in resultats if r[1] is not None]
        if resultats:
            conn.executemany(
                """
                INSERT INTO resultats_exercices (
                    session_id, exercice_id, series_effectuees,
                    reps_effectuees, charge_utilisee, feedback_client
                ) VALUES (?,?,?,?,?,?)
                """,
                resultats,
            )

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

        try:
            with open(ALIMENTS_CSV, newline="", encoding="utf-8") as f:
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
        except FileNotFoundError:
            print(
                "INFO: Fichier de base des aliments non trouvé. Le seeding continuera sans."
            )

        conn.commit()


if __name__ == "__main__":
    create_schema()
    print("Base de données recréée.")
    seed_data()
    print("Données insérées.")
