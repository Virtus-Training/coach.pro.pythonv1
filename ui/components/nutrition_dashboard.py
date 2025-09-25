"""
Advanced Nutrition Dashboard Component
=====================================

Premium nutrition management interface with:
- Quick nutrition sheet generation
- Visual nutrition analytics
- Client nutrition history
- Interactive charts and graphs
- Professional coach dashboard
"""

from typing import Optional, List, Dict, Any, Callable
import customtkinter as ctk
import tkinter as tk
from datetime import datetime, date
import logging

from controllers.advanced_nutrition_controller import AdvancedNutritionController
from ui.components.design_system.cards import Card
from ui.components.design_system.typography import PageTitle, CardTitle
from ui.components.design_system import PrimaryButton, SecondaryButton
from services.advanced_nutrition_calculator import NutritionResults, ActivityLevel, NutritionGoal
from models.client import Client
from models.fiche_nutrition import FicheNutrition

logger = logging.getLogger(__name__)


class NutritionStatsCard(Card):
    """Card displaying nutrition statistics"""

    def __init__(self, parent, title: str, value: str, subtitle: str = "", icon: str = "📊"):
        super().__init__(parent)
        self.configure(fg_color=self._get_theme_color("surface"))

        # Icon and title
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(15, 5), padx=15)

        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left")

        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=(10, 0))

        # Value
        value_label = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self._get_theme_color("primary")
        )
        value_label.pack(pady=5)

        # Subtitle
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                self,
                text=subtitle,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            subtitle_label.pack(pady=(0, 15))

    def _get_theme_color(self, color_name: str) -> str:
        """Get theme color"""
        colors = ctk.ThemeManager.theme["color"]
        color_map = {
            "primary": colors.get("primary", "#22D3EE"),
            "surface": colors.get("surface", "#F8FAFC"),
            "text": colors.get("text", "#1F2937")
        }
        return color_map.get(color_name, "#000000")


class NutritionHistoryList(ctk.CTkScrollableFrame):
    """Scrollable list of nutrition history"""

    def __init__(
        self,
        parent,
        on_view_callback: Optional[Callable] = None,
        on_regenerate_callback: Optional[Callable] = None,
        on_delete_callback: Optional[Callable] = None
    ):
        super().__init__(parent, fg_color="transparent")
        self.on_view = on_view_callback
        self.on_regenerate = on_regenerate_callback
        self.on_delete = on_delete_callback
        self.history_items = []

    def update_history(self, history: List[FicheNutrition]):
        """Update history list"""
        # Clear existing items
        for item in self.history_items:
            item.destroy()
        self.history_items.clear()

        # Add new items
        for fiche in history:
            item = self._create_history_item(fiche)
            item.pack(fill="x", pady=5, padx=10)
            self.history_items.append(item)

    def _create_history_item(self, fiche: FicheNutrition) -> ctk.CTkFrame:
        """Create history item widget"""
        item_frame = Card(self)
        item_frame.configure(fg_color=ctk.ThemeManager.theme["color"]["surface_light"])

        # Header with date and objective
        header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=10, padx=15)

        # Date
        date_text = fiche.date_creation or "Date inconnue"
        try:
            if fiche.date_creation:
                date_obj = datetime.strptime(fiche.date_creation, "%Y-%m-%d %H:%M:%S")
                date_text = date_obj.strftime("%d/%m/%Y")
        except Exception:
            pass

        date_label = ctk.CTkLabel(
            header_frame,
            text=f"📅 {date_text}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        date_label.pack(side="left")

        # Objective
        objective_text = fiche.objectif or "Objectif non défini"
        objective_label = ctk.CTkLabel(
            header_frame,
            text=f"🎯 {objective_text}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary"]
        )
        objective_label.pack(side="right")

        # Main metrics
        metrics_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=5, padx=15)

        # Calories
        calories_label = ctk.CTkLabel(
            metrics_frame,
            text=f"🔥 {fiche.objectif_kcal} kcal/jour",
            font=ctk.CTkFont(size=12)
        )
        calories_label.pack(side="left")

        # Weight
        weight_label = ctk.CTkLabel(
            metrics_frame,
            text=f"⚖️ {fiche.poids_kg_mesure} kg",
            font=ctk.CTkFont(size=12)
        )
        weight_label.pack(side="left", padx=(20, 0))

        # Macros summary
        macros_text = f"🥩{fiche.proteines_g}g | 🍞{fiche.glucides_g}g | 🥑{fiche.lipides_g}g"
        macros_label = ctk.CTkLabel(
            metrics_frame,
            text=macros_text,
            font=ctk.CTkFont(size=12)
        )
        macros_label.pack(side="right")

        # Action buttons
        actions_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=5, padx=15)

        if self.on_view:
            view_btn = SecondaryButton(
                actions_frame,
                text="👁️ Voir",
                command=lambda: self.on_view(fiche)
            )
            view_btn.pack(side="left", padx=(0, 5))

        if self.on_regenerate:
            regen_btn = PrimaryButton(
                actions_frame,
                text="📄 PDF",
                command=lambda: self.on_regenerate(fiche.id)
            )
            regen_btn.pack(side="left", padx=5)

        if self.on_delete:
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="🗑️",
                width=30,
                fg_color="#EF4444",
                hover_color="#DC2626",
                command=lambda: self.on_delete(fiche.id)
            )
            delete_btn.pack(side="right")

        return item_frame


