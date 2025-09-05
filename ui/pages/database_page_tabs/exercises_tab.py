from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from typing import List, Optional

import customtkinter as ctk

from models.exercices import Exercise
from repositories.exercices_repo import ExerciseRepository
from ui.components.design_system import (
    AccordionSection,
    Card,
    CardTitle,
    ChipCheckboxGroup,
    ChipRadioGroup,
    DangerButton,
    GhostButton,
    LabeledInput,
    PrimaryButton,
    SecondaryButton,
)

# Vocabulaire normalisÃ© pour Ã©viter la casse et les variations d'Ã©criture
MUSCLE_GROUPS = [
    "Poitrine",
    "Dos",
    "\u00c9paules",  # Ã‰paules
    "Jambes",
    "Fessiers",
    "Biceps",
    "Triceps",
    "Abdominaux",
    "Lombaires",
    "Mollets",
    "Avant-bras",
]

EQUIPMENT_OPTIONS = [
    "Poids du corps",
    "Halt\u00e8res",  # HaltÃ¨res
    "Barre",
    "Kettlebell",
    "\u00c9lastiques",  # Ã‰lastiques
    "Machine",
    "Poulie",
    "TRX",
    "Anneaux",
    "Banc",
]

TAG_OPTIONS = [
    "Unilat\u00e9ral",
    "Bilat\u00e9ral",
    "Explosif",
    "Tempo lent",
    "Isom\u00e9trie",
    "Mobilit\u00e9",
]

# Tags de cours collectifs (persistÃ©s dans le champ `tags`)
COURSE_TAGS = [
    "CAF",
    "Core & Glutes",
    "Cross-Training",
    "Crossfit",
    "Hyrox",
    "TRX",
]

MOVEMENT_PATTERNS = [
    "Push",
    "Pull",
    "Squat",
    "Hinge",
    "Carry",
    "Lunge",
    "Twist",
    "Gait",
    "Jump",
]

EFFORT_TYPES = [
    "Force",
    "Hypertrophie",
    "Endurance",
    "Cardio",
    "Technique",
    "Mobilit\u00e9",
]

# CatÃ©gories de mouvement (poly-articulaire, isolation, gainage)
MOVEMENT_CATEGORIES = [
    "Polyarticulaire",
    "Isolation",
    "Gainage",
]


