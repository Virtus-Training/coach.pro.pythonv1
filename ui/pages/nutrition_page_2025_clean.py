"""🍽️ Interface Nutrition 2025 - Version Simplifiée et Claire

Interface nutrition complètement redessinée pour être :
- ✅ Simple à comprendre
- ✅ Rapide à utiliser
- ✅ Focus sur l'essentiel
- ✅ Workflow intuitif
"""

import customtkinter as ctk
from datetime import datetime
from typing import Optional, Dict, Callable

from ui.components.nutrition_2025 import (
    AnimatedCard, ProgressBar, ScoreIndicator,
    AdvancedFoodLogger
)


class NutritionPageClean(ctk.CTkFrame):
    """🚀 Interface Nutrition 2025 - Version Simplifiée"""

    def __init__(self, parent, controller, client_id: Optional[int] = None):
        super().__init__(parent)

        self.controller = controller
        self.client_id = client_id

        # Chargement des données
        self._load_data()

        # Construction de l'interface simplifiée
        self._create_clean_interface()

    def _load_data(self) -> None:
        """📊 Chargement des données essentielles"""
        try:
            self.data = self.controller.get_nutrition_page_data(self.client_id)
            self.client = self.data.client if self.data else None
            self.fiche = self.data.fiche if self.data else None
            self.plan = self.data.plan if self.data else None
        except Exception:
            self.data = self.client = self.fiche = self.plan = None

    def _create_clean_interface(self) -> None:
        """🎨 Interface simple et claire"""
        # Configuration grille principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Actions
        self.grid_rowconfigure(2, weight=1)  # Contenu

        # 1. Header simple
        self._create_simple_header()

        # 2. Action principale
        self._create_main_action()

        # 3. Vue d'ensemble en 2 colonnes
        self._create_overview_section()

    def _create_simple_header(self) -> None:
        """📱 Header clair et informatif"""
        header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=8)
        header.grid_propagate(False)

        # Titre principal
        title = ctk.CTkLabel(
            header,
            text="🍽️ Nutrition",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left", pady=16)

        # Score du jour - TRÈS visible
        score = self._calculate_score()
        score_frame = ctk.CTkFrame(header, corner_radius=25)
        score_frame.pack(side="right", pady=8)

        score_big = ctk.CTkLabel(
            score_frame,
            text=f"{score}/100",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self._get_score_color(score)
        )
        score_big.pack(padx=20, pady=8)

        score_text = ctk.CTkLabel(
            header,
            text="Score du jour",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray40")
        )
        score_text.pack(side="right", padx=(0, 12))

    def _create_main_action(self) -> None:
        """⚡ Action principale bien visible"""
        action_frame = ctk.CTkFrame(self, fg_color="transparent", height=70)
        action_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=4)
        action_frame.grid_propagate(False)

        # Bouton principal centré et grand
        main_btn = ctk.CTkButton(
            action_frame,
            text="+ Ajouter un Aliment",
            command=self._add_food,
            width=250,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=22
        )
        main_btn.pack(expand=True, pady=12)

    def _create_overview_section(self) -> None:
        """📊 Vue d'ensemble en 2 parties claires"""
        main_content = ctk.CTkFrame(self, fg_color="transparent")
        main_content.grid(row=2, column=0, sticky="nsew", padx=12, pady=(4, 12))

        # 2 colonnes égales
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)
        main_content.grid_rowconfigure(0, weight=1)

        # Gauche: Progression du jour
        self._create_daily_progress(main_content)

        # Droite: Ajout rapide d'aliments
        self._create_food_logger(main_content)

    def _create_daily_progress(self, parent) -> None:
        """📈 Progression quotidienne simple"""
        progress_card = AnimatedCard(parent, title="📈 Progression du Jour")
        progress_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        content = progress_card.content_frame

        # Macros essentielles avec barres claires
        self._create_macro_progress(content, "🔥 Calories",
                                   self._get_current_calories(), self._get_target_calories(), "kcal")

        self._create_macro_progress(content, "💪 Protéines",
                                   self._get_current_protein(), self._get_target_protein(), "g")

        self._create_macro_progress(content, "🌾 Glucides",
                                   self._get_current_carbs(), self._get_target_carbs(), "g")

        # Résumé simple
        meals_today = self._count_meals_today()
        summary = ctk.CTkLabel(
            content,
            text=f"🍽️ {meals_today} repas aujourd'hui",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray40")
        )
        summary.pack(pady=(16, 8))

    def _create_macro_progress(self, parent, label: str, current: float, target: float, unit: str) -> None:
        """📊 Barre de progression macro simple et claire"""
        container = ctk.CTkFrame(parent, fg_color="transparent", height=65)
        container.pack(fill="x", pady=6, padx=16)
        container.pack_propagate(False)

        # Header avec label et valeurs
        header = ctk.CTkFrame(container, fg_color="transparent")
        header.pack(fill="x", pady=(8, 4))

        ctk.CTkLabel(
            header,
            text=label,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left")

        percentage = (current / target * 100) if target > 0 else 0
        values_text = f"{current:.0f}/{target:.0f} {unit} ({percentage:.0f}%)"

        ctk.CTkLabel(
            header,
            text=values_text,
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray40")
        ).pack(side="right")

        # Barre de progression
        progress = ProgressBar(container, width=250, height=16,
                              progress=current, target=target, show_percentage=False)
        progress.pack(fill="x", pady=4)

    def _create_food_logger(self, parent) -> None:
        """🍽️ Zone d'ajout d'aliments"""
        food_card = AnimatedCard(parent, title="🔍 Rechercher des Aliments")
        food_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        # Logger intégré
        self.food_logger = AdvancedFoodLogger(
            food_card.content_frame,
            self.controller,
            client_id=self.client_id,
            on_food_added=self._on_food_added,
            compact_mode=True
        )
        self.food_logger.pack(fill="both", expand=True, padx=8, pady=8)

    # === MÉTHODES UTILITAIRES SIMPLIFIÉES ===

    def _calculate_score(self) -> int:
        """🧮 Score nutritionnel simplifié"""
        if not self.plan or not self.fiche:
            return 0

        score = 0

        # Calories (50 points)
        if self.fiche.objectif_kcal > 0:
            ratio = self.plan.totals_kcal / self.fiche.objectif_kcal
            if 0.9 <= ratio <= 1.1:
                score += 50
            elif 0.8 <= ratio <= 1.2:
                score += 30

        # Protéines (30 points)
        if self.fiche.proteines_g > 0:
            ratio = self.plan.totals_proteines / self.fiche.proteines_g
            if ratio >= 0.8:
                score += 30
            elif ratio >= 0.6:
                score += 15

        # Nombre de repas (20 points)
        meals = len([r for r in self.plan.repas if r.items])
        if meals >= 3:
            score += 20
        elif meals >= 2:
            score += 10

        return min(score, 100)

    def _get_score_color(self, score: int) -> str:
        """🎨 Couleur selon le score"""
        if score >= 80:
            return "#22C55E"  # Vert
        elif score >= 60:
            return "#F59E0B"  # Orange
        else:
            return "#EF4444"  # Rouge

    def _get_current_calories(self) -> float:
        return self.plan.totals_kcal if self.plan else 0

    def _get_target_calories(self) -> float:
        return self.fiche.objectif_kcal if self.fiche else 2000

    def _get_current_protein(self) -> float:
        return self.plan.totals_proteines if self.plan else 0

    def _get_target_protein(self) -> float:
        return self.fiche.proteines_g if self.fiche else 150

    def _get_current_carbs(self) -> float:
        return self.plan.totals_glucides if self.plan else 0

    def _get_target_carbs(self) -> float:
        return self.fiche.glucides_g if self.fiche else 200

    def _count_meals_today(self) -> int:
        if not self.plan:
            return 0
        return len([r for r in self.plan.repas if r.items])

    # === ACTIONS ===

    def _add_food(self) -> None:
        """🍽️ Ajouter un aliment - focus sur la recherche"""
        # Faire défiler vers la zone de recherche ou l'ouvrir
        if hasattr(self.food_logger, 'search_var'):
            # Focus sur le champ de recherche
            for widget in self.food_logger.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.focus_set()
                    break

    def _on_food_added(self, food_data: Dict) -> None:
        """📝 Callback ajout d'aliment"""
        try:
            # Traitement de l'ajout
            self.controller.add_food_to_plan(self.client_id, food_data)

            # Rafraîchissement
            self._load_data()
            self._refresh_display()

            # Message de succès discret
            print(f"✅ {food_data['food'].nom} ajouté avec succès")

        except Exception as e:
            print(f"❌ Erreur ajout aliment: {e}")

    def _refresh_display(self) -> None:
        """🔄 Rafraîchissement visuel simple"""
        # Recalculer le score
        score = self._calculate_score()

        # Trouver et mettre à jour les éléments visuels
        for child in self.winfo_children():
            if hasattr(child, 'winfo_children'):
                for subchild in child.winfo_children():
                    # Mise à jour du score si trouvé
                    if hasattr(subchild, 'configure') and 'Score' in str(subchild):
                        try:
                            subchild.configure(text=f"{score}/100")
                        except:
                            pass

    # === INTERFACE PUBLIQUE ===

    def refresh(self) -> None:
        """🔄 Rafraîchissement complet"""
        self._load_data()
        self._refresh_display()

    def get_current_score(self) -> int:
        """📊 Score actuel"""
        return self._calculate_score()

    def focus_food_search(self) -> None:
        """🔍 Focus sur la recherche d'aliments"""
        self._add_food()