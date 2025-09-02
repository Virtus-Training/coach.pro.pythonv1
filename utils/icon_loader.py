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


def load_square_image(path: str, size: Tuple[int, int] | int) -> ctk.CTkImage:
    """Load any image and render it into a square without distortion.

    Pads the shorter side with transparency so the image becomes square,
    then returns a CTkImage scaled to the requested square ``size``.

    Parameters
    ----------
    path: str
        Filesystem path to the image (e.g., ``assets/Logo.png``).
    size: tuple[int, int] | int
        Desired square size. If a tuple is provided, the max side is used
        to produce a square size.
    """

    if isinstance(size, int):
        target_size = (size, size)
    else:
        # Ensure square target size by using the max of provided tuple
        s = max(size)
        target_size = (s, s)

    key = (path, target_size)
    if key not in _ICON_CACHE:
        img = Image.open(path).convert("RGBA")
        w, h = img.size
        side = max(w, h)
        # Create transparent square canvas and paste centered
        square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        square.paste(img, ((side - w) // 2, (side - h) // 2))
        _ICON_CACHE[key] = ctk.CTkImage(square, size=target_size)
    return _ICON_CACHE[key]