class ExerciseForm(ctk.CTkToplevel):
    """Formulaire d'exercice pour ajout et modification."""

    def __init__(self, master, on_submit, exercise: Optional[Exercise] = None) -> None:
        super().__init__(
            master, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        )  # fallback if CTkToplevel not themed
        self.title("Exercice")
        self.geometry("760x720")
        self.minsize(640, 560)
        self.resizable(True, True)
        self._on_submit = on_submit

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=16)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0)
        frame.grid_rowconfigure(0, weight=1)

        # Scrollable content (left)
        content = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        content.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        # Sidebar summary (right)
        sidebar = ctk.CTkFrame(
            frame,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
            corner_radius=8,
        )
        sidebar.grid(row=0, column=1, sticky="ns")
        CardTitle(sidebar, text="Synth\u00e8se").pack(anchor="w", padx=12, pady=(12, 6))
        self.summary_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        self.summary_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # GÃ©nÃ©ral
        CardTitle(content, text="G\u00e9n\u00e9ral").pack(anchor="w", pady=(0, 6))
        self.in_nom = LabeledInput(content, label="Nom")
        self.in_nom.pack(fill="x", pady=(0, 8))

        self.grp_groupe = ChipRadioGroup(
            content,
            label="Groupe musculaire principal",
            options=MUSCLE_GROUPS,
            helper="Choix unique",
            selected_color="#34D399",
            on_change=lambda _v=None: (
                self._update_summary(),
                self._update_submit_state(),
            ),
        )
        self.grp_groupe.pack(fill="x", pady=(4, 8))

        # Ã‰quipements
        sec_equip = AccordionSection(
            content, title="\u00c9quipements", initially_open=False
        )
        sec_equip.pack(fill="x")
        self.grp_equip = ChipCheckboxGroup(
            sec_equip.body,
            label="",
            options=EQUIPMENT_OPTIONS,
            helper="Multi-s\u00e9lection",
            selected_color="#60A5FA",
            on_change=lambda _v=None: (
                self._update_summary(),
                self._update_submit_state(),
            ),
        )
        self.grp_equip.pack(fill="x", pady=(0, 8))

        # Cours collectifs
        sec_course = AccordionSection(
            content, title="Cours collectifs", initially_open=False
        )
        sec_course.pack(fill="x")
        self.grp_course = ChipCheckboxGroup(
            sec_course.body,
            label="",
            options=COURSE_TAGS,
            helper="Multi-s\u00e9lection",
            selected_color="#F59E0B",
            on_change=lambda _v=None: (
                self._update_summary(),
                self._update_submit_state(),
            ),
        )
        self.grp_course.pack(fill="x", pady=(0, 8))

        # Tags
        sec_tags = AccordionSection(content, title="Tags", initially_open=False)
        sec_tags.pack(fill="x")
        self.grp_tags = ChipCheckboxGroup(
            sec_tags.body,
            label="",
            options=TAG_OPTIONS,
            helper="Multi-s\u00e9lection",
            selected_color="#F472B6",
            on_change=lambda _v=None: (
                self._update_summary(),
                self._update_submit_state(),
            ),
        )
        self.grp_tags.pack(fill="x", pady=(0, 8))

        # Mouvement
        sec_move = AccordionSection(content, title="Mouvement", initially_open=True)
        sec_move.pack(fill="x")
        self.grp_pattern = ChipRadioGroup(
            sec_move.body,
            label="Pattern",
            options=MOVEMENT_PATTERNS,
            helper="Choix unique",
            selected_color="#22D3EE",
            on_change=lambda _v=None: (
                self._update_summary(),
                self._update_submit_state(),
            ),
        )
        self.grp_pattern.pack(fill="x", pady=(0, 8))

        # Type de mouvement (catÃ©gorie)
        sec_cat = AccordionSection(
            content, title="Type de mouvement", initially_open=False
        )
        sec_cat.pack(fill="x")
        self.grp_category = ChipRadioGroup(
            sec_cat.body,
            label="",
            options=MOVEMENT_CATEGORIES,
            helper="Choix unique",
            selected_color="#16A34A",
            on_change=lambda _v=None: (
                self._update_summary(),
                self._update_submit_state(),
            ),
        )
        self.grp_category.pack(fill="x", pady=(0, 8))

        # Type d'effort
        sec_type = AccordionSection(content, title="Type d'effort", initially_open=True)
        sec_type.pack(fill="x")
        self.grp_type = ChipRadioGroup(
            sec_type.body,
            label="",
            options=EFFORT_TYPES,
            helper="Choix unique",
            selected_color="#A78BFA",
            on_change=lambda _v=None: (
                self._update_summary(),
                self._update_submit_state(),
            ),
        )
        self.grp_type.pack(fill="x", pady=(0, 8))

        # ParamÃ¨tres
        sec_params = AccordionSection(
            content, title="Param\u00e8tres", initially_open=False
        )
        sec_params.pack(fill="x")
        meta_row = ctk.CTkFrame(sec_params.body, fg_color="transparent")
        meta_row.pack(fill="x", pady=(0, 8))
        meta_row.grid_columnconfigure(0, weight=1)
        meta_row.grid_columnconfigure(1, weight=1)

        self.var_charge = ctk.BooleanVar(value=False)
        self.sw_charge = ctk.CTkSwitch(
            meta_row, text="Chargeable", variable=self.var_charge
        )
        self.sw_charge.configure(
            command=lambda: (self._update_summary(), self._update_submit_state())
        )
        self.sw_charge.grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.in_coeff = LabeledInput(meta_row, label="Coeff. volume (ex: 1.0)")
        self.in_coeff.grid(row=0, column=1, sticky="ew")
        try:
            self.in_coeff.entry.bind(
                "<KeyRelease>", lambda _e=None: self._update_summary()
            )
        except Exception:
            pass

        # Footer
        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ctk.CTkButton(btn_row, text="Annuler", command=self.destroy, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])).pack(side="right")
        self.btn_submit = ctk.CTkButton(btn_row, text="Valider", command=self._submit, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]))
        self.btn_submit.pack(side="right", padx=(0, 8))
        self.btn_submit_new = ctk.CTkButton(
            btn_row,
            text="Valider + Nouveau",
            command=lambda: self._submit(reset_after=True, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])),
        )
        self.btn_submit_new.pack(side="right", padx=(0, 8))

        # PrÃ©-remplissage
        if exercise:
            self.in_nom.set_value(exercise.nom)
            self.grp_groupe.set_value(exercise.groupe_musculaire_principal)
            if exercise.equipement:
                vals = [
                    v.strip() for v in str(exercise.equipement).split(",") if v.strip()
                ]
                self.grp_equip.set_values(vals)
            if exercise.tags:
                vals_all = [
                    v.strip() for v in str(exercise.tags).split(",") if v.strip()
                ]
                vals_course = [v for v in vals_all if v in COURSE_TAGS]
                vals_tags = [v for v in vals_all if v in TAG_OPTIONS]
                if vals_course:
                    self.grp_course.set_values(vals_course)
                if vals_tags:
                    self.grp_tags.set_values(vals_tags)
            self.grp_pattern.set_value(exercise.movement_pattern or None)
            try:
                self.grp_category.set_value(
                    getattr(exercise, "movement_category", None)
                )
            except Exception:
                pass
            self.grp_type.set_value(exercise.type_effort or None)
            self.in_coeff.set_value(str(exercise.coefficient_volume or 1.0))
            self.var_charge.set(bool(exercise.est_chargeable))
        # Bind live validation on name and coeff
        try:
            self.in_nom.entry.bind(
                "<KeyRelease>",
                lambda _e=None: (self._update_summary(), self._update_submit_state()),
            )
        except Exception:
            pass
        try:
            self.in_coeff.entry.bind(
                "<KeyRelease>", lambda _e=None: self._update_submit_state()
            )
        except Exception:
            pass

        self._update_summary()
        self._update_submit_state()

        # Modal behavior
        try:
            self.transient(master)
        except Exception:
            pass
        try:
            self.in_nom.entry.focus_set()
        except Exception:
            self.focus_set()
        self.bind("<Return>", lambda _e=None: self._submit())
        self.bind("<Escape>", lambda _e=None: self.destroy())
        try:
            self.attributes("-topmost", True)
        except Exception:
            pass
        self.after(150, lambda: self.attributes("-topmost", False))
        try:
            self.grab_set()
        except Exception:
            pass
        self.lift()
        self.focus_force()

    def _submit(self, reset_after: bool = False) -> None:
        nom = self.in_nom.get_value()
        if not nom:
            self.in_nom.show_error("Nom requis")
            return
        try:
            coeff = float(self.in_coeff.get_value() or 1.0)
        except ValueError:
            self.in_coeff.show_error("Nombre invalide")
            return

        tags_vals: list[str] = []
        try:
            tags_vals += self.grp_tags.get_values()
        except Exception:
            pass
        try:
            tags_vals += self.grp_course.get_values()
        except Exception:
            pass

        # Normalisation des tags (synonymes -> canonique)
        def _canon_tag(v: str) -> str:
            if v == "Plyo":
                return "Explosif"
            if v == "Isometrie":
                return "IsomÃ©trie"
            return v

        canon_tags = [_canon_tag(t) for t in tags_vals if t]
        tags_csv = ",".join(sorted(set(canon_tags))) if canon_tags else None

        # Normalisation du pattern
        def _canon_pattern(v: Optional[str]) -> Optional[str]:
            if not v:
                return None
            vv = v.strip().lower()
            if vv in {"plyo", "saut", "jump"}:
                return "Jump"
            return v

        payload = {
            "nom": nom,
            "groupe": self.grp_groupe.get_value() or "",
            "equip": self.grp_equip.get_csv(),
            "tags": tags_csv,
            "pattern": _canon_pattern(self.grp_pattern.get_value()),
            "category": self.grp_category.get_value(),
            "type_effort": self.grp_type.get_value() or "",
            "coeff": coeff,
            "charge": bool(self.var_charge.get()),
        }
        self._on_submit(payload)
        if reset_after:
            try:
                self.in_nom.set_value("")
                self.in_nom.entry.focus_set()
            except Exception:
                pass
        else:
            self.destroy()

    def _is_valid(self) -> bool:
        """Validation simple: nom requis, coeff numÃ©rique si prÃ©sent."""
        try:
            name_ok = bool(self.in_nom.get_value())
        except Exception:
            name_ok = False
        coeff_val = None
        try:
            coeff_val = self.in_coeff.get_value()
        except Exception:
            coeff_val = None
        coeff_ok = True
        if coeff_val:
            try:
                float(coeff_val)
            except Exception:
                coeff_ok = False
        return bool(name_ok and coeff_ok)

    def _update_submit_state(self) -> None:
        valid = self._is_valid()
        state = "normal" if valid else "disabled"
        try:
            self.btn_submit.configure(state=state)
            self.btn_submit_new.configure(state=state)
        except Exception:
            pass

    def _update_summary(self) -> None:
        for w in self.summary_frame.winfo_children():
            w.destroy()

        colors = {
            "group": "#34D399",
            "pattern": "#22D3EE",
            "category": "#16A34A",
            "type": "#A78BFA",
            "equip": "#60A5FA",
            "course": "#F59E0B",
            "tags": "#F472B6",
            "flag": "#10B981",
            "meta": "#9CA3AF",
        }

        def add_section(title: str, items: list[str], color: str):
            if not items:
                return
            sec = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
            sec.pack(fill="x", pady=(0, 6))
            ctk.CTkLabel(sec, text=title).pack(anchor="w")
            row = ctk.CTkFrame(sec, fg_color="transparent")
            row.pack(anchor="w")
            for it in items:
                f = ctk.CTkFrame(row, fg_color=color, corner_radius=999)
                ctk.CTkLabel(
                    f,
                    text=it,
                    padx=8,
                    pady=2,
                    text_color="#111827",
                    font=("Segoe UI", 11, "bold"),
                ).pack()
                f.pack(side="left", padx=(0, 6), pady=(2, 0))

        g = [self.grp_groupe.get_value()] if self.grp_groupe.get_value() else []
        p = [self.grp_pattern.get_value()] if self.grp_pattern.get_value() else []
        cat = (
            [self.grp_category.get_value()]
            if hasattr(self, "grp_category") and self.grp_category.get_value()
            else []
        )
        t = [self.grp_type.get_value()] if self.grp_type.get_value() else []
        equips = sorted(
            self.grp_equip.get_values() if hasattr(self.grp_equip, "get_values") else []
        )
        courses = sorted(
            self.grp_course.get_values()
            if hasattr(self.grp_course, "get_values")
            else []
        )
        tags = sorted(
            self.grp_tags.get_values() if hasattr(self.grp_tags, "get_values") else []
        )

        add_section("Groupe", g, colors["group"])
        add_section("Mouvement", p, colors["pattern"])
        add_section("CatÃ©gorie", cat, colors["category"])
        add_section("Type", t, colors["type"])
        add_section("\u00c9quipements", equips, colors["equip"])
        add_section("Cours", courses, colors["course"])
        add_section("Tags", tags, colors["tags"])

        flags = ["Chargeable"] if bool(self.var_charge.get()) else []
        if flags:
            add_section("Options", flags, colors["flag"])
        coeff_txt = (
            self.in_coeff.get_value() if hasattr(self.in_coeff, "get_value") else None
        ) or "1.0"
        add_section("Coeff.", [coeff_txt], colors["meta"])


class _Listbox(ctk.CTkFrame):
    """Listbox Ã  hautes performances pour grandes listes.

    Utilise tkinter.Listbox pour minimiser le nombre de widgets.
    """

    def __init__(self, master, on_select=None):
        super().__init__(master, fg_color="transparent")
        self.on_select = on_select

        colors = ctk.ThemeManager.theme["color"]
        bg = colors.get("surface_light", "#1F2937")
        fg = colors.get("primary_text", "#E5E7EB")
        sel_bg = ctk.ThemeManager.theme.get("DataTable", {}).get(
            "row_hover_fg_color", "#374151"
        )
        sel_fg = fg

        # Bigger, more readable font for the list
        try:
            self._font = tkfont.Font(family="Segoe UI", size=14)
        except Exception:
            self._font = None

        self._lb = tk.Listbox(
            self,
            activestyle="dotbox",
            exportselection=False,
            selectmode=tk.EXTENDED,
            background=bg,
            foreground=fg,
            selectbackground=sel_bg,
            selectforeground=sel_fg,
            highlightthickness=0,
            bd=0,
            relief="flat",
            font=self._font if self._font else None,
        )
        self._lb.pack(fill="both", expand=True)
        self._lb.bind("<<ListboxSelect>>", self._on_select)

        # Backing store (text = key = exercise name)
        self._items_all: list[str] = []
        self._items_visible: list[str] = []

    def set_items(self, items: list[str]):
        self._items_all = list(items)
        self._items_visible = list(items)
        self._refresh()

    def _refresh(self):
        self._lb.delete(0, tk.END)
        for text in self._items_visible:
            self._lb.insert(tk.END, text)

    def filter(self, term: str):
        t = (term or "").strip().lower()
        if not t:
            self._items_visible = list(self._items_all)
        else:
            self._items_visible = [it for it in self._items_all if t in it.lower()]
        self._refresh()

    def current_key(self) -> Optional[str]:
        cur = self._lb.curselection()
        if not cur:
            return None
        idx = int(cur[0])
        if 0 <= idx < len(self._items_visible):
            return self._items_visible[idx]
        return None

    def selected_keys(self) -> list[str]:
        cur = self._lb.curselection()
        keys: list[str] = []
        for i in cur:
            try:
                idx = int(i)
                if 0 <= idx < len(self._items_visible):
                    keys.append(self._items_visible[idx])
            except Exception:
                pass
        return keys

    def _on_select(self, _e=None):
        if self.on_select:
            self.on_select(self.current_key())

    def set_font_size(self, size: int) -> None:
        try:
            if self._font is None:
                # Lazily create font if unavailable on platform
                import tkinter.font as tkfont

                self._font = tkfont.Font(size=int(size))
            else:
                self._font.configure(size=int(size))
            self._lb.configure(font=self._font)
            # Force re-render to apply row height immediately
            self._refresh()
        except Exception:
            pass


