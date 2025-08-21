import datetime
from dataclasses import asdict
from tkinter import filedialog

import customtkinter as ctk

from controllers.client_controller import ClientController
from controllers.nutrition_controller import NutritionController
from services.nutrition_service import ACTIVITY_FACTORS, OBJECTIVE_ADJUST
from ui.components.design_system import Card, CardTitle, PrimaryButton
from ui.theme.colors import TEXT
from ui.theme.fonts import get_text_font


class FicheNutritionTab(ctk.CTkFrame):
    def __init__(
        self,
        master,
        controller: ClientController,
        nutrition_controller: NutritionController,
        client_id: int,
    ):
        super().__init__(master, fg_color="transparent")
        self.client_id = client_id
        self.controller = controller
        self.nutrition_controller = nutrition_controller
        self.client = self.controller.get_client_by_id(client_id)
        self.fiche = self.nutrition_controller.get_last_sheet_for_client(client_id)

        self.display = Card(self)
        self.display.pack(fill="both", expand=True, padx=20, pady=20)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=20)
        PrimaryButton(
            btn_frame,
            text="Générer / Mettre à jour la fiche",
            command=self.open_modal,
        ).pack(side="left", padx=5)
        self.export_btn = PrimaryButton(
            btn_frame,
            text="Exporter en PDF",
            command=self.export_pdf,
        )
        self.export_btn.pack(side="left", padx=5)

        self.refresh()

    def refresh(self):
        for w in self.display.winfo_children():
            w.destroy()
        if not self.fiche:
            message = (
                "Aucune fiche nutritionnelle n'a encore été générée pour ce client."
            )
            ctk.CTkLabel(
                self.display,
                text=message,
                text_color=TEXT,
                font=get_text_font(),
            ).pack(expand=True, fill="both")
            self.export_btn.configure(state="disabled")
        else:
            self.export_btn.configure(state="normal")
            CardTitle(self.display, text="Dernière Fiche Nutritionnelle").pack(
                anchor="w", padx=20, pady=(20, 20)
            )
            info_frame = ctk.CTkFrame(self.display, fg_color="transparent")
            info_frame.pack(fill="x", padx=20)
            info_frame.grid_columnconfigure(0, weight=1)
            info_frame.grid_columnconfigure(1, weight=1)

            fields = [
                ("Date", str(self.fiche.date_creation)),
                ("Objectif", self.fiche.objectif),
                ("Maintenance", f"{self.fiche.maintenance_kcal} kcal"),
                ("Objectif (kcal)", f"{self.fiche.objectif_kcal} kcal"),
                ("Protéines", f"{self.fiche.proteines_g} g"),
                ("Glucides", f"{self.fiche.glucides_g} g"),
                ("Lipides", f"{self.fiche.lipides_g} g"),
            ]

            for row, (label, value) in enumerate(fields):
                ctk.CTkLabel(
                    info_frame,
                    text=label,
                    text_color=TEXT,
                    font=get_text_font(),
                ).grid(row=row, column=0, sticky="w", pady=2)
                ctk.CTkLabel(
                    info_frame,
                    text=value,
                    text_color=TEXT,
                    font=get_text_font(),
                ).grid(row=row, column=1, sticky="e", pady=2)

    # Modal
    def open_modal(self):
        GenerateFicheModal(self)

    def export_pdf(self):
        if not self.fiche or not self.client:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")]
        )
        if path:
            self.nutrition_controller.export_sheet_to_pdf(
                asdict(self.fiche), self.client, path
            )


class GenerateFicheModal(ctk.CTkToplevel):
    def __init__(self, parent: FicheNutritionTab):
        super().__init__(parent)
        self.parent = parent
        self.title("Générer une fiche")
        self.geometry("400x600")

        c = parent.client
        self.poids_var = ctk.StringVar(value=str(c.poids_kg or ""))
        self.taille_var = ctk.StringVar(value=str(c.taille_cm or ""))
        self.date_var = ctk.StringVar(value=c.date_naissance or "")
        self.sexe_var = ctk.StringVar(value=c.sexe or "Homme")
        self.activite_var = ctk.StringVar(value=c.niveau_activite or "Sédentaire")
        self.obj_var = ctk.StringVar(value="Maintenance")
        self.prot_var = ctk.DoubleVar(value=1.8)
        self.ratio_var = ctk.DoubleVar(value=self._default_ratio())

        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        def add_entry(label, var):
            ctk.CTkLabel(frame, text=label, text_color=TEXT).pack(anchor="w")
            ctk.CTkEntry(frame, textvariable=var).pack(fill="x", pady=(0, 10))

        add_entry("Poids (kg)", self.poids_var)
        add_entry("Taille (cm)", self.taille_var)
        add_entry("Date de naissance (AAAA-MM-JJ)", self.date_var)

        ctk.CTkLabel(frame, text="Sexe", text_color=TEXT).pack(anchor="w")
        ctk.CTkOptionMenu(
            frame, variable=self.sexe_var, values=["Homme", "Femme"]
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame, text="Niveau d'activité", text_color=TEXT).pack(anchor="w")
        ctk.CTkOptionMenu(
            frame,
            variable=self.activite_var,
            values=list(ACTIVITY_FACTORS.keys()),
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame, text="Objectif", text_color=TEXT).pack(anchor="w")
        ctk.CTkOptionMenu(
            frame,
            variable=self.obj_var,
            values=list(OBJECTIVE_ADJUST.keys()),
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame, text="Protéines (g/kg)", text_color=TEXT).pack(anchor="w")
        ctk.CTkSlider(
            frame, from_=1.0, to=3.0, number_of_steps=20, variable=self.prot_var
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame, text="Répartition G/L (%)", text_color=TEXT).pack(
            anchor="w"
        )
        ctk.CTkSlider(
            frame, from_=0, to=100, number_of_steps=100, variable=self.ratio_var
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkButton(self, text="Générer", command=self.generate).pack(pady=10)

    def _default_ratio(self) -> float:
        try:
            data = {
                "poids_kg": float(self.parent.client.poids_kg or 0),
                "taille_cm": float(self.parent.client.taille_cm or 0),
                "age": self._age(self.parent.client.date_naissance),
                "sexe": self.parent.client.sexe or "Homme",
                "niveau_activite": self.parent.client.niveau_activite or "Sédentaire",
                "objectif": "Maintenance",
            }
            res = self.parent.nutrition_controller.calculate_nutrition_targets(data)
            return res["ratio_glucides_lipides_cible"]
        except Exception:
            return 50.0

    def _age(self, date_str: str | None) -> int:
        if not date_str:
            return 0
        try:
            birth = datetime.date.fromisoformat(date_str)
            today = datetime.date.today()
            return (
                today.year
                - birth.year
                - ((today.month, today.day) < (birth.month, birth.day))
            )
        except Exception:
            return 0

    def generate(self):
        age = self._age(self.date_var.get())
        data = {
            "poids_kg": float(self.poids_var.get()),
            "taille_cm": float(self.taille_var.get()),
            "age": age,
            "sexe": self.sexe_var.get(),
            "niveau_activite": self.activite_var.get(),
            "objectif": self.obj_var.get(),
            "proteines_g_par_kg": float(self.prot_var.get()),
            "ratio_glucides": float(self.ratio_var.get()),
        }
        fiche = self.parent.nutrition_controller.generate_nutrition_sheet(
            self.parent.client_id, data
        )
        self.parent.fiche = fiche
        self.parent.refresh()
        self.destroy()
