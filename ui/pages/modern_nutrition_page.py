"""
Page nutritionnelle moderne avec interface inspirée des meilleures apps
Intègre recherche avancée, génération intelligente et analyses nutritionnelles
"""

from datetime import datetime
from tkinter import messagebox
from typing import List, Optional

import customtkinter as ctk

from models.aliment import Aliment
from models.profil_nutritionnel import ProfilNutritionnel
from repositories.aliment_repo import AlimentRepository
from repositories.profil_nutritionnel_repo import ProfilNutritionnelRepository
from services.food_search_service import FiltreRecherche, FoodSearchService
from services.meal_plan_generator_service import MealPlanGeneratorService
from ui.components.design_system import PrimaryButton, SecondaryButton


class ModernNutritionPage(ctk.CTkFrame):
    """Interface nutritionnelle moderne avec fonctionnalités avancées"""

    def __init__(self, parent, client_id: int):
        super().__init__(parent)

        self.client_id = client_id

        # Services
        self.meal_generator = MealPlanGeneratorService()
        self.food_search = FoodSearchService()
        self.profil_repo = ProfilNutritionnelRepository()
        self.aliment_repo = AlimentRepository()

        # État de l'interface
        self.current_profile: Optional[ProfilNutritionnel] = None
        self.current_plan = None
        self.selected_meal_index = 0

        # Configuration de la grille
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_columnconfigure(0, weight=1, minsize=300)  # Sidebar
        self.grid_columnconfigure(1, weight=2, minsize=400)  # Main
        self.grid_columnconfigure(2, weight=1, minsize=300)  # Search

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Configure l'interface utilisateur"""

        # Header avec actions principales
        self._create_header()

        # Panneau de gauche: Profil + Objectifs
        self._create_profile_panel()

        # Panneau central: Plan alimentaire
        self._create_meal_plan_panel()

        # Panneau de droite: Recherche + Suggestions
        self._create_search_panel()

    def _create_header(self):
        """Crée l'en-tête avec les actions principales"""

        header = ctk.CTkFrame(self, height=80)
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(10, 0))
        header.grid_columnconfigure(1, weight=1)

        # Titre
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        ctk.CTkLabel(
            title_frame,
            text="🍎 Nutrition Intelligente",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Génération automatique de plans alimentaires personnalisés",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray40"),
        ).pack(anchor="w")

        # Actions principales
        actions_frame = ctk.CTkFrame(header, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e", padx=20, pady=10)

        PrimaryButton(
            actions_frame,
            text="🤖 Générer Plan Auto",
            command=self._generate_automatic_plan,
            width=180,
        ).pack(side="right", padx=(0, 10))

        SecondaryButton(
            actions_frame,
            text="⚙️ Configurer Profil",
            command=self._open_profile_config,
            width=160,
        ).pack(side="right", padx=(0, 10))

    def _create_profile_panel(self):
        """Crée le panneau de profil et objectifs nutritionnels"""

        self.profile_frame = ctk.CTkFrame(self)
        self.profile_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)

        # Titre du profil
        profile_header = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        profile_header.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            profile_header,
            text="👤 Profil Nutritionnel",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w")

        # Informations du profil
        self.profile_info_frame = ctk.CTkFrame(self.profile_frame)
        self.profile_info_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Objectifs macronutriments
        objectives_header = ctk.CTkFrame(self.profile_frame, fg_color="transparent")
        objectives_header.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            objectives_header,
            text="🎯 Objectifs Journaliers",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w")

        # Barres de progression
        self.objectives_frame = ctk.CTkFrame(self.profile_frame)
        self.objectives_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Recommandations intelligentes
        recommendations_header = ctk.CTkFrame(
            self.profile_frame, fg_color="transparent"
        )
        recommendations_header.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            recommendations_header,
            text="💡 Recommandations",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w")

        self.recommendations_frame = ctk.CTkFrame(self.profile_frame)
        self.recommendations_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _create_meal_plan_panel(self):
        """Crée le panneau principal du plan alimentaire"""

        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)

        # En-tête du plan
        plan_header = ctk.CTkFrame(main_frame, fg_color="transparent")
        plan_header.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            plan_header,
            text="🍽️ Plan Alimentaire Personnalisé",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w")

        # Actions du plan
        plan_actions = ctk.CTkFrame(plan_header, fg_color="transparent")
        plan_actions.pack(fill="x", pady=(10, 0))

        SecondaryButton(
            plan_actions,
            text="📊 Analyser",
            command=self._analyze_current_plan,
            width=100,
        ).pack(side="left", padx=(0, 10))

        SecondaryButton(
            plan_actions,
            text="🔄 Optimiser",
            command=self._optimize_current_plan,
            width=100,
        ).pack(side="left", padx=(0, 10))

        SecondaryButton(
            plan_actions,
            text="📄 Exporter PDF",
            command=self._export_plan_pdf,
            width=120,
        ).pack(side="right")

        # Zone de contenu scrollable
        self.meal_content_frame = ctk.CTkScrollableFrame(main_frame)
        self.meal_content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Message de bienvenue par défaut
        self._show_welcome_message()

    def _create_search_panel(self):
        """Crée le panneau de recherche avancée"""

        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=1, column=2, sticky="nsew", padx=(5, 10), pady=10)

        # En-tête de recherche
        search_header = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_header.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            search_header,
            text="🔍 Recherche Intelligente",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w")

        # Barre de recherche principale
        search_input_frame = ctk.CTkFrame(search_frame)
        search_input_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._on_search_change)

        self.search_entry = ctk.CTkEntry(
            search_input_frame,
            textvariable=self.search_var,
            placeholder_text="Rechercher un aliment...",
            font=ctk.CTkFont(size=14),
        )
        self.search_entry.pack(fill="x", padx=10, pady=10)

        # Filtres avancés
        self._create_advanced_filters(search_frame)

        # Résultats de recherche
        results_header = ctk.CTkFrame(search_frame, fg_color="transparent")
        results_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            results_header, text="Résultats", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        # Zone de résultats scrollable
        self.results_frame = ctk.CTkScrollableFrame(search_frame, height=200)
        self.results_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        # Suggestions intelligentes
        self._create_smart_suggestions(search_frame)

    def _create_advanced_filters(self, parent):
        """Crée les filtres avancés de recherche"""

        filters_frame = ctk.CTkFrame(parent)
        filters_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Titre des filtres
        ctk.CTkLabel(
            filters_frame, text="Filtres", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Filtre par catégorie
        ctk.CTkLabel(filters_frame, text="Catégorie:").pack(
            anchor="w", padx=10, pady=(5, 0)
        )

        self.category_var = ctk.StringVar(value="Toutes")
        self.category_menu = ctk.CTkOptionMenu(
            filters_frame,
            variable=self.category_var,
            values=[
                "Toutes",
                "Légumes",
                "Fruits",
                "Viandes",
                "Poissons",
                "Céréales",
                "Légumineuses",
            ],
            command=self._on_filter_change,
        )
        self.category_menu.pack(fill="x", padx=10, pady=(5, 10))

        # Filtre par objectif nutritionnel
        ctk.CTkLabel(filters_frame, text="Objectif:").pack(
            anchor="w", padx=10, pady=(5, 0)
        )

        self.objective_var = ctk.StringVar(value="Tous")
        self.objective_menu = ctk.CTkOptionMenu(
            filters_frame,
            variable=self.objective_var,
            values=[
                "Tous",
                "Riche en protéines",
                "Faible en calories",
                "Riche en fibres",
                "Équilibré",
            ],
            command=self._on_filter_change,
        )
        self.objective_menu.pack(fill="x", padx=10, pady=(5, 10))

        # Toggle pour compatibilité régime
        self.regime_compatible = ctk.BooleanVar(value=True)
        self.regime_checkbox = ctk.CTkCheckBox(
            filters_frame,
            text="Compatible avec mon régime",
            variable=self.regime_compatible,
            command=self._on_filter_change,
        )
        self.regime_checkbox.pack(anchor="w", padx=10, pady=5)

    def _create_smart_suggestions(self, parent):
        """Crée la zone de suggestions intelligentes"""

        suggestions_frame = ctk.CTkFrame(parent)
        suggestions_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(
            suggestions_frame,
            text="💡 Suggestions pour vous",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.suggestions_content = ctk.CTkFrame(suggestions_frame)
        self.suggestions_content.pack(fill="x", padx=10, pady=(5, 10))

        # Chargement des suggestions par défaut
        self._load_smart_suggestions()

    def _load_data(self):
        """Charge les données initiales"""

        try:
            # Chargement du profil nutritionnel
            self.current_profile = self.profil_repo.get_by_client_id(self.client_id)

            if not self.current_profile:
                self._show_profile_setup_needed()
                return

            # Mise à jour de l'interface avec les données du profil
            self._update_profile_display()
            self._load_smart_suggestions()

        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            messagebox.showerror("Erreur", f"Impossible de charger les données: {e}")

    def _show_welcome_message(self):
        """Affiche le message de bienvenue"""

        welcome_frame = ctk.CTkFrame(self.meal_content_frame, fg_color="transparent")
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=50)

        ctk.CTkLabel(
            welcome_frame,
            text="🌟 Bienvenue dans votre espace nutritionnel personnalisé !",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=20)

        ctk.CTkLabel(
            welcome_frame,
            text="Pour commencer, configurez votre profil nutritionnel ou\ngénérez automatiquement un plan alimentaire.",
            font=ctk.CTkFont(size=14),
            justify="center",
        ).pack(pady=10)

        actions_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        actions_frame.pack(pady=30)

        PrimaryButton(
            actions_frame,
            text="🤖 Générer mon premier plan",
            command=self._generate_automatic_plan,
            width=250,
            height=50,
        ).pack(pady=10)

        SecondaryButton(
            actions_frame,
            text="⚙️ Configurer mon profil",
            command=self._open_profile_config,
            width=200,
            height=40,
        ).pack()

    def _show_profile_setup_needed(self):
        """Affiche l'interface de configuration de profil nécessaire"""

        setup_frame = ctk.CTkFrame(
            self.profile_info_frame, fg_color=("orange", "dark_orange")
        )
        setup_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            setup_frame,
            text="⚠️ Configuration Requise",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            setup_frame,
            text="Créez votre profil nutritionnel\npour des recommandations personnalisées",
            justify="center",
        ).pack(pady=5)

        PrimaryButton(
            setup_frame,
            text="Configurer maintenant",
            command=self._open_profile_config,
            width=180,
        ).pack(pady=(10, 15))

    def _update_profile_display(self):
        """Met à jour l'affichage du profil"""

        if not self.current_profile:
            return

        # Nettoyage du frame existant
        for widget in self.profile_info_frame.winfo_children():
            widget.destroy()

        # Informations de base
        info_text = f"""👤 {self.current_profile.age} ans, {self.current_profile.sexe}
🎯 {self.current_profile.objectif_principal}
⚡ {self.current_profile.niveau_activite}
🔥 {int(self.current_profile.besoins_caloriques or 0)} kcal/jour"""

        ctk.CTkLabel(
            self.profile_info_frame,
            text=info_text,
            justify="left",
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=10, pady=10)

        self._update_objectives_display()

    def _update_objectives_display(self):
        """Met à jour l'affichage des objectifs avec barres de progression"""

        if not self.current_profile or not self.current_profile.repartition_macros:
            return

        # Nettoyage du frame existant
        for widget in self.objectives_frame.winfo_children():
            widget.destroy()

        macros = self.current_profile.repartition_macros

        # Création des barres de progression pour chaque macro
        objectives = [
            ("Calories", int(self.current_profile.besoins_caloriques or 0), 0, "kcal"),
            ("Protéines", int(macros.get("proteines_g", 0)), 0, "g"),
            ("Glucides", int(macros.get("glucides_g", 0)), 0, "g"),
            ("Lipides", int(macros.get("lipides_g", 0)), 0, "g"),
        ]

        for name, target, current, unit in objectives:
            self._create_progress_bar(
                self.objectives_frame, name, target, current, unit
            )

    def _create_progress_bar(
        self, parent, name: str, target: int, current: int, unit: str
    ):
        """Crée une barre de progression pour un objectif nutritionnel"""

        bar_frame = ctk.CTkFrame(parent)
        bar_frame.pack(fill="x", padx=10, pady=5)

        # Label avec nom et valeurs
        label_text = f"{name}: {current} / {target} {unit}"
        ctk.CTkLabel(bar_frame, text=label_text, font=ctk.CTkFont(size=12)).pack(
            anchor="w", padx=10, pady=(5, 0)
        )

        # Barre de progression
        progress = min(1.0, current / target if target > 0 else 0)

        progress_bar = ctk.CTkProgressBar(bar_frame, width=200, height=8)
        progress_bar.set(progress)
        progress_bar.pack(fill="x", padx=10, pady=(2, 8))

    def _load_smart_suggestions(self):
        """Charge les suggestions intelligentes basées sur le profil"""

        # Nettoyage du frame existant
        for widget in self.suggestions_content.winfo_children():
            widget.destroy()

        if not self.current_profile:
            ctk.CTkLabel(
                self.suggestions_content,
                text="Configurez votre profil pour\ndes suggestions personnalisées",
                justify="center",
            ).pack(pady=10)
            return

        # Obtention des top aliments selon l'objectif
        try:
            if "perte" in self.current_profile.objectif_principal.lower():
                # Aliments faibles en calories, riches en fibres
                suggestions = self.food_search.obtenir_top_aliments(
                    critere="fibres_100g",
                    limit=5,
                    exclude_categories=["Sucres et produits sucrés"],
                )
                suggestion_title = "🌿 Parfait pour la perte de poids"

            elif "muscle" in self.current_profile.objectif_principal.lower():
                # Aliments riches en protéines
                suggestions = self.food_search.obtenir_top_aliments(
                    critere="proteines_100g", limit=5
                )
                suggestion_title = "💪 Excellent pour la prise de muscle"

            else:
                # Aliments équilibrés avec bon score healthy
                suggestions = self.food_search.obtenir_top_aliments(
                    critere="indice_healthy", limit=5
                )
                suggestion_title = "⭐ Recommandés pour vous"

            # Affichage du titre
            ctk.CTkLabel(
                self.suggestions_content,
                text=suggestion_title,
                font=ctk.CTkFont(size=12, weight="bold"),
            ).pack(anchor="w", padx=5, pady=(5, 10))

            # Affichage des suggestions
            for aliment in suggestions[:3]:  # Top 3 seulement
                self._create_suggestion_item(aliment)

        except Exception as e:
            print(f"Erreur lors du chargement des suggestions: {e}")
            ctk.CTkLabel(
                self.suggestions_content, text="Suggestions indisponibles"
            ).pack(pady=10)

    def _create_suggestion_item(self, aliment: Aliment):
        """Crée un élément de suggestion"""

        item_frame = ctk.CTkFrame(
            self.suggestions_content, fg_color=("gray85", "gray20")
        )
        item_frame.pack(fill="x", padx=5, pady=2)

        # Nom de l'aliment
        name_label = ctk.CTkLabel(
            item_frame,
            text=aliment.nom[:20] + ("..." if len(aliment.nom) > 20 else ""),
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        name_label.pack(anchor="w", padx=8, pady=(5, 0))

        # Informations nutritionnelles clés
        info_text = f"{aliment.kcal_100g:.0f} kcal | {aliment.proteines_100g:.1f}g prot"
        ctk.CTkLabel(
            item_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray50"),
        ).pack(anchor="w", padx=8, pady=(0, 5))

        # Clic pour ajouter
        item_frame.bind("<Button-1>", lambda e: self._add_suggested_food(aliment))
        name_label.bind("<Button-1>", lambda e: self._add_suggested_food(aliment))

    def _on_search_change(self, *args):
        """Déclenché lors de la modification de la recherche"""

        query = self.search_var.get().strip()

        if len(query) < 2:
            self._clear_search_results()
            return

        # Recherche avec délai pour éviter trop de requêtes
        self.after_cancel(getattr(self, "_search_job", None))
        self._search_job = self.after(300, lambda: self._perform_search(query))

    def _perform_search(self, query: str):
        """Effectue la recherche d'aliments"""

        try:
            # Construction du filtre basé sur l'UI
            filtre = FiltreRecherche(
                nom=query,
                categories=None
                if self.category_var.get() == "Toutes"
                else [self.category_var.get()],
                limit=10,
            )

            # Ajustement du filtre selon l'objectif sélectionné
            objective = self.objective_var.get()
            if objective == "Riche en protéines":
                filtre.proteines_min = 15.0
            elif objective == "Faible en calories":
                filtre.kcal_max = 150.0
            elif objective == "Riche en fibres":
                filtre.fibres_min = 5.0

            # Application du filtre de compatibilité régime
            if self.regime_compatible.get() and self.current_profile:
                filtre.regimes_compatibles = self.current_profile.regimes_compatibles
                filtre.aliments_exclus = self.current_profile.aliments_exclus

            # Exécution de la recherche
            if self.current_profile:
                resultat = self.food_search.recherche_pour_profil(query, self.client_id)
            else:
                resultat = self.food_search.recherche_avancee(filtre)

            self._display_search_results(resultat.aliments)

        except Exception as e:
            print(f"Erreur de recherche: {e}")
            self._clear_search_results()

    def _display_search_results(self, aliments: List[Aliment]):
        """Affiche les résultats de recherche"""

        # Nettoyage des résultats existants
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not aliments:
            ctk.CTkLabel(
                self.results_frame,
                text="Aucun résultat trouvé.\nEssayez d'élargir vos critères.",
                justify="center",
                text_color=("gray60", "gray50"),
            ).pack(pady=20)
            return

        # Affichage des résultats
        for aliment in aliments:
            self._create_search_result_item(aliment)

    def _create_search_result_item(self, aliment: Aliment):
        """Crée un élément de résultat de recherche"""

        item_frame = ctk.CTkFrame(self.results_frame)
        item_frame.pack(fill="x", padx=5, pady=3)

        # Configuration du layout
        item_frame.grid_columnconfigure(0, weight=1)

        # Nom et catégorie
        name_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        name_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 2))

        ctk.CTkLabel(
            name_frame, text=aliment.nom, font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w")

        if aliment.categorie:
            ctk.CTkLabel(
                name_frame,
                text=aliment.categorie,
                font=ctk.CTkFont(size=10),
                text_color=("gray60", "gray50"),
            ).pack(anchor="w")

        # Informations nutritionnelles
        nutrition_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        nutrition_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 2))

        nutrition_text = f"🔥 {aliment.kcal_100g:.0f} kcal | 🥩 {aliment.proteines_100g:.1f}g | 🌾 {aliment.glucides_100g:.1f}g | 🧈 {aliment.lipides_100g:.1f}g"
        ctk.CTkLabel(
            nutrition_frame,
            text=nutrition_text,
            font=ctk.CTkFont(size=9),
            text_color=("gray70", "gray40"),
        ).pack(anchor="w")

        # Score de qualité nutritionnelle
        if aliment.indice_healthy:
            score_text = f"⭐ Score santé: {aliment.indice_healthy}/10"
            ctk.CTkLabel(
                nutrition_frame,
                text=score_text,
                font=ctk.CTkFont(size=9),
                text_color=("green", "light_green"),
            ).pack(anchor="w")

        # Bouton d'ajout
        add_btn = ctk.CTkButton(
            item_frame,
            text="+ Ajouter",
            width=80,
            height=28,
            font=ctk.CTkFont(size=10),
            command=lambda: self._add_food_to_meal(aliment),
        )
        add_btn.grid(row=0, rowspan=2, column=1, padx=(5, 10), pady=8)

    def _clear_search_results(self):
        """Vide les résultats de recherche"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def _on_filter_change(self, *args):
        """Déclenché lors du changement de filtres"""
        # Relancer la recherche si il y a une query active
        if len(self.search_var.get().strip()) >= 2:
            self._perform_search(self.search_var.get().strip())

    # Actions principales

    def _generate_automatic_plan(self):
        """Génère automatiquement un plan alimentaire"""

        if not self.current_profile:
            messagebox.showwarning(
                "Profil requis",
                "Veuillez d'abord configurer votre profil nutritionnel.",
            )
            self._open_profile_config()
            return

        try:
            # Génération du plan
            plan = self.meal_generator.generer_plan_automatique(
                client_id=self.client_id,
                duree_jours=1,  # Plan d'une journée pour commencer
                nom_plan=f"Plan auto {datetime.now().strftime('%d/%m')}",
            )

            self.current_plan = plan
            self._display_meal_plan(plan)

            messagebox.showinfo(
                "Succès",
                "Plan alimentaire généré automatiquement !\nPersonnalisez-le en ajoutant/supprimant des aliments.",
            )

        except Exception as e:
            print(f"Erreur génération plan: {e}")
            messagebox.showerror("Erreur", f"Impossible de générer le plan: {e}")

    def _open_profile_config(self):
        """Ouvre la configuration du profil nutritionnel"""

        # TODO: Créer un modal de configuration de profil complet
        messagebox.showinfo(
            "Configuration du profil",
            "Interface de configuration du profil à implémenter.\nPour l'instant, utilisez la génération automatique.",
        )

    def _add_food_to_meal(self, aliment: Aliment):
        """Ajoute un aliment au repas actuel"""

        if not self.current_plan or not self.current_plan.repas:
            messagebox.showwarning(
                "Plan requis", "Veuillez d'abord générer un plan alimentaire."
            )
            return

        # TODO: Ouvrir un modal pour choisir la quantité et la portion
        # Pour l'instant, ajout direct avec quantité par défaut

        try:
            # Ajout à l'item du premier repas (ou repas sélectionné)
            repas = self.current_plan.repas[self.selected_meal_index]

            # Création d'un nouvel item (structure simplifiée pour la démo)
            from models.plan_alimentaire import RepasItem

            nouvel_item = RepasItem(
                id=len(repas.items) + 1,  # ID temporaire
                repas_id=repas.id,
                aliment_id=aliment.id,
                portion_id=1,  # Portion par défaut
                quantite=100.0,  # Quantité par défaut
            )

            # Ajout de propriétés d'affichage
            nouvel_item.nom = aliment.nom

            repas.items.append(nouvel_item)

            # Mise à jour de l'affichage
            self._display_meal_plan(self.current_plan)

            messagebox.showinfo("Succès", f"{aliment.nom} ajouté au repas !")

        except Exception as e:
            print(f"Erreur ajout aliment: {e}")
            messagebox.showerror("Erreur", f"Impossible d'ajouter l'aliment: {e}")

    def _add_suggested_food(self, aliment: Aliment):
        """Ajoute un aliment suggéré"""
        self._add_food_to_meal(aliment)

    def _display_meal_plan(self, plan):
        """Affiche le plan alimentaire généré"""
        messagebox.showinfo("Info", "Affichage du plan alimentaire à implémenter")

    def _analyze_current_plan(self):
        """Analyse le plan alimentaire actuel"""
        messagebox.showinfo("Info", "Analyse du plan à implémenter")

    def _optimize_current_plan(self):
        """Optimise le plan alimentaire actuel"""
        messagebox.showinfo("Info", "Optimisation du plan à implémenter")

    def _export_plan_pdf(self):
        """Exporte le plan en PDF"""
        messagebox.showinfo("Info", "Export PDF à implémenter")


if __name__ == "__main__":
    # Test de l'interface
    app = ctk.CTk()
    app.title("Test - Nutrition Moderne")
    app.geometry("1400x900")

    page = ModernNutritionPage(app, client_id=1)
    page.pack(fill="both", expand=True)

    app.mainloop()
