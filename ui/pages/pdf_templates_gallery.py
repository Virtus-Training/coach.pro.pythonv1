import json
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image

from controllers.pdf_template_controller import PdfTemplateController
from ui.components.design_system import HeroBanner, Card, CardTitle, PrimaryButton, SecondaryButton


class _TemplateTile(ctk.CTkFrame):
    def __init__(self, master, name: str, is_default: bool, on_click, icon_path: str):
        colors = ctk.ThemeManager.theme["color"]
        super().__init__(master, fg_color=colors.get("surface_light", "#111827"), corner_radius=8)
        self._on_click = on_click
        self._selected = False
        self.configure(cursor="hand2")
        self.grid_propagate(False)
        self._img = None
        try:
            if os.path.exists(icon_path):
                self._img = ctk.CTkImage(Image.open(icon_path), size=(96, 64))
        except Exception:
            self._img = None
        ctk.CTkLabel(self, text="", image=self._img).pack(pady=(8, 4))
        label = f"* {name}" if is_default else name
        ctk.CTkLabel(self, text=label).pack(pady=(0, 8))
        self.bind("<Button-1>", lambda e: self._on_click())
        for ch in self.winfo_children():
            ch.bind("<Button-1>", lambda e: self._on_click())

    def set_selected(self, selected: bool):
        self._selected = selected
        try:
            border = ctk.ThemeManager.theme.get("color", {}).get("primary", "#22D3EE")
            self.configure(border_width=(2 if selected else 0), border_color=border)
        except Exception:
            pass


class _CreateTemplateModal(ctk.CTkToplevel):
    def __init__(self, master, on_create, t: str):
        super().__init__(master)
        self.title("Nouveau template")
        self.geometry("360x180")
        self.resizable(False, False)
        self._on_create = on_create
        self._t = t
        ctk.CTkLabel(self, text="Nom du template").pack(anchor="w", padx=12, pady=(12, 4))
        self._name = ctk.CTkEntry(self)
        self._name.insert(0, "Nouveau template")
        self._name.pack(fill="x", padx=12)
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=12)
        SecondaryButton(btns, text="Annuler", command=self.destroy).pack(side="right", padx=6)
        PrimaryButton(btns, text="Créer", command=self._create).pack(side="right", padx=6)
        try:
            self._name.focus_set()
            self.bind("<Return>", lambda e: self._create())
        except Exception:
            pass
        # ensure on top and focused
        try:
            from utils.ui_helpers import bring_to_front  # local import to avoid cycles
            bring_to_front(self, make_modal=True)
        except Exception:
            pass

    def _create(self):
        name = self._name.get().strip() or "Template"
        self._on_create(self._t, name)
        self.destroy()


