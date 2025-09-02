import customtkinter as ctk


class SessionPreview(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text="Aperçu de la Séance",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.title.grid(row=0, column=0, sticky="ew", pady=(16, 0), padx=16)

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)

        self.empty_label = ctk.CTkLabel(
            self.content_frame,
            text="Générer une séance pour voir l'aperçu",
            font=ctk.CTkFont(size=14),
        )
        self.empty_label.pack(fill="both", expand=True)

    def render_session(self, session_dto, client_id):
        # ... (votre logique existante pour afficher la séance) ...
        pass
