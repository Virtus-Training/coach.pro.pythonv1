import sqlite3
from typing import List

from models.plan_alimentaire import PlanAlimentaire, Repas, RepasItem

DB_PATH = "coach.db"


class PlanAlimentaireRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    # Plans
    def list_plans(self) -> List[PlanAlimentaire]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM plans_alimentaires ORDER BY nom"
            ).fetchall()
        return [
            PlanAlimentaire(
                id=row["id"],
                nom=row["nom"],
                description=row["description"],
                tags=row["tags"],
                repas=[],
            )
            for row in rows
        ]

    def get_plan(self, plan_id: int) -> PlanAlimentaire:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            plan_row = conn.execute(
                "SELECT * FROM plans_alimentaires WHERE id = ?", (plan_id,)
            ).fetchone()
            if not plan_row:
                raise ValueError("Plan introuvable")
            repas_rows = conn.execute(
                "SELECT * FROM repas WHERE plan_id = ? ORDER BY ordre", (plan_id,)
            ).fetchall()
            repas_list = []
            for rr in repas_rows:
                items_rows = conn.execute(
                    "SELECT * FROM repas_items WHERE repas_id = ?", (rr["id"],)
                ).fetchall()
                items = [
                    RepasItem(
                        id=ir["id"],
                        repas_id=ir["repas_id"],
                        aliment_id=ir["aliment_id"],
                        portion_id=ir["portion_id"],
                        quantite=ir["quantite"],
                    )
                    for ir in items_rows
                ]
                repas_list.append(
                    Repas(
                        id=rr["id"],
                        plan_id=rr["plan_id"],
                        nom=rr["nom"],
                        ordre=rr["ordre"],
                        items=items,
                    )
                )
            return PlanAlimentaire(
                id=plan_row["id"],
                nom=plan_row["nom"],
                description=plan_row["description"],
                tags=plan_row["tags"],
                repas=repas_list,
            )

    def create_plan(self, plan: PlanAlimentaire) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO plans_alimentaires (nom, description, tags) VALUES (?, ?, ?)",
                (plan.nom, plan.description, plan.tags),
            )
            plan_id = cur.lastrowid
            for repas in plan.repas:
                cur.execute(
                    "INSERT INTO repas (plan_id, nom, ordre) VALUES (?, ?, ?)",
                    (plan_id, repas.nom, repas.ordre),
                )
                repas_id = cur.lastrowid
                for item in repas.items:
                    cur.execute(
                        """
                        INSERT INTO repas_items (repas_id, aliment_id, portion_id, quantite)
                        VALUES (?, ?, ?, ?)
                        """,
                        (repas_id, item.aliment_id, item.portion_id, item.quantite),
                    )
            conn.commit()
            return plan_id

    def update_plan(self, plan: PlanAlimentaire) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE plans_alimentaires SET nom = ?, description = ?, tags = ? WHERE id = ?",
                (plan.nom, plan.description, plan.tags, plan.id),
            )
            repas_ids = [r[0] for r in cur.execute("SELECT id FROM repas WHERE plan_id = ?", (plan.id,)).fetchall()]
            for rid in repas_ids:
                cur.execute("DELETE FROM repas_items WHERE repas_id = ?", (rid,))
            cur.execute("DELETE FROM repas WHERE plan_id = ?", (plan.id,))
            for repas in plan.repas:
                cur.execute(
                    "INSERT INTO repas (plan_id, nom, ordre) VALUES (?, ?, ?)",
                    (plan.id, repas.nom, repas.ordre),
                )
                repas_id = cur.lastrowid
                for item in repas.items:
                    cur.execute(
                        """
                        INSERT INTO repas_items (repas_id, aliment_id, portion_id, quantite)
                        VALUES (?, ?, ?, ?)
                        """,
                        (repas_id, item.aliment_id, item.portion_id, item.quantite),
                    )
            conn.commit()

    def delete_plan(self, plan_id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            repas_ids = [r[0] for r in cur.execute("SELECT id FROM repas WHERE plan_id = ?", (plan_id,)).fetchall()]
            for rid in repas_ids:
                cur.execute("DELETE FROM repas_items WHERE repas_id = ?", (rid,))
            cur.execute("DELETE FROM repas WHERE plan_id = ?", (plan_id,))
            cur.execute("DELETE FROM plans_alimentaires WHERE id = ?", (plan_id,))
            conn.commit()

    # Repas CRUD
    def add_repas(self, plan_id: int, repas: Repas) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO repas (plan_id, nom, ordre) VALUES (?, ?, ?)",
                (plan_id, repas.nom, repas.ordre),
            )
            repas_id = cur.lastrowid
            conn.commit()
            return repas_id

    def update_repas(self, repas: Repas) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE repas SET nom = ?, ordre = ? WHERE id = ?",
                (repas.nom, repas.ordre, repas.id),
            )
            conn.commit()

    def delete_repas(self, repas_id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM repas_items WHERE repas_id = ?", (repas_id,))
            cur.execute("DELETE FROM repas WHERE id = ?", (repas_id,))
            conn.commit()

    # Items CRUD
    def add_item(self, repas_id: int, item: RepasItem) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO repas_items (repas_id, aliment_id, portion_id, quantite)
                VALUES (?, ?, ?, ?)
                """,
                (repas_id, item.aliment_id, item.portion_id, item.quantite),
            )
            item_id = cur.lastrowid
            conn.commit()
            return item_id

    def update_item(self, item: RepasItem) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE repas_items SET aliment_id = ?, portion_id = ?, quantite = ? WHERE id = ?",
                (item.aliment_id, item.portion_id, item.quantite, item.id),
            )
            conn.commit()

    def delete_item(self, item_id: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM repas_items WHERE id = ?", (item_id,))
            conn.commit()
