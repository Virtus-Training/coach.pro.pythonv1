import customtkinter as ctk
from ui.theme.fonts import get_section_font
from ui.components.layout import two_columns
from ui.pages.session_preview_panel import render_preview
from .session_page_components.session_form import SessionForm
from controllers.session_controller import generate_session_preview

class SessionPage(ctk.CTkFrame):
    """
    The main page for the session generator.
    This class acts as a controller, initializing the form and preview components
    and managing the communication between them.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1b1b1b")
        self._full_preview_win = None
        self._full_preview_container = None
        self._last_session = None
        self._last_dto = None
        self._current_cols = 1
        self._form_hidden = False

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Générateur de séances – Collectifs (V1)",
            font=get_section_font(),
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        self.left_col, self.right_col = two_columns(content)
        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=8)
        self.right_col.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=8)

        self.form = SessionForm(
            parent=self.left_col,
            generate_callback=self.on_generate,
            open_preview_callback=self.open_full_preview,
            toggle_form_callback=self.toggle_form,
        )
        self.form.pack(fill="both", expand=True, padx=8, pady=8)

        ctk.CTkLabel(
            self.right_col,
            text="Aucune séance générée",
            text_color="#9ca3af",
        ).pack(padx=20, pady=20)

        self.bind("<Configure>", self._on_resize)

    def toggle_form(self):
        """Shows or hides the form panel."""
        if not self._form_hidden:
            self.left_col.grid_remove()
            self._form_hidden = True
        else:
            self.left_col.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=8)
            self._form_hidden = False

    def on_generate(self):
        """
        Called when the 'Generate' button is clicked.
        Gets parameters from the form, generates a session, and tells the preview to render it.
        """
        params = self.form.get_params()
        self._last_session, dto = generate_session_preview(params)
        self._last_dto = dto
        self._current_cols = render_preview(self.right_col, dto)

        if self._full_preview_win and self._full_preview_win.winfo_exists():
            render_preview(self._full_preview_container, dto)

    def open_full_preview(self):
        """Opens a new top-level window to display the session in full screen."""
        if self._full_preview_win and self._full_preview_win.winfo_exists():
            self._full_preview_win.focus()
            return

        if not self._last_dto:
            # Here you might want to show a message to the user
            print("Please generate a session first.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Aperçu de séance — Plein écran")
        win.geometry("1280x860")
        win.configure(fg_color="#131313")
        self._full_preview_win = win

        container = ctk.CTkScrollableFrame(win, fg_color="#131313")
        container.pack(fill="both", expand=True, padx=16, pady=16)
        self._full_preview_container = container
        render_preview(container, self._last_dto)
        win.bind("<Configure>", lambda e: render_preview(container, self._last_dto))
        self._full_preview_win = win

    def _on_resize(self, _event):
        if self._last_dto:
            cols = 2 if self.winfo_width() >= 1200 else 1
            if cols != self._current_cols:
                self._current_cols = render_preview(self.right_col, self._last_dto)
