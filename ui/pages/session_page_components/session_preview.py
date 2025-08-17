import customtkinter as ctk

from repositories.exercices_repo import ExerciseRepository
from repositories.sessions_repo import SessionsRepository

from .block_card import BlockCard
from .ui_helpers import create_icon_label


class SessionPreview(ctk.CTkFrame):
    """
    A widget to display the full details of a generated session.
    It handles the empty state and the rendering of the session's header, blocks, and footer.
    """

    def __init__(self, parent):
        super().__init__(parent, fg_color="#171717", corner_radius=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.preview_scroll_area = ctk.CTkScrollableFrame(self, fg_color="#171717")
        self.preview_scroll_area.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        self._empty_frame = None
        self._last_session = None
        self.show_empty_state()

    def show_empty_state(self):
        """Displays a message when no session has been generated yet."""
        self.clear_preview()
        self._empty_frame = ctk.CTkFrame(
            self.preview_scroll_area, fg_color="#0f0f0f", corner_radius=12
        )
        self._empty_frame.pack(fill="both", expand=True, padx=16, pady=16)
        ctk.CTkLabel(
            self._empty_frame,
            text="Aucune séance générée.\nChoisis tes critères à gauche puis clique « Générer ».",
            justify="center",
        ).pack(padx=24, pady=32)

    def clear_preview(self):
        """Removes all widgets from the preview area."""
        if self._empty_frame:
            self._empty_frame.destroy()
            self._empty_frame = None

        for widget in self.preview_scroll_area.winfo_children():
            widget.destroy()

    def render_session(self, session, two_cols=True):
        """Renders a complete session object."""
        self.clear_preview()
        self._last_session = session
        self.preview_scroll_area._parent_canvas.yview_moveto(0.0)

        # --- Résumé (en-tête)
        header = ctk.CTkFrame(
            self.preview_scroll_area, fg_color="#1d2228", corner_radius=12
        )
        header.pack(fill="x", padx=12, pady=(12, 6))
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=12, pady=10)
        create_icon_label(left, "assets/icons/dumbbell.png", session.label).pack(
            side="left", padx=(0, 16)
        )
        create_icon_label(
            left, "assets/icons/clock.png", f"{session.duration_sec // 60} min"
        ).pack(side="left")

        # --- Grille responsive pour les cartes de bloc
        grid = ctk.CTkFrame(self.preview_scroll_area, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=6, pady=6)
        ncols = 2 if two_cols else 1
        for c in range(ncols):
            grid.grid_columnconfigure(c, weight=1, uniform="col")

        # --- Meta exercices (nom + matériel)
        repo = ExerciseRepository()
        all_ids = [it.exercise_id for b in session.blocks for it in b.items]
        if hasattr(repo, "get_name_equipment_by_ids"):
            meta_map = repo.get_name_equipment_by_ids(all_ids)
        else:
            names = repo.get_names_by_ids(all_ids)
            meta_map = {k: {"name": v, "equipment": []} for k, v in names.items()}

        # --- Cartes de blocs
        for i, b in enumerate(session.blocks):
            col = i % ncols
            row = i // ncols
            card = BlockCard(grid, b, meta_map)
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
            grid.grid_rowconfigure(row, weight=1)

        # --- Footer
        footer = ctk.CTkFrame(
            self.preview_scroll_area, fg_color="#1d2228", corner_radius=12
        )
        footer.pack(fill="x", padx=12, pady=(6, 12))
        ctk.CTkButton(footer, text="Enregistrer", command=self._save_session).pack(
            side="right", padx=10, pady=10
        )

    def _save_session(self):
        if self._last_session:
            SessionsRepository().save(self._last_session)
            # Maybe show a confirmation message
            print("Session saved!")
        else:
            print("No session to save.")
