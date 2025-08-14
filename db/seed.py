import sqlite3

DB_PATH = "coach.db"
SCHEMA_PATH = "db/schema.sql"


def reset_db():
    with sqlite3.connect(DB_PATH) as conn, open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def seed():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(
            """
            DELETE FROM resultats_exercices;
            DELETE FROM seances;
            DELETE FROM clients;
            DELETE FROM exercices;
            """
        )

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

        def get_exercice_id(nom):
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


if __name__ == "__main__":
    reset_db()
    seed()

