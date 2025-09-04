from typing import Callable, List, Tuple

import customtkinter as ctk


class CommandPalette(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(
            master, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        )  # fallback if CTkToplevel not themed
        self.title("Commandes")
        self.geometry("520x420")
        self.resizable(True, True)
        self._commands: List[Tuple[str, Callable[[], None], bool, str | None]] = []
        self._filtered: List[int] = []

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        self.entry = ctk.CTkEntry(
            frame, placeholder_text="Tapez une commande… (ex: ajouter, modifier)"
        )
        self.entry.pack(fill="x", pady=(0, 8))
        self.entry.bind("<KeyRelease>", self._on_change)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Escape>", lambda _e=None: self.destroy())

        self.list = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        self.list.pack(fill="both", expand=True)

        self._labels: list[ctk.CTkLabel] = []
        self._active_index: int = 0

        try:
            self.transient(master)
            self.grab_set()
            self.attributes("-topmost", True)
            self.after(150, lambda: self.attributes("-topmost", False))
        except Exception:
            pass

    def add_command(
        self,
        label: str,
        action: Callable[[], None],
        enabled: bool = True,
        shortcut: str | None = None,
    ):
        self._commands.append((label, action, enabled, shortcut))

    def open(self):
        self._render()
        self.entry.focus_set()

    def _render(self):
        for w in self.list.winfo_children():
            w.destroy()
        self._labels.clear()
        self._filtered = [i for i, c in enumerate(self._commands) if c[2]]
        for i in self._filtered:
            label, _action, _enabled, shortcut = self._commands[i]
            text = f"{label}" + (f"   ({shortcut})" if shortcut else "")
            label_widget = ctk.CTkLabel(self.list, text=text)
            label_widget.pack(fill="x", pady=2)
            self._labels.append(label_widget)
        self._active_index = 0
        self._highlight()
        # Bind arrows after list created
        self.bind("<Down>", lambda _e=None: self._move(1))
        self.bind("<Up>", lambda _e=None: self._move(-1))

    def _on_change(self, _e=None):
        q = self.entry.get().strip().lower()
        for w in self.list.winfo_children():
            w.destroy()
        self._labels.clear()
        self._filtered.clear()
        for i, (label, _action, enabled, shortcut) in enumerate(self._commands):
            if not enabled:
                continue
            if q and q not in label.lower():
                continue
            text = f"{label}" + (f"   ({shortcut})" if shortcut else "")
            label_widget = ctk.CTkLabel(self.list, text=text)
            label_widget.pack(fill="x", pady=2)
            self._labels.append(label_widget)
            self._filtered.append(i)
        self._active_index = 0
        self._highlight()

    def _highlight(self):
        for idx, label_widget in enumerate(self._labels):
            if idx == self._active_index:
                try:
                    label_widget.configure(
                        text_color=ctk.ThemeManager.theme["color"].get(
                            "primary", "#22D3EE"
                        )
                    )
                except Exception:
                    pass
            else:
                label_widget.configure(text_color=None)

    def _move(self, delta: int):
        if not self._labels:
            return
        self._active_index = max(
            0, min(len(self._labels) - 1, self._active_index + delta)
        )
        self._highlight()

    def _on_enter(self, _e=None):
        if not self._labels or not self._filtered:
            return
        cmd_index = self._filtered[self._active_index]
        _label, action, _enabled, _sc = self._commands[cmd_index]
        try:
            self.destroy()
        except Exception:
            pass
        action()
