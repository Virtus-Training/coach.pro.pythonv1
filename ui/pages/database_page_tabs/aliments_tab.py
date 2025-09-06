from typing import List, Optional

import customtkinter as ctk

from models.aliment import Aliment
from repositories.aliment_repo import AlimentRepository
from ui.components.design_system import DataTable, LabeledInput


class AlimentForm(ctk.CTkToplevel):
    def __init__(self, master, on_submit, aliment: Optional[Aliment] = None):
        super().__init__(master)
        self.title("Aliment")
        self.geometry("520x520")
        self.resizable(False, False)
        self._on_submit = on_submit

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        self.in_nom = LabeledInput(frame, label="Nom")
        self.in_nom.pack(fill="x", pady=(0, 8))
        self.in_cat = LabeledInput(frame, label="Catégorie")
        self.in_cat.pack(fill="x", pady=(0, 8))
        self.in_type = LabeledInput(frame, label="Type d'alimentation")
        self.in_type.pack(fill="x", pady=(0, 8))
        self.in_kcal = LabeledInput(frame, label="Kcal/100g")
        self.in_kcal.pack(fill="x", pady=(0, 8))
        self.in_prot = LabeledInput(frame, label="Protéines/100g")
        self.in_prot.pack(fill="x", pady=(0, 8))
        self.in_gluc = LabeledInput(frame, label="Glucides/100g")
        self.in_gluc.pack(fill="x", pady=(0, 8))
        self.in_lip = LabeledInput(frame, label="Lipides/100g")
        self.in_lip.pack(fill="x", pady=(0, 8))
        self.in_unite = LabeledInput(frame, label="Unité base", text="g")
        self.in_unite.pack(fill="x", pady=(0, 8))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(fill="x", pady=(8, 0))
        ctk.CTkButton(btn_row, text="Annuler", command=self.destroy, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])).pack(side="right")
        ctk.CTkButton(btn_row, text="Enregistrer", command=self._submit, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])).pack(
            side="right", padx=(0, 8)
        )

        if aliment:
            self.in_nom.set_value(aliment.nom)
            self.in_cat.set_value(aliment.categorie or "")
            self.in_type.set_value(aliment.type_alimentation or "")
            self.in_kcal.set_value(str(aliment.kcal_100g))
            self.in_prot.set_value(str(aliment.proteines_100g))
            self.in_gluc.set_value(str(aliment.glucides_100g))
            self.in_lip.set_value(str(aliment.lipides_100g))
            self.in_unite.set_value(aliment.unite_base or "g")

        self.lift()
        self.focus()

    def _submit(self) -> None:
        nom = self.in_nom.get_value()
        if not nom:
            self.in_nom.show_error("Nom requis")
            return

        def _num(val: str) -> float:
            try:
                return float(val.replace(",", ".").strip()) if val.strip() else 0.0
            except Exception:
                return 0.0

        payload = {
            "nom": nom,
            "categorie": self.in_cat.get_value() or None,
            "type_alimentation": self.in_type.get_value() or None,
            "kcal": _num(self.in_kcal.get_value()),
            "prot": _num(self.in_prot.get_value()),
            "gluc": _num(self.in_gluc.get_value()),
            "lip": _num(self.in_lip.get_value()),
            "unite": self.in_unite.get_value() or "g",
        }
        self._on_submit(payload)
        self.destroy()


class AlimentsTab(ctk.CTkFrame):
    def __init__(self, parent, repo: AlimentRepository | None = None):
        super().__init__(parent, fg_color="transparent")
        self.repo = repo or AlimentRepository()

        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=10, pady=(10, 0))
        self.search_entry = ctk.CTkEntry(toolbar, placeholder_text="Rechercher...")
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search)

        self.btn_add = ctk.CTkButton(toolbar, text="Ajouter", command=self._on_add, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]))
        self.btn_add.pack(side="right", padx=(8, 0))
        self.btn_edit = ctk.CTkButton(
            toolbar, text="Modifier", command=self._on_edit, state="disabled", font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]))
        self.btn_edit.pack(side="right", padx=(8, 0))
        self.btn_del = ctk.CTkButton(
            toolbar, text="Supprimer", command=self._on_delete, state="disabled", font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]))
        self.btn_del.pack(side="right")

        self.selected_name: Optional[str] = None
        self._load()

    def _on_search(self, event):
        self.table.filter(self.search_entry.get())

    def _load(self) -> None:
        self.aliments: List[Aliment] = self.repo.list_all()
        data = [
            [a.nom, a.kcal_100g, a.proteines_100g, a.glucides_100g, a.lipides_100g]
            for a in self.aliments
        ]
        headers = ["Nom", "Kcal", "Protéines", "Glucides", "Lipides"]
        if hasattr(self, "table"):
            self.table.destroy()
        self.table = DataTable(
            self, headers=headers, data=data, on_select=self._on_select
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=(10, 10))
        self.selected_name = None
        self.btn_edit.configure(state="disabled")
        self.btn_del.configure(state="disabled")

    def _on_select(self, idx: int, row: list) -> None:
        self.selected_name = str(row[0]) if row else None
        state = "normal" if self.selected_name else "disabled"
        self.btn_edit.configure(state=state)
        self.btn_del.configure(state=state)

    def _on_add(self) -> None:
        def handle_submit(p: dict):
            a = Aliment(
                id=0,
                nom=p["nom"],
                categorie=p["categorie"],
                type_alimentation=p["type_alimentation"],
                kcal_100g=p["kcal"],
                proteines_100g=p["prot"],
                glucides_100g=p["gluc"],
                lipides_100g=p["lip"],
                fibres_100g=None,
                unite_base=p["unite"],
                indice_healthy=None,
                indice_commun=None,
            )
            self.repo.create(a)
            self._load()

        AlimentForm(self, on_submit=handle_submit)

    def _on_edit(self) -> None:
        if not self.selected_name:
            return
        a = self.repo.get_by_name(self.selected_name)
        if not a:
            return

        def handle_submit(p: dict):
            a.nom = p["nom"]
            a.categorie = p["categorie"]
            a.type_alimentation = p["type_alimentation"]
            a.kcal_100g = p["kcal"]
            a.proteines_100g = p["prot"]
            a.glucides_100g = p["gluc"]
            a.lipides_100g = p["lip"]
            a.unite_base = p["unite"]
            self.repo.update(a)
            self._load()

        AlimentForm(self, on_submit=handle_submit, aliment=a)

    def _on_delete(self) -> None:
        if not self.selected_name:
            return
        a = self.repo.get_by_name(self.selected_name)
        if not a:
            return
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirmer la suppression")
        ctk.CTkLabel(confirm, text=f"Supprimer '{a.nom}' ?").pack(padx=16, pady=16)
        row = ctk.CTkFrame(confirm, fg_color="transparent")
        row.pack(pady=(0, 12))

        def do_del():
            self.repo.delete(int(a.id))
            confirm.destroy()
            self._load()

        ctk.CTkButton(row, text="Annuler", command=confirm.destroy, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])).pack(
            side="left", padx=8
        )
        ctk.CTkButton(
            row,
            text="Supprimer",
            fg_color="#B00020",
            hover_color="#8E001A",
            command=do_del,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]),
        ).pack(side="left")

