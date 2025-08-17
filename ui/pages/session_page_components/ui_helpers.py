import customtkinter as ctk
from PIL import Image


def choose_equipment_icon(equip_list: list[str]) -> str | None:
    """Selects a representative equipment icon from a list of equipment."""
    if not equip_list:
        return None
    # Prioritize dumbbell icon for common strength equipment
    e = (equip_list[0] or "").lower()
    keywords = [
        "halt",
        "kettlebell",
        "barre",
        "poids",
        "trx",
        "anneaux",
        "machine",
        "élastique",
        "elastique",
    ]
    if any(k in e for k in keywords):
        return "assets/icons/dumbbell.png"
    return None


def create_chip(parent, text):
    """Creates a small, rounded rectangular frame with text, like a chip or tag."""
    f = ctk.CTkFrame(parent, fg_color="#2b2f35", corner_radius=999)
    ctk.CTkLabel(f, text=text, padx=8, pady=2, font=("Segoe UI", 11)).pack()
    return f


def create_pill(parent, text, fg_color="#0a6b84"):
    """Creates a pill-shaped, colored frame with text."""
    f = ctk.CTkFrame(parent, fg_color=fg_color, corner_radius=999)
    ctk.CTkLabel(
        f, text=text, padx=10, pady=2, font=("Segoe UI", 11, "bold"), text_color="#fff"
    ).pack()
    return f


def create_badge(parent, text):
    """Creates a simple badge with a dark background."""
    f = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=8)
    ctk.CTkLabel(f, text=text, padx=8, pady=2).pack()
    return f


def create_icon_label(parent, icon_path, text):
    """Creates a row with an icon and a text label."""
    row = ctk.CTkFrame(parent, fg_color="transparent")
    try:
        img = ctk.CTkImage(light_image=Image.open(icon_path), size=(18, 18))
        icon_label = ctk.CTkLabel(row, image=img, text="")
        icon_label.pack(side="left", padx=(0, 6))
        # Keep a reference to the image to prevent garbage collection
        icon_label.image = img
    except Exception as e:
        print(f"Failed to load icon: {e}")
        # Add a placeholder or empty space if icon fails
        ctk.CTkFrame(row, width=18, fg_color="transparent").pack(
            side="left", padx=(0, 6)
        )

    ctk.CTkLabel(row, text=text).pack(side="left")
    return row