class _ExercisePreview(ctk.CTkFrame):
    """AperÃ§u dÃ©taillÃ© d'un ou plusieurs exercices.

    - Aucun Ã©lÃ©ment sÃ©lectionnÃ©: affiche un placeholder.
    - Un exercice sÃ©lectionnÃ©: affiche ses mÃ©tadonnÃ©es, Ã©quipements et tags.
    - SÃ©lection multiple: affiche un rÃ©sumÃ© (compte + premiers noms).
    """

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.colors = ctk.ThemeManager.theme.get("color", {})
        self.fonts = ctk.ThemeManager.theme.get("font", {})

        # Wrapper pour marges internes
        self._wrap = ctk.CTkFrame(
            self,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
            corner_radius=8,
        )
        self._wrap.pack(fill="both", expand=True)

        self._content = ctk.CTkFrame(self._wrap, fg_color="transparent")
        self._content.pack(fill="both", expand=True, padx=12, pady=12)

        # Titre par dÃ©faut
        CardTitle(self._content, text="AperÃ§u").pack(anchor="w", pady=(0, 8))
        self._body = ctk.CTkFrame(self._content, fg_color="transparent")
        self._body.pack(fill="both", expand=True)

        self._render_placeholder()

    def _clear(self):
        for w in self._body.winfo_children():
            w.destroy()

    def _render_placeholder(self):
        self._clear()
        ctk.CTkLabel(
            self._body,
            text="SÃ©lectionnez un exercice pour afficher l'aperÃ§u",
            text_color=self.colors.get("secondary_text", "#9CA3AF"),
            font=ctk.CTkFont(**self.fonts.get("Body", {})),
        ).pack(expand=True)

    def _render_pills(self, parent, title: str, items: list[str], color: str):
        if not items:
            return
        sec = ctk.CTkFrame(parent, fg_color="transparent")
        sec.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(
            sec,
            text=title,
            font=ctk.CTkFont(**self.fonts.get("Body", {})),
            text_color=self.colors.get("primary_text"),
        ).pack(anchor="w")
        row = ctk.CTkFrame(sec, fg_color="transparent")
        row.pack(anchor="w")
        for it in items:
            pill = ctk.CTkFrame(row, fg_color=color, corner_radius=999)
            ctk.CTkLabel(
                pill,
                text=it,
                padx=8,
                pady=2,
                text_color="#111827",
                font=("Segoe UI", 11, "bold"),
            ).pack()
            pill.pack(side="left", padx=(0, 6), pady=(2, 0))

    def _csv_to_list(self, s: str | None) -> list[str]:
        return [x.strip() for x in str(s).split(",") if x and x.strip()] if s else []

    def show(self, exercise: Optional[Exercise], multi_names: list[str] | None = None):
        """Affiche l'aperÃ§u. Si `exercise` est None, utilise `multi_names` pour rendu multiple/placeholder."""
        self._clear()
        if not exercise and not multi_names:
            self._render_placeholder()
            return

        if exercise is None and multi_names:
            # RÃ©sumÃ© multi-sÃ©lection
            count = len(multi_names)
            ctk.CTkLabel(
                self._body,
                text=f"{count} exercice(s) sÃ©lectionnÃ©(s)",
                font=ctk.CTkFont(**self.fonts.get("H3", {})),
                text_color=self.colors.get("primary_text"),
            ).pack(anchor="w", pady=(0, 6))
            preview = ", ".join(multi_names[:5]) + (" â€¦" if count > 5 else "")
            ctk.CTkLabel(
                self._body,
                text=preview,
                font=ctk.CTkFont(**self.fonts.get("Body", {})),
                text_color=self.colors.get("secondary_text", "#9CA3AF"),
            ).pack(anchor="w")
            return

        # Rendu dÃ©taillÃ© d'un exercice
        assert exercise is not None
        title = ctk.CTkLabel(
            self._body,
            text=exercise.nom,
            font=ctk.CTkFont(**self.fonts.get("H3", {})),
            text_color=self.colors.get("primary_text"),
        )
        title.pack(anchor="w", pady=(0, 4))

        # Sous-titre: infos clÃ©s
        meta_bits: list[str] = []
        if exercise.groupe_musculaire_principal:
            meta_bits.append(exercise.groupe_musculaire_principal)
        if exercise.movement_pattern:
            meta_bits.append(exercise.movement_pattern)
        if exercise.type_effort:
            meta_bits.append(exercise.type_effort)
        subtitle = " â€¢ ".join(meta_bits) if meta_bits else ""
        if subtitle:
            ctk.CTkLabel(
                self._body,
                text=subtitle,
                font=ctk.CTkFont(**self.fonts.get("Body", {})),
                text_color=self.colors.get("secondary_text", "#9CA3AF"),
            ).pack(anchor="w", pady=(0, 6))

        # Sections avec chips
        colors = {
            "group": "#34D399",
            "pattern": "#22D3EE",
            "category": "#16A34A",
            "type": "#A78BFA",
            "equip": "#60A5FA",
            "course": "#F59E0B",
            "tags": "#F472B6",
            "flag": "#10B981",
            "meta": "#9CA3AF",
        }

        # Groupe, Mouvement, Type en chips unitaires si prÃ©sents
        if exercise.groupe_musculaire_principal:
            self._render_pills(
                self._body,
                "Groupe",
                [exercise.groupe_musculaire_principal],
                colors["group"],
            )
        if exercise.movement_pattern:
            self._render_pills(
                self._body, "Mouvement", [exercise.movement_pattern], colors["pattern"]
            )
        if getattr(exercise, "movement_category", None):
            self._render_pills(
                self._body,
                "CatÃ©gorie",
                [exercise.movement_category],
                colors["category"],
            )
        if exercise.type_effort:
            self._render_pills(
                self._body, "Type", [exercise.type_effort], colors["type"]
            )

        equips = sorted(self._csv_to_list(exercise.equipement))
        tags_all = sorted(self._csv_to_list(exercise.tags))
        # SÃ©pare cours vs autres tags comme dans le formulaire
        course_tags = [t for t in tags_all if t in COURSE_TAGS]
        other_tags = [t for t in tags_all if t in TAG_OPTIONS or t not in COURSE_TAGS]

        self._render_pills(self._body, "Ã‰quipements", equips, colors["equip"])
        self._render_pills(self._body, "Cours", course_tags, colors["course"])
        self._render_pills(self._body, "Tags", other_tags, colors["tags"])

        # Flags et meta
        flags = ["Chargeable"] if bool(exercise.est_chargeable) else []
        if flags:
            self._render_pills(self._body, "Options", flags, colors["flag"])
        coeff_txt = str(exercise.coefficient_volume or 1.0)
        self._render_pills(self._body, "Coeff.", [coeff_txt], colors["meta"])


