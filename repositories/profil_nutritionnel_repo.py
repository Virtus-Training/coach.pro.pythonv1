from typing import List, Optional, Dict
from datetime import datetime
import json

from db.database_manager import db_manager
from models.profil_nutritionnel import ProfilNutritionnel, ObjectifMacro


class ProfilNutritionnelRepository:
    """Repository pour la gestion des profils nutritionnels des clients"""
    
    def _row_to_profil(self, row) -> ProfilNutritionnel:
        """Convertit une ligne de base de données en objet ProfilNutritionnel"""
        return ProfilNutritionnel(
            id=row["id"],
            client_id=row["client_id"],
            age=row["age"],
            sexe=row["sexe"],
            poids_kg=row["poids_kg"],
            taille_cm=row["taille_cm"],
            objectif_principal=row["objectif_principal"],
            niveau_activite=row["niveau_activite"],
            restrictions_alimentaires=json.loads(row["restrictions_alimentaires"] or "[]"),
            regimes_compatibles=json.loads(row["regimes_compatibles"] or "[]"),
            aliments_preferes=json.loads(row["aliments_preferes"] or "[]"),
            aliments_exclus=json.loads(row["aliments_exclus"] or "[]"),
            nombre_repas_souhaite=row["nombre_repas_souhaite"],
            metabolism_basal=row["metabolism_basal"],
            besoins_caloriques=row["besoins_caloriques"],
            repartition_macros=json.loads(row["repartition_macros"] or "{}"),
            date_creation=datetime.fromisoformat(row["date_creation"]) if row["date_creation"] else datetime.now(),
            date_mise_a_jour=datetime.fromisoformat(row["date_mise_a_jour"]) if row["date_mise_a_jour"] else datetime.now(),
        )
    
    def get_by_client_id(self, client_id: int) -> Optional[ProfilNutritionnel]:
        """Récupère le profil nutritionnel d'un client"""
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM profils_nutritionnels WHERE client_id = ?",
                (client_id,)
            ).fetchone()
        
        return self._row_to_profil(row) if row else None
    
    def get_by_id(self, profil_id: int) -> Optional[ProfilNutritionnel]:
        """Récupère un profil par son ID"""
        with db_manager.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM profils_nutritionnels WHERE id = ?",
                (profil_id,)
            ).fetchone()
        
        return self._row_to_profil(row) if row else None
    
    def create(self, profil: ProfilNutritionnel) -> int:
        """Crée un nouveau profil nutritionnel"""
        # Mise à jour des calculs avant sauvegarde
        profil.mettre_a_jour_profil()
        
        with db_manager.get_connection() as conn:
            cur = conn.execute(
                \"\"\"\n                INSERT INTO profils_nutritionnels (\n                    client_id, age, sexe, poids_kg, taille_cm, objectif_principal,\n                    niveau_activite, restrictions_alimentaires, regimes_compatibles,\n                    aliments_preferes, aliments_exclus, nombre_repas_souhaite,\n                    metabolism_basal, besoins_caloriques, repartition_macros,\n                    date_creation, date_mise_a_jour\n                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)\n                \"\"\",\n                (\n                    profil.client_id,\n                    profil.age,\n                    profil.sexe,\n                    profil.poids_kg,\n                    profil.taille_cm,\n                    profil.objectif_principal,\n                    profil.niveau_activite,\n                    json.dumps(profil.restrictions_alimentaires),\n                    json.dumps(profil.regimes_compatibles),\n                    json.dumps(profil.aliments_preferes),\n                    json.dumps(profil.aliments_exclus),\n                    profil.nombre_repas_souhaite,\n                    profil.metabolism_basal,\n                    profil.besoins_caloriques,\n                    json.dumps(profil.repartition_macros),\n                    profil.date_creation.isoformat(),\n                    profil.date_mise_a_jour.isoformat(),\n                )\n            )\n            conn.commit()\n            return int(cur.lastrowid)\n    \n    def update(self, profil: ProfilNutritionnel) -> None:\n        \"\"\"Met à jour un profil nutritionnel existant\"\"\"\n        # Mise à jour des calculs avant sauvegarde\n        profil.mettre_a_jour_profil()\n        \n        with db_manager.get_connection() as conn:\n            conn.execute(\n                \"\"\"\n                UPDATE profils_nutritionnels SET \n                    age=?, sexe=?, poids_kg=?, taille_cm=?, objectif_principal=?,\n                    niveau_activite=?, restrictions_alimentaires=?, regimes_compatibles=?,\n                    aliments_preferes=?, aliments_exclus=?, nombre_repas_souhaite=?,\n                    metabolism_basal=?, besoins_caloriques=?, repartition_macros=?,\n                    date_mise_a_jour=?\n                WHERE id=?\n                \"\"\",\n                (\n                    profil.age,\n                    profil.sexe,\n                    profil.poids_kg,\n                    profil.taille_cm,\n                    profil.objectif_principal,\n                    profil.niveau_activite,\n                    json.dumps(profil.restrictions_alimentaires),\n                    json.dumps(profil.regimes_compatibles),\n                    json.dumps(profil.aliments_preferes),\n                    json.dumps(profil.aliments_exclus),\n                    profil.nombre_repas_souhaite,\n                    profil.metabolism_basal,\n                    profil.besoins_caloriques,\n                    json.dumps(profil.repartition_macros),\n                    profil.date_mise_a_jour.isoformat(),\n                    profil.id,\n                )\n            )\n            conn.commit()\n    \n    def delete(self, profil_id: int) -> None:\n        \"\"\"Supprime un profil nutritionnel\"\"\"\n        with db_manager.get_connection() as conn:\n            conn.execute(\"DELETE FROM profils_nutritionnels WHERE id = ?\", (profil_id,))\n            conn.commit()\n    \n    def list_all(self) -> List[ProfilNutritionnel]:\n        \"\"\"Liste tous les profils nutritionnels\"\"\"\n        with db_manager.get_connection() as conn:\n            rows = conn.execute(\n                \"SELECT * FROM profils_nutritionnels ORDER BY date_creation DESC\"\n            ).fetchall()\n        \n        return [self._row_to_profil(row) for row in rows]\n    \n    def get_by_objectif(self, objectif: str) -> List[ProfilNutritionnel]:\n        \"\"\"Récupère les profils par objectif nutritionnel\"\"\"\n        with db_manager.get_connection() as conn:\n            rows = conn.execute(\n                \"SELECT * FROM profils_nutritionnels WHERE objectif_principal = ? ORDER BY date_creation DESC\",\n                (objectif,)\n            ).fetchall()\n        \n        return [self._row_to_profil(row) for row in rows]\n    \n    def add_aliment_favori(self, client_id: int, aliment_id: int) -> None:\n        \"\"\"Ajoute un aliment aux favoris d'un client\"\"\"\n        profil = self.get_by_client_id(client_id)\n        if profil and aliment_id not in profil.aliments_preferes:\n            profil.aliments_preferes.append(aliment_id)\n            self.update(profil)\n    \n    def remove_aliment_favori(self, client_id: int, aliment_id: int) -> None:\n        \"\"\"Retire un aliment des favoris d'un client\"\"\"\n        profil = self.get_by_client_id(client_id)\n        if profil and aliment_id in profil.aliments_preferes:\n            profil.aliments_preferes.remove(aliment_id)\n            self.update(profil)\n    \n    def add_aliment_exclu(self, client_id: int, aliment_id: int) -> None:\n        \"\"\"Ajoute un aliment aux exclusions d'un client\"\"\"\n        profil = self.get_by_client_id(client_id)\n        if profil and aliment_id not in profil.aliments_exclus:\n            profil.aliments_exclus.append(aliment_id)\n            # Retirer des favoris si présent\n            if aliment_id in profil.aliments_preferes:\n                profil.aliments_preferes.remove(aliment_id)\n            self.update(profil)\n    \n    def remove_aliment_exclu(self, client_id: int, aliment_id: int) -> None:\n        \"\"\"Retire un aliment des exclusions d'un client\"\"\"\n        profil = self.get_by_client_id(client_id)\n        if profil and aliment_id in profil.aliments_exclus:\n            profil.aliments_exclus.remove(aliment_id)\n            self.update(profil)\n    \n    def get_objectifs_macros(self, client_id: int) -> Optional[ObjectifMacro]:\n        \"\"\"Récupère les objectifs macronutriments d'un client\"\"\"\n        profil = self.get_by_client_id(client_id)\n        if not profil or not profil.repartition_macros:\n            return None\n        \n        return ObjectifMacro(\n            proteines_g=profil.repartition_macros.get(\"proteines_g\", 0),\n            glucides_g=profil.repartition_macros.get(\"glucides_g\", 0),\n            lipides_g=profil.repartition_macros.get(\"lipides_g\", 0),\n            kcal_total=profil.besoins_caloriques or 2000\n        )\n    \n    def get_statistics(self) -> Dict[str, any]:\n        \"\"\"Retourne des statistiques sur les profils nutritionnels\"\"\"\n        with db_manager.get_connection() as conn:\n            stats = {\n                \"total_profils\": conn.execute(\"SELECT COUNT(*) FROM profils_nutritionnels\").fetchone()[0],\n                \"objectifs_populaires\": dict(conn.execute(\n                    \"SELECT objectif_principal, COUNT(*) FROM profils_nutritionnels GROUP BY objectif_principal ORDER BY COUNT(*) DESC\"\n                ).fetchall()),\n                \"age_moyen\": conn.execute(\"SELECT AVG(age) FROM profils_nutritionnels\").fetchone()[0],\n                \"poids_moyen\": conn.execute(\"SELECT AVG(poids_kg) FROM profils_nutritionnels\").fetchone()[0],\n                \"taille_moyenne\": conn.execute(\"SELECT AVG(taille_cm) FROM profils_nutritionnels\").fetchone()[0],\n                \"besoins_caloriques_moyens\": conn.execute(\"SELECT AVG(besoins_caloriques) FROM profils_nutritionnels\").fetchone()[0],\n            }\n        \n        return stats\n    \n    def ensure_table_exists(self):\n        \"\"\"S'assure que la table profils_nutritionnels existe\"\"\"\n        with db_manager.get_connection() as conn:\n            conn.execute(\n                \"\"\"\n                CREATE TABLE IF NOT EXISTS profils_nutritionnels (\n                    id INTEGER PRIMARY KEY,\n                    client_id INTEGER NOT NULL,\n                    age INTEGER NOT NULL,\n                    sexe TEXT NOT NULL,\n                    poids_kg REAL NOT NULL,\n                    taille_cm REAL NOT NULL,\n                    objectif_principal TEXT NOT NULL,\n                    niveau_activite TEXT NOT NULL,\n                    restrictions_alimentaires TEXT DEFAULT '[]',\n                    regimes_compatibles TEXT DEFAULT '[]',\n                    aliments_preferes TEXT DEFAULT '[]',\n                    aliments_exclus TEXT DEFAULT '[]',\n                    nombre_repas_souhaite INTEGER DEFAULT 3,\n                    metabolism_basal REAL,\n                    besoins_caloriques REAL,\n                    repartition_macros TEXT DEFAULT '{}',\n                    date_creation TEXT NOT NULL,\n                    date_mise_a_jour TEXT NOT NULL,\n                    FOREIGN KEY(client_id) REFERENCES clients(id),\n                    UNIQUE(client_id)\n                )\n                \"\"\"\n            )\n            conn.commit()