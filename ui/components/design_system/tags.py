from typing import Callable, Iterable, List, Optional

import customtkinter as ctk


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % rgb


def _blend(c1: str, c2: str, t: float) -> str:
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return _rgb_to_hex((r, g, b))


class TagRadioGroup(ctk.CTkFrame):
    """Single-choice pill-like selector built on CTkSegmentedButton.

    - label: title shown above the control
    - options: list of string options to choose from
    """

    def __init__(
        self,
        master,
        label: str,
        options: Iterable[str],
        helper: str | None = None,
        on_change: Optional[Callable[[Optional[str]], None]] = None,
    ):
        super().__init__(master, fg_color="transparent")
        self._colors = ctk.ThemeManager.theme.get("color", {})
        self._fonts = ctk.ThemeManager.theme.get("font", {})
        self._on_change = on_change

        ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont(**self._fonts.get("Body", {})),
            text_color=self._colors.get("primary_text"),
        ).pack(anchor="w")
        if helper:
            ctk.CTkLabel(
                self,
                text=helper,
                font=ctk.CTkFont(**self._fonts.get("Small", {})),
                text_color=self._colors.get("secondary_text", "#9CA3AF"),
            ).pack(anchor="w")

        self._seg = ctk.CTkSegmentedButton(self, values=list(options))
        self._seg.pack(fill="x", pady=(4, 0))
        try:
            self._seg.configure(
                command=lambda v: self._on_change(v) if self._on_change else None
            )
        except Exception:
            pass

    def get_value(self) -> Optional[str]:
        val = self._seg.get()
        return val if val else None

    def set_value(self, value: Optional[str]) -> None:
        if value:
            try:
                self._seg.set(value)
            except Exception:
                pass
        if self._on_change:
            self._on_change(self.get_value())


class TagCheckboxGroup(ctk.CTkFrame):
    """Multi-select group rendered as a grid of checkboxes with a live list of selected tags.

    Methods:
    - get_values() -> List[str]
    - set_values(values: Iterable[str]) -> None
    - get_csv() -> Optional[str]
    """

    def __init__(
        self,
        master,
        label: str,
        options: Iterable[str],
        columns: int = 3,
        helper: str | None = None,
        compact: bool = False,
        on_change: Optional[Callable[[List[str]], None]] = None,
    ):
        super().__init__(master, fg_color="transparent")
        self._colors = ctk.ThemeManager.theme.get("color", {})
        self._fonts = ctk.ThemeManager.theme.get("font", {})
        self._columns = max(1, int(columns))
        self._vars: dict[str, ctk.BooleanVar] = {}
        self._on_change = on_change

        ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont(**self._fonts.get("Body", {})),
            text_color=self._colors.get("primary_text"),
        ).pack(anchor="w")
        if helper:
            ctk.CTkLabel(
                self,
                text=helper,
                font=ctk.CTkFont(**self._fonts.get("Small", {})),
                text_color=self._colors.get("secondary_text", "#9CA3AF"),
            ).pack(anchor="w")

        self._grid = ctk.CTkFrame(self, fg_color="transparent")
        self._grid.pack(fill="x", pady=(6, 4))

        # Build grid of checkboxes
        r = 0
        c = 0
        for opt in options:
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(
                self._grid, text=opt, variable=var, command=self._on_toggle
            )
            pad_x = (0, 8 if compact else 12)
            pad_y = (0, 4 if compact else 6)
            cb.grid(row=r, column=c, padx=pad_x, pady=pad_y, sticky="w")
            self._vars[opt] = var
            c += 1
            if c >= self._columns:
                c = 0
                r += 1

        # Selected tags area
        self._tags_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._tags_frame.pack(fill="x", pady=(4, 0))

        self._render_pills()

    def _on_toggle(self):
        self._render_pills()
        if self._on_change:
            self._on_change(self.get_values())

    def _clear_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def _render_pills(self):
        self._clear_frame(self._tags_frame)
        selected = self.get_values()
        if not selected:
            return
        # Render tag-like pills
        # Colors pulled from segmented button theme to match selected/unselected palette
        try:
            seg_theme = ctk.ThemeManager.theme.get("CTkSegmentedButton", {})
            sel_color = seg_theme.get("selected_color", ["#22D3EE"])[0]
        except Exception:
            sel_color = "#22D3EE"

        row = ctk.CTkFrame(self._tags_frame, fg_color="transparent")
        row.pack(anchor="w")
        for tag in selected:
            pill = ctk.CTkFrame(row, fg_color=sel_color, corner_radius=999)
            ctk.CTkLabel(
                pill,
                text=tag,
                padx=8,
                pady=2,
                font=("Segoe UI", 11, "bold"),
                text_color="#111827",
            ).pack()
            pill.pack(side="left", padx=(0, 6), pady=(2, 0))

    def get_values(self) -> List[str]:
        return [k for k, v in self._vars.items() if bool(v.get())]

    def set_values(self, values: Iterable[str]) -> None:
        wanted = {v.strip() for v in values if v is not None}
        for k, var in self._vars.items():
            var.set(k in wanted)
        self._render_pills()
        if self._on_change:
            self._on_change(self.get_values())

    def get_csv(self) -> Optional[str]:
        vals = self.get_values()
        if not vals:
            return None
        return ",".join(vals)


