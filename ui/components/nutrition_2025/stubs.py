"""🔧 Stubs temporaires pour l'intégration rapide

Composants simplifiés pour permettre l'intégration immédiate
de la nouvelle interface nutrition 2025
"""

import customtkinter as ctk
from typing import Dict, List, Optional, Callable, Any


class AnimatedCard(ctk.CTkFrame):
    """🎴 Version simplifiée de la carte animée"""

    def __init__(self, parent, title: str = "", **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title

        if title:
            title_label = ctk.CTkLabel(
                self,
                text=title,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            title_label.pack(anchor="w", padx=16, pady=(16, 8))

        # Zone de contenu
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))


class ProgressBar(ctk.CTkFrame):
    """📊 Barre de progression simplifiée"""

    def __init__(self, parent, width: int = 200, height: int = 20,
                 progress: float = 0.0, target: float = 100.0,
                 color_scheme: str = "default", show_percentage: bool = True,
                 **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)

        self.target = target
        self.show_percentage = show_percentage

        # Barre de progression personnalisée pour éviter les problèmes CustomTkinter
        ratio = min(progress / target, 1.0)

        # Background frame
        bg_frame = ctk.CTkFrame(self, width=width-10, height=8, corner_radius=4,
                               fg_color=("gray80", "gray30"))
        bg_frame.pack(pady=5)
        bg_frame.pack_propagate(False)

        # Progress fill
        progress_width = max(2, int((width-10) * ratio))
        self.progress_fill = ctk.CTkFrame(bg_frame, width=progress_width, height=6,
                                        fg_color="#22D3EE", corner_radius=3)
        self.progress_fill.place(x=1, y=1)

        # Store reference for updates
        self.progress_bg = bg_frame
        self.progress_bar = self  # Pour compatibilité
        self.current_ratio = ratio
        self.bar_width = width - 10

        if show_percentage:
            percentage = min((progress / target) * 100, 100)
            self.label = ctk.CTkLabel(
                self,
                text=f"{percentage:.0f}%",
                font=ctk.CTkFont(size=10)
            )
            self.label.pack()

    def set_progress(self, progress: float, target: Optional[float] = None):
        if target:
            self.target = target
        ratio = min(progress / self.target, 1.0)

        # Update custom progress bar
        if hasattr(self, 'progress_fill') and hasattr(self, 'bar_width'):
            progress_width = max(2, int(self.bar_width * ratio))
            self.progress_fill.configure(width=progress_width)
            self.current_ratio = ratio

        if hasattr(self, 'label'):
            self.label.configure(text=f"{ratio * 100:.0f}%")


class ScoreIndicator(ctk.CTkFrame):
    """🎯 Indicateur de score simplifié"""

    def __init__(self, parent, score: float = 0, max_score: float = 100,
                 label: str = "Score", color_scheme: str = "health", **kwargs):
        super().__init__(parent, **kwargs)

        self.score = score
        self.max_score = max_score

        # Score affiché
        score_label = ctk.CTkLabel(
            self,
            text=f"{score:.0f}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        score_label.pack(pady=8)

        # Libellé
        desc_label = ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray50")
        )
        desc_label.pack()

        # Barre de progression
        progress_bar = ProgressBar(
            self,
            width=100,
            height=8,
            progress=score,
            target=max_score,
            show_percentage=False
        )
        progress_bar.pack(pady=8)

    def update_score(self, new_score: float):
        self.score = new_score
        # Mise à jour simple - dans la version complète il y aurait des animations