class ExercisesTab(ctk.CTkFrame):
    """Gestion basique des exercices: liste, ajout, modification, suppression."""

    def __init__(self, parent, repo: ExerciseRepository | None = None):
        super().__init__(parent, fg_color="transparent")
        self.repo = repo or ExerciseRepository()

        self.selected_name: Optional[str] = None
        self.colors = ctk.ThemeManager.theme["color"]
        self.fonts = ctk.ThemeManager.theme["font"]

        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=12, pady=(12, 0))

        self.search_entry = ctk.CTkEntry(
            toolbar, placeholder_text="Rechercher un exercice..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search)

        # Affichage adaptable: rÃ©glage rapide de la taille de police de la liste
        try:
            self.font_size_ctrl = ctk.CTkSegmentedButton(
                toolbar, values=["A", "A+", "A++"], command=self._on_font_change
            )
            self.font_size_ctrl.set("A+")
            self.font_size_ctrl.pack(side="left", padx=(8, 0))
        except Exception:
            # Fallback: OptionMenu si SegmentedButton indisponible
            try:
                self._font_var = ctk.StringVar(value="A+")
                self.font_size_ctrl = ctk.CTkOptionMenu(
                    toolbar,
                    variable=self._font_var,
                    values=["A", "A+", "A++"],
                    command=self._on_font_change,
                )
                self.font_size_ctrl.pack(side="left", padx=(8, 0))
            except Exception:
                self.font_size_ctrl = None

        self.btn_add = PrimaryButton(toolbar, text="Ajouter", command=self._on_add)
        self.btn_add.pack(side="right", padx=(8, 0))
        self.btn_edit = SecondaryButton(
            toolbar, text="Modifier", command=self._on_edit, state="disabled"
        )
        self.btn_edit.pack(side="right", padx=(8, 0))
        self.btn_del = DangerButton(
            toolbar, text="Supprimer", command=self._on_delete, state="disabled"
        )
        self.btn_del.pack(side="right")

        # Nettoyage base (normalisation)
        self.btn_clean = GhostButton(toolbar, text="Nettoyer", command=self._on_cleanup)
        self.btn_clean.pack(side="right", padx=(12, 0))

        # Body
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=12, pady=(10, 12))
        body.grid_columnconfigure(0, weight=1, uniform="columns")
        body.grid_columnconfigure(1, weight=1, uniform="columns")
        body.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            body,
            text="Liste des exercices",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors.get("primary_text", None),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))
        ctk.CTkLabel(
            body,
            text="AperÃ§u",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors.get("primary_text", None),
        ).grid(row=0, column=1, sticky="w", pady=(0, 6))

        self.listbox = _Listbox(body, on_select=self._on_select)
        self.listbox.grid(row=1, column=0, sticky="nsew")
        self.preview = _ExercisePreview(body)
        self.preview.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        self._load()

    def _on_font_change(self, value: str | None) -> None:
        mapping = {"A": 12, "A+": 14, "A++": 16}
        size = mapping.get(str(value), 14)
        try:
            self.listbox.set_font_size(size)
        except Exception:
            pass

    def _load(self) -> None:
        self.exercises: List[Exercise] = self.repo.list_all()
        names: list[str] = [e.nom for e in self.exercises]
        self.listbox.set_items(names)
        self.selected_name = None
        for b in (self.btn_del, self.btn_edit):
            b.configure(state="disabled")
        # Reset apercu
        if hasattr(self, "preview"):
            self.preview.show(None, [])

    def _on_select(self, name: Optional[str]) -> None:
        self.selected_name = name
        keys = self.listbox.selected_keys()
        has_any = bool(keys)
        single = len(keys) == 1
        self.btn_del.configure(state=("normal" if has_any else "disabled"))
        self.btn_edit.configure(state=("normal" if single else "disabled"))
        # Update preview
        if not has_any:
            self.preview.show(None, [])
            return
        if single:
            # Recherche dans cache actuel pour Ã©viter un aller DB
            ex = next((e for e in self.exercises if e.nom == keys[0]), None)
            if not ex:
                # Fallback repo si non trouvÃ©
                ex = self.repo.get_by_name(keys[0])
            self.preview.show(ex, None)
        else:
            self.preview.show(None, keys)

    def _on_search(self, _event=None):
        self.listbox.filter(self.search_entry.get())

    def _on_add(self) -> None:
        def handle_submit(payload: dict):
            e = Exercise(
                id=0,
                nom=payload["nom"],
                groupe_musculaire_principal=payload["groupe"],
                equipement=payload["equip"],
                tags=payload["tags"],
                movement_pattern=payload["pattern"],
                movement_category=payload.get("category"),
                type_effort=payload["type_effort"],
                coefficient_volume=payload["coeff"],
                est_chargeable=payload["charge"],
            )
            self.repo.create(e)
            self._load()

        ExerciseForm(self, on_submit=handle_submit)

    def _on_cleanup(self) -> None:
        # Confirmation
        confirm = ctk.CTkToplevel(self)
        confirm.title("Nettoyer la base")
        ctk.CTkLabel(
            confirm,
            text=(
                "Cette action va normaliser les donnÃ©es 'exercices' (pattern, catÃ©gorie, tags).\n"
                "Voulez-vous continuer ?"
            ),
        ).pack(padx=16, pady=12)
        row = ctk.CTkFrame(confirm, fg_color="transparent")
        row.pack(pady=(0, 12))

        def do_clean():
            try:
                changes = self.repo.cleanup_normalize()
            except Exception:
                changes = 0
            confirm.destroy()
            self._load()
            # Feedback
            toast = ctk.CTkToplevel(self)
            toast.title("Nettoyage terminÃ©")
            ctk.CTkLabel(
                toast,
                text=f"Normalisation effectuÃ©e. Modifications: {changes}",
            ).pack(padx=12, pady=10)
            try:
                toast.after(1600, toast.destroy)
            except Exception:
                pass

        ctk.CTkButton(row, text="Annuler", command=confirm.destroy, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])).pack(
            side="left", padx=8
        )
        ctk.CTkButton(row, text="Nettoyer", command=do_clean, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])).pack(side="left")

    def _on_edit(self) -> None:
        if not self.selected_name:
            return
        e = self.repo.get_by_name(self.selected_name)
        if not e:
            return

        def handle_submit(payload: dict):
            e.nom = payload["nom"]
            e.groupe_musculaire_principal = payload["groupe"]
            e.equipement = payload["equip"]
            e.tags = payload["tags"]
            e.movement_pattern = payload["pattern"]
            e.movement_category = payload.get("category")
            e.type_effort = payload["type_effort"]
            e.coefficient_volume = payload["coeff"]
            e.est_chargeable = payload["charge"]
            self.repo.update(e)
            self._load()

        ExerciseForm(self, on_submit=handle_submit, exercise=e)

    def _on_delete(self) -> None:
        keys = self.listbox.selected_keys()
        if not keys:
            return
        e = self.repo.get_by_name(keys[0]) if len(keys) == 1 else None
        confirm = ctk.CTkToplevel(
            self, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        )  # fallback if CTkToplevel not themed
        confirm.title("Confirmer la suppression")
        if len(keys) == 1 and e:
            msg = f"Supprimer '{e.nom}' ?"
        else:
            preview = ", ".join(keys[:3]) + ("â€¦" if len(keys) > 3 else "")
            msg = f"Supprimer {len(keys)} exercice(s) : {preview}"
        ctk.CTkLabel(confirm, text=msg).pack(padx=16, pady=16)
        row = ctk.CTkFrame(confirm, fg_color="transparent")
        row.pack(pady=(0, 12))

        def do_del():
            for name in keys:
                ex = self.repo.get_by_name(name)
                if ex:
                    self.repo.delete(int(ex.id))
            confirm.destroy()
            self._load()

        ctk.CTkButton(row, text="Annuler", command=confirm.destroy, font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"])).pack(
            side="left", padx=8
        )
        ctk.CTkButton(
            row,
            text="Supprimer",
            fg_color="#B00020",
            hover_color="#8E001A",
            command=do_del,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]),
        ).pack(side="left")




