"""Reusable layout helpers."""

import customtkinter as ctk


def two_columns(parent, left_width: int = 360):
    """Creates a two-column layout with fixed-width left column and expandable right column."""
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=0, minsize=left_width)
    parent.grid_columnconfigure(1, weight=1)

    left = ctk.CTkFrame(parent, width=left_width, fg_color="transparent")
    right = ctk.CTkFrame(parent, fg_color="transparent")
    return left, right


__all__ = ["two_columns"]
