### Patch Notes

- `ui/pages/session_page.py` now uses `two_columns` layout and the new
  `render_preview` API.
- Preview rendering lives in `ui/pages/session_preview_panel.py` and builds
  `WorkoutBlock` components.
- Exercise ID→meta mapping handled in
  `controllers/session_controller.generate_session_preview`.
- New helper `two_columns` in `ui/components/layout.py` creates the fixed-width
  form column and scrollable preview column.