class ChipRadioGroup(ctk.CTkFrame):
    """Auto-wrapping chip radio group.

    Renders each option as a pill-shaped button that sizes to its text and wraps to the next line based on width.
    """

    def __init__(
        self,
        master,
        label: str,
        options: Iterable[str],
        helper: str | None = None,
        on_change: Optional[Callable[[Optional[str]], None]] = None,
        selected_color: str | None = None,
        unselected_color: str | None = None,
    ):
        super().__init__(master, fg_color="transparent")
        self._colors = ctk.ThemeManager.theme.get("color", {})
        self._fonts = ctk.ThemeManager.theme.get("font", {})
        self._on_change = on_change
        self._selected: Optional[str] = None

        ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont(**self._fonts.get("Body", {})),
            text_color=self._colors.get("primary_text"),
        ).pack(anchor="w")
        if helper:
            ctk.CTkLabel(
                self,
                text=helper,
                font=ctk.CTkFont(**self._fonts.get("Small", {})),
                text_color=self._colors.get("secondary_text", "#9CA3AF"),
            ).pack(anchor="w")

        self._wrap = ctk.CTkFrame(self, fg_color="transparent")
        self._wrap.pack(fill="x", pady=(6, 4))

        seg_theme = ctk.ThemeManager.theme.get("CTkSegmentedButton", {})
        self._sel_color = (
            selected_color or seg_theme.get("selected_color", ["#22D3EE"])[0]
        )
        self._unsel_color = (
            unselected_color or seg_theme.get("unselected_color", ["#374151"])[0]
        )
        self._unsel_text = self._colors.get("primary_text", "#E5E7EB")

        self._chips: list[ctk.CTkButton] = []
        for opt in list(options):
            btn = ctk.CTkButton(
                self._wrap,
                text=opt,
                corner_radius=18,
                height=28,
                fg_color=self._unsel_color,
                hover_color=_blend(self._unsel_color, "#ffffff", 0.08),
                text_color=self._unsel_text,
                command=lambda v=opt: self._select(v),
            )
            btn.pack_forget()
            try:
                btn.configure(corner_radius=18)
            except Exception:
                pass
            self._chips.append(btn)

        self.bind("<Configure>", lambda _e: self._relayout())
        self.after(0, self._relayout)

    def _relayout(self):
        self.update_idletasks()
        w = self._wrap.winfo_width()
        if w <= 1:
            w = self.winfo_width()
        if w <= 1:
            w = 400
        x = 0
        row = 0
        col = 0
        for btn in self._chips:
            btn.update_idletasks()
            req = btn.winfo_reqwidth()
            if x + req > w and x > 0:
                row += 1
                col = 0
                x = 0
            btn.grid(row=row, column=col, padx=(0, 8), pady=(0, 6), sticky="w")
            col += 1
            x += req + 8

    def _apply_style(self, btn: ctk.CTkButton, selected: bool):
        if selected:
            btn.configure(fg_color=self._sel_color, text_color="#111827")
        else:
            btn.configure(fg_color=self._unsel_color, text_color=self._unsel_text)

    def _pulse(self, btn: ctk.CTkButton):
        try:
            c0 = self._sel_color
            c1 = _blend(self._sel_color, "#ffffff", 0.25)
            btn.configure(fg_color=c1)
            self.after(80, lambda: btn.configure(fg_color=c0))
        except Exception:
            pass

    def _select(self, value: str):
        self._selected = value
        for btn in self._chips:
            self._apply_style(btn, btn.cget("text") == value)
            if btn.cget("text") == value:
                self._pulse(btn)
        if self._on_change:
            self._on_change(self._selected)

    def get_value(self) -> Optional[str]:
        return self._selected

    def set_value(self, value: Optional[str]) -> None:
        if value is None:
            self._selected = None
            for b in self._chips:
                self._apply_style(b, False)
            if self._on_change:
                self._on_change(None)
            return
        self._select(value)


