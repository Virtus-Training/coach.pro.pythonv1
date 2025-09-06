import customtkinter as ctk

from ui.pages.session_preview_panel import render_preview


class SessionPreview(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._current_dto = None
        self._last_cols = None

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text="Aperçu de la Séance",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.title.grid(row=0, column=0, sticky="ew", pady=(16, 0), padx=16)

        # Scrollable container for preview content
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)

        self.empty_label = ctk.CTkLabel(
            self.content_frame,
            text="Générez une séance pour voir l'aperçu",
            font=ctk.CTkFont(size=14),
        )
        self.empty_label.pack(fill="both", expand=True)

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
        self._last_cols = render_preview(self.content_frame, session_dto)
import customtkinter as ctk
from tkinter import filedialog, messagebox

from ui.components.design_system import PrimaryButton, SecondaryButton
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

        self.title = ctk.CTkLabel(
            self,
            text="Aperçu de la Séance",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.title.grid(row=0, column=0, sticky="ew", pady=(16, 0), padx=16)

        # Scrollable container for preview content
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)

        self.empty_label = ctk.CTkLabel(
            self.content_frame,
            text="Générez une séance pour voir l'aperçu",
            font=ctk.CTkFont(size=14),
        )
        self.empty_label.pack(fill="both", expand=True)

        # Footer action bar
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        if self._show_actions:
            self.footer.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))
            self.footer.grid_columnconfigure(0, weight=1)
            SecondaryButton(
                self.footer,
                text="Exporter PDF",
                command=self._on_export_pdf,
            ).grid(row=0, column=1, padx=6, sticky="e")
            PrimaryButton(
                self.footer,
                text="Enregistrer",
                command=self._on_save_session,
            ).grid(row=0, column=2, padx=6, sticky="e")

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
        self._last_cols = render_preview(self.content_frame, session_dto)

    # --- Actions
    def _on_save_session(self):  # pragma: no cover - UI callback
        if not self._current_dto:
            return
        try:
            self.controller.save_session(self._current_dto, self._current_client_id)
            messagebox.showinfo("Succès", "Séance enregistrée dans la base de données.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer: {e}")

    def _on_export_pdf(self):  # pragma: no cover - UI callback
        if not self._current_dto:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")]
        )
        if not path:
            return
        try:
            self.controller.export_session_to_pdf(
                self._current_dto, self._current_client_id, path
            )
            messagebox.showinfo("Export PDF", "Export réalisé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'export PDF: {e}")
