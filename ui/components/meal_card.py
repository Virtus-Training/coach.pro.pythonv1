from typing import Dict, List, Callable

import customtkinter as ctk

from ui.components.design_system.cards import Card
from ui.components.design_system.typography import CardTitle
from ui.theme.colors import PRIMARY, NEUTRAL_700


class MealCard(Card):
    def __init__(
        self,
        master,
        title: str,
        on_select: Callable[[], None],
        on_delete_item: Callable[[int], None],
    ) -> None:
        super().__init__(master)
        self.on_select = on_select
        self.on_delete_item = on_delete_item

        self.bind("<Button-1>", lambda e: self.on_select())

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=8, pady=4)
        for widget in [self, header]:
            widget.bind("<Button-1>", lambda e: self.on_select())

        self.title_label = CardTitle(header, text=title)
        self.title_label.pack(side="left")
        self.title_label.bind("<Button-1>", lambda e: self.on_select())

        self.totals_label = ctk.CTkLabel(header, text="0 kcal P0 G0 L0")
        self.totals_label.pack(side="right")
        self.totals_label.bind("<Button-1>", lambda e: self.on_select())

        self.items_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.items_frame.pack(fill="both", expand=True, padx=8, pady=4)

    def set_active(self, active: bool) -> None:
        color = PRIMARY if active else NEUTRAL_700
        self.configure(border_color=color)

    def update(self, items: List[Dict], totals: Dict[str, float]) -> None:
        self.totals_label.configure(
            text=(
                f"{totals['kcal']:.0f} kcal "
                f"P{totals['proteines']:.1f} "
                f"G{totals['glucides']:.1f} "
                f"L{totals['lipides']:.1f}"
            )
        )
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        for item in items:
            row = ctk.CTkFrame(self.items_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            lbl = ctk.CTkLabel(row, text=item["label"], anchor="w")
            lbl.pack(side="left", fill="x", expand=True)
            btn = ctk.CTkButton(
                row,
                text="x",
                width=24,
                command=lambda iid=item["id"]: self.on_delete_item(iid),
            )
            btn.pack(side="right")
