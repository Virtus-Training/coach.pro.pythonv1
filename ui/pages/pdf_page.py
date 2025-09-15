import json
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from controllers.pdf_template_controller import PdfTemplateController
from ui.components.design_system import (
    Card,
    CardTitle,
    HeroBanner,
    PrimaryButton,
    SecondaryButton,
)


class PdfPage(ctk.CTkFrame):
    def __init__(self, parent, controller: PdfTemplateController | None = None):
        super().__init__(parent)
        colors = ctk.ThemeManager.theme["color"]
        self.configure(fg_color=colors["surface_dark"])
        self.controller = controller or PdfTemplateController()

        hero = HeroBanner(
            self,
            title="PDF",
            subtitle="Exports et templates",
            icon_path="assets/icons/pdf.png",
        )
        hero.pack(fill="x", padx=12, pady=(6, 8))

        # Manager de templates
        root = Card(self)
        root.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        root.grid_columnconfigure(0, weight=0)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(1, weight=1)

        CardTitle(root, text="Templates de séance").grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12, 8)
        )

        left = ctk.CTkFrame(root, fg_color="transparent")
        left.grid(row=1, column=0, sticky="nsw", padx=(12, 8), pady=8)
        left.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(left, text="Templates").grid(row=0, column=0, sticky="w")
        # CTkListbox may not exist in older versions; fallback to Tk Listbox
        try:
            self.listbox = ctk.CTkListbox(left, width=240, height=360)
        except Exception:
            self.listbox = tk.Listbox(left, width=36, height=20)
        self.listbox.grid(row=1, column=0, sticky="nsw")
        btns = ctk.CTkFrame(left, fg_color="transparent")
        btns.grid(row=2, column=0, sticky="ew", pady=(6, 0))
        SecondaryButton(btns, text="Nouveau", command=self._on_new).pack(
            side="left", padx=4
        )
        SecondaryButton(btns, text="Définir par défaut", command=self._on_set_default).pack(
            side="left", padx=4
        )
        SecondaryButton(btns, text="Supprimer", command=self._on_delete).pack(
            side="left", padx=4
        )

        right = ctk.CTkFrame(root, fg_color="transparent")
        right.grid(row=1, column=1, sticky="nsew", padx=(8, 12), pady=8)
        right.grid_rowconfigure(1, weight=1)
        CardTitle(right, text="Style JSON").grid(row=0, column=0, sticky="w")
        self.editor = tk.Text(right, height=22)
        self.editor.grid(row=1, column=0, sticky="nsew")

        footer = ctk.CTkFrame(right, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="e", pady=(8, 0))
        SecondaryButton(footer, text="Aperçu PDF", command=self._on_preview).pack(
            side="right", padx=6
        )
        PrimaryButton(footer, text="Enregistrer", command=self._on_save).pack(
            side="right", padx=6
        )

        self._templates: list[dict] = []
        self._selected_id: int | None = None
        self._refresh_list()
        self._load_selected_style()

    # --- Data ops
    def _refresh_list(self):
        # Reset items
        if hasattr(self.listbox, "delete"):
            try:
                self.listbox.delete(0, "end")
            except Exception:
                self.listbox.delete("1.0", "end")
        self._templates = self.controller.list_session_templates()
        if hasattr(self.listbox, "insert"):
            for t in self._templates:
                label = f"{'* ' if t['is_default'] else ''}{t['name']}"
                try:
                    self.listbox.insert("end", label)
                except Exception:
                    self.listbox.insert("end", label + "\n")
        try:
            self.listbox.bind("<<ListboxSelect>>", lambda e: self._on_select())
        except Exception:
            pass

    def _load_selected_style(self):
        # select default if none
        idx = 0
        for i, t in enumerate(self._templates):
            if t.get("is_default"):
                idx = i
                break
        try:
            self.listbox.select_set(idx)
        except Exception:
            pass
        self._on_select()

    def _on_select(self):
        idx = 0
        try:
            sel = self.listbox.curselection()
            idx = sel[0] if isinstance(sel, (list, tuple)) else int(sel)
        except Exception:
            idx = 0
        if not self._templates:
            self._selected_id = None
            self.editor.delete("1.0", "end")
            style = self.controller.get_session_style(None)
            self.editor.insert("1.0", json.dumps(style, indent=2, ensure_ascii=False))
            return
        idx = max(0, min(idx, len(self._templates) - 1))
        t = self._templates[idx]
        self._selected_id = int(t["id"]) if t.get("id") is not None else None
        style = self.controller.get_session_style(self._selected_id)
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", json.dumps(style, indent=2, ensure_ascii=False))

    # --- Actions
    def _on_new(self):
        name = f"Template {len(self._templates)+1}"
        try:
            style = self.controller.get_session_style(None)
            _ = self.controller.save_session_template(
                name, json.dumps(style, ensure_ascii=False), None, False
            )
            self._refresh_list()
            try:
                self.listbox.select_set(len(self._templates) - 1)
            except Exception:
                pass
            self._on_select()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer: {e}")

    def _on_set_default(self):
        if self._selected_id is None:
            return
        try:
            style_txt = self.editor.get("1.0", "end").strip()
            _ = json.loads(style_txt)  # validate
            self.controller.save_session_template("", style_txt, self._selected_id, True)
            self._refresh_list()
        except Exception as e:
            messagebox.showerror("Erreur", f"Echec: {e}")

    def _on_delete(self):
        if self._selected_id is None:
            return
        try:
            self.controller.delete_template(self._selected_id)
            self._refresh_list()
            self._load_selected_style()
        except Exception as e:
            messagebox.showerror("Erreur", f"Echec suppression: {e}")

    def _on_save(self):
        style_txt = self.editor.get("1.0", "end").strip()
        try:
            json.loads(style_txt)
            name = None
            if self._selected_id is None:
                name = "Template"
            tpl_id = self.controller.save_session_template(
                name or "", style_txt, self._selected_id, False
            )
            self._selected_id = tpl_id
            self._refresh_list()
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
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")]
        )
        if not path:
            return
        sample = {
            "meta": {"title": "Séance Exemple", "duration": "45 min"},
            "blocks": [
                {
                    "title": "SETSxREPS – 10 min",
                    "format": "SETSxREPS",
                    "duration": "10 min",
                    "exercises": [
                        {"nom": "Squat", "reps": "3x10", "repos_s": 60},
                        {"nom": "Pompes", "reps": "3x12", "repos_s": 45},
                    ],
                },
                {
                    "title": "AMRAP – 20 min",
                    "format": "AMRAP",
                    "duration": "20 min",
                    "exercises": [
                        {"nom": "Row", "reps": "10 reps"},
                        {"nom": "Burpees", "reps": "8 reps"},
                    ],
                },
                {
                    "title": "EMOM – 10 min",
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
