"""
Repository pour la gestion des profils nutritionnels.
Gère la persistance et les opérations CRUD sur les profils.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

from db.database_manager import db_manager
from dtos.objectif_macro import ObjectifMacro
from models.profil_nutritionnel import ProfilNutritionnel


class ProfilNutritionnelRepository:
    """Repository pour les profils nutritionnels"""

    def __init__(self):
        self.ensure_table_exists()

    def _row_to_profil(self, row) -> ProfilNutritionnel:
        """Convertit une ligne DB en objet ProfilNutritionnel"""
        return ProfilNutritionnel(
            id=row[0],
            client_id=row[1],
            age=row[2],
            sexe=row[3],
            poids_kg=row[4],
            taille_cm=row[5],
            objectif_principal=row[6],
            niveau_activite=row[7],
            restrictions_alimentaires=json.loads(row[8]) if row[8] else [],
            regimes_compatibles=json.loads(row[9]) if row[9] else [],
            aliments_preferes=json.loads(row[10]) if row[10] else [],
            aliments_exclus=json.loads(row[11]) if row[11] else [],
            nombre_repas_souhaite=row[12],
            metabolism_basal=row[13],
            besoins_caloriques=row[14],
            repartition_macros=json.loads(row[15]) if row[15] else {},
            date_creation=datetime.fromisoformat(row[16]),
            date_mise_a_jour=datetime.fromisoformat(row[17]),
        )

    def get_by_id(self, profil_id: int) -> Optional[ProfilNutritionnel]:
        """Récupère un profil par son ID"""
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM profils_nutritionnels WHERE id = ?", (profil_id,)
            ).fetchone()

        return self._row_to_profil(row) if row else None

    def get_by_client_id(self, client_id: int) -> Optional[ProfilNutritionnel]:
        """Récupère le profil d'un client"""
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM profils_nutritionnels WHERE client_id = ?", (client_id,)
            ).fetchone()

        return self._row_to_profil(row) if row else None

    def add(self, profil: ProfilNutritionnel) -> int:
        """Ajoute un nouveau profil nutritionnel"""
        # Mise à jour des calculs avant sauvegarde
        profil.mettre_a_jour_profil()

        with db_manager.get_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO profils_nutritionnels (
                    client_id, age, sexe, poids_kg, taille_cm, objectif_principal,
                    niveau_activite, restrictions_alimentaires, regimes_compatibles,
                    aliments_preferes, aliments_exclus, nombre_repas_souhaite,
                    metabolism_basal, besoins_caloriques, repartition_macros,
                    date_creation, date_mise_a_jour
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    profil.client_id,
                    profil.age,
                    profil.sexe,
                    profil.poids_kg,
                    profil.taille_cm,
                    profil.objectif_principal,
                    profil.niveau_activite,
                    json.dumps(profil.restrictions_alimentaires),
                    json.dumps(profil.regimes_compatibles),
                    json.dumps(profil.aliments_preferes),
                    json.dumps(profil.aliments_exclus),
                    profil.nombre_repas_souhaite,
                    profil.metabolism_basal,
                    profil.besoins_caloriques,
                    json.dumps(profil.repartition_macros),
                    profil.date_creation.isoformat(),
                    profil.date_mise_a_jour.isoformat(),
                ),
            )
            conn.commit()
            return int(cur.lastrowid)

    def update(self, profil: ProfilNutritionnel) -> None:
        """Met à jour un profil nutritionnel existant"""
        # Mise à jour des calculs avant sauvegarde
        profil.mettre_a_jour_profil()

        with db_manager.get_connection() as conn:
            conn.execute(
                """
                UPDATE profils_nutritionnels SET
                    age=?, sexe=?, poids_kg=?, taille_cm=?, objectif_principal=?,
                    niveau_activite=?, restrictions_alimentaires=?, regimes_compatibles=?,
                    aliments_preferes=?, aliments_exclus=?, nombre_repas_souhaite=?,
                    metabolism_basal=?, besoins_caloriques=?, repartition_macros=?,
                    date_mise_a_jour=?
                WHERE id=?
                """,
                (
                    profil.age,
                    profil.sexe,
                    profil.poids_kg,
                    profil.taille_cm,
                    profil.objectif_principal,
                    profil.niveau_activite,
                    json.dumps(profil.restrictions_alimentaires),
                    json.dumps(profil.regimes_compatibles),
                    json.dumps(profil.aliments_preferes),
                    json.dumps(profil.aliments_exclus),
                    profil.nombre_repas_souhaite,
                    profil.metabolism_basal,
                    profil.besoins_caloriques,
                    json.dumps(profil.repartition_macros),
                    profil.date_mise_a_jour.isoformat(),
                    profil.id,
                ),
            )
            conn.commit()

    def delete(self, profil_id: int) -> None:
        """Supprime un profil nutritionnel"""
        with db_manager.get_connection() as conn:
            conn.execute("DELETE FROM profils_nutritionnels WHERE id = ?", (profil_id,))
            conn.commit()

    def list_all(self) -> List[ProfilNutritionnel]:
        """Liste tous les profils nutritionnels"""
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM profils_nutritionnels ORDER BY date_creation DESC"
            ).fetchall()

        return [self._row_to_profil(row) for row in rows]

    def get_by_objectif(self, objectif: str) -> List[ProfilNutritionnel]:
        """Récupère les profils par objectif nutritionnel"""
        with db_manager.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM profils_nutritionnels WHERE objectif_principal = ? ORDER BY date_creation DESC",
                (objectif,),
            ).fetchall()

        return [self._row_to_profil(row) for row in rows]

    def add_aliment_favori(self, client_id: int, aliment_id: int) -> None:
        """Ajoute un aliment aux favoris d'un client"""
        profil = self.get_by_client_id(client_id)
        if profil and aliment_id not in profil.aliments_preferes:
            profil.aliments_preferes.append(aliment_id)
            self.update(profil)

    def remove_aliment_favori(self, client_id: int, aliment_id: int) -> None:
        """Retire un aliment des favoris d'un client"""
        profil = self.get_by_client_id(client_id)
        if profil and aliment_id in profil.aliments_preferes:
            profil.aliments_preferes.remove(aliment_id)
            self.update(profil)

    def add_aliment_exclu(self, client_id: int, aliment_id: int) -> None:
        """Ajoute un aliment aux exclusions d'un client"""
        profil = self.get_by_client_id(client_id)
        if profil and aliment_id not in profil.aliments_exclus:
            profil.aliments_exclus.append(aliment_id)
            # Retirer des favoris si présent
            if aliment_id in profil.aliments_preferes:
                profil.aliments_preferes.remove(aliment_id)
            self.update(profil)

    def remove_aliment_exclu(self, client_id: int, aliment_id: int) -> None:
        """Retire un aliment des exclusions d'un client"""
        profil = self.get_by_client_id(client_id)
        if profil and aliment_id in profil.aliments_exclus:
            profil.aliments_exclus.remove(aliment_id)
            self.update(profil)

    def get_objectifs_macros(self, client_id: int) -> Optional[ObjectifMacro]:
        """Récupère les objectifs macronutriments d'un client"""
        profil = self.get_by_client_id(client_id)
        if not profil or not profil.repartition_macros:
            return None

        return ObjectifMacro(
            proteines_g=profil.repartition_macros.get("proteines_g", 0),
            glucides_g=profil.repartition_macros.get("glucides_g", 0),
            lipides_g=profil.repartition_macros.get("lipides_g", 0),
            kcal_total=profil.besoins_caloriques or 2000,
        )

    def get_statistics(self) -> Dict[str, any]:
        """Retourne des statistiques sur les profils nutritionnels"""
        with db_manager.get_connection() as conn:
            stats = {
                "total_profils": conn.execute(
                    "SELECT COUNT(*) FROM profils_nutritionnels"
                ).fetchone()[0],
                "objectifs_populaires": dict(
                    conn.execute(
                        "SELECT objectif_principal, COUNT(*) FROM profils_nutritionnels GROUP BY objectif_principal ORDER BY COUNT(*) DESC"
                    ).fetchall()
                ),
                "age_moyen": conn.execute(
                    "SELECT AVG(age) FROM profils_nutritionnels"
                ).fetchone()[0],
                "poids_moyen": conn.execute(
                    "SELECT AVG(poids_kg) FROM profils_nutritionnels"
                ).fetchone()[0],
                "taille_moyenne": conn.execute(
                    "SELECT AVG(taille_cm) FROM profils_nutritionnels"
                ).fetchone()[0],
                "besoins_caloriques_moyens": conn.execute(
                    "SELECT AVG(besoins_caloriques) FROM profils_nutritionnels"
                ).fetchone()[0],
            }

        return stats

    def ensure_table_exists(self):
        """S'assure que la table profils_nutritionnels existe"""
        with db_manager.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS profils_nutritionnels (
                    id INTEGER PRIMARY KEY,
                    client_id INTEGER NOT NULL,
                    age INTEGER NOT NULL,
                    sexe TEXT NOT NULL,
                    poids_kg REAL NOT NULL,
                    taille_cm REAL NOT NULL,
                    objectif_principal TEXT NOT NULL,
                    niveau_activite TEXT NOT NULL,
                    restrictions_alimentaires TEXT DEFAULT '[]',
                    regimes_compatibles TEXT DEFAULT '[]',
                    aliments_preferes TEXT DEFAULT '[]',
                    aliments_exclus TEXT DEFAULT '[]',
                    nombre_repas_souhaite INTEGER DEFAULT 3,
                    metabolism_basal REAL,
                    besoins_caloriques REAL,
                    repartition_macros TEXT DEFAULT '{}',
                    date_creation TEXT NOT NULL,
                    date_mise_a_jour TEXT NOT NULL,
                    FOREIGN KEY(client_id) REFERENCES clients(id),
                    UNIQUE(client_id)
                )
                """
            )
            conn.commit()