class ChipCheckboxGroup(ctk.CTkFrame):
    """Auto-wrapping chip checkbox group (multi-select)."""

    def __init__(
        self,
        master,
        label: str,
        options: Iterable[str],
        helper: str | None = None,
        on_change: Optional[Callable[[List[str]], None]] = None,
        selected_color: str | None = None,
        unselected_color: str | None = None,
    ):
        super().__init__(master, fg_color="transparent")
        self._colors = ctk.ThemeManager.theme.get("color", {})
        self._fonts = ctk.ThemeManager.theme.get("font", {})
        self._on_change = on_change
        self._selected: set[str] = set()

        ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont(**self._fonts.get("Body", {})),
            text_color=self._colors.get("primary_text"),
        ).pack(anchor="w")
        if helper:
            ctk.CTkLabel(
                self,
                text=helper,
                font=ctk.CTkFont(**self._fonts.get("Small", {})),
                text_color=self._colors.get("secondary_text", "#9CA3AF"),
            ).pack(anchor="w")

        self._wrap = ctk.CTkFrame(self, fg_color="transparent")
        self._wrap.pack(fill="x", pady=(6, 4))

        seg_theme = ctk.ThemeManager.theme.get("CTkSegmentedButton", {})
        self._sel_color = (
            selected_color or seg_theme.get("selected_color", ["#22D3EE"])[0]
        )
        self._unsel_color = (
            unselected_color or seg_theme.get("unselected_color", ["#374151"])[0]
        )
        self._unsel_text = self._colors.get("primary_text", "#E5E7EB")

        self._chips: list[ctk.CTkButton] = []
        for opt in list(options):
            btn = ctk.CTkButton(
                self._wrap,
                text=opt,
                corner_radius=18,
                height=28,
                fg_color=self._unsel_color,
                hover_color=_blend(self._unsel_color, "#ffffff", 0.08),
                text_color=self._unsel_text,
                command=lambda v=opt: self._toggle(v),
            )
            btn.pack_forget()
            try:
                btn.configure(corner_radius=18)
            except Exception:
                pass
            self._chips.append(btn)

        self.bind("<Configure>", lambda _e: self._relayout())
        self.after(0, self._relayout)

    def _relayout(self):
        self.update_idletasks()
        w = self._wrap.winfo_width()
        if w <= 1:
            w = self.winfo_width()
        if w <= 1:
            w = 400
        x = 0
        row = 0
        col = 0
        for btn in self._chips:
            btn.update_idletasks()
            req = btn.winfo_reqwidth()
            if x + req > w and x > 0:
                row += 1
                col = 0
                x = 0
            btn.grid(row=row, column=col, padx=(0, 8), pady=(0, 6), sticky="w")
            col += 1
            x += req + 8

    def _apply_style(self, btn: ctk.CTkButton, selected: bool):
        if selected:
            btn.configure(fg_color=self._sel_color, text_color="#111827")
        else:
            btn.configure(fg_color=self._unsel_color, text_color=self._unsel_text)

    def _pulse(self, btn: ctk.CTkButton):
        try:
            c0 = self._sel_color
            c1 = _blend(self._sel_color, "#ffffff", 0.25)
            btn.configure(fg_color=c1)
            self.after(80, lambda: btn.configure(fg_color=c0))
        except Exception:
            pass

    def _toggle(self, value: str):
        if value in self._selected:
            self._selected.remove(value)
        else:
            self._selected.add(value)
        for btn in self._chips:
            sel = btn.cget("text") in self._selected
            self._apply_style(btn, sel)
            if btn.cget("text") == value and sel:
                self._pulse(btn)
        if self._on_change:
            self._on_change(self.get_values())

    def get_values(self) -> List[str]:
        return list(self._selected)

    def set_values(self, values: Iterable[str]) -> None:
        self._selected = {v for v in values if v is not None}
        for btn in self._chips:
            self._apply_style(btn, btn.cget("text") in self._selected)
        if self._on_change:
            self._on_change(self.get_values())

    def get_csv(self) -> Optional[str]:
        vals = self.get_values()
        if not vals:
            return None
        return ",".join(vals)
