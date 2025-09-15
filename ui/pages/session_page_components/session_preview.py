from tkinter import filedialog, messagebox

import customtkinter as ctk

from ui.components.design_system import CardTitle, PrimaryButton, SecondaryButton
from ui.pages.session_preview_panel import render_preview


class SessionPreview(ctk.CTkFrame):
    def __init__(self, parent, controller, show_action_buttons: bool = True):
        super().__init__(parent)
        self.controller = controller
        self._current_dto = None
        self._current_client_id = None
        self._last_cols = None
        self._show_actions = show_action_buttons

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Header professionnel avec gradient
        self.header = ctk.CTkFrame(
            self, fg_color=("gray95", "gray20"), corner_radius=12, height=60
        )
        self.header.grid(row=0, column=0, sticky="ew", pady=(16, 8), padx=16)
        self.header.grid_propagate(False)

        header_content = ctk.CTkFrame(self.header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=16, pady=12)

        CardTitle(header_content, text="📋 Aperçu de la Séance").pack(
            side="left", anchor="w"
        )

        # Indicateur de statut
        self.status_indicator = ctk.CTkLabel(
            header_content,
            text="Prêt",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray60", "gray40"),
        )
        self.status_indicator.pack(side="right", anchor="e")

        # Scrollable container for preview content avec style amélioré
        self.content_frame = ctk.CTkScrollableFrame(
            self, fg_color=("gray98", "gray17"), corner_radius=8
        )
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=8)

        # Message d'état initial plus attractif
        self.empty_state = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.empty_state.pack(fill="both", expand=True, padx=32, pady=64)

        empty_icon = ctk.CTkLabel(
            self.empty_state, text="🎯", font=ctk.CTkFont(size=48)
        )
        empty_icon.pack(pady=(0, 16))

        self.empty_label = ctk.CTkLabel(
            self.empty_state,
            text="Générez une séance pour voir l'aperçu",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray50", "gray60"),
        )
        self.empty_label.pack(pady=(0, 8))

        empty_subtitle = ctk.CTkLabel(
            self.empty_state,
            text="Utilisez le formulaire pour créer votre séance personnalisée",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray50"),
        )
        empty_subtitle.pack()

        # Footer action bar modernisé
        if self._show_actions:
            self.footer = ctk.CTkFrame(
                self, fg_color=("gray95", "gray20"), corner_radius=8, height=60
            )
            self.footer.grid(row=2, column=0, sticky="ew", padx=16, pady=(8, 16))
            self.footer.grid_propagate(False)
            self.footer.grid_columnconfigure(0, weight=1)

            footer_content = ctk.CTkFrame(self.footer, fg_color="transparent")
            footer_content.pack(fill="both", expand=True, padx=16, pady=12)

            # Boutons d'action avec icônes
            SecondaryButton(
                footer_content,
                text="📄 Exporter PDF",
                command=self._on_export_pdf,
                width=140,
            ).pack(side="right", padx=(8, 0))

            self.save_button = PrimaryButton(
                footer_content,
                text="💾 Enregistrer",
                command=self._on_save_session,
                width=140,
            )
            self.save_button.pack(side="right", padx=(8, 0))

            # Info session dans le footer
            self.session_info = ctk.CTkLabel(
                footer_content,
                text="",
                font=ctk.CTkFont(size=11),
                text_color=("gray60", "gray50"),
            )
            self.session_info.pack(side="left", anchor="w")

        # Reflow on resize
        self.bind("<Configure>", self._on_resize)

    def _predict_cols(self) -> int:
        try:
            width = self.winfo_toplevel().winfo_width()
        except Exception:
            width = self.winfo_width()
        return 2 if width >= 1200 else 1

    def _on_resize(self, _event=None):
        if not self._current_dto:
            return
        new_cols = self._predict_cols()
        if new_cols == self._last_cols:
            return
        self._last_cols = render_preview(self.content_frame, self._current_dto)

    def render_session(self, session_dto, client_id):
        # Store the dto and render using the shared renderer
        self._current_dto = session_dto
        self._current_client_id = client_id

        # Cacher l'état vide
        self.empty_state.pack_forget()

        # Mettre à jour les indicateurs
        self._update_session_indicators(session_dto)

        # Render le contenu
        self._last_cols = render_preview(self.content_frame, session_dto)

    def _update_session_indicators(self, session_dto):
        """Met à jour les indicateurs de status et d'info."""
        meta = session_dto.get("meta", {})
        blocks_count = len(session_dto.get("blocks", []))

        # Status indicator
        if meta.get("smart_generated"):
            self.status_indicator.configure(
                text="✨ IA", text_color=("green", "lightgreen")
            )
        else:
            self.status_indicator.configure(
                text="✅ Généré", text_color=("blue", "lightblue")
            )

        # Session info dans le footer
        if hasattr(self, "session_info"):
            duration = meta.get("duration", "")
            course_type = meta.get("course_type", "")
            info_text = f"📊 {blocks_count} blocs • {course_type} • {duration}"
            self.session_info.configure(text=info_text)

    # --- Actions
    def _on_save_session(self):  # pragma: no cover - UI callback
        if not self._current_dto:
            return
        try:
            # Feedback visuel
            original_text = self.save_button.cget("text")
            self.save_button.configure(text="💾 Enregistrement...")
            self.save_button.update()

            self.controller.save_session(self._current_dto, self._current_client_id)

            # Success feedback
            self.save_button.configure(text="✅ Enregistré!")
            self.after(2000, lambda: self.save_button.configure(text=original_text))

            messagebox.showinfo(
                "Succès", "✅ Séance enregistrée avec succès dans la base de données."
            )

        except Exception as e:
            self.save_button.configure(text=original_text)
            messagebox.showerror("Erreur", f"❌ Impossible d'enregistrer: {e}")

    def _on_export_pdf(self):  # pragma: no cover - UI callback
        if not self._current_dto:
            return

        # Nom par défaut basé sur la séance
        meta = self._current_dto.get("meta", {})
        default_name = f"Seance_{meta.get('course_type', 'Workout')}_{meta.get('duration', '')}.pdf"

        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialvalue=default_name,
        )
        if not path:
            return
        try:
            self.controller.export_session_to_pdf(
                self._current_dto, self._current_client_id, path
            )
            messagebox.showinfo("Export PDF", "📄 Export PDF réalisé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"❌ Échec de l'export PDF: {e}")
