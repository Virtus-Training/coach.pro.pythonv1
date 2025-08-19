"""Reusable layout helpers."""

import customtkinter as ctk


def two_columns(parent, left_width: int = 360):
    """Create a two-column grid within ``parent``.

    The left column has a fixed ``left_width`` while the right column expands to
    occupy remaining space. Both columns are returned as ``CTkScrollableFrame``
    instances so their content can scroll independently.
    """
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=0, minsize=left_width)
    parent.grid_columnconfigure(1, weight=1)

    left = ctk.CTkScrollableFrame(parent, width=left_width, fg_color="#222")
    right = ctk.CTkScrollableFrame(parent, fg_color="#171717")
    return left, right


__all__ = ["two_columns"]
