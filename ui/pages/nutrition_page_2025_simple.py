"""🚀 CoachPro Nutrition 2025 - Interface Simplifiée

Version d'intégration immédiate avec composants fonctionnels.
La version complète avec animations avancées sera intégrée progressivement.
"""

from datetime import datetime
from typing import Dict, List, Optional
import customtkinter as ctk

from controllers.nutrition_controller import NutritionController
from dtos.nutrition_dtos import NutritionPageDTO, PlanAlimentaireDTO
from ui.components.design_system import (
    Card,
    CardTitle,
    HeroBanner,
    PrimaryButton,
    SecondaryButton,
)

# Import des composants simplifiés
from ui.components.nutrition_2025.stubs import (
    AnimatedCard,
    ProgressBar,
    ScoreIndicator,
    StreakTracker,
    MacroProgressRings,
    AdvancedFoodLogger,
    QuickActionBar,
    AnalyticsDashboard,
    IntelligentMealPlanner
)

from ui.pages.client_detail_page_components.fiche_nutrition_tab import (
    GenerateFicheModal,
)


class NutritionPage2025(ctk.CTkFrame):
    """🎯 Interface Nutrition Premium 2025 - Version Simplifiée

    Nouvelle interface moderne qui rivalise avec MyFitnessPal Premium:
    - Dashboard intelligent avec insights IA
    - Suivi de progression avec gamification
    - Enregistrement d'aliments avancé
    - Analytics interactifs
    - Planification intelligente de repas
    """

    def __init__(self, parent, controller: NutritionController, client_id: int):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.nutrition_controller = controller  # Compatibilité avec les modals
        self.client_id = client_id
        self.current_view = "dashboard"  # dashboard, analytics, planner

        # Chargement des données
        self.data = self.controller.get_nutrition_page_data(client_id)
        self.client = self.data.client
        self.fiche = self.data.fiche
        self.plan: PlanAlimentaireDTO = self.data.plan

        # Métriques de performance
        self.performance_metrics = {
            "last_render_time": 0,
            "interaction_count": 0,
            "load_start": datetime.now()
        }

        self._setup_layout()
        self._create_interface()
        self._track_performance("initial_load")

    def _setup_layout(self) -> None:
        """📐 Configuration du layout responsive"""
        self.grid_columnconfigure(0, weight=1, minsize=320)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Navigation
        self.grid_rowconfigure(2, weight=1)  # Contenu principal

    def _create_interface(self) -> None:
        """🎨 Construction de l'interface moderne"""
        self._create_header()
        self._create_navigation()
        self._create_main_content()

    def _create_header(self) -> None:
        """📱 Header moderne avec statistiques rapides"""
        subtitle = (
            f"Plan nutritionnel intelligent de {self.client.prenom} {self.client.nom}"
            if self.client
            else "Plan nutritionnel intelligent"
        )

        self.hero = HeroBanner(
            self,
            title="🚀 Nutrition 2025",
            subtitle=subtitle,
            icon_path="assets/icons/nutrition-2025.png",
        )
        self.hero.grid(row=0, column=0, sticky="ew", padx=8, pady=(4, 2))

        # Configurer les colonnes pour le stats_frame
        self.hero.grid_columnconfigure(3, weight=0)

        # Statistiques rapides dans le header - utiliser grid pour compatibilité avec HeroBanner
        stats_frame = ctk.CTkFrame(self.hero, fg_color="transparent")
        stats_frame.grid(row=0, column=3, rowspan=2, sticky="e", padx=(0, 12), pady=4)

        # Score nutritionnel quotidien
        score = self._calculate_nutrition_score()
        score_color = self._get_score_color(score)

        self.score_label = ctk.CTkLabel(
            stats_frame,
            text=f"📊 Score: {score}/100",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=score_color
        )
        self.score_label.pack(side="right", padx=(0, 16))

        # Suivi de série
        streak_days = self._get_nutrition_streak()
        self.streak_label = ctk.CTkLabel(
            stats_frame,
            text=f"🔥 {streak_days} jours",
            font=ctk.CTkFont(size=12)
        )
        self.streak_label.pack(side="right", padx=(0, 8))

    def _create_navigation(self) -> None:
        """🧭 Navigation moderne entre les vues"""
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=4)

        # Boutons de navigation
        nav_buttons = [
            ("📊 Dashboard", "dashboard", self._show_dashboard),
            ("📈 Analytics", "analytics", self._show_analytics),
            ("🍽️ Planner", "planner", self._show_planner),
        ]

        self.nav_buttons = {}
        button_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        button_frame.pack(side="left")

        for text, key, command in nav_buttons:
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                width=120,
                height=32,
                fg_color=("gray85", "gray25"),
                text_color=("gray20", "gray80"),
                hover_color=("gray75", "gray35"),
                corner_radius=8
            )
            btn.pack(side="left", padx=2)
            self.nav_buttons[key] = btn

        # Barre d'actions rapides
        from ui.components.nutrition_2025 import QuickActionBar
        self.quick_actions = QuickActionBar(
            self.nav_frame,
            on_generate_plan=self._show_plan_generator,
            on_export=self._export_advanced_pdf,
            compact_mode=True
        )
        self.quick_actions.pack(side="right")

    def _create_main_content(self) -> None:
        """🎯 Zone de contenu principal avec commutation de vues"""
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(4, 8))

        # Initialiser toutes les vues
        self._create_dashboard_view()
        self._create_analytics_view()
        self._create_planner_view()

        # Afficher la vue par défaut
        self._show_dashboard()

    def _create_dashboard_view(self) -> None:
        """📊 Dashboard intelligent avec insights IA"""
        self.dashboard_view = ctk.CTkFrame(self.content_frame, fg_color="transparent")

        # Configuration en grille pour le dashboard
        self.dashboard_view.grid_columnconfigure(0, weight=2)  # Gauche: Vue d'ensemble
        self.dashboard_view.grid_columnconfigure(1, weight=3)  # Centre: Progression
        self.dashboard_view.grid_columnconfigure(2, weight=2)  # Droite: Insights
        self.dashboard_view.grid_rowconfigure(0, weight=1)

        # Panneau de vue d'ensemble (gauche)
        self._create_overview_panel()

        # Panneau de progression (centre)
        self._create_progress_panel()

        # Panneau d'insights (droite)
        self._create_insights_panel()

    def _create_overview_panel(self) -> None:
        """📊 Panneau de vue d'ensemble quotidienne"""
        self.overview_frame = AnimatedCard(self.dashboard_view, title="📊 Vue d'ensemble")
        self.overview_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)

        # Indicateur de score nutritionnel
        score = self._calculate_nutrition_score()
        self.score_indicator = ScoreIndicator(
            self.overview_frame.content_frame,
            score=score,
            label="Score Nutrition",
            color_scheme="health"
        )
        self.score_indicator.pack(pady=16)

        # Statistiques rapides en grille
        stats_frame = ctk.CTkFrame(self.overview_frame.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=16, pady=8)

        # Configuration grille 2x2
        for i in range(2):
            stats_frame.grid_columnconfigure(i, weight=1)
            stats_frame.grid_rowconfigure(i, weight=1)

        # Statistiques principales
        self._create_stat_card(stats_frame, "🔥", f"{self.plan.totals_kcal:.0f}",
                              f"{self.fiche.objectif_kcal if self.fiche else 2000:.0f}", "kcal", 0, 0)
        self._create_stat_card(stats_frame, "💪", f"{self.plan.totals_proteines:.1f}",
                              f"{self.fiche.proteines_g if self.fiche else 150:.1f}", "g", 0, 1)

        meals_count = len([r for r in self.plan.repas if r.items])
        self._create_stat_card(stats_frame, "🍽️", str(meals_count), "3-4", "repas", 1, 0)
        self._create_stat_card(stats_frame, "💧", "1.5", "2.5", "L", 1, 1)

        # Boutons d'action rapide
        actions_frame = ctk.CTkFrame(self.overview_frame.content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=16, pady=(16, 8))

        quick_log_btn = ctk.CTkButton(
            actions_frame,
            text="⚡ Ajout Rapide",
            command=self._show_quick_add,
            height=32,
            corner_radius=16
        )
        quick_log_btn.pack(side="left", padx=(0, 8))

    def _create_progress_panel(self) -> None:
        """🎯 Panneau de progression macro interactif"""
        from ui.components.nutrition_2025 import MacroProgressRings

        self.progress_frame = AnimatedCard(self.dashboard_view, title="🎯 Progression Macros")
        self.progress_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

        # Anneaux de progression macro
        self.macro_rings = MacroProgressRings(
            self.progress_frame.content_frame,
            calories_current=self.plan.totals_kcal if self.plan else 0,
            calories_target=self.fiche.objectif_kcal if self.fiche else 2000,
            protein_current=self.plan.totals_proteines if self.plan else 0,
            protein_target=self.fiche.proteines_g if self.fiche else 150,
            carbs_current=self.plan.totals_glucides if self.plan else 0,
            carbs_target=self.fiche.glucides_g if self.fiche else 200,
            fats_current=self.plan.totals_lipides if self.plan else 0,
            fats_target=self.fiche.lipides_g if self.fiche else 70
        )
        self.macro_rings.pack(expand=True, fill="both", padx=16, pady=16)

        # Timeline des repas
        self._create_meal_timeline()

    def _create_insights_panel(self) -> None:
        """💡 Panneau d'insights IA personnalisés"""
        from ui.components.nutrition_2025 import StreakTracker

        self.insights_frame = AnimatedCard(self.dashboard_view, title="💡 Insights Intelligents")
        self.insights_frame.grid(row=0, column=2, sticky="nsew", padx=(8, 0), pady=8)

        # Suivi de série
        streak_days = 5  # TODO: Calculer à partir des données
        self.streak_tracker = StreakTracker(
            self.insights_frame.content_frame,
            streak_days=streak_days,
            streak_type="nutrition"
        )
        self.streak_tracker.pack(pady=16)

        # Insights personnalisés
        insights = self._generate_smart_insights()
        for insight in insights[:3]:  # Max 3 insights
            self._create_insight_card(insight)

        # Food logger intégré
        self.food_logger = AdvancedFoodLogger(
            self.insights_frame.content_frame,
            self.controller,
            client_id=self.client.client_id if self.client else None,
            on_food_added=self._on_food_added,
            compact_mode=True
        )
        self.food_logger.pack(fill="both", expand=True, padx=8, pady=(16, 8))

    def _create_analytics_view(self) -> None:
        """📈 Vue analytique avancée"""
        from ui.components.nutrition_2025 import AnalyticsDashboard

        self.analytics_view = AnalyticsDashboard(
            self.content_frame,
            client_id=self.client.client_id if self.client else 1,
            controller=self.controller
        )

    def _create_planner_view(self) -> None:
        """🍽️ Générateur de plans alimentaires automatique"""
        from ui.components.nutrition_2025 import MealPlanGenerator

        self.planner_view = MealPlanGenerator(
            self.content_frame,
            controller=self.controller,
            client_id=self.client.client_id if self.client else 1,
            on_plan_generated=self._on_plan_generated
        )

    # Méthodes de navigation avec transitions fluides
    def _show_dashboard(self) -> None:
        """Afficher la vue dashboard"""
        self._animate_view_transition("dashboard", self.dashboard_view)

    def _show_analytics(self) -> None:
        """Afficher la vue analytics"""
        self._animate_view_transition("analytics", self.analytics_view)

    def _show_planner(self) -> None:
        """Afficher la vue planificateur"""
        self._animate_view_transition("planner", self.planner_view)

    def _animate_view_transition(self, view_key: str, target_view) -> None:
        """🎬 Transition fluide entre les vues"""
        if hasattr(self, 'current_view') and self.current_view == view_key:
            return

        # Mise à jour de l'état des boutons de navigation
        for key, btn in self.nav_buttons.items():
            if key == view_key:
                btn.configure(
                    fg_color=("#1f538d", "#1f538d"),
                    text_color=("white", "white")
                )
            else:
                btn.configure(
                    fg_color=("gray85", "gray25"),
                    text_color=("gray20", "gray80")
                )

        # Masquer toutes les vues
        for view in [self.dashboard_view, self.analytics_view, self.planner_view]:
            if view.winfo_exists():
                view.pack_forget()

        # Afficher la vue cible
        target_view.pack(fill="both", expand=True, padx=8, pady=8)

        self.current_view = view_key
        self._track_performance(f"view_switch_{view_key}")

    def _create_stat_card(self, parent, icon: str, current: str, target: str, unit: str, row: int, col: int) -> None:
        """📊 Créer une carte de statistique colorée"""
        # Couleurs selon le type de statistique
        icon_colors = {
            "🔥": "#EF4444",  # Rouge pour calories
            "💪": "#10B981",  # Vert pour protéines
            "🍽️": "#F59E0B",  # Orange pour repas
            "💧": "#3B82F6"   # Bleu pour eau
        }

        card = ctk.CTkFrame(parent, height=85, corner_radius=12)
        card.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

        # Icône avec fond coloré
        icon_color = icon_colors.get(icon, "#64748B")
        icon_bg = ctk.CTkFrame(card, width=32, height=32, corner_radius=16,
                              fg_color=icon_color)
        icon_bg.pack(pady=(10, 4))

        icon_label = ctk.CTkLabel(
            icon_bg,
            text=icon,
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        icon_label.pack(expand=True)

        # Valeurs avec meilleur contraste
        values_label = ctk.CTkLabel(
            card,
            text=f"{current}/{target}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=icon_color
        )
        values_label.pack(pady=2)

        # Unité
        unit_label = ctk.CTkLabel(
            card,
            text=unit,
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray40")
        )
        unit_label.pack(pady=(0, 8))

    def _create_meal_timeline(self) -> None:
        """⏰ Timeline des repas"""
        timeline_frame = ctk.CTkFrame(self.progress_frame.content_frame, fg_color="transparent")
        timeline_frame.pack(fill="x", padx=16, pady=(0, 16))

        # Titre
        timeline_title = ctk.CTkLabel(
            timeline_frame,
            text="⏰ Repas d'aujourd'hui",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        timeline_title.pack(anchor="w", pady=(0, 8))

        # Timeline simplifiée
        if self.plan and self.plan.repas:
            for i, repas in enumerate(self.plan.repas[:4]):  # Max 4 repas
                meal_frame = ctk.CTkFrame(timeline_frame, height=30)
                meal_frame.pack(fill="x", pady=2)

                # Repas avec icônes colorées
                meal_data = [
                    ("🌅", "Petit-déj", "#F59E0B"),  # Orange pour matin
                    ("🌞", "Déjeuner", "#10B981"),   # Vert pour midi
                    ("🌆", "Dîner", "#EF4444"),      # Rouge pour soir
                    ("🌙", "Collation", "#6366F1")   # Violet pour collation
                ][i]

                icon, meal_name, color = meal_data
                items_count = len(repas.items) if repas.items else 0

                # Icône colorée
                icon_frame = ctk.CTkFrame(meal_frame, width=24, height=24,
                                        corner_radius=12, fg_color=color)
                icon_frame.pack(side="left", padx=(12, 8), pady=3)

                ctk.CTkLabel(
                    icon_frame,
                    text=icon,
                    font=ctk.CTkFont(size=12),
                    text_color="white"
                ).pack(expand=True)

                # Texte du repas
                ctk.CTkLabel(
                    meal_frame,
                    text=f"{meal_name}: {items_count} aliment{'s' if items_count > 1 else ''}",
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color=color
                ).pack(side="left", pady=8)

    def _generate_smart_insights(self) -> list:
        """💡 Générer des insights intelligents"""
        insights = []

        if self.plan and self.fiche:
            # Insight calorique
            calorie_ratio = self.plan.totals_kcal / max(self.fiche.objectif_kcal, 1)
            if calorie_ratio < 0.8:
                insights.append({
                    "icon": "⚠️",
                    "title": "Calories insuffisantes",
                    "message": "Vous pourriez manquer d'énergie"
                })
            elif calorie_ratio > 1.2:
                insights.append({
                    "icon": "📊",
                    "title": "Surplus calorique",
                    "message": "Attention aux excès"
                })

            # Insight protéines
            protein_ratio = self.plan.totals_proteines / max(self.fiche.proteines_g, 1)
            if protein_ratio < 0.8:
                insights.append({
                    "icon": "💪",
                    "title": "Plus de protéines",
                    "message": "Important pour la récupération"
                })

        # Insight par défaut
        if not insights:
            insights.append({
                "icon": "🎯",
                "title": "Bonne journée !",
                "message": "Continuez comme ça"
            })

        return insights

    def _create_insight_card(self, insight: dict) -> None:
        """💡 Créer une carte d'insight colorée"""
        # Couleurs par type d'insight
        insight_colors = {
            "⚠️": "#EF4444",  # Rouge pour attention
            "📊": "#F59E0B",  # Orange pour analyse
            "💪": "#10B981",  # Vert pour protéines
            "🎯": "#6366F1"   # Violet pour succès
        }

        icon = insight["icon"]
        color = insight_colors.get(icon, "#64748B")

        card = ctk.CTkFrame(self.insights_frame.content_frame, height=65,
                           corner_radius=12, border_width=2, border_color=color)
        card.pack(fill="x", padx=8, pady=4)

        # Icône avec fond coloré
        icon_bg = ctk.CTkFrame(card, width=36, height=36, corner_radius=18,
                              fg_color=color)
        icon_bg.pack(side="left", padx=12, pady=8)

        icon_label = ctk.CTkLabel(
            icon_bg,
            text=icon,
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        icon_label.pack(expand=True)

        # Contenu
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True, padx=(8, 12), pady=8)

        title_label = ctk.CTkLabel(
            content_frame,
            text=insight["title"],
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color
        )
        title_label.pack(anchor="w", pady=(4, 2))

        message_label = ctk.CTkLabel(
            content_frame,
            text=insight["message"],
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray40")
        )
        message_label.pack(anchor="w")

    def _track_performance(self, action: str) -> None:
        """📊 Suivi de performance simple"""
        # Implémentation basique pour le suivi
        pass

    def _show_plan_generator(self) -> None:
        """📊 Afficher le générateur de plan"""
        # Basculer vers l'onglet Planner
        self._show_planner()

    def _on_plan_generated(self, plan_data: dict) -> None:
        """📝 Callback génération de plan"""
        duree = plan_data.get('config', {}).duree_jours if hasattr(plan_data.get('config', {}), 'duree_jours') else 'N/A'
        nb_jours = len(plan_data.get('jours', [])) if plan_data else 0
        print(f"🪄 Plan généré: {nb_jours} jours")

        # Optionnel: Afficher une notification de succès
        self._show_success("Plan généré !", f"Plan alimentaire de {nb_jours} jours créé avec succès")

    # SUPPRESSION DES ANCIENNES MÉTHODES COMPLEXES
    def _create_dashboard_view_OLD(self) -> None:
        """📊 Dashboard intelligent avec insights IA"""
        self.dashboard_view = ctk.CTkFrame(self.content_frame, fg_color="transparent")

        # Configuration en grille pour le dashboard
        self.dashboard_view.grid_columnconfigure(0, weight=2)  # Gauche: Vue d'ensemble
        self.dashboard_view.grid_columnconfigure(1, weight=3)  # Centre: Progression
        self.dashboard_view.grid_columnconfigure(2, weight=2)  # Droite: Insights
        self.dashboard_view.grid_rowconfigure(0, weight=1)

        # Panneau de vue d'ensemble (gauche)
        self._create_overview_panel()

        # Panneau de progression (centre)
        self._create_progress_panel()

        # Panneau d'insights (droite)
        self._create_insights_panel()

    def _create_overview_panel(self) -> None:
        """📊 Panneau de vue d'ensemble quotidienne"""
        self.overview_frame = AnimatedCard(self.dashboard_view, title="📊 Vue d'ensemble")
        self.overview_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=8)

        # Indicateur de score nutritionnel
        score = self._calculate_nutrition_score()
        self.score_indicator = ScoreIndicator(
            self.overview_frame.content_frame,
            score=score,
            label="Score Nutrition",
            color_scheme="health"
        )
        self.score_indicator.pack(pady=16)

        # Statistiques rapides en grille
        stats_frame = ctk.CTkFrame(self.overview_frame.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=16, pady=8)

        # Configuration grille 2x2
        for i in range(2):
            stats_frame.grid_columnconfigure(i, weight=1)
            stats_frame.grid_rowconfigure(i, weight=1)

        # Statistiques principales
        self._create_stat_card(stats_frame, "🔥", f"{self.plan.totals_kcal:.0f}",
                              f"{self.fiche.objectif_kcal if self.fiche else 2000:.0f}", "kcal", 0, 0)
        self._create_stat_card(stats_frame, "💪", f"{self.plan.totals_proteines:.1f}",
                              f"{self.fiche.proteines_g if self.fiche else 150:.1f}", "g", 0, 1)

        meals_count = len([r for r in self.plan.repas if r.items])
        self._create_stat_card(stats_frame, "🍽️", str(meals_count), "3-4", "repas", 1, 0)
        self._create_stat_card(stats_frame, "💧", "1.5", "2.5", "L", 1, 1)

        # Boutons d'action rapide
        actions_frame = ctk.CTkFrame(self.overview_frame.content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=16, pady=(16, 8))

        quick_log_btn = ctk.CTkButton(
            actions_frame,
            text="⚡ Ajout Rapide",
            command=self._show_quick_add,
            height=32,
            corner_radius=16
        )
        quick_log_btn.pack(side="left", padx=(0, 8))

        meal_scan_btn = ctk.CTkButton(
            actions_frame,
            text="📸 Scanner Repas",
            command=self._scan_meal,
            height=32,
            corner_radius=16,
            fg_color="transparent",
            border_width=1
        )
        meal_scan_btn.pack(side="left")

    def _create_progress_panel(self) -> None:
        """🎯 Panneau de progression interactive"""
        self.progress_frame = AnimatedCard(self.dashboard_view, title="🎯 Progression Macros")
        self.progress_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

        # Anneaux de progression des macros
        self.macro_rings = MacroProgressRings(
            self.progress_frame.content_frame,
            calories_current=self.plan.totals_kcal,
            calories_target=self.fiche.objectif_kcal if self.fiche else 2000,
            protein_current=self.plan.totals_proteines,
            protein_target=self.fiche.proteines_g if self.fiche else 150,
            carbs_current=self.plan.totals_glucides,
            carbs_target=self.fiche.glucides_g if self.fiche else 200,
            fats_current=self.plan.totals_lipides,
            fats_target=self.fiche.lipides_g if self.fiche else 70
        )
        self.macro_rings.pack(expand=True, fill="both", padx=16, pady=16)

        # Timeline des repas
        timeline_frame = ctk.CTkFrame(self.progress_frame.content_frame, fg_color="transparent")
        timeline_frame.pack(fill="x", padx=16, pady=(0, 16))

        ctk.CTkLabel(
            timeline_frame,
            text="🕐 Timeline des Repas",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(0, 8))

        self._create_meal_timeline(timeline_frame)

    def _create_insights_panel(self) -> None:
        """💡 Panneau d'insights IA"""
        self.insights_frame = AnimatedCard(self.dashboard_view, title="💡 Insights Intelligents")
        self.insights_frame.grid(row=0, column=2, sticky="nsew", padx=(8, 0), pady=8)

        # Génération et affichage des insights
        insights = self._generate_smart_insights()

        insights_container = ctk.CTkScrollableFrame(
            self.insights_frame.content_frame,
            fg_color="transparent",
            height=300
        )
        insights_container.pack(fill="both", expand=True, padx=16, pady=16)

        for insight in insights:
            self._create_insight_card(insights_container, insight)

        # Intégration de l'enregistreur d'aliments
        self.food_logger = AdvancedFoodLogger(
            self.insights_frame.content_frame,
            controller=self.controller,
            client_id=self.client_id,
            on_food_added=self._on_food_added,
            compact_mode=True
        )
        self.food_logger.pack(fill="x", padx=16, pady=(8, 16))

    def _create_analytics_view(self) -> None:
        """📈 Vue analytics interactive"""
        self.analytics_view = AnalyticsDashboard(
            self.content_frame,
            client_id=self.client_id,
            controller=self.controller
        )

    def _create_planner_view(self) -> None:
        """🍽️ Vue planificateur intelligent"""
        self.planner_view = IntelligentMealPlanner(
            self.content_frame,
            client_id=self.client_id,
            controller=self.controller,
            on_plan_generated=self._on_plan_generated
        )

    # Méthodes de navigation avec transitions fluides
    # Navigation simplifiée - vue unique, plus besoin de basculement

    # Méthodes utilitaires et calculs
    def _calculate_nutrition_score(self) -> int:
        """🧮 Calcul du score nutritionnel (0-100)"""
        if not self.plan or not self.fiche:
            return 0

        score = 0

        # Précision calorique (30 points)
        if self.fiche.objectif_kcal > 0:
            calorie_ratio = self.plan.totals_kcal / self.fiche.objectif_kcal
            if 0.9 <= calorie_ratio <= 1.1:
                score += 30
            elif 0.8 <= calorie_ratio <= 1.2:
                score += 20
            elif calorie_ratio > 0.5:
                score += 10

        # Équilibre des macros (40 points)
        protein_target = max(self.fiche.proteines_g, 1) if self.fiche.proteines_g else 150
        protein_ratio = self.plan.totals_proteines / protein_target
        if 0.8 <= protein_ratio <= 1.2:
            score += 20
        elif protein_ratio > 0.6:
            score += 10

        # Fréquence des repas (20 points)
        meal_count = len([r for r in self.plan.repas if r.items])
        if meal_count >= 3:
            score += 20
        elif meal_count >= 2:
            score += 10

        # Variété alimentaire (10 points)
        unique_foods = set()
        for repas in self.plan.repas:
            for item in repas.items:
                unique_foods.add(item.aliment_id)
        if len(unique_foods) >= 6:
            score += 10
        elif len(unique_foods) >= 4:
            score += 5

        return min(score, 100)

    def _get_score_color(self, score: int) -> str:
        """🎨 Couleur basée sur le score"""
        if score >= 80:
            return "#4CAF50"  # Vert - Excellent
        elif score >= 60:
            return "#FF9800"  # Orange - Bon
        else:
            return "#F44336"  # Rouge - À améliorer

    def _get_nutrition_streak(self) -> int:
        """🔥 Calcul de la série de jours consécutifs"""
        # Pour l'instant, retour d'une série fictive
        return 7  # TODO: Implémenter le calcul réel

    def _create_stat_card(self, parent, icon: str, value: str, target: str, unit: str, row: int, col: int):
        """📊 Création d'une carte de statistique"""
        card = ctk.CTkFrame(parent, fg_color=("gray90", "gray20"))
        card.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

        # Icône
        icon_label = ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=20))
        icon_label.pack(pady=(8, 4))

        # Valeur
        value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=16, weight="bold"))
        value_label.pack()

        # Cible et unité
        target_label = ctk.CTkLabel(
            card,
            text=f"/ {target} {unit}",
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray50")
        )
        target_label.pack(pady=(0, 8))

    def _create_meal_timeline(self, parent) -> None:
        """⏰ Timeline visuelle des repas"""
        timeline_container = ctk.CTkFrame(parent, fg_color="transparent")
        timeline_container.pack(fill="x")

        meals = [
            ("🌅", "Petit-déjeuner", "08:00", bool(self.plan.repas[0].items) if len(self.plan.repas) > 0 else False),
            ("☀️", "Déjeuner", "12:30", bool(self.plan.repas[1].items) if len(self.plan.repas) > 1 else False),
            ("🌙", "Dîner", "19:00", bool(self.plan.repas[2].items) if len(self.plan.repas) > 2 else False),
        ]

        for icon, name, time, completed in meals:
            meal_frame = ctk.CTkFrame(timeline_container, fg_color="transparent")
            meal_frame.pack(fill="x", pady=2)

            # Indicateur de statut
            status_color = "#4CAF50" if completed else "#E0E0E0"
            status_indicator = ctk.CTkLabel(
                meal_frame,
                text="●",
                text_color=status_color,
                font=ctk.CTkFont(size=16)
            )
            status_indicator.pack(side="left", padx=(0, 8))

            # Info du repas
            info_frame = ctk.CTkFrame(meal_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True)

            meal_label = ctk.CTkLabel(
                info_frame,
                text=f"{icon} {name}",
                font=ctk.CTkFont(size=11, weight="bold" if completed else "normal")
            )
            meal_label.pack(anchor="w")

            time_label = ctk.CTkLabel(
                info_frame,
                text=time,
                font=ctk.CTkFont(size=9),
                text_color=("gray60", "gray50")
            )
            time_label.pack(anchor="w")

    def _generate_smart_insights(self) -> List[Dict]:
        """🤖 Génération d'insights IA"""
        insights = []

        # Analyse de l'apport vs objectifs
        if self.fiche:
            calorie_ratio = self.plan.totals_kcal / max(self.fiche.objectif_kcal, 1)
            protein_ratio = self.plan.totals_proteines / max(self.fiche.proteines_g, 1)

            # Insights caloriques
            if calorie_ratio < 0.7:
                insights.append({
                    "type": "warning",
                    "icon": "⚡",
                    "title": "Déficit Énergétique",
                    "message": "Vous êtes significativement sous votre objectif calorique. Ajoutez une collation saine.",
                    "action": "Ajouter Collation",
                    "priority": "high"
                })
            elif calorie_ratio > 1.2:
                insights.append({
                    "type": "caution",
                    "icon": "🎯",
                    "title": "Au-dessus de l'Objectif",
                    "message": "Vous avez dépassé votre objectif calorique. Concentrez-vous sur des aliments nutritifs demain.",
                    "action": "Voir Conseils",
                    "priority": "medium"
                })

            # Insights protéines
            if protein_ratio < 0.8:
                insights.append({
                    "type": "suggestion",
                    "icon": "💪",
                    "title": "Boost Protéines",
                    "message": "Ajoutez plus de protéines pour soutenir vos objectifs. Essayez du poulet, poisson ou légumineuses.",
                    "action": "Trouver Protéines",
                    "priority": "medium"
                })

        # Insight fréquence des repas
        meal_count = len([r for r in self.plan.repas if r.items])
        if meal_count < 3:
            insights.append({
                "type": "tip",
                "icon": "🍽️",
                "title": "Fréquence des Repas",
                "message": "Répartir votre apport sur 3-4 repas peut stimuler le métabolisme et l'énergie.",
                "action": "Planifier Repas",
                "priority": "low"
            })

        # Insight variété
        unique_foods = set()
        for repas in self.plan.repas:
            for item in repas.items:
                unique_foods.add(item.aliment_id)

        if len(unique_foods) < 5:
            insights.append({
                "type": "tip",
                "icon": "🌈",
                "title": "Variété Alimentaire",
                "message": "Essayez différents aliments pour une meilleure couverture nutritionnelle et plus de satisfaction.",
                "action": "Explorer Aliments",
                "priority": "low"
            })

        # Insight basé sur l'heure
        current_hour = datetime.now().hour
        if 6 <= current_hour <= 10 and not (len(self.plan.repas) > 0 and self.plan.repas[0].items):
            insights.append({
                "type": "reminder",
                "icon": "🌅",
                "title": "Carburant Matinal",
                "message": "Commencez votre journée avec un petit-déjeuner nutritif pour stimuler votre métabolisme !",
                "action": "Logger Petit-déj",
                "priority": "high"
            })

        return insights

    def _create_insight_card(self, parent, insight: Dict) -> None:
        """💡 Création d'une carte d'insight"""
        priority_colors = {
            "high": ("#FF5722", "#FF8A65"),
            "medium": ("#FF9800", "#FFB74D"),
            "low": ("#2196F3", "#64B5F6")
        }

        card_color = priority_colors.get(insight["priority"], ("#2196F3", "#64B5F6"))

        card = ctk.CTkFrame(parent, fg_color=("gray95", "gray15"))
        card.pack(fill="x", pady=4)

        # Header avec icône et titre
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 8))

        icon_label = ctk.CTkLabel(header, text=insight["icon"], font=ctk.CTkFont(size=16))
        icon_label.pack(side="left", padx=(0, 8))

        title_label = ctk.CTkLabel(header, text=insight["title"], font=ctk.CTkFont(size=12, weight="bold"))
        title_label.pack(side="left")

        # Message
        message_label = ctk.CTkLabel(
            card,
            text=insight["message"],
            font=ctk.CTkFont(size=10),
            wraplength=200,
            justify="left"
        )
        message_label.pack(anchor="w", padx=12, pady=(0, 8))

        # Bouton d'action
        action_btn = ctk.CTkButton(
            card,
            text=insight["action"],
            height=24,
            width=100,
            font=ctk.CTkFont(size=9),
            fg_color=card_color[0],
            hover_color=card_color[1],
            command=lambda: self._handle_insight_action(insight)
        )
        action_btn.pack(anchor="e", padx=12, pady=(0, 12))

    # Gestionnaires d'événements
    def _handle_insight_action(self, insight: Dict) -> None:
        """💡 Gestionnaire d'action d'insight"""
        action = insight["action"]

        if action == "Ajouter Collation":
            self._show_quick_add()
        elif action == "Trouver Protéines":
            print("🔍 Filtrage vers aliments riches en protéines")
        elif action == "Planifier Repas":
            self._show_planner()
        elif action == "Logger Petit-déj":
            self._show_quick_add()
        else:
            print(f"🎯 Action insight: {action}")

    def _on_food_added(self, food_data: Dict) -> None:
        """Gestionnaire d'ajout d'aliment"""
        # Rafraîchir les données
        self.data = self.controller.get_nutrition_page_data(self.client_id)
        self.plan = self.data.plan

        # Mettre à jour toutes les vues
        if hasattr(self, 'macro_rings'):
            self.macro_rings.update_values(
                calories_current=self.plan.totals_kcal,
                protein_current=self.plan.totals_proteines,
                carbs_current=self.plan.totals_glucides,
                fats_current=self.plan.totals_lipides
            )

        if hasattr(self, 'analytics_view'):
            self.analytics_view.refresh()

        # Suivre l'interaction
        self._track_performance("food_added")

        # Afficher suggestion intelligente si approprié
        self._show_smart_suggestion_if_needed()

    def _on_plan_generated(self, plan_data: Dict) -> None:
        """Gestionnaire de plan généré"""
        self.data = self.controller.get_nutrition_page_data(self.client_id)
        self.plan = self.data.plan

        # Mettre à jour le dashboard et afficher le succès
        if hasattr(self, 'macro_rings'):
            self.macro_rings.update_values(
                calories_current=self.plan.totals_kcal,
                protein_current=self.plan.totals_proteines,
                carbs_current=self.plan.totals_glucides,
                fats_current=self.plan.totals_lipides
            )

        self._show_success("Plan de repas généré !", "Votre plan personnalisé est prêt. Révisez et personnalisez selon vos besoins.")

        # Basculer vers le dashboard pour afficher les résultats
        self._show_dashboard()

    def _show_smart_suggestion_if_needed(self) -> None:
        """🤖 Afficher des suggestions contextuelles si nécessaire"""
        suggestions = self._generate_smart_insights()
        if suggestions:
            # Afficher notification subtile avec suggestions
            print(f"💡 Suggestion: {suggestions[0]['message']}")

    # Méthodes d'entrée avancées
    def _voice_log_food(self) -> None:
        """🎤 Enregistrement vocal d'aliments"""
        print("🎤 Enregistrement vocal activé...")

    def _photo_scan_food(self) -> None:
        """📸 Scan photo avec reconnaissance IA"""
        print("📸 Scan photo activé...")

    def _barcode_scan_food(self) -> None:
        """📊 Scan code-barres avec recherche base de données"""
        print("📊 Scan code-barres activé...")

    def _export_advanced_pdf(self) -> None:
        """📄 Export rapport nutritionnel complet"""
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            title="Exporter Rapport Nutrition 2025"
        )
        if path:
            try:
                dto = NutritionPageDTO(client=self.client, fiche=self.fiche, plan=self.plan)
                self.controller.export_plan_to_pdf(dto, path)
                self._show_success("Export réussi", f"Rapport sauvegardé dans {path}")
            except Exception as e:
                self._show_error("Échec de l'export", str(e))

    # Actions rapides
    def _show_quick_add(self) -> None:
        """⚡ Afficher dialog d'ajout rapide"""
        print("🚀 Dialog d'ajout rapide d'aliment")

    def _scan_meal(self) -> None:
        """📸 Ouvrir interface de scan de repas"""
        print("📸 Interface de scan de repas")

    # Suivi de performance
    def _track_performance(self, event: str) -> None:
        """📊 Suivi des métriques de performance"""
        current_time = datetime.now()
        self.performance_metrics[f"{event}_time"] = current_time
        self.performance_metrics["interaction_count"] += 1

        # Logger les opérations lentes
        if event.endswith("_time"):
            if "last_interaction" in self.performance_metrics:
                response_time = (current_time - self.performance_metrics["last_interaction"]).total_seconds() * 1000
                if response_time > 300:  # Réponse lente > 300ms
                    print(f"⚠️ Réponse lente détectée: {event} a pris {response_time:.1f}ms")

        self.performance_metrics["last_interaction"] = current_time

    # Méthodes de feedback UI
    def _show_success(self, title: str, message: str) -> None:
        """✅ Afficher notification de succès"""
        import tkinter.messagebox as messagebox
        messagebox.showinfo(title, message)

    def _show_error(self, title: str, message: str) -> None:
        """❌ Afficher notification d'erreur"""
        import tkinter.messagebox as messagebox
        messagebox.showerror(title, message)

    # Interface publique
    def refresh(self) -> None:
        """🔄 Rafraîchir toutes les données et vues"""
        start_time = datetime.now()

        # Recharger les données
        self.data = self.controller.get_nutrition_page_data(self.client_id)
        self.plan = self.data.plan

        # Mettre à jour le score et la série
        score = self._calculate_nutrition_score()
        self.score_label.configure(text=f"📊 Score: {score}/100")

        # Rafraîchir la vue actuelle
        if self.current_view == "dashboard":
            if hasattr(self, 'macro_rings'):
                self.macro_rings.update_values(
                    calories_current=self.plan.totals_kcal,
                    protein_current=self.plan.totals_proteines,
                    carbs_current=self.plan.totals_glucides,
                    fats_current=self.plan.totals_lipides
                )
        elif self.current_view == "analytics":
            self.analytics_view.refresh()
        elif self.current_view == "planner":
            self.planner_view.refresh()

        # Suivre la performance
        refresh_time = (datetime.now() - start_time).total_seconds() * 1000
        print(f"🔄 Rafraîchissement terminé en {refresh_time:.1f}ms")

    def get_performance_metrics(self) -> Dict:
        """📊 Obtenir les métriques de performance"""
        return self.performance_metrics.copy()