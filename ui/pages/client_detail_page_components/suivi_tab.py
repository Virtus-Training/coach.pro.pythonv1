import customtkinter as ctk

from repositories.seance_repo import SeanceRepository
from ui.components.design_system import Card, CardTitle, PrimaryButton
from ui.modals.session_log_modal import SessionLogModal


class SuiviTab(ctk.CTkFrame):
    def __init__(self, master, client_id: int):
        super().__init__(master, fg_color="transparent")
        self.client_id = client_id
        self.repo = SeanceRepository()

        PrimaryButton(
            self,
            text="Enregistrer une nouvelle séance",
            command=self._open_modal,
        ).pack(anchor="e", padx=20, pady=20)

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self._load_seances()

    def _load_seances(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        seances = self.repo.get_by_client_id(self.client_id)
        for s in seances:
            card = Card(self.list_frame)
            card.pack(fill="x", pady=10)

            CardTitle(card, text=s.titre).pack(anchor="w", padx=20, pady=(20, 5))
            colors = ctk.ThemeManager.theme["color"]
            fonts = ctk.ThemeManager.theme["font"]
            ctk.CTkLabel(
                card,
                text=s.date_creation,
                text_color=colors["secondary_text"],
                font=ctk.CTkFont(**fonts["Small"]),
            ).pack(anchor="w", padx=20)
            ctk.CTkLabel(
                card,
                text=f"Objectif: {s.type_seance}",
                text_color=colors["primary_text"],
                font=ctk.CTkFont(**fonts["Body"]),
            ).pack(anchor="w", padx=20, pady=(0, 20))

    def _open_modal(self):
        SessionLogModal(self, self.client_id, on_saved=self._load_seances)
