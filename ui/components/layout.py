"""Reusable layout helpers."""

import customtkinter as ctk


def two_columns(
    parent,
    left_width: int = 360,
    *,
    right_width: int | None = None,
    fixed_side: str = "left",
):
    """Create a two-column layout.

    - fixed_side="left" (default): left column is fixed to ``left_width`` and right expands.
    - fixed_side="right": right column is fixed to ``right_width`` if provided, otherwise ``left_width``; left expands.
    """
    parent.grid_rowconfigure(0, weight=1)

    if fixed_side == "right":
        rw = right_width if right_width is not None else left_width
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0, minsize=rw)

        left = ctk.CTkFrame(parent, fg_color="transparent")
        right = ctk.CTkFrame(parent, width=rw, fg_color="transparent")
    else:
        parent.grid_columnconfigure(0, weight=0, minsize=left_width)
        parent.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(parent, width=left_width, fg_color="transparent")
        right = ctk.CTkFrame(parent, fg_color="transparent")

    return left, right


__all__ = ["two_columns"]
