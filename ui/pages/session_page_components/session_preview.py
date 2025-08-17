"""Session preview panel for generated sessions."""

from __future__ import annotations

import customtkinter as ctk

from ui.components.design_system import Card, CardTitle, PrimaryButton


class SessionPreview(ctk.CTkFrame):
    """Display area for generated session details."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._content.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        self._last_dto: dict | None = None
        self.show_empty_state()

    def show_empty_state(self) -> None:
        """Show a placeholder message when no session is available."""
        for w in self._content.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self._content,
            text="Aucune séance générée.\nChoisis tes critères à gauche puis clique « Générer ».",
            justify="center",
        ).pack(expand=True, padx=16, pady=16)

    def render_session(self, session_dto: dict) -> None:
        """Render the session preview from a DTO."""
        self._last_dto = session_dto
        for w in self._content.winfo_children():
            w.destroy()

        meta = session_dto.get("meta", {})
        if meta:
            header = Card(self._content)
            header.pack(fill="x", padx=8, pady=(0, 8))
            CardTitle(header, text=meta.get("title", "")).pack(
                side="left", padx=12, pady=8
            )
            if meta.get("duration"):
                ctk.CTkLabel(header, text=meta["duration"]).pack(
                    side="left", padx=12, pady=8
                )

        for block in session_dto.get("blocks", []):
            card = Card(self._content)
            card.pack(fill="x", padx=8, pady=8)
            CardTitle(card, text=block.get("title", "")).pack(
                anchor="w", padx=12, pady=(12, 8)
            )
            for ex in block.get("exercises", []):
                line = f"• {ex.get('nom', '')}"
                details: list[str] = []
                reps = ex.get("reps")
                if reps:
                    details.append(reps)
                rest = ex.get("repos_s")
                if rest:
                    details.append(f"repos {rest}s")
                if details:
                    line += " – " + " | ".join(details)
                ctk.CTkLabel(card, text=line, anchor="w", justify="left").pack(
                    fill="x", padx=20, pady=2
                )

        PrimaryButton(
            self._content, text="Enregistrer la séance", command=self._on_save
        ).pack(padx=8, pady=12, anchor="e")

    def _on_save(self) -> None:  # pragma: no cover - placeholder
        pass


__all__ = ["SessionPreview"]