class PdfTemplatesPage(ctk.CTkFrame):
    def __init__(self, parent, controller: PdfTemplateController | None = None):
        super().__init__(parent)
        colors = ctk.ThemeManager.theme["color"]
        self.configure(fg_color=colors["surface_dark"])
        self.controller = controller or PdfTemplateController()

        hero = HeroBanner(
            self,
            title="Templates PDF",
            subtitle="Sélectionnez, créez et éditez vos templates",
            icon_path="assets/icons/pdf.png",
        )
        hero.pack(fill="x", padx=20, pady=20)

        root = Card(self)
        root.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        # Rendre tout le contenu scrollable pour éviter d'être rogné
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        content = ctk.CTkScrollableFrame(root, fg_color="transparent")
        content.grid(row=0, column=0, sticky="nsew")

        tabs = ctk.CTkTabview(content)
        tabs.pack(fill="x", expand=False, padx=12, pady=12)
        self._families = [
            ("Séances", "session", "assets/icons/pdf.png"),
            ("Fiches nutrition", "nutrition", "assets/icons/pdf.png"),
            ("Plans alimentaires", "meal_plan", "assets/icons/pdf.png"),
            ("Programmes", "program", "assets/icons/pdf.png"),
        ]
        self._grids: dict[str, ctk.CTkScrollableFrame] = {}
        self._tiles: dict[str, list[tuple[int | None, _TemplateTile]]] = {}
        self._selected: dict[str, int | None] = {t: None for _, t, _ in self._families}

        for label, t, _ in self._families:
            tab = tabs.add(label)
            frame = ctk.CTkFrame(tab, fg_color="transparent")
            frame.pack(fill="both", expand=True)
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            bar = ctk.CTkFrame(frame, fg_color="transparent")
            bar.grid(row=0, column=0, sticky="ew")
            SecondaryButton(bar, text="Nouveau", command=lambda typ=t: self._open_create_modal(typ)).pack(side="left")
            SecondaryButton(bar, text="Définir par défaut", command=lambda typ=t: self._on_set_default(typ)).pack(side="left", padx=6)
            SecondaryButton(bar, text="Supprimer", command=lambda typ=t: self._on_delete(typ)).pack(side="left", padx=6)
            SecondaryButton(bar, text="Modèles types", command=lambda typ=t: self._open_presets_modal(typ)).pack(side="left", padx=6)

            grid_wrap = ctk.CTkScrollableFrame(frame, fg_color="transparent")
            grid_wrap.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
            self._grids[t] = grid_wrap
            self._tiles[t] = []

        # Editor area
        editor = ctk.CTkFrame(content, fg_color="transparent")
        editor.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        editor.grid_columnconfigure(0, weight=1)
        topbar = ctk.CTkFrame(editor, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew")
        CardTitle(topbar, text="Éditeur de style").pack(side="left")
        try:
            self.mode_switch = ctk.CTkSegmentedButton(topbar, values=["Visuel", "JSON"], command=lambda v: self._on_mode_change(v))
            self.mode_switch.set("Visuel")
            self.mode_switch.pack(side="right")
        except Exception:
            self.mode_switch = None

        # Visual editor
        self.visual_wrap = ctk.CTkFrame(editor, fg_color="transparent")
        self.visual_wrap.grid(row=1, column=0, sticky="nsew")
        self.visual_wrap.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.visual_wrap, text="Largeur logo").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.ve_logo = ctk.CTkEntry(self.visual_wrap, width=80)
        self.ve_logo.grid(row=0, column=1, sticky="w")

        self._color_keys = [
            ("table_header_bg", "Entête tableau"),
            ("table_row_odd_bg", "Ligne impaire"),
            ("table_row_even_bg", "Ligne paire"),
            ("table_grid", "Grille"),
            ("table_text", "Texte"),
        ]
        self._color_vars: dict[str, ctk.CTkButton] = {}
        start_row = 1
        for i, (key, label) in enumerate(self._color_keys):
            r = start_row + i
            ctk.CTkLabel(self.visual_wrap, text=label).grid(row=r, column=0, sticky="w", pady=2)
            btn = ctk.CTkButton(self.visual_wrap, text="#000000", width=80, command=lambda k=key: self._pick_color(k))
            btn.grid(row=r, column=1, sticky="w")
            self._color_vars[key] = btn

        ctk.CTkLabel(self.visual_wrap, text="Colonnes par défaut (ex: 250,60,120,60)").grid(
            row=start_row + len(self._color_keys), column=0, columnspan=2, sticky="w", pady=(8, 2)
        )
        self.ve_cols = ctk.CTkEntry(self.visual_wrap)
        self.ve_cols.grid(row=start_row + len(self._color_keys) + 1, column=0, columnspan=2, sticky="ew")

        # JSON editor
        self.json_wrap = ctk.CTkFrame(editor, fg_color="transparent")
        self.json_wrap.grid(row=1, column=0, sticky="nsew")
        self.json_wrap.grid_remove()
        self.editor = tk.Text(self.json_wrap, height=14)
        self.editor.pack(fill="both", expand=True)

        footer = ctk.CTkFrame(editor, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="e", pady=(8, 0))
        SecondaryButton(footer, text="Aperçu PDF", command=self._on_preview).pack(side="right", padx=6)
        PrimaryButton(footer, text="Enregistrer", command=self._on_save).pack(side="right", padx=6)

        self._selected_family = "session"
        self._refresh_all()

    # --- Data ops / UI helpers --------------------------------------------
    def _refresh_all(self):
        for _, t, icon in self._families:
            self._refresh_grid(t, icon)
        self._load_selected_style()

    def _on_mode_change(self, value: str):
        if str(value) == "JSON":
            self.visual_wrap.grid_remove()
            self.json_wrap.grid()
        else:
            self.json_wrap.grid_remove()
            self.visual_wrap.grid()

    def _set_json(self, style: dict):
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", json.dumps(style, indent=2, ensure_ascii=False))

    def _load_visual(self, style: dict):
        try:
            self.ve_logo.delete(0, "end")
            self.ve_logo.insert(0, str(style.get("logo_width", 70)))
        except Exception:
            pass
        colors = style.get("colors", {}) or {}
        for key, _ in self._color_keys:
            btn = self._color_vars.get(key)
            if not btn:
                continue
            val = colors.get(key, "#000000")
            try:
                btn.configure(text=val, fg_color=val)
            except Exception:
                btn.configure(text=val)
        cols = style.get("column_widths", {}) or {}
        default_cols = cols.get("DEFAULT", [])
        try:
            self.ve_cols.delete(0, "end")
            if default_cols:
                self.ve_cols.insert(0, ",".join(str(x) for x in default_cols))
        except Exception:
            pass

    def _pick_color(self, key: str):
        _rgb, hexv = colorchooser.askcolor()
        if not hexv:
            return
        btn = self._color_vars.get(key)
        if btn is None:
            return
        try:
            btn.configure(text=hexv, fg_color=hexv)
        except Exception:
            btn.configure(text=hexv)

    def _compose_style_from_visual(self) -> dict:
        try:
            base = json.loads(self.editor.get("1.0", "end").strip() or "{}")
        except Exception:
            base = {}
        base.setdefault("logo_width", 70)
        try:
            base["logo_width"] = int(self.ve_logo.get() or 70)
        except Exception:
            pass
        colors = base.get("colors", {}) or {}
        for key, _ in self._color_keys:
            btn = self._color_vars.get(key)
            if btn is None:
                continue
            try:
                colors[key] = str(btn.cget("text"))
            except Exception:
                pass
        base["colors"] = colors
        cols = base.get("column_widths", {}) or {}
        try:
            vals = [int(x.strip()) for x in (self.ve_cols.get() or "").split(",") if x.strip()]
            if vals:
                cols["DEFAULT"] = vals
        except Exception:
            pass
        base["column_widths"] = cols
        return base

    def _refresh_grid(self, t: str, icon_path: str):
        for w in self._grids[t].winfo_children():
            w.destroy()
        try:
            data = self.controller.list_templates(t)
        except Exception:
            data = []
        self._tiles[t] = []
        cols = 4
        for i, item in enumerate(data):
            r, c = divmod(i, cols)
            tile = _TemplateTile(
                self._grids[t],
                name=item.get("name", ""),
                is_default=bool(item.get("is_default")),
                on_click=lambda _id=item.get("id"), _t=t: self._select_tile(_t, _id),
                icon_path=icon_path,
            )
            tile.grid(row=r, column=c, padx=8, pady=8)
            tile.configure(width=160, height=120)
            self._tiles[t].append((item.get("id"), tile))

    def _select_tile(self, t: str, template_id: int | None):
        for tid, tile in self._tiles.get(t, []):
            tile.set_selected(bool(tid == template_id))
        self._selected_family = t
        self._selected[t] = template_id
        try:
            style = self.controller.get_style(t, template_id)
        except Exception:
            style = {}
        self._set_json(style)
        self._load_visual(style)

    def _load_selected_style(self):
        fam = self._selected_family
        selected_id = self._selected.get(fam)
        try:
            style = self.controller.get_style(fam, selected_id)
        except Exception:
            style = {}
        self._set_json(style)
        self._load_visual(style)

    # --- Actions ------------------------------------------------------------
    def _open_create_modal(self, t: str):
        def handle_create(typ: str, name: str):
            try:
                style = self.controller.get_style(typ, None)
                self.controller.save_template(typ, name, json.dumps(style, ensure_ascii=False), None, False)
                icon = next((ic for lbl, typ2, ic in self._families if typ2 == typ), "assets/icons/pdf.png")
                self._refresh_grid(typ, icon)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de créer: {e}")

        _CreateTemplateModal(self, handle_create, t)

    def _open_presets_modal(self, t: str):
        win = ctk.CTkToplevel(self)
        win.title("Modèles types")
        ctk.CTkLabel(win, text="Choisir un modèle à ajouter").pack(padx=12, pady=8)
        row = ctk.CTkFrame(win, fg_color="transparent")
        row.pack(padx=12, pady=8)

        def add(name: str):
            try:
                style = self._make_preset_style(t, name)
                self.controller.save_template(t, name, json.dumps(style, ensure_ascii=False), None, False)
                icon = next((ic for lbl, typ2, ic in self._families if typ2 == t), "assets/icons/pdf.png")
                self._refresh_grid(t, icon)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Échec: {e}")

        for name in ["Basique sombre", "Basique clair", "Compact"]:
            PrimaryButton(row, text=name, command=lambda n=name: add(n)).pack(side="left", padx=6)

    def _make_preset_style(self, t: str, name: str) -> dict:
        if t == "session":
            base = {
                "logo_width": 70,
                "colors": {
                    "table_header_bg": "#374151",
                    "table_row_odd_bg": "#1F2937",
                    "table_row_even_bg": "#111827",
                    "table_grid": "#374151",
                    "table_text": "#E5E7EB",
                },
                "column_widths": {"DEFAULT": [250, 60, 120, 60], "EMOM": [250, 180]},
            }
            if name == "Basique clair":
                base["colors"].update({
                    "table_header_bg": "#E5E7EB",
                    "table_row_odd_bg": "#FFFFFF",
                    "table_row_even_bg": "#F3F4F6",
                    "table_grid": "#D1D5DB",
                    "table_text": "#111827",
                })
            if name == "Compact":
                base["logo_width"] = 50
                base["column_widths"]["DEFAULT"] = [220, 60, 100, 50]
            return base
        else:
            if name == "Basique clair":
                return {
                    "logo_width": 70,
                    "colors": {
                        "header_bg": "#E5E7EB",
                        "row_odd_bg": "#FFFFFF",
                        "row_even_bg": "#F3F4F6",
                        "grid": "#D1D5DB",
                        "text": "#111827",
                    },
                }
            if name == "Compact":
                return {
                    "logo_width": 50,
                    "colors": {
                        "header_bg": "#374151",
                        "row_odd_bg": "#1F2937",
                        "row_even_bg": "#111827",
                        "grid": "#374151",
                        "text": "#E5E7EB",
                    },
                }
            return {
                "logo_width": 70,
                "colors": {
                    "header_bg": "#374151",
                    "row_odd_bg": "#1F2937",
                    "row_even_bg": "#111827",
                    "grid": "#374151",
                    "text": "#E5E7EB",
                },
            }

    def _on_set_default(self, t: str):
        tpl_id = self._selected.get(t)
        if tpl_id is None:
            return
        try:
            style_txt = self.editor.get("1.0", "end").strip()
            _ = json.loads(style_txt)
            self.controller.save_template(t, "", style_txt, tpl_id, True)
            icon = next((ic for lbl, typ2, ic in self._families if typ2 == t), "assets/icons/pdf.png")
            self._refresh_grid(t, icon)
        except Exception as e:
            messagebox.showerror("Erreur", f"Echec: {e}")

    def _on_delete(self, t: str):
        tpl_id = self._selected.get(t)
        if tpl_id is None:
            return
        try:
            self.controller.delete_template(int(tpl_id))
            icon = next((ic for lbl, typ2, ic in self._families if typ2 == t), "assets/icons/pdf.png")
            self._refresh_grid(t, icon)
            self._load_selected_style()
        except Exception as e:
            messagebox.showerror("Erreur", f"Echec suppression: {e}")

    def _on_save(self):
        mode = "JSON"
        try:
            mode = self.mode_switch.get()
        except Exception:
            pass
        if mode == "Visuel":
            style = self._compose_style_from_visual()
            self._set_json(style)
            style_txt = json.dumps(style, ensure_ascii=False)
        else:
            style_txt = self.editor.get("1.0", "end").strip()
        fam = self._selected_family
        try:
            json.loads(style_txt)
            tpl_id = self._selected.get(fam)
            if tpl_id is None:
                name = "Template"
                self.controller.save_template(fam, name, style_txt, None, False)
            else:
                self.controller.save_template(fam, "", style_txt, int(tpl_id), False)
            icon = next((ic for lbl, typ2, ic in self._families if typ2 == fam), "assets/icons/pdf.png")
            self._refresh_grid(fam, icon)
            messagebox.showinfo("OK", "Template sauvegardé.")
        except Exception as e:
            messagebox.showerror("Erreur", f"JSON invalide ou erreur de sauvegarde: {e}")

    def _on_preview(self):
        style_txt = self.editor.get("1.0", "end").strip()
        try:
            style = json.loads(style_txt)
        except Exception as e:
            messagebox.showerror("Erreur", f"JSON invalide: {e}")
            return
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not path:
            return
        sample = {
            "meta": {"title": "Séance Exemple", "duration": "45 min"},
            "blocks": [
                {
                    "title": "SETSxREPS - 10 min",
                    "format": "SETSxREPS",
                    "duration": "10 min",
                    "exercises": [
                        {"nom": "Squat", "reps": "3x10", "repos_s": 60},
                        {"nom": "Pompes", "reps": "3x12", "repos_s": 45},
                    ],
                },
                {
                    "title": "AMRAP - 20 min",
                    "format": "AMRAP",
                    "duration": "20 min",
                    "exercises": [
                        {"nom": "Row", "reps": "10 reps"},
                        {"nom": "Burpees", "reps": "8 reps"},
                    ],
                },
                {
                    "title": "EMOM - 10 min",
                    "format": "EMOM",
                    "duration": "10 min",
                    "exercises": [
                        {"nom": "Kettlebell swing", "reps": "12 reps"},
                    ],
                },
            ],
        }
        try:
            from services.pdf_generator import generate_session_pdf_with_style

            generate_session_pdf_with_style(sample, None, path, style)
            messagebox.showinfo("OK", "Aperçu PDF exporté.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Echec export: {e}")


__all__ = ["PdfTemplatesPage"]
