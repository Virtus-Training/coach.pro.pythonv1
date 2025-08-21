# ui/theme/colors.py

"""Design tokens for application colors.

These constants mirror the values defined in the SRS V1 (section 4.1).
Legacy color names are kept as aliases for backwards compatibility.
"""

# --- Palette Principale ---
PRIMARY = "#00A3FF"  # Bleu vif pour les actions principales
SUCCESS = "#2ECC71"  # Vert pour les confirmations
DANGER = "#E74C3C"  # Rouge pour les erreurs ou actions destructrices
WARNING = "#F1C40F"  # Jaune/Orange pour les avertissements

# --- Niveaux de Gris (Neutres) ---
NEUTRAL_900 = "#121212"  # Fond principal de l'application
NEUTRAL_800 = "#1E1E1E"  # Fond des cartes et éléments en surélévation
NEUTRAL_700 = "#333333"  # Bordures, séparateurs
NEUTRAL_100 = "#FFFFFF"  # Texte principal (fort contraste)
NEUTRAL_300 = "#B3B3B3"  # Texte secondaire (moins de contraste)


# --- Aliases for legacy names -------------------------------------------------
# These aliases allow existing code to continue functioning while the
# application gradually adopts the new design tokens.
DARK_BG = NEUTRAL_900
DARK_PANEL = NEUTRAL_800
DARK_SOFT = NEUTRAL_700
TEXT = NEUTRAL_100
TEXT_SECONDARY = NEUTRAL_300
TEXT_MUTED = NEUTRAL_300
TEXT_ON_PRIMARY = NEUTRAL_100
BORDER_COLOR = NEUTRAL_700
INFO = PRIMARY

__all__ = [
    "PRIMARY",
    "SUCCESS",
    "DANGER",
    "WARNING",
    "NEUTRAL_900",
    "NEUTRAL_800",
    "NEUTRAL_700",
    "NEUTRAL_100",
    "NEUTRAL_300",
]
