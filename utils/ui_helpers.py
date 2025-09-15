"""UI helpers for window behavior and focus management."""

from __future__ import annotations

from typing import Any


def bring_to_front(win: Any, make_modal: bool = False) -> None:
    """Raise a Toplevel window to the front and focus it.

    - Temporarily sets '-topmost' to True then back to False to ensure front.
    - Optionally applies modal behavior (transient + grab_set).
    """
    try:
        # Make it a child of the master for stacking (if available)
        if hasattr(win, "master") and win.master is not None:
            try:
                win.transient(win.master)
            except Exception:
                pass
    except Exception:
        pass
    try:
        win.lift()
    except Exception:
        pass
    try:
        win.attributes("-topmost", True)
        # reset after a short delay to avoid staying always-on-top
        try:
            win.after(200, lambda: _unset_topmost_safe(win))
        except Exception:
            _unset_topmost_safe(win)
    except Exception:
        pass
    try:
        win.focus_force()
    except Exception:
        pass

    if make_modal:
        try:
            win.grab_set()
        except Exception:
            pass


def _unset_topmost_safe(win: Any) -> None:
    try:
        win.attributes("-topmost", False)
    except Exception:
        pass