class QuickNutritionCalculator(Card):
    """Quick nutrition calculation widget"""

    def __init__(self, parent, on_calculate_callback: Optional[Callable] = None):
        super().__init__(parent)
        self.on_calculate = on_calculate_callback
        self.setup_ui()

    def setup_ui(self):
        # Title
        title = ctk.CTkLabel(
            self,
            text="⚡ Calcul Rapide",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(15, 10), padx=15)

        # Input frame
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", pady=10, padx=15)

        # Age, Sexe, Poids, Taille in 2x2 grid
        grid_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        grid_frame.pack(fill="x")

        # Age
        age_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        age_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")
        ctk.CTkLabel(age_frame, text="Âge", font=ctk.CTkFont(size=12)).pack()
        self.age_entry = ctk.CTkEntry(age_frame, width=80, placeholder_text="30")
        self.age_entry.pack()

        # Sexe
        sexe_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        sexe_frame.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(sexe_frame, text="Sexe", font=ctk.CTkFont(size=12)).pack()
        self.sexe_var = tk.StringVar(value="Homme")
        sexe_option = ctk.CTkOptionMenu(sexe_frame, variable=self.sexe_var, values=["Homme", "Femme"], width=80)
        sexe_option.pack()

        # Poids
        poids_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        poids_frame.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="ew")
        ctk.CTkLabel(poids_frame, text="Poids (kg)", font=ctk.CTkFont(size=12)).pack()
        self.poids_entry = ctk.CTkEntry(poids_frame, width=80, placeholder_text="70")
        self.poids_entry.pack()

        # Taille
        taille_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        taille_frame.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(taille_frame, text="Taille (cm)", font=ctk.CTkFont(size=12)).pack()
        self.taille_entry = ctk.CTkEntry(taille_frame, width=80, placeholder_text="175")
        self.taille_entry.pack()

        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)

        # Activity and Goal
        activity_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        activity_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(activity_frame, text="Niveau d'activité", font=ctk.CTkFont(size=12)).pack()
        self.activity_var = tk.StringVar(value="Modérément actif")
        activity_values = [level.label for level in ActivityLevel]
        self.activity_option = ctk.CTkOptionMenu(activity_frame, variable=self.activity_var, values=activity_values)
        self.activity_option.pack(fill="x")

        goal_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        goal_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(goal_frame, text="Objectif", font=ctk.CTkFont(size=12)).pack()
        self.goal_var = tk.StringVar(value="Maintenance")
        goal_values = [goal.label for goal in NutritionGoal]
        self.goal_option = ctk.CTkOptionMenu(goal_frame, variable=self.goal_var, values=goal_values)
        self.goal_option.pack(fill="x")

        # Calculate button
        calc_btn = PrimaryButton(
            self,
            text="🧮 Calculer",
            command=self._calculate
        )
        calc_btn.pack(pady=15, padx=15)

        # Results area
        self.results_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.results_frame.pack(fill="x", pady=10, padx=15)

        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Saisissez les données et cliquez sur Calculer",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        self.results_label.pack()

    def _calculate(self):
        """Perform quick calculation"""
        try:
            # Validate inputs
            age = int(self.age_entry.get() or 30)
            poids = float(self.poids_entry.get() or 70)
            taille = float(self.taille_entry.get() or 175)

            # Find activity level
            activity_level = ActivityLevel.SEDENTARY
            for level in ActivityLevel:
                if level.label == self.activity_var.get():
                    activity_level = level
                    break

            # Find goal
            goal = NutritionGoal.MAINTENANCE
            for g in NutritionGoal:
                if g.label == self.goal_var.get():
                    goal = g
                    break

            # Create data dict
            client_data = {
                'age': age,
                'sexe': self.sexe_var.get(),
                'poids_kg': poids,
                'taille_cm': taille,
                'niveau_activite': activity_level,
                'objectif': goal
            }

            # Call callback if provided
            if self.on_calculate:
                results = self.on_calculate(client_data)
                if results:
                    self._display_results(results)
                else:
                    self.results_label.configure(text="Erreur lors du calcul")

        except ValueError:
            self.results_label.configure(text="❌ Veuillez saisir des valeurs numériques valides")
        except Exception as e:
            self.results_label.configure(text=f"❌ Erreur: {str(e)}")

    def _display_results(self, results: NutritionResults):
        """Display calculation results"""
        results_text = f"""✅ Résultats du calcul:

🔥 Objectif calories: {results.objectif_kcal} kcal/jour
📊 BMR: {results.bmr_kcal} kcal | TDEE: {results.tdee_kcal} kcal

🥩 Protéines: {results.proteines_g}g ({results.proteines_pct}%)
🍞 Glucides: {results.glucides_g}g ({results.glucides_pct}%)
🥑 Lipides: {results.lipides_g}g ({results.lipides_pct}%)

⚖️ Balance: {results.deficit_surplus:+d} kcal/jour"""

        self.results_label.configure(text=results_text)


class AdvancedNutritionDashboard(ctk.CTkScrollableFrame):
    """
    Advanced nutrition dashboard with complete nutrition management.

    Features:
    - Quick nutrition calculations
    - Professional nutrition sheet generation
    - Client nutrition history
    - Visual analytics and charts
    - Export and management tools
    """

    def __init__(
        self,
        parent,
        nutrition_controller: AdvancedNutritionController,
        client_service=None
    ):
        super().__init__(parent, fg_color="transparent")
        self.nutrition_controller = nutrition_controller
        self.client_service = client_service
        self.current_client = None

        self.setup_ui()

    def setup_ui(self):
        """Setup dashboard UI"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20), padx=20)

        title = ctk.CTkLabel(
            header_frame,
            text="🥗 Nutrition Avancée",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")

        # New nutrition sheet button
        new_sheet_btn = PrimaryButton(
            header_frame,
            text="➕ Nouvelle Fiche",
            command=self._create_new_nutrition_sheet
        )
        new_sheet_btn.pack(side="right")

        # Main content in grid layout
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20)

        # Left column - Quick calculator and stats
        left_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Quick calculator
        self.quick_calc = QuickNutritionCalculator(
            left_column,
            on_calculate_callback=self._handle_quick_calculation
        )
        self.quick_calc.pack(fill="x", pady=(0, 20))

        # Stats cards
        stats_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))

        # Create stats cards
        self.stats_cards = {}
        stats_data = [
            ("total_sheets", "Fiches Créées", "0", "📊"),
            ("avg_calories", "Moy. Calories", "0 kcal", "🔥"),
            ("most_common_goal", "Objectif Fréquent", "N/A", "🎯"),
        ]

        for i, (key, title, value, icon) in enumerate(stats_data):
            card = NutritionStatsCard(stats_frame, title, value, "", icon)
            card.pack(fill="x", pady=5)
            self.stats_cards[key] = card

        # Right column - History and management
        right_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Client selector
        client_frame = ctk.CTkFrame(right_column, fg_color="transparent")
        client_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(client_frame, text="👤 Client:", font=ctk.CTkFont(size=14)).pack(side="left")

        self.client_var = tk.StringVar()
        self.client_selector = ctk.CTkComboBox(
            client_frame,
            variable=self.client_var,
            command=self._on_client_selected,
            state="readonly"
        )
        self.client_selector.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # History section
        history_header = ctk.CTkFrame(right_column, fg_color="transparent")
        history_header.pack(fill="x", pady=(0, 10))

        history_title = ctk.CTkLabel(
            history_header,
            text="📋 Historique Nutrition",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        history_title.pack(side="left")

        refresh_btn = SecondaryButton(
            history_header,
            text="🔄",
            command=self._refresh_history
        )
        refresh_btn.pack(side="right")

        # History list
        self.history_list = NutritionHistoryList(
            right_column,
            on_view_callback=self._view_nutrition_sheet,
            on_regenerate_callback=self._regenerate_pdf,
            on_delete_callback=self._delete_nutrition_sheet
        )
        self.history_list.pack(fill="both", expand=True)

        # Load initial data
        self._load_clients()
        self._update_stats()

    def _load_clients(self):
        """Load client list"""
        if not self.client_service:
            return

        try:
            clients = self.client_service.get_all_clients()
            client_values = [f"{client.prenom} {client.nom}" for client in clients]
            self.client_selector.configure(values=client_values)

            # Store client mapping
            self.client_mapping = {
                f"{client.prenom} {client.nom}": client
                for client in clients
            }

        except Exception as e:
            logger.error(f"Erreur chargement clients: {e}")

    def _on_client_selected(self, value):
        """Handle client selection"""
        if value in self.client_mapping:
            self.current_client = self.client_mapping[value]
            self._refresh_history()

    def _create_new_nutrition_sheet(self):
        """Create new nutrition sheet"""
        client_id = self.current_client.id if self.current_client else None
        self.nutrition_controller.open_nutrition_form_for_client(client_id)

    def _handle_quick_calculation(self, client_data: Dict[str, Any]) -> Optional[NutritionResults]:
        """Handle quick calculation"""
        return self.nutrition_controller.quick_nutrition_calculation(client_data)

    def _refresh_history(self):
        """Refresh nutrition history"""
        if not self.current_client:
            self.history_list.update_history([])
            return

        try:
            history = self.nutrition_controller.get_nutrition_history_for_client(
                self.current_client.id
            )
            self.history_list.update_history(history)
        except Exception as e:
            logger.error(f"Erreur refresh historique: {e}")

    def _view_nutrition_sheet(self, fiche: FicheNutrition):
        """View nutrition sheet details"""
        # For now, just show info dialog
        import tkinter.messagebox as messagebox

        info_text = f"""Fiche Nutrition

