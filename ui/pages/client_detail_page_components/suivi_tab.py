import customtkinter as ctk

from repositories.seance_repo import SeanceRepository
from ui.modals.session_log_modal import SessionLogModal


class SuiviTab(ctk.CTkFrame):
    def __init__(self, master, client_id: int):
        super().__init__(master, fg_color="transparent")
        self.client_id = client_id
        self.repo = SeanceRepository()

        ctk.CTkButton(
            self,
            text="Enregistrer une nouvelle séance",
            command=self._open_modal,
        ).pack(anchor="e", padx=10, pady=10)

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self._load_seances()

    def _load_seances(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        seances = self.repo.get_by_client_id(self.client_id)
        for s in seances:
            item = ctk.CTkFrame(self.list_frame)
            item.pack(fill="x", pady=5)
            ctk.CTkLabel(item, text=s.titre).pack(side="left", padx=10)
            ctk.CTkLabel(item, text=s.date_creation).pack(side="right", padx=10)

    def _open_modal(self):
        SessionLogModal(self, self.client_id, on_saved=self._load_seances)
