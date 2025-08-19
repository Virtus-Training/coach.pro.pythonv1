import customtkinter as ctk
from PIL import Image

from .ui_helpers import choose_equipment_icon, create_chip, create_pill


class BlockCard(ctk.CTkFrame):
    """
    A card widget that displays the details of a single session block (e.g., an AMRAP or EMOM).
    """

    def __init__(self, parent, block, meta_map):
        super().__init__(parent, fg_color="transparent")

        # Palette douce par type
        type_colors = {
            "EMOM": ("#0b3a44", "#0a6b84"),  # fond / accent
            "AMRAP": ("#2b2a1f", "#b78b0a"),
            "SETSxREPS": ("#29222b", "#8b46b9"),
            "For Time": ("#222a29", "#138f6b"),
            "TABATA": ("#2b2121", "#b05555"),
        }
        bg, accent = type_colors.get(block.type.upper(), ("#232323", "#0a6b84"))

        # Carte + barre latérale d’accent
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        accent_bar = ctk.CTkFrame(self, fg_color=accent, width=4, corner_radius=6)
        accent_bar.grid(row=0, column=0, sticky="ns", pady=0, padx=(0, 6))

        card = ctk.CTkFrame(self, fg_color=bg, corner_radius=12)
        card.grid(row=0, column=1, sticky="nsew")

        # --- En-tête du bloc
        top = ctk.CTkFrame(card, fg_color="#1b1b1b")
        top.pack(fill="x", padx=12, pady=(12, 8))
        title = block.title or (
            f"{block.type} – {block.duration_sec // 60}’"
            if block.duration_sec
            else block.type
        )
        ctk.CTkLabel(top, text=title, font=("Segoe UI", 14, "bold")).pack(side="left")

        badges = ctk.CTkFrame(top, fg_color="transparent")
        badges.pack(side="right")
        create_chip(badges, block.type).pack(side="left", padx=4)
        if getattr(block, "rounds", None):
            create_chip(badges, f"{block.rounds} rounds").pack(side="left", padx=4)
        if getattr(block, "work_sec", None) and getattr(block, "rest_sec", None):
            create_chip(badges, f"{block.work_sec}/{block.rest_sec}").pack(
                side="left", padx=4
            )

        # --- Liste d'exercices
        body = ctk.CTkFrame(card, fg_color="#121416", corner_radius=10)
        body.pack(fill="x", padx=12, pady=(0, 10))

        for it in block.items:
            meta = meta_map.get(
                it.exercise_id, {"name": it.exercise_id, "equipment": []}
            )
            name = meta["name"]
            equip_list = meta.get("equipment", [])
            equip_text = " · ".join(equip_list) if equip_list else "Poids du corps"

            presc = []
            reps = it.prescription.get("reps")
            rest = it.prescription.get("rest_sec") or it.prescription.get("rest")
            if reps:
                presc.append(f"{reps} reps")
            if rest:
                presc.append(f"repos {rest}")
            presc_txt = " • ".join(presc) if presc else ""

            rowf = ctk.CTkFrame(body, fg_color="transparent")
            rowf.pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(rowf, text="•", font=("Segoe UI", 14)).pack(
                side="left", padx=(0, 8)
            )
            icon_path = choose_equipment_icon(equip_list)
            if icon_path:
                try:
                    img = ctk.CTkImage(light_image=Image.open(icon_path), size=(16, 16))
                    icon_label = ctk.CTkLabel(rowf, image=img, text="")
                    icon_label.pack(side="left", padx=(0, 6))
                    icon_label.image = img
                except Exception:
                    pass

            left = ctk.CTkFrame(rowf, fg_color="transparent")
            left.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(
                left,
                text=name,
                font=("Segoe UI", 13, "bold"),
                anchor="w",
                wraplength=380,
            ).pack(anchor="w")
            ctk.CTkLabel(left, text=equip_text, font=("Segoe UI", 11)).pack(anchor="w")

            if presc_txt:
                create_pill(rowf, presc_txt, fg_color=accent).pack(side="right", padx=6)
                ctk.CTkFrame(
                    rowf, fg_color=accent, width=6, height=20, corner_radius=3
                ).pack(side="right", padx=(0, 6))
                rowf.pack_propagate(False)

        # --- Actions
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill="x", padx=12, pady=(2, 12))
        ctk.CTkButton(actions, text="Regénérer ce bloc").pack(side="left", padx=4)
        ctk.CTkButton(actions, text="Remplacer un exercice").pack(side="left", padx=4)
