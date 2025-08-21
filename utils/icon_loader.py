import os
from typing import Tuple

import customtkinter as ctk
from PIL import Image

# Simple in-memory cache for loaded icons
_ICON_CACHE: dict[Tuple[str, Tuple[int, int]], ctk.CTkImage] = {}


def load_icon(filename: str, size: Tuple[int, int] | int) -> ctk.CTkImage:
    """Load an icon from assets/icons with basic caching.

    Parameters
    ----------
    filename: str
        Name of the icon file located in ``assets/icons``.
    size: tuple[int, int] | int
        Desired size of the icon. If an int is provided, a square icon is
        created.
    """

    if isinstance(size, int):
        size = (size, size)

    key = (filename, size)
    if key not in _ICON_CACHE:
        path = os.path.join("assets", "icons", filename)
        image = Image.open(path)
        _ICON_CACHE[key] = ctk.CTkImage(image, size=size)
    return _ICON_CACHE[key]
