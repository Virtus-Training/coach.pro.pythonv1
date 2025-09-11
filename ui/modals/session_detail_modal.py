from tkinter import filedialog

import customtkinter as ctk
from utils.ui_helpers import bring_to_front

# Support execution of this file directly by fixing sys.path
try:
    from controllers.session_controller import SessionController
    from models.session import Session
    from ui.components.design_system import PrimaryButton, SecondaryButton
    from ui.pages.session_page_components.session_preview import SessionPreview
except ModuleNotFoundError:
    import os
    import sys

    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    from controllers.session_controller import SessionController
    from models.session import Session
    from ui.components.design_system import PrimaryButton, SecondaryButton
    from ui.pages.session_page_components.session_preview import SessionPreview


class SessionDetailModal(ctk.CTkToplevel):
    def __init__(self, parent, session: Session, controller: SessionController) -> None:
        super().__init__(parent)
        self.session = session
        self.controller = controller
        self.configure(fg_color=ctk.ThemeManager.theme["color"]["surface_dark"])
        self.title(session.label)
        self.geometry("700x600")
        self.resizable(False, False)
        self.grab_set()
        try:
            bring_to_front(self, make_modal=True)
        except Exception:
            pass

        self.dto = self.controller.build_preview_from_session(session)
        self.preview = SessionPreview(self, controller, show_action_buttons=False)
        self.preview.pack(fill="both", expand=True, padx=10, pady=10)
        self.preview.render_session(self.dto, session.client_id)

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(pady=10)
        PrimaryButton(footer, text="Exporter en PDF", command=self._on_export_pdf).pack(
            side="right", padx=5
        )
        SecondaryButton(footer, text="Fermer", command=self.destroy).pack(
            side="right", padx=5
        )

    def _on_export_pdf(self) -> None:  # pragma: no cover - UI callback
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")]
        )
        if path:
            self.controller.export_session_to_pdf(
                self.dto, self.session.client_id, path
            )


__all__ = ["SessionDetailModal"]
