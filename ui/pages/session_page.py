import customtkinter as ctk
from ui.theme.fonts import get_section_font
from services.session_generator import generate_collectif

# Import the new, refactored components
from .session_page_components.session_form import SessionForm
from .session_page_components.session_preview import SessionPreview

class SessionPage(ctk.CTkFrame):
    """
    The main page for the session generator.
    This class acts as a controller, initializing the form and preview components
    and managing the communication between them.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1b1b1b")
        self._full_preview_win = None
        self._last_session = None
        self._form_hidden = False

        # --- Main Layout ---
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Form column (fixed width)
        self.grid_columnconfigure(1, weight=1)  # Preview column (flexible)

        # --- Page Title ---
        ctk.CTkLabel(self, text="Générateur de séances – Collectifs (V1)",
                     font=get_section_font()).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16,8))

        # --- Left Column: The Form ---
        self.form = SessionForm(
            parent=self,
            generate_callback=self.on_generate,
            open_preview_callback=self.open_full_preview,
            toggle_form_callback=self.toggle_form
        )
        self.form.grid(row=1, column=0, sticky="nsw", padx=(16,8), pady=8)

        # --- Right Column: The Preview ---
        self.preview = SessionPreview(self)
        self.preview.grid(row=1, column=1, sticky="nsew", padx=(8,16), pady=8)

    def toggle_form(self):
        """Shows or hides the form panel."""
        if not self._form_hidden:
            self.form.grid_remove()
            self._form_hidden = True
        else:
            self.form.grid(row=1, column=0, sticky="nsw", padx=(16,8), pady=8)
            self._form_hidden = False

    def on_generate(self):
        """
        Called when the 'Generate' button is clicked.
        Gets parameters from the form, generates a session, and tells the preview to render it.
        """
        params = self.form.get_params()
        session = generate_collectif(params)
        self._last_session = session
        self.preview.render_session(session)

        # If the full preview window is open, update it as well
        if self._full_preview_win and self._full_preview_win.winfo_exists():
            # Clear previous content
            for widget in self._full_preview_win.winfo_children():
                widget.destroy()
            # Re-render the new session in the preview window
            full_preview = SessionPreview(self._full_preview_win)
            full_preview.pack(fill="both", expand=True, padx=16, pady=16)
            full_preview.render_session(self._last_session)

    def open_full_preview(self):
        """Opens a new top-level window to display the session in full screen."""
        if self._full_preview_win and self._full_preview_win.winfo_exists():
            self._full_preview_win.focus()
            return

        if not self._last_session:
            # Here you might want to show a message to the user
            print("Please generate a session first.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Aperçu de séance — Plein écran")
        win.geometry("1280x860")
        win.configure(fg_color="#131313")
        self._full_preview_win = win

        # Use a new SessionPreview component to render the content in the new window
        full_preview = SessionPreview(win)
        full_preview.pack(fill="both", expand=True, padx=16, pady=16)
        full_preview.render_session(self._last_session)