Date: {fiche.date_creation or 'N/A'}
Poids: {fiche.poids_kg_mesure} kg
Objectif: {fiche.objectif}

Calories:
- Maintenance: {fiche.maintenance_kcal} kcal
- Objectif: {fiche.objectif_kcal} kcal

Macronutriments:
- Protéines: {fiche.proteines_g}g
- Glucides: {fiche.glucides_g}g
- Lipides: {fiche.lipides_g}g

Protéines cible: {fiche.proteines_cible_g_par_kg}g/kg
Ratio glucides: {fiche.ratio_glucides_lipides_cible}%"""

        messagebox.showinfo("Détails Fiche Nutrition", info_text)

    def _regenerate_pdf(self, fiche_id: int):
        """Regenerate PDF for nutrition sheet"""
        self.nutrition_controller.regenerate_pdf_for_existing_fiche(fiche_id)

    def _delete_nutrition_sheet(self, fiche_id: int):
        """Delete nutrition sheet"""
        if self.nutrition_controller.delete_nutrition_sheet(fiche_id):
            self._refresh_history()
            self._update_stats()

    def _update_stats(self):
        """Update statistics cards"""
        try:
            # This would normally come from a service/repository
            # For now, just placeholder updates
            self.stats_cards["total_sheets"].children[2].configure(text="12")
            self.stats_cards["avg_calories"].children[2].configure(text="2,200 kcal")
            self.stats_cards["most_common_goal"].children[2].configure(text="Maintenance")
        except Exception as e:
            logger.error(f"Erreur mise à jour stats: {e}")

    def set_current_client(self, client: Client):
        """Set current client"""
        self.current_client = client
        if hasattr(client, 'prenom') and hasattr(client, 'nom'):
            client_name = f"{client.prenom} {client.nom}"
            self.client_var.set(client_name)
            self._refresh_history()