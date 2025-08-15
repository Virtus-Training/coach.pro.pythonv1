# ui/theme/fonts.py
from customtkinter import CTkFont

def get_title_font():
    return CTkFont(family="Segoe UI", size=22, weight="bold")

def get_section_font():
    return CTkFont(family="Segoe UI", size=18, weight="bold")

def get_text_font():
    return CTkFont(family="Segoe UI", size=14)

def get_small_font():
    return CTkFont(family="Segoe UI", size=12)

def get_mono_font():
    return CTkFont(family="Consolas", size=13)


def get_button_font():
    """Retourne la police standard pour les boutons."""
    return ("Roboto", 14, "bold")