class StreakTracker(ctk.CTkFrame):
    """🔥 Suivi de série simplifié"""

    def __init__(self, parent, streak_days: int = 0, streak_type: str = "nutrition", **kwargs):
        super().__init__(parent, **kwargs)

        # Icône flamme
        fire_label = ctk.CTkLabel(
            self,
            text="🔥" * min(streak_days // 3 + 1, 4),
            font=ctk.CTkFont(size=24)
        )
        fire_label.pack(pady=8)

        # Nombre de jours
        streak_label = ctk.CTkLabel(
            self,
            text=f"{streak_days} jour{'s' if streak_days != 1 else ''}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        streak_label.pack()

        # Type de série
        type_label = ctk.CTkLabel(
            self,
            text=f"{streak_type.title()} Streak",
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray50")
        )
        type_label.pack(pady=(0, 8))


class MacroProgressRings(ctk.CTkFrame):
    """🎯 Anneaux de progression macro simplifiés"""

    def __init__(self, parent, calories_current: float = 0, calories_target: float = 2000,
                 protein_current: float = 0, protein_target: float = 150,
                 carbs_current: float = 0, carbs_target: float = 200,
                 fats_current: float = 0, fats_target: float = 70, **kwargs):
        super().__init__(parent, **kwargs)

        # Configuration en grille 2x2
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        # Données des macros
        macros = [
            ("🔥", "Calories", calories_current, calories_target, "kcal"),
            ("💪", "Protéines", protein_current, protein_target, "g"),
            ("🌾", "Glucides", carbs_current, carbs_target, "g"),
            ("🧈", "Lipides", fats_current, fats_target, "g")
        ]

        for i, (icon, name, current, target, unit) in enumerate(macros):
            row = i // 2
            col = i % 2

            macro_frame = ctk.CTkFrame(self)
            macro_frame.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

            # Icône
            icon_label = ctk.CTkLabel(
                macro_frame,
                text=icon,
                font=ctk.CTkFont(size=20)
            )
            icon_label.pack(pady=(12, 4))

            # Barre de progression
            progress_bar = ProgressBar(
                macro_frame,
                width=100,
                height=12,
                progress=current,
                target=target,
                show_percentage=False
            )
            progress_bar.pack(pady=4)

            # Valeurs
            values_label = ctk.CTkLabel(
                macro_frame,
                text=f"{current:.0f} / {target:.0f} {unit}",
                font=ctk.CTkFont(size=9)
            )
            values_label.pack()

            # Nom
            name_label = ctk.CTkLabel(
                macro_frame,
                text=name,
                font=ctk.CTkFont(size=10, weight="bold")
            )
            name_label.pack(pady=(2, 12))

    def update_values(self, calories_current=None, protein_current=None,
                     carbs_current=None, fats_current=None):
        # Version simplifiée - pas de mise à jour dynamique
        pass

    def update_animation(self, frame: int):
        # Version simplifiée - pas d'animation
        pass


class AdvancedFoodLogger(ctk.CTkFrame):
    """🍽️ Enregistreur d'aliments avancé simplifié"""

    def __init__(self, parent, controller, client_id: Optional[int] = None,
                 on_food_added: Optional[Callable] = None, compact_mode: bool = False, **kwargs):
        super().__init__(parent, **kwargs)

        self.controller = controller
        self.on_food_added = on_food_added or (lambda x: None)

        # Titre
        if not compact_mode:
            title_label = ctk.CTkLabel(
                self,
                text="🍽️ Enregistrement d'aliments",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            title_label.pack(anchor="w", padx=16, pady=(16, 8))

        # Barre de recherche
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            self,
            textvariable=self.search_var,
            placeholder_text="Rechercher un aliment...",
            width=200 if compact_mode else 300
        )
        search_entry.pack(fill="x", padx=16, pady=8)

        # Zone de résultats
        self.results_frame = ctk.CTkScrollableFrame(
            self,
            height=150 if compact_mode else 200
        )
        self.results_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # Lier la recherche
        self.search_var.trace_add("write", self._on_search_change)

        # Charger des suggestions initiales
        self._load_suggestions()

    def _on_search_change(self, *args):
        query = self.search_var.get().strip()
        if len(query) >= 2:
            try:
                results = self.controller.search_aliments(query)
                self._display_results(results[:5])  # Limiter à 5 résultats
            except:
                pass
        elif len(query) == 0:
            self._load_suggestions()

    def _load_suggestions(self):
        try:
            suggestions = self.controller.search_aliments("")[:5]
            self._display_results(suggestions)
        except:
            pass

    def _display_results(self, aliments):
        # Nettoyer les résultats précédents
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for aliment in aliments:
            item_frame = ctk.CTkFrame(self.results_frame)
            item_frame.pack(fill="x", pady=2)

            # Nom de l'aliment
            name_btn = ctk.CTkButton(
                item_frame,
                text=aliment.nom,
                anchor="w",
                fg_color="transparent",
                text_color=("black", "white"),
                hover_color=("gray80", "gray30"),
                command=lambda a=aliment: self._add_aliment(a)
            )
            name_btn.pack(side="left", fill="x", expand=True, padx=8, pady=4)

            # Info nutritionnelle
            info_label = ctk.CTkLabel(
                item_frame,
                text=f"{aliment.kcal_100g:.0f} kcal",
                font=ctk.CTkFont(size=10),
                text_color=("gray60", "gray50")
            )
            info_label.pack(side="right", padx=8, pady=4)

    def _add_aliment(self, aliment):
        # Ajouter avec 100g par défaut
        food_data = {
            "food": aliment,
            "quantity": 100.0,
            "input_method": "manual"
        }
        self.on_food_added(food_data)

        # Effacer la recherche
        self.search_var.set("")
        self._load_suggestions()


class QuickActionBar(ctk.CTkFrame):
    """⚡ Barre d'actions rapides simplifiée"""

    def __init__(self, parent, on_generate_plan=None, on_export=None, compact_mode=False, **kwargs):
        super().__init__(parent, **kwargs)

        self.on_generate_plan = on_generate_plan or (lambda: print("📊 Générer plan"))
        self.on_export = on_export or (lambda: print("📤 Export PDF"))

        # Actions utiles seulement
        actions = [
            ("📊", "Générer Plan", self.on_generate_plan, "#10B981"),  # Vert pour génération
            ("📤", "Export PDF", self.on_export, "#6366F1")           # Violet pour export
        ]

        for icon, label, command, color in actions:
            btn = ctk.CTkButton(
                self,
                text=f"{icon} {label}",
                width=120 if compact_mode else 140,
                height=36,
                command=command,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color=color,
                hover_color=self._darken_color(color),
                corner_radius=18
            )
            btn.pack(side="left", padx=6, pady=2)

    def _darken_color(self, hex_color: str) -> str:
        """🎨 Assombrir une couleur pour l'effet hover"""
        # Conversion basique pour assombrir la couleur
        color_map = {
            "#10B981": "#059669",  # Vert -> Vert foncé
            "#6366F1": "#4F46E5",  # Violet -> Violet foncé
        }
        return color_map.get(hex_color, hex_color)


class AnalyticsDashboard(ctk.CTkFrame):
    """📊 Tableau de bord analytique simplifié"""

    def __init__(self, parent, client_id: int, controller, **kwargs):
        super().__init__(parent, **kwargs)

        self.client_id = client_id
        self.controller = controller

        # Titre
        title_label = ctk.CTkLabel(
            self,
            text="📊 Analyses Nutritionnelles",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=16)

        # Métriques de base
        metrics_frame = ctk.CTkFrame(self)
        metrics_frame.pack(fill="x", padx=16, pady=8)

        metrics_label = ctk.CTkLabel(
            metrics_frame,
            text="Analyse simplifiée disponible",
            font=ctk.CTkFont(size=12)
        )
        metrics_label.pack(pady=16)

    def refresh(self):
        pass


class IntelligentMealPlanner(ctk.CTkFrame):
    """🧠 Planificateur de repas intelligent simplifié"""

    def __init__(self, parent, client_id: int, controller,
                 on_plan_generated: Optional[Callable] = None, **kwargs):
        super().__init__(parent, **kwargs)

        self.client_id = client_id
        self.controller = controller
        self.on_plan_generated = on_plan_generated or (lambda x: None)

        # Titre
        title_label = ctk.CTkLabel(
            self,
            text="🧠 Planificateur de Repas Intelligent",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=16)

        # Bouton de génération
        generate_btn = ctk.CTkButton(
            self,
            text="🪄 Générer Plan",
            command=self._generate_plan,
            width=160,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        generate_btn.pack(pady=16)

        # Zone de statut
        self.status_label = ctk.CTkLabel(
            self,
            text="Prêt à générer votre plan personnalisé",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray50")
        )
        self.status_label.pack()

    def _generate_plan(self):
        self.status_label.configure(text="🪄 Génération en cours...")

        # Simuler la génération
        self.after(2000, self._complete_generation)

    def _complete_generation(self):
        self.status_label.configure(text="✅ Plan généré avec succès!")

        # Notifier le parent
        mock_plan = {
            "id": "generated_plan",
            "name": "Plan Personnalisé",
            "duration": 7,
            "meals": []
        }
        self.on_plan_generated(mock_plan)

    def refresh(self):
        pass