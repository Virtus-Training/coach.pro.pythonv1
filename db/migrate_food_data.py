import csv
import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = "coach.db"
CSV_PATH = Path("data/base_aliments_enrichie_bloc4.csv")


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


def migrate() -> None:
    if not CSV_PATH.exists():
        print(f"Fichier introuvable: {CSV_PATH}")
        return

    with sqlite3.connect(DB_PATH) as conn, open(CSV_PATH, newline="", encoding="utf-8") as f:
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
    migrate()
