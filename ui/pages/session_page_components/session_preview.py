"""Session preview panel for generated sessions."""

from __future__ import annotations

import customtkinter as ctk

from ui.components.design_system import Card, CardTitle, PrimaryButton
from ui.components.workout_block import WorkoutBlock
from controllers.session_controller import SessionController


class SessionPreview(ctk.CTkFrame):
    """Display area for generated session details."""

    def __init__(self, parent, controller: SessionController) -> None:
        super().__init__(parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._content.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        self._last_dto: dict | None = None
        self._client_id: int | None = None
        self._grid: ctk.CTkFrame | None = None
        self._blocks: list[WorkoutBlock] = []
        self._save_btn: PrimaryButton | None = None
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

    def render_session(self, session_dto: dict, client_id: int | None = None) -> None:
        """Render the session preview from a DTO."""
        self._last_dto = session_dto
        self._client_id = client_id
        for w in self._content.winfo_children():
            w.destroy()

        self._blocks = []
        self._grid = None

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

        self._grid = ctk.CTkFrame(self._content, fg_color="transparent")
        self._grid.pack(fill="both", expand=True)

        for block in session_dto.get("blocks", []):
            wb = WorkoutBlock(
                self._grid,
                title=block.get("title", ""),
                fmt=block.get("format", ""),
                duration=block.get("duration", ""),
            )
            self._blocks.append(wb)
            for ex in block.get("exercises", []):
                wb.add_exercise(
                    ex.get("nom", ""),
                    ex.get("reps"),
                    ex.get("repos_s"),
                    ex.get("muscle", ""),
                    ex.get("equip", ""),
                )

        self.after(10, self._arrange_blocks)
        self._grid.bind("<Configure>", lambda e: self._arrange_blocks())

        self._save_btn = PrimaryButton(
            self._content, text="Enregistrer la séance", command=self._on_save
        )
        self._save_btn.pack(padx=8, pady=12, anchor="e")

    def _arrange_blocks(self) -> None:
        """Place workout blocks in a responsive grid."""
        if not self._grid:
            return
        width = self._grid.winfo_width()
        cols = 2 if width >= 480 else 1

        for blk in self._blocks:
            blk.grid_forget()

        for i, blk in enumerate(self._blocks):
            blk.grid(
                row=i // cols,
                column=i % cols,
                sticky="nsew",
                padx=8,
                pady=8,
            )

        for c in range(cols):
            self._grid.grid_columnconfigure(c, weight=1)

    def _on_save(self) -> None:  # pragma: no cover - UI callback
        if not self._last_dto or not self._save_btn:
            return
        self._save_btn.configure(state="disabled")
        self.controller.save_session(self._last_dto, self._client_id)
        print("Séance enregistrée !")


__all__ = ["SessionPreview"]
