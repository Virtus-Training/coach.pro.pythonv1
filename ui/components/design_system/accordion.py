import customtkinter as ctk


class AccordionSection(ctk.CTkFrame):
    """Collapsible section with a header and a smoothly-animated body.

    Usage:
        sec = AccordionSection(parent, title="Section", initially_open=True)
        sec.pack(fill="x")
        # Add children to sec.body
    """

    def __init__(self, master, title: str, initially_open: bool = True):
        super().__init__(master, fg_color="transparent")
        self._colors = ctk.ThemeManager.theme["color"]
        self._fonts = ctk.ThemeManager.theme["font"]
        self._open = bool(initially_open)

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x")
        self.header.configure(cursor="hand2")

        self._chev = ctk.CTkLabel(
            self.header,
            text=self._chevron(),
            font=ctk.CTkFont(**self._fonts["H3"]),
            text_color=self._colors["primary_text"],
            width=18,
        )
        self._chev.pack(side="left", padx=(0, 4))

        self._title = ctk.CTkLabel(
            self.header,
            text=title,
            font=ctk.CTkFont(**self._fonts["H3"]),
            text_color=self._colors["primary_text"],
        )
        self._title.pack(side="left")

        # Bind clicks on header and its children
        self.header.bind("<Button-1>", lambda _e: self.toggle())
        self._chev.bind("<Button-1>", lambda _e: self.toggle())
        self._title.bind("<Button-1>", lambda _e: self.toggle())

        # Body container (for height animation)
        self._container = ctk.CTkFrame(self, fg_color="transparent")
        self._container.pack(fill="x")
        self._container.pack_propagate(False)

        # Actual body content frame
        self.body = ctk.CTkFrame(self._container, fg_color="transparent")
        self.body.pack(fill="x", pady=(6, 8))

        # Initialize height
        self.after(0, self._init_height)

    def _chevron(self) -> str:
        return "▾" if self._open else "▸"

    def _init_height(self):
        self.update_idletasks()
        target = self.body.winfo_reqheight() if self._open else 0
        try:
            self._container.configure(height=target)
        except Exception:
            pass

    def toggle(self) -> None:
        if self._open:
            self.collapse()
        else:
            self.expand()

    def expand(self) -> None:
        if self._open:
            return
        self._open = True
        self._chev.configure(text=self._chevron())
        # light header flash animation
        try:
            base = self.header.cget("fg_color")
            self.header.configure(fg_color=self._colors.get("surface_light", base))
            self.after(120, lambda: self.header.configure(fg_color="transparent"))
        except Exception:
            pass
        self._animate(to_open=True)

    def collapse(self) -> None:
        if not self._open:
            return
        self._open = False
        self._chev.configure(text=self._chevron())
        self._animate(to_open=False)

    def _animate(self, to_open: bool, duration_ms: int = 180, steps: int = 6) -> None:
        # Animate container height from current to target
        self.update_idletasks()
        cur_h = self._container.winfo_height()
        target_h = self.body.winfo_reqheight() if to_open else 0
        if steps <= 0:
            steps = 1
        delta = (target_h - cur_h) / steps
        interval = max(10, duration_ms // steps)

        def step(i=0, h=cur_h):
            nh = int(h + delta)
            try:
                self._container.configure(height=max(0, nh))
            except Exception:
                pass
            if i + 1 < steps:
                self.after(interval, lambda: step(i + 1, nh))
            else:
                try:
                    self._container.configure(height=target_h)
                except Exception:
                    pass

        step()
