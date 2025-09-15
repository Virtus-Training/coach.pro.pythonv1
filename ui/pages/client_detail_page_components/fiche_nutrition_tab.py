import datetime
from dataclasses import asdict
from tkinter import filedialog

import customtkinter as ctk

from controllers.client_controller import ClientController
from controllers.nutrition_controller import NutritionController
from services.nutrition_service import ACTIVITY_FACTORS, OBJECTIVE_ADJUST
from ui.components.design_system import Card, CardTitle, PrimaryButton
from utils.ui_helpers import bring_to_front


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
        colors = ctk.ThemeManager.theme["color"]
        ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Body"])._kwargs
        if not self.fiche:
            message = (
                "Aucune fiche nutritionnelle n'a encore été générée pour ce client."
            )
            ctk.CTkLabel(
                self.display,
                text=message,
                text_color=colors["primary_text"],
                font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Body"]),
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
                    text_color=colors["primary_text"],
                    font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Body"]),
                ).grid(row=row, column=0, sticky="w", pady=2)
                ctk.CTkLabel(
                    info_frame,
                    text=value,
                    text_color=colors["primary_text"],
                    font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Body"]),
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
        self.geometry("480x700")
        try:
            bring_to_front(self, make_modal=True)
        except Exception:
            pass

        c = parent.client
        # Identité
        self.prenom_var = ctk.StringVar(value=str(getattr(c, "prenom", "") or ""))
        self.nom_var = ctk.StringVar(value=str(getattr(c, "nom", "") or ""))
        # Mesures
        self.poids_var = ctk.StringVar(value=str(c.poids_kg or ""))
        self.taille_var = ctk.StringVar(value=str(c.taille_cm or ""))
        # Date JJ/MM/AAAA
        self.date_var = ctk.StringVar(value="")
        if c.date_naissance:
            try:
                d = datetime.date.fromisoformat(c.date_naissance)
                self.date_var.set(d.strftime("%d/%m/%Y"))
            except Exception:
                self.date_var.set(c.date_naissance)
        self.sexe_var = ctk.StringVar(value=c.sexe or "Homme")
        self.activite_var = ctk.StringVar(value=c.niveau_activite or "Sédentaire")
        self.obj_var = ctk.StringVar(value="Maintenance")
        self.prot_var = ctk.DoubleVar(value=1.8)
        self.ratio_var = ctk.DoubleVar(value=30.0)

        form = ctk.CTkScrollableFrame(self)
        form.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        frame = form
        colors = ctk.ThemeManager.theme["color"]

        def add_entry(label: str, var):
            ctk.CTkLabel(frame, text=label, text_color=colors["primary_text"]).pack(
                anchor="w"
            )
            ctk.CTkEntry(frame, textvariable=var).pack(fill="x", pady=(0, 10))

        # Identité
        add_entry("Prénom", self.prenom_var)
        add_entry("Nom", self.nom_var)
        # Mesures
        add_entry("Poids (kg)", self.poids_var)
        add_entry("Taille (cm)", self.taille_var)
        add_entry("Date de naissance (JJ/MM/AAAA)", self.date_var)

        ctk.CTkLabel(frame, text="Sexe", text_color=colors["primary_text"]).pack(
            anchor="w"
        )
        ctk.CTkOptionMenu(
            frame, variable=self.sexe_var, values=["Homme", "Femme"]
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame, text="Niveau d'activité", text_color=colors["primary_text"]
        ).pack(anchor="w")
        ctk.CTkOptionMenu(
            frame, variable=self.activite_var, values=list(ACTIVITY_FACTORS.keys())
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame, text="Objectif", text_color=colors["primary_text"]).pack(
            anchor="w"
        )
        ctk.CTkOptionMenu(
            frame, variable=self.obj_var, values=list(OBJECTIVE_ADJUST.keys())
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            frame, text="Protéines (g/kg)", text_color=colors["primary_text"]
        ).pack(anchor="w")
        ctk.CTkSlider(
            frame, from_=1.0, to=3.0, number_of_steps=20, variable=self.prot_var
        ).pack(fill="x", pady=(0, 2))
        self.prot_value_lbl = ctk.CTkLabel(
            frame,
            text=f"{float(self.prot_var.get()):.1f}",
            text_color=colors["primary_text"],
        )
        self.prot_value_lbl.pack(anchor="e", pady=(0, 8))
        self.prot_var.trace_add(
            "write",
            lambda *_: self.prot_value_lbl.configure(
                text=f"{float(self.prot_var.get()):.1f}"
            ),
        )

        ctk.CTkLabel(
            frame, text="Répartition G/L (%)", text_color=colors["primary_text"]
        ).pack(anchor="w")
        ctk.CTkSlider(
            frame, from_=0, to=100, number_of_steps=100, variable=self.ratio_var
        ).pack(fill="x", pady=(0, 2))
        self.ratio_value_lbl = ctk.CTkLabel(
            frame,
            text=f"{int(float(self.ratio_var.get()))}%",
            text_color=colors["primary_text"],
        )
        self.ratio_value_lbl.pack(anchor="e", pady=(0, 8))
        self.ratio_var.trace_add(
            "write",
            lambda *_: self.ratio_value_lbl.configure(
                text=f"{int(float(self.ratio_var.get()))}%"
            ),
        )

        # Footer (erreur + action)
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=(0, 16))
        self.error_lbl = ctk.CTkLabel(
            footer,
            text="",
            text_color=ctk.ThemeManager.theme["color"].get("error", "#EF4444"),
        )
        self.error_lbl.pack(side="left")
        ctk.CTkButton(
            footer,
            text="Générer",
            command=self.generate,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]),
        ).pack(side="right")

    def _parse_age(self, date_str: str | None) -> int:
        if not date_str:
            return 0
        try:
            d = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
        except Exception:
            try:
                d = datetime.date.fromisoformat(date_str)
            except Exception:
                return 0
        today = datetime.date.today()
        return today.year - d.year - ((today.month, today.day) < (d.month, d.day))

    def generate(self):
        self.error_lbl.configure(text="")
        try:
            poids = float(self.poids_var.get())
        except Exception:
            self.error_lbl.configure(text="Veuillez saisir un poids valide (kg).")
            return
        try:
            taille = float(self.taille_var.get())
        except Exception:
            self.error_lbl.configure(text="Veuillez saisir une taille valide (cm).")
            return

        age = self._parse_age(self.date_var.get())
        data = {
            "poids_kg": poids,
            "taille_cm": taille,
            "age": age,
            "sexe": self.sexe_var.get(),
            "niveau_activite": self.activite_var.get(),
            "objectif": self.obj_var.get(),
            "proteines_g_par_kg": float(self.prot_var.get()),
            "ratio_glucides": float(self.ratio_var.get()),
        }
        try:
            fiche = self.parent.nutrition_controller.generate_nutrition_sheet(
                self.parent.client_id, data
            )
        except Exception as e:
            self.error_lbl.configure(text=f"Erreur: {e}")
            return

        self.parent.fiche = fiche

        # Enregistrement immédiat en PDF + ouverture
        try:
            import os
            import subprocess
            import sys

            prenom = (
                self.prenom_var.get() or getattr(self.parent.client, "prenom", "") or ""
            ).strip()
            nom = (
                self.nom_var.get() or getattr(self.parent.client, "nom", "") or ""
            ).strip()
            default_name = f"Fiche_Nutrition_{prenom}_{nom}_{datetime.date.today().isoformat()}.pdf".replace(
                " ", "_"
            )
            path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=default_name,
                filetypes=[("PDF", "*.pdf")],
            )
            if path:
                try:
                    self.parent.client.prenom = prenom or self.parent.client.prenom
                    self.parent.client.nom = nom or self.parent.client.nom
                except Exception:
                    pass
                self.parent.nutrition_controller.export_sheet_to_pdf(
                    asdict(fiche), self.parent.client, path
                )
                try:
                    if os.name == "nt":
                        os.startfile(path)  # type: ignore[attr-defined]
                    elif sys.platform == "darwin":
                        subprocess.run(["open", path], check=False)
                    else:
                        subprocess.run(["xdg-open", path], check=False)
                except Exception:
                    pass
        except Exception:
            pass

        try:
            self.parent.refresh()
        except Exception:
            pass
        self.destroy()
