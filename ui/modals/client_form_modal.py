import customtkinter as ctk
from typing import Optional
from tkinter import messagebox

from models.client import Client
from repositories.client_repo import ClientRepository
from ui.theme.fonts import get_title_font, get_text_font
from ui.theme.colors import DARK_BG, TEXT


class ClientFormModal(ctk.CTkToplevel):
    """Fenêtre modale pour ajouter ou modifier un client."""

    def __init__(self, parent, client_a_modifier: Optional[Client] = None):
        super().__init__(parent)
        self.client = client_a_modifier
        self.title("Ajouter/Modifier un client")
        self.geometry("400x340")
        self.configure(fg_color=DARK_BG)
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="Ajouter/Modifier un client",
            font=get_title_font(),
            text_color=TEXT,
        ).pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20)

        self.prenom_var = ctk.StringVar(value=self.client.prenom if self.client else "")
        self.nom_var = ctk.StringVar(value=self.client.nom if self.client else "")
        self.email_var = ctk.StringVar(value=self.client.email if self.client else "")
        self.date_var = ctk.StringVar(value=self.client.date_naissance if self.client else "")

        # Champ Prénom
        ctk.CTkLabel(form_frame, text="Prénom", font=get_text_font(), text_color=TEXT).pack(anchor="w")
        ctk.CTkEntry(form_frame, textvariable=self.prenom_var).pack(fill="x", pady=(0, 10))

        # Champ Nom
        ctk.CTkLabel(form_frame, text="Nom", font=get_text_font(), text_color=TEXT).pack(anchor="w")
        ctk.CTkEntry(form_frame, textvariable=self.nom_var).pack(fill="x", pady=(0, 10))

        # Champ Email
        ctk.CTkLabel(form_frame, text="Email", font=get_text_font(), text_color=TEXT).pack(anchor="w")
        ctk.CTkEntry(form_frame, textvariable=self.email_var).pack(fill="x", pady=(0, 10))

        # Champ Date de naissance
        ctk.CTkLabel(
            form_frame,
            text="Date de Naissance (AAAA-MM-JJ)",
            font=get_text_font(),
            text_color=TEXT,
        ).pack(anchor="w")
        ctk.CTkEntry(form_frame, textvariable=self.date_var).pack(fill="x", pady=(0, 10))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Enregistrer", command=self._on_save).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Annuler", command=self.destroy).pack(side="left", padx=5)

    def _on_save(self) -> None:
        prenom = self.prenom_var.get().strip()
        nom = self.nom_var.get().strip()
        email = self.email_var.get().strip() or None
        date_naissance = self.date_var.get().strip() or None

        if not prenom or not nom:
            messagebox.showerror("Erreur", "Le nom et le prénom sont obligatoires.")
            return

        repo = ClientRepository()

        if self.client:
            self.client.prenom = prenom
            self.client.nom = nom
            self.client.email = email
            self.client.date_naissance = date_naissance
            repo.update(self.client)
        else:
            nouveau_client = Client(
                id=None,
                prenom=prenom,
                nom=nom,
                email=email,
                date_naissance=date_naissance,
            )
            repo.add(nouveau_client)

        self.destroy()
