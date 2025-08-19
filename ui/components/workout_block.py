"""Compact visual card representing a workout block."""

import customtkinter as ctk

FORMAT_COLORS = {
    "EMOM": "#22D3EE",
    "AMRAP": "#F59E0B",
    "FOR_TIME": "#10B981",
    "TABATA": "#A78BFA",
    "SETSxREPS": "#94A3B8",
}


class WorkoutBlock(ctk.CTkFrame):
    """Block card with a colored strip and compact exercise list."""

    def __init__(self, parent, title: str, fmt: str, duration: str = ""):
        super().__init__(parent, fg_color="#1d1d1d", corner_radius=8)
        color = FORMAT_COLORS.get(fmt.upper(), "#94A3B8")

        strip = ctk.CTkFrame(self, fg_color=color, width=4, corner_radius=0)
        strip.pack(side="left", fill="y")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        header = ctk.CTkFrame(body, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=title, font=("", 13, "bold")).pack(side="left")
        if duration:
            ctk.CTkLabel(
                header, text=duration, text_color="#9ca3af", font=("", 12)
            ).pack(side="right")

        self._ex_container = ctk.CTkFrame(body, fg_color="transparent")
        self._ex_container.pack(fill="both", expand=True, pady=(4, 0))

    # ------------------------------------------------------------------
    def add_exercise(
        self,
        nom: str,
        reps: str | None,
        repos_s: int | None,
        muscle: str,
        equip: str,
    ) -> None:
        """Render a compact two-line exercise entry."""

        wrapper = ctk.CTkFrame(self._ex_container, fg_color="transparent")
        wrapper.pack(fill="x", pady=2)

        top = ctk.CTkFrame(wrapper, fg_color="transparent")
        top.pack(fill="x")
        ctk.CTkLabel(top, text=nom, font=("", 12, "bold")).pack(side="left")

        chips: list[str] = []
        if reps:
            chips.append(reps)
        if repos_s is not None:
            chips.append(f"repos {repos_s}s")
        if chips:
            chip = ctk.CTkLabel(
                top,
                text=" • ".join(chips),
                fg_color="#2a2a2a",
                corner_radius=6,
                padx=4,
                pady=1,
                font=("", 11),
                text_color="#d1d5db",
            )
            chip.pack(side="right")

        bottom_txt = " · ".join(filter(None, [muscle, equip]))
        ctk.CTkLabel(
            wrapper, text=bottom_txt, font=("", 11), text_color="#9ca3af"
        ).pack(anchor="w")


__all__ = ["WorkoutBlock", "FORMAT_COLORS"]
