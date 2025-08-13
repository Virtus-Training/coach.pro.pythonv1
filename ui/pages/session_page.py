import customtkinter as ctk
from ui.theme.fonts import get_section_font
from services.session_generator import generate_collectif
from repositories.exercices_repo import ExerciseRepository
from PIL import Image

COURSE_TYPES = ["CAF", "Core & Glutes", "Cross-Training", "Hyrox"]
DURATIONS = ["45", "60"]
EQUIPMENTS = ["Haltères","Barre","Kettlebell","Poids du corps","Machine",
              "Élastiques","TRX/anneaux","Box","Rameur","Ski","Sled"]
FORMATS = ["EMOM","AMRAP","For Time","Tabata"]
INTENSITIES = ["Low","Medium","High"]

def _choose_equipment_icon(equip_list: list[str]) -> str | None:
    if not equip_list:
        return None
    e = (equip_list[0] or "").lower()
    keywords = ["halt", "kettlebell", "barre", "poids", "trx", "anneaux", "machine", "élastique", "elastique"]
    if any(k in e for k in keywords):
        return "assets/icons/dumbbell.png"
    return None

class SessionPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1b1b1b")
        self._full_preview_win = None
        self._last_session = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Générateur de séances – Collectifs (V1)",
                     font=get_section_font()).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16,8))

        # Colonne gauche scrollable
        form = ctk.CTkScrollableFrame(self, fg_color="#222", corner_radius=10)
        form.grid(row=1, column=0, sticky="nsw", padx=(16,8), pady=8)
        form.configure(width=360)
        form.configure(width=360)
        form.grid_columnconfigure(0, weight=1)

        # Ligne 1
        row1 = ctk.CTkFrame(form, fg_color="transparent")
        row1.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        row1.grid_columnconfigure((1, 3), weight=1)
        ctk.CTkLabel(row1, text="Type de cours").grid(row=0, column=0, sticky="w", padx=(0,8))
        self.course_var = ctk.StringVar(value=COURSE_TYPES[0])
        ctk.CTkOptionMenu(row1, variable=self.course_var, values=COURSE_TYPES)\
            .grid(row=0, column=1, sticky="ew", padx=(0,12))
        ctk.CTkLabel(row1, text="Durée").grid(row=0, column=2, sticky="w", padx=(4,8))
        self.duration_var = ctk.StringVar(value=DURATIONS[0])
        ctk.CTkOptionMenu(row1, variable=self.duration_var, values=DURATIONS, width=80)\
            .grid(row=0, column=3, sticky="ew")

        # Ligne 2
        row2 = ctk.CTkFrame(form, fg_color="transparent")
        row2.grid(row=1, column=0, sticky="ew", padx=12, pady=4)
        row2.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row2, text="Intensité").grid(row=0, column=0, sticky="w", padx=(0,8))
        self.intensity_var = ctk.StringVar(value=INTENSITIES[1])
        ctk.CTkOptionMenu(row2, variable=self.intensity_var, values=INTENSITIES)\
            .grid(row=0, column=1, sticky="ew", padx=(0,12))

        # Sliders
        sliders = ctk.CTkFrame(form, fg_color="transparent")
        sliders.grid(row=2, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkLabel(sliders, text="Variabilité").grid(row=0, column=0, sticky="w", padx=(0,8))
        self.variability = ctk.IntVar(value=50)
        ctk.CTkSlider(sliders, from_=0, to=100, number_of_steps=100, variable=self.variability, width=220)\
            .grid(row=0, column=1, sticky="ew")
        ctk.CTkLabel(sliders, text="Intensité (1-10)").grid(row=1, column=0, sticky="w", padx=(0,8), pady=(6,0))
        self.intensity_cont = ctk.IntVar(value=6)
        ctk.CTkSlider(sliders, from_=1, to=10, number_of_steps=9, variable=self.intensity_cont, width=220)\
            .grid(row=1, column=1, sticky="ew", pady=(6,0))
        ctk.CTkLabel(sliders, text="Densité").grid(row=2, column=0, sticky="w", padx=(0,8), pady=(6,0))
        self.density = ctk.IntVar(value=5)
        ctk.CTkSlider(sliders, from_=1, to=10, number_of_steps=9, variable=self.density, width=220)\
            .grid(row=2, column=1, sticky="ew", pady=(6,0))

        # Matériel
        equip_frame = ctk.CTkFrame(form, fg_color="#1f1f1f")
        equip_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkLabel(equip_frame, text="Matériel disponible").grid(row=0, column=0, sticky="w", padx=8, pady=(8,4))
        grid = ctk.CTkFrame(equip_frame, fg_color="transparent")
        grid.grid(row=1, column=0, sticky="ew", padx=8, pady=(0,8))
        grid.grid_columnconfigure((0,1), weight=1)
        self.equip_vars = {}
        for i, label in enumerate(EQUIPMENTS):
            v = ctk.BooleanVar(value=label in ("Poids du corps",))
            ctk.CTkCheckBox(grid, text=label, variable=v)\
                .grid(row=i//2, column=i%2, sticky="w", padx=6, pady=4)
            self.equip_vars[label] = v

        # Formats
        formats = ctk.CTkFrame(form, fg_color="transparent")
        formats.grid(row=4, column=0, sticky="ew", padx=12, pady=6)
        ctk.CTkLabel(formats, text="Formats").grid(row=0, column=0, sticky="w", pady=(0,4))
        self.format_vars = {f: ctk.BooleanVar(value=(f in ("AMRAP","EMOM"))) for f in FORMATS}
        frm = ctk.CTkFrame(formats, fg_color="transparent")
        frm.grid(row=1, column=0, sticky="ew")
        for i, f in enumerate(FORMATS):
            frm.grid_columnconfigure(i%2, weight=1)
            ctk.CTkCheckBox(frm, text=f, variable=self.format_vars[f])\
                .grid(row=i//2, column=i%2, sticky="w", padx=6, pady=2)

        # Boutons actions 2x2
        btns = ctk.CTkFrame(form, fg_color="transparent")
        btns.grid(row=98, column=0, sticky="ew", padx=12, pady=(6,12))
        for c in range(2):
            btns.grid_columnconfigure(c, weight=1)
        ctk.CTkButton(btns, text="Générer", command=self.on_generate)\
            .grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        ctk.CTkButton(btns, text="Regénérer tout", command=self.on_generate)\
            .grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        ctk.CTkButton(btns, text="Agrandir l’aperçu", command=self.open_full_preview)\
            .grid(row=1, column=0, sticky="ew", padx=4, pady=4)
        ctk.CTkButton(btns, text="Masquer le formulaire", command=self.toggle_form)\
            .grid(row=1, column=1, sticky="ew", padx=4, pady=4)

        # Colonne droite inchangée
        right = ctk.CTkFrame(self, fg_color="#171717", corner_radius=10)
        right.grid(row=1, column=1, sticky="nsew", padx=(8,16), pady=8)
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)
        self.preview = ctk.CTkScrollableFrame(right, fg_color="#171717")
        self.preview.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self._empty = ctk.CTkFrame(self.preview, fg_color="#0f0f0f", corner_radius=12)
        self._empty.pack(fill="both", expand=True, padx=16, pady=16)
        ctk.CTkLabel(self._empty, text="Aucune séance générée.\nChoisis tes critères à gauche puis clique « Générer ».",
                    justify="center").pack(padx=24, pady=32)

        self._form = form
        self._right = right
        self._form_hidden = False

    def toggle_form(self):
        if not self._form_hidden:
            self._form.grid_remove()
            self.grid_columnconfigure(1, weight=1)
            self._form_hidden = True
        else:
            self._form.grid(row=1, column=0, sticky="nsw", padx=(16,8), pady=8)
            self.grid_columnconfigure(1, weight=1)
            self._form_hidden = False

    def on_generate(self):
        params = {
            "course_type": self.course_var.get(),
            "duration_min": int(self.duration_var.get()),
            "intensity": self.intensity_var.get(),
            "variability": int(self.variability.get()),
            "intensity_cont": int(self.intensity_cont.get()),
            "density": int(self.density.get()),
            "equipment": [k for k,v in self.equip_vars.items() if v.get()],
            "enabled_formats": [f for f, var in self.format_vars.items() if var.get()],
        }
        session = generate_collectif(params)
        self.render_session(session)

    def open_full_preview(self):
        if self._full_preview_win and ctk.CTkToplevel.winfo_exists(self._full_preview_win):
            self._full_preview_win.focus()
            return
        win = ctk.CTkToplevel(self)
        win.title("Aperçu de séance — Plein écran")
        win.geometry("1280x860")
        win.configure(fg_color="#131313")
        self._full_preview_win = win
        container = ctk.CTkScrollableFrame(win, fg_color="#131313")
        container.pack(fill="both", expand=True, padx=16, pady=16)
        if self._last_session:
            self._render_session_into(self._last_session, container, two_cols=True)

    def render_session(self, session):
        # Efface empty state + ancien rendu
        try:
            self._empty.destroy()
        except Exception:
            pass
        for child in self.preview.winfo_children():
            try:
                child.destroy()
            except Exception:
                pass

        self._last_session = session
        self.preview._parent_canvas.yview_moveto(0.0)
        self._render_session_into(session, self.preview, two_cols=True)


    def _render_session_into(self, session, container, two_cols=True):
        # --- Résumé doux (entête)
        header = ctk.CTkFrame(container, fg_color="#1d2228", corner_radius=12)
        header.pack(fill="x", padx=12, pady=(12,6))
        left = ctk.CTkFrame(header, fg_color="transparent"); left.pack(side="left", padx=12, pady=10)
        self._icon_label(left, "assets/icons/dumbbell.png", session.label).pack(side="left", padx=(0,16))
        self._icon_label(left, "assets/icons/clock.png", f"{session.duration_sec//60} min").pack(side="left")

        # --- Grille responsive
        grid = ctk.CTkFrame(container, fg_color="#171717")
        grid.pack(fill="both", expand=True, padx=6, pady=6)
        ncols = 2 if two_cols else 1
        for c in range(ncols):
            grid.grid_columnconfigure(c, weight=1, uniform="col")

        # Meta exercices (nom + matériel)
        repo = ExerciseRepository()
        all_ids = [it.exercise_id for b in session.blocks for it in b.items]
        if hasattr(repo, "get_name_equipment_by_ids"):
            meta_map = repo.get_name_equipment_by_ids(all_ids)
        else:
            names = repo.get_names_by_ids(all_ids)
            meta_map = {k: {"name": v, "equipment": []} for k, v in names.items()}

        # Cartes de blocs
        for i, b in enumerate(session.blocks):
            col = i % ncols
            row = i // ncols
            self._render_block_card(grid, row, col, b, meta_map)

        # Footer
        footer = ctk.CTkFrame(container, fg_color="#1d2228", corner_radius=12)
        footer.pack(fill="x", padx=12, pady=(6,12))
        ctk.CTkButton(footer, text="Enregistrer", command=lambda: self._save_session(session)).pack(side="right", padx=10, pady=10)

    def _render_block_card(self, parent, row, col, block, meta_map):
        # Palette douce par type
        type_colors = {
            "EMOM":  ("#0b3a44", "#0a6b84"),     # fond / accent
            "AMRAP": ("#2b2a1f", "#b78b0a"),
            "SETSxREPS": ("#29222b", "#8b46b9"),
            "For Time": ("#222a29", "#138f6b"),
            "TABATA": ("#2b2121", "#b05555"),
        }
        bg, accent = type_colors.get(block.type.upper(), ("#232323", "#0a6b84"))

        # Carte + barre latérale d’accent
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
        parent.grid_rowconfigure(row, weight=1)

        accent_bar = ctk.CTkFrame(wrapper, fg_color=accent, width=4, corner_radius=6)
        accent_bar.pack(side="left", fill="y", padx=(0,6), pady=(0,0))

        card = ctk.CTkFrame(wrapper, fg_color=bg, corner_radius=12)
        card.pack(side="left", fill="both", expand=True)

        # --- En-tête du bloc
        top = ctk.CTkFrame(card, fg_color="#1b1b1b")
        top.pack(fill="x", padx=12, pady=(12,8))
        title = block.title or (f"{block.type} – {block.duration_sec//60}’" if block.duration_sec else block.type)
        ctk.CTkLabel(top, text=title, font=("Segoe UI", 14, "bold")).pack(side="left")

        badges = ctk.CTkFrame(top, fg_color="transparent"); badges.pack(side="right")
        self._chip(badges, block.type).pack(side="left", padx=4)
        if getattr(block, "rounds", None):
            self._chip(badges, f"{block.rounds} rounds").pack(side="left", padx=4)
        if getattr(block, "work_sec", None) and getattr(block, "rest_sec", None):
            self._chip(badges, f"{block.work_sec}/{block.rest_sec}").pack(side="left", padx=4)

        # --- Liste d'exercices
        body = ctk.CTkFrame(card, fg_color="#121416", corner_radius=10)
        body.pack(fill="x", padx=12, pady=(0,10))

        for it in block.items:
            meta = meta_map.get(it.exercise_id, {"name": it.exercise_id, "equipment": []})
            name = meta["name"]
            equip_list = meta.get("equipment", [])
            equip_text = " · ".join(equip_list) if equip_list else "Poids du corps"

            # Prescription compacte
            presc = []
            reps = it.prescription.get("reps")
            rest = it.prescription.get("rest_sec") or it.prescription.get("rest")
            if reps: presc.append(f"{reps} reps")
            if rest: presc.append(f"repos {rest}")
            presc_txt = " • ".join(presc) if presc else ""

            rowf = ctk.CTkFrame(body, fg_color="transparent")
            rowf.pack(fill="x", padx=10, pady=6)

            # Puce et icône matériel
            ctk.CTkLabel(rowf, text="•", font=("Segoe UI", 14)).pack(side="left", padx=(0,8))
            icon_path = _choose_equipment_icon(equip_list)
            if icon_path:
                try:
                    img = ctk.CTkImage(light_image=Image.open(icon_path), size=(16,16))
                    ctk.CTkLabel(rowf, image=img, text="").pack(side="left", padx=(0,6))
                    rowf._img = img
                except Exception:
                    pass

            # Texte à gauche (nom gras + équipement muted)
            left = ctk.CTkFrame(rowf, fg_color="transparent"); left.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(left, text=name, font=("Segoe UI", 13, "bold"), anchor="w", wraplength=380).pack(anchor="w")
            ctk.CTkLabel(left, text=equip_text, font=("Segoe UI", 11)).pack(anchor="w")

            # Pastille prescription à droite
            if presc_txt:
                self._pill(rowf, presc_txt, fg=accent).pack(side="right", padx=6)
                # petite "poignée" verticale façon carte
                ctk.CTkFrame(rowf, fg_color=accent, width=6, height=20, corner_radius=3).pack(side="right", padx=(0,6))
                rowf.pack_propagate(False)

        # --- Actions
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill="x", padx=12, pady=(2,12))
        ctk.CTkButton(actions, text="Regénérer ce bloc").pack(side="left", padx=4)
        ctk.CTkButton(actions, text="Remplacer un exercice").pack(side="left", padx=4)



    def _chip(self, parent, text):
        f = ctk.CTkFrame(parent, fg_color="#2b2f35", corner_radius=999)
        ctk.CTkLabel(f, text=text, padx=8, pady=2, font=("Segoe UI", 11)).pack()
        return f

    def _pill(self, parent, text, fg="#0a6b84"):
        f = ctk.CTkFrame(parent, fg_color=fg, corner_radius=999)
        ctk.CTkLabel(f, text=text, padx=10, pady=2, font=("Segoe UI", 11)).pack()
        return f


    def _badge(self, parent, text):
        f = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=8)
        ctk.CTkLabel(f, text=text, padx=8, pady=2).pack()
        return f

    def _icon_label(self, parent, icon_path, text):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        try:
            img = ctk.CTkImage(light_image=Image.open(icon_path), size=(18,18))
            ctk.CTkLabel(row, image=img, text="").pack(side="left", padx=(0,6))
            row._img = img
        except Exception:
            pass
        ctk.CTkLabel(row, text=text).pack(side="left")
        return row

    def _save_session(self, session):
        from repositories.sessions_repo import SessionsRepository
        SessionsRepository().save(session)
