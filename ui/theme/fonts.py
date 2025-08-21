# ui/theme/fonts.py

"""Font tokens used throughout the UI.

The values follow the SRS V1 specification (section 4.1).  A few helper
functions are kept for compatibility with existing code that still relies on
the previous API.
"""

# --- Famille de police ---
FONT_FAMILY = "Roboto"

# --- Tailles & Poids ---
H1_BOLD = (FONT_FAMILY, 32, "bold")
H2_BOLD = (FONT_FAMILY, 24, "bold")
H3_NORMAL = (FONT_FAMILY, 18, "normal")
BODY_NORMAL = (FONT_FAMILY, 16, "normal")
LABEL_NORMAL = (FONT_FAMILY, 14, "normal")
CARD_TITLE = (FONT_FAMILY, 16, "bold")


# --- Legacy helper functions -----------------------------------------------
# These functions mirror the previous API so that untouched modules continue to
# operate while the codebase migrates to the new constants.


def get_title_font():
    """Return font for page titles (H1)."""

    return H1_BOLD


def get_section_font():
    """Return font for section titles (H2)."""

    return H2_BOLD


def get_text_font():
    """Return default body text font."""

    return BODY_NORMAL


def get_small_font():
    """Return small label font."""

    return LABEL_NORMAL


def get_button_font():
    """Return font used for buttons."""

    return H3_NORMAL


__all__ = [
    "FONT_FAMILY",
    "H1_BOLD",
    "H2_BOLD",
    "H3_NORMAL",
    "BODY_NORMAL",
    "LABEL_NORMAL",
    "CARD_TITLE",
    "get_title_font",
    "get_section_font",
    "get_text_font",
    "get_small_font",
    "get_button_font",
]
