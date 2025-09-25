"""
Advanced Nutrition Form Modal with Progressive Disclosure
========================================================

Multi-step nutrition form with:
- 5-step progressive disclosure UX
- Real-time calculation preview
- Smart validation with contextual feedback
- Professional UX patterns (Typeform-inspired)
- Responsive design with smooth animations
"""

from typing import Any, Callable, Dict, List, Optional, Tuple
import tkinter as tk
import customtkinter as ctk
from dataclasses import asdict

from services.advanced_nutrition_calculator import (
    AdvancedNutritionCalculator,
    PersonalData,
    MacroTargets,
    ActivityLevel,
    NutritionGoal,
    BMRMethod,
    NutritionResults
)
from ui.components.design_system import PrimaryButton, SecondaryButton
from utils.ui_helpers import bring_to_front


class ProgressIndicator(ctk.CTkFrame):
    """Visual progress indicator for multi-step forms"""

    def __init__(self, parent, total_steps: int = 5):
        super().__init__(parent, fg_color="transparent")
        self.total_steps = total_steps
        self.current_step = 1

        # Progress bar container
        self.progress_frame = ctk.CTkFrame(self, height=8, fg_color="#E5E7EB")
        self.progress_frame.pack(fill="x", padx=20, pady=(10, 20))

        # Progress fill
        self.progress_fill = ctk.CTkFrame(self.progress_frame, height=8, fg_color="#22D3EE")
        self.progress_fill.place(x=0, y=0, relheight=1.0)

        # Step indicators
        self.step_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.step_frame.pack(fill="x", padx=20)

        self.step_labels = []
        for i in range(total_steps):
            label = ctk.CTkLabel(
                self.step_frame,
                text=f"{i+1}",
                width=30,
                height=30,
                corner_radius=15,
                fg_color="#E5E7EB",
                text_color="#9CA3AF"
            )
            label.pack(side="left", padx=5)
            self.step_labels.append(label)

    def update_progress(self, step: int):
        """Update progress indicator"""
        self.current_step = step
        progress_width = (step / self.total_steps)

        # Animate progress bar
        self.progress_fill.place(x=0, y=0, relwidth=progress_width, relheight=1.0)

        # Update step indicators
        for i, label in enumerate(self.step_labels):
            if i < step:
                # Completed steps
                label.configure(fg_color="#22D3EE", text_color="white", text="✓")
            elif i == step - 1:
                # Current step
                label.configure(fg_color="#22D3EE", text_color="white", text=f"{i+1}")
            else:
                # Future steps
                label.configure(fg_color="#E5E7EB", text_color="#9CA3AF", text=f"{i+1}")


class ValidationMixin:
    """Mixin for real-time validation"""

    @staticmethod
    def validate_age(age: str) -> Tuple[bool, str]:
        try:
            age_int = int(age)
            if 16 <= age_int <= 80:
                return True, ""
            return False, "L'âge doit être entre 16 et 80 ans"
        except ValueError:
            return False, "Veuillez saisir un âge valide"

    @staticmethod
    def validate_taille(taille: str) -> Tuple[bool, str]:
        try:
            taille_float = float(taille)
            if 140 <= taille_float <= 220:
                return True, ""
            return False, "La taille doit être entre 140cm et 220cm"
        except ValueError:
            return False, "Veuillez saisir une taille valide"

    @staticmethod
    def validate_poids(poids: str) -> Tuple[bool, str]:
        try:
            poids_float = float(poids)
            if 40 <= poids_float <= 200:
                return True, ""
            return False, "Le poids doit être entre 40kg et 200kg"
        except ValueError:
            return False, "Veuillez saisir un poids valide"


class PersonalInfoStep(ctk.CTkFrame, ValidationMixin):
    """Step 1: Personal Information"""

    def __init__(self, parent, on_change: Callable = None):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="👤 Informations Personnelles",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Nom
        self.nom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nom_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(self.nom_frame, text="Nom", width=100).pack(side="left", padx=(0, 10))
        self.nom_entry = ctk.CTkEntry(self.nom_frame, placeholder_text="Dupont")
        self.nom_entry.pack(side="right", fill="x", expand=True)
        self.nom_entry.bind("<KeyRelease>", self._on_change)

        # Prénom
        self.prenom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.prenom_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(self.prenom_frame, text="Prénom", width=100).pack(side="left", padx=(0, 10))
        self.prenom_entry = ctk.CTkEntry(self.prenom_frame, placeholder_text="Jean")
        self.prenom_entry.pack(side="right", fill="x", expand=True)
        self.prenom_entry.bind("<KeyRelease>", self._on_change)

        # Âge
        self.age_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.age_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(self.age_frame, text="Âge", width=100).pack(side="left", padx=(0, 10))
        self.age_entry = ctk.CTkEntry(self.age_frame, placeholder_text="30")
        self.age_entry.pack(side="right", fill="x", expand=True)
        self.age_entry.bind("<KeyRelease>", self._validate_age)

        # Error label for age
        self.age_error = ctk.CTkLabel(self, text="", text_color="#EF4444", font=ctk.CTkFont(size=12))
        self.age_error.pack(pady=2)

        # Sexe
        self.sexe_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sexe_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(self.sexe_frame, text="Sexe", width=100).pack(side="left", padx=(0, 10))

        self.sexe_var = tk.StringVar(value="Homme")
        self.sexe_homme = ctk.CTkRadioButton(
            self.sexe_frame, text="Homme", variable=self.sexe_var,
            value="Homme", command=self._on_change
        )
        self.sexe_homme.pack(side="left", padx=10)

        self.sexe_femme = ctk.CTkRadioButton(
            self.sexe_frame, text="Femme", variable=self.sexe_var,
            value="Femme", command=self._on_change
        )
        self.sexe_femme.pack(side="left", padx=10)

    def _validate_age(self, event=None):
        age_text = self.age_entry.get()
        is_valid, error_msg = self.validate_age(age_text)

        if age_text and not is_valid:
            self.age_error.configure(text=error_msg)
            self.age_entry.configure(border_color="#EF4444")
        else:
            self.age_error.configure(text="")
            self.age_entry.configure(border_color="#565B5E")

        if self.on_change:
            self.on_change()

    def _on_change(self, event=None):
        if self.on_change:
            self.on_change()

    def get_data(self) -> Dict[str, Any]:
        return {
            "nom": self.nom_entry.get().strip(),
            "prenom": self.prenom_entry.get().strip(),
            "age": self.age_entry.get().strip(),
            "sexe": self.sexe_var.get()
        }

    def is_valid(self) -> bool:
        data = self.get_data()
        return (
            bool(data["nom"]) and bool(data["prenom"]) and
            self.validate_age(data["age"])[0]
        )


class MorphologyStep(ctk.CTkFrame, ValidationMixin):
    """Step 2: Morphology & Body Composition"""

    def __init__(self, parent, on_change: Callable = None):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.setup_ui()

    def setup_ui(self):
        title_label = ctk.CTkLabel(
            self,
            text="📏 Morphologie & Composition",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Taille
        self.taille_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.taille_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(self.taille_frame, text="Taille (cm)", width=120).pack(side="left", padx=(0, 10))
        self.taille_entry = ctk.CTkEntry(self.taille_frame, placeholder_text="175")
        self.taille_entry.pack(side="right", fill="x", expand=True)
        self.taille_entry.bind("<KeyRelease>", self._validate_taille)

        # Error label for taille
        self.taille_error = ctk.CTkLabel(self, text="", text_color="#EF4444", font=ctk.CTkFont(size=12))
        self.taille_error.pack(pady=2)

        # Poids
        self.poids_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.poids_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(self.poids_frame, text="Poids (kg)", width=120).pack(side="left", padx=(0, 10))
        self.poids_entry = ctk.CTkEntry(self.poids_frame, placeholder_text="75")
        self.poids_entry.pack(side="right", fill="x", expand=True)
        self.poids_entry.bind("<KeyRelease>", self._validate_poids)

        # Error label for poids
        self.poids_error = ctk.CTkLabel(self, text="", text_color="#EF4444", font=ctk.CTkFont(size=12))
        self.poids_error.pack(pady=2)

        # Mass grasse (optionnel)
        self.masse_grasse_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.masse_grasse_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(self.masse_grasse_frame, text="% Masse Grasse", width=120).pack(side="left", padx=(0, 10))

        self.masse_grasse_var = tk.StringVar()
        self.masse_grasse_slider = ctk.CTkSlider(
            self.masse_grasse_frame,
            from_=5, to=50,
            command=self._update_masse_grasse,
            variable=self.masse_grasse_var
        )
        self.masse_grasse_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.masse_grasse_slider.set(15)  # Default value

        self.masse_grasse_label = ctk.CTkLabel(self.masse_grasse_frame, text="15%", width=50)
        self.masse_grasse_label.pack(side="right")

        # Optionnel notice
        notice_label = ctk.CTkLabel(
            self,
            text="💡 Le % de masse grasse est optionnel mais améliore la précision",
            font=ctk.CTkFont(size=12),
            text_color="#9CA3AF"
        )
        notice_label.pack(pady=10)

    def _validate_taille(self, event=None):
        taille_text = self.taille_entry.get()
        is_valid, error_msg = self.validate_taille(taille_text)

        if taille_text and not is_valid:
            self.taille_error.configure(text=error_msg)
            self.taille_entry.configure(border_color="#EF4444")
        else:
            self.taille_error.configure(text="")
            self.taille_entry.configure(border_color="#565B5E")

        if self.on_change:
            self.on_change()

    def _validate_poids(self, event=None):
        poids_text = self.poids_entry.get()
        is_valid, error_msg = self.validate_poids(poids_text)

        if poids_text and not is_valid:
            self.poids_error.configure(text=error_msg)
            self.poids_entry.configure(border_color="#EF4444")
        else:
            self.poids_error.configure(text="")
            self.poids_entry.configure(border_color="#565B5E")

        if self.on_change:
            self.on_change()

    def _update_masse_grasse(self, value):
        self.masse_grasse_label.configure(text=f"{int(value)}%")
        if self.on_change:
            self.on_change()

    def get_data(self) -> Dict[str, Any]:
        return {
            "taille_cm": self.taille_entry.get().strip(),
            "poids_kg": self.poids_entry.get().strip(),
            "masse_grasse_pct": int(self.masse_grasse_slider.get())
        }

    def is_valid(self) -> bool:
        data = self.get_data()
        return (
            self.validate_taille(data["taille_cm"])[0] and
            self.validate_poids(data["poids_kg"])[0]
        )


class ActivityStep(ctk.CTkFrame):
    """Step 3: Activity & Lifestyle"""

    def __init__(self, parent, on_change: Callable = None):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.setup_ui()

    def setup_ui(self):
        title_label = ctk.CTkLabel(
            self,
            text="🏃 Activité & Style de Vie",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Sélectionnez votre niveau d'activité physique habituel",
            font=ctk.CTkFont(size=14),
            text_color="#9CA3AF"
        )
        subtitle_label.pack(pady=(0, 20))

        self.activity_var = tk.StringVar(value=ActivityLevel.SEDENTARY.label)

        # Activity options
        for activity in ActivityLevel:
            activity_frame = ctk.CTkFrame(self, fg_color="#F8FAFC", corner_radius=8)
            activity_frame.pack(fill="x", pady=5, padx=10)

            radio_button = ctk.CTkRadioButton(
                activity_frame,
                text="",
                variable=self.activity_var,
                value=activity.label,
                command=self._on_change
            )
            radio_button.pack(side="left", padx=15, pady=15)

            label_frame = ctk.CTkFrame(activity_frame, fg_color="transparent")
            label_frame.pack(side="left", fill="x", expand=True, pady=15)

            title_label = ctk.CTkLabel(
                label_frame,
                text=activity.label,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title_label.pack(anchor="w")

            desc_label = ctk.CTkLabel(
                label_frame,
                text=activity.description,
                font=ctk.CTkFont(size=12),
                text_color="#6B7280"
            )
            desc_label.pack(anchor="w")

            factor_label = ctk.CTkLabel(
                activity_frame,
                text=f"×{activity.factor}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#22D3EE"
            )
            factor_label.pack(side="right", padx=15, pady=15)

    def _on_change(self):
        if self.on_change:
            self.on_change()

    def get_data(self) -> Dict[str, Any]:
        selected_label = self.activity_var.get()
        for activity in ActivityLevel:
            if activity.label == selected_label:
                return {"niveau_activite": activity}
        return {"niveau_activite": ActivityLevel.SEDENTARY}

    def is_valid(self) -> bool:
        return True  # Always valid, has default


class ObjectivesStep(ctk.CTkFrame):
    """Step 4: Nutrition Goals"""

    def __init__(self, parent, on_change: Callable = None):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.setup_ui()

    def setup_ui(self):
        title_label = ctk.CTkLabel(
            self,
            text="🎯 Objectifs Nutritionnels",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Goal selection
        goal_frame = ctk.CTkFrame(self, fg_color="transparent")
        goal_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(goal_frame, text="Objectif Principal", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(0, 10))

        self.goal_var = tk.StringVar(value=NutritionGoal.MAINTENANCE.label)

        # Group goals by category
        maintenance_goals = [NutritionGoal.MAINTENANCE]
        fat_loss_goals = [NutritionGoal.FAT_LOSS_MILD, NutritionGoal.FAT_LOSS_MODERATE, NutritionGoal.FAT_LOSS_AGGRESSIVE]
        lean_gain_goals = [NutritionGoal.LEAN_GAIN_SLOW, NutritionGoal.LEAN_GAIN_MODERATE, NutritionGoal.LEAN_GAIN_AGGRESSIVE]

        # Maintenance
        self._create_goal_section("🎯 Maintenance", maintenance_goals, goal_frame)

        # Fat Loss
        self._create_goal_section("✂️ Perte de Poids", fat_loss_goals, goal_frame)

        # Lean Gain
        self._create_goal_section("💪 Prise de Masse", lean_gain_goals, goal_frame)

    def _create_goal_section(self, section_title: str, goals: List[NutritionGoal], parent):
        section_frame = ctk.CTkFrame(parent, fg_color="#F8FAFC", corner_radius=8)
        section_frame.pack(fill="x", pady=5)

        section_label = ctk.CTkLabel(
            section_frame,
            text=section_title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        section_label.pack(anchor="w", padx=15, pady=(10, 5))

        for goal in goals:
            goal_radio_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
            goal_radio_frame.pack(fill="x", padx=15, pady=2)

            radio_button = ctk.CTkRadioButton(
                goal_radio_frame,
                text="",
                variable=self.goal_var,
                value=goal.label,
                command=self._on_change
            )
            radio_button.pack(side="left")

            label_frame = ctk.CTkFrame(goal_radio_frame, fg_color="transparent")
            label_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))

            title = ctk.CTkLabel(
                label_frame,
                text=goal.label,
                font=ctk.CTkFont(size=14)
            )
            title.pack(anchor="w")

            desc = ctk.CTkLabel(
                label_frame,
                text=goal.description,
                font=ctk.CTkFont(size=11),
                text_color="#6B7280"
            )
            desc.pack(anchor="w")

            adjustment_color = "#EF4444" if goal.adjustment < 0 else "#10B981" if goal.adjustment > 0 else "#6B7280"
            adjustment_text = f"{goal.adjustment:+d} kcal" if goal.adjustment != 0 else "0 kcal"

            adjustment_label = ctk.CTkLabel(
                goal_radio_frame,
                text=adjustment_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=adjustment_color
            )
            adjustment_label.pack(side="right", padx=10)

        # Add padding at bottom of section
        padding = ctk.CTkFrame(section_frame, fg_color="transparent", height=10)
        padding.pack()

    def _on_change(self):
        if self.on_change:
            self.on_change()

    def get_data(self) -> Dict[str, Any]:
        selected_label = self.goal_var.get()
        for goal in NutritionGoal:
            if goal.label == selected_label:
                return {"objectif": goal}
        return {"objectif": NutritionGoal.MAINTENANCE}

    def is_valid(self) -> bool:
        return True  # Always valid, has default


class MacrosStep(ctk.CTkFrame):
    """Step 5: Macronutrient Distribution"""

    def __init__(self, parent, on_change: Callable = None):
        super().__init__(parent, fg_color="transparent")
        self.on_change = on_change
        self.preview_data = None
        self.setup_ui()

    def setup_ui(self):
        title_label = ctk.CTkLabel(
            self,
            text="🥗 Répartition Macronutriments",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Protéines par kg
        protein_frame = ctk.CTkFrame(self, fg_color="transparent")
        protein_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(protein_frame, text="Protéines par kg de poids corporel", font=ctk.CTkFont(size=14)).pack(anchor="w")

        self.protein_var = tk.DoubleVar(value=1.6)
        protein_slider = ctk.CTkSlider(
            protein_frame,
            from_=0.8, to=3.0,
            number_of_steps=22,  # 0.1 increments
            variable=self.protein_var,
            command=self._update_protein_preview
        )
        protein_slider.pack(fill="x", pady=5)

        self.protein_label = ctk.CTkLabel(
            protein_frame,
            text="1.6 g/kg",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#22D3EE"
        )
        self.protein_label.pack(anchor="w")

        # Glucides percentage
        carbs_frame = ctk.CTkFrame(self, fg_color="transparent")
        carbs_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(carbs_frame, text="Proportion de glucides (% calories restantes)", font=ctk.CTkFont(size=14)).pack(anchor="w")

        self.carbs_var = tk.DoubleVar(value=50.0)
        carbs_slider = ctk.CTkSlider(
            carbs_frame,
            from_=20.0, to=70.0,
            number_of_steps=50,
            variable=self.carbs_var,
            command=self._update_carbs_preview
        )
        carbs_slider.pack(fill="x", pady=5)

        self.carbs_label = ctk.CTkLabel(
            carbs_frame,
            text="50% glucides - 50% lipides",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#FFAD05"
        )
        self.carbs_label.pack(anchor="w")

        # Preview frame
        self.preview_frame = ctk.CTkFrame(self, fg_color="#F8FAFC", corner_radius=8)
        self.preview_frame.pack(fill="x", pady=20)

        preview_title = ctk.CTkLabel(
            self.preview_frame,
            text="📊 Aperçu des calculs",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        preview_title.pack(pady=10)

        self.preview_content = ctk.CTkLabel(
            self.preview_frame,
            text="Remplissez les étapes précédentes pour voir l'aperçu",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280",
            justify="left"
        )
        self.preview_content.pack(pady=10, padx=20)

    def _update_protein_preview(self, value):
        self.protein_label.configure(text=f"{value:.1f} g/kg")
        self._update_preview()
        if self.on_change:
            self.on_change()

    def _update_carbs_preview(self, value):
        fat_pct = 100.0 - value
        self.carbs_label.configure(text=f"{value:.0f}% glucides - {fat_pct:.0f}% lipides")
        self._update_preview()
        if self.on_change:
            self.on_change()

    def _update_preview(self):
        if not self.preview_data:
            return

        try:
            # Create temporary calculation
            protein_per_kg = self.protein_var.get()
            carbs_pct = self.carbs_var.get()
            fat_pct = 100.0 - carbs_pct

            macro_targets = MacroTargets(
                proteines_g_par_kg=protein_per_kg,
                glucides_pct=carbs_pct,
                lipides_pct=fat_pct
            )

            results = AdvancedNutritionCalculator.calculate_complete_nutrition(
                self.preview_data, macro_targets
            )

            preview_text = f"""🔥 Calories objectif: {results.objectif_kcal} kcal/jour

🥩 Protéines: {results.proteines_g}g ({results.proteines_pct}%)
🍞 Glucides: {results.glucides_g}g ({results.glucides_pct}%)
🥑 Lipides: {results.lipides_g}g ({results.lipides_pct}%)

📈 BMR: {results.bmr_kcal} kcal | TDEE: {results.tdee_kcal} kcal
⚖️ Balance: {results.deficit_surplus:+d} kcal/jour"""

            self.preview_content.configure(text=preview_text)

        except Exception:
            self.preview_content.configure(text="Impossible de calculer l'aperçu")

    def update_preview_data(self, personal_data: PersonalData):
        """Update preview with personal data from previous steps"""
        self.preview_data = personal_data
        self._update_preview()

    def get_data(self) -> Dict[str, Any]:
        return {
            "proteines_g_par_kg": self.protein_var.get(),
            "glucides_pct": self.carbs_var.get(),
            "lipides_pct": 100.0 - self.carbs_var.get()
        }

    def is_valid(self) -> bool:
        return True  # Always valid, has defaults


class AdvancedNutritionFormModal(ctk.CTkToplevel):
    """
    Advanced multi-step nutrition form modal.

    Features:
    - 5-step progressive disclosure
    - Real-time validation and preview
    - Professional UX with smooth navigation
    - Complete nutrition calculations
    """

    def __init__(
        self,
        parent,
        client_data: Optional[Dict] = None,
        save_callback: Callable[[NutritionResults], None] = None
    ):
        super().__init__(parent)

        self.client_data = client_data or {}
        self.save_callback = save_callback
        self.current_step = 1
        self.total_steps = 5

        # Configure modal
        colors = ctk.ThemeManager.theme["color"]
        self.title("Fiche Nutrition Personnalisée")
        self.configure(fg_color=colors["surface_dark"])
        self.geometry("700x600")
        self.resizable(False, False)
        self.grab_set()

        self.setup_ui()
        self.populate_from_client()

        # Bring to front
        try:
            bring_to_front(self, make_modal=True)
        except Exception:
            pass

    def setup_ui(self):
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Progress indicator
        self.progress_indicator = ProgressIndicator(main_container, self.total_steps)
        self.progress_indicator.pack(fill="x", pady=(0, 20))

        # Steps container
        self.steps_container = ctk.CTkFrame(main_container, fg_color="transparent")
        self.steps_container.pack(fill="both", expand=True)

        # Create all steps
        self.steps = {
            1: PersonalInfoStep(self.steps_container, self._on_step_change),
            2: MorphologyStep(self.steps_container, self._on_step_change),
            3: ActivityStep(self.steps_container, self._on_step_change),
            4: ObjectivesStep(self.steps_container, self._on_step_change),
            5: MacrosStep(self.steps_container, self._on_step_change)
        }

        # Navigation buttons
        nav_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(20, 0))

        self.prev_button = SecondaryButton(
            nav_frame, text="⬅ Précédent", command=self._prev_step
        )
        self.prev_button.pack(side="left")

        self.next_button = PrimaryButton(
            nav_frame, text="Suivant ➡", command=self._next_step
        )
        self.next_button.pack(side="right")

        self.generate_button = PrimaryButton(
            nav_frame, text="🎯 Générer Fiche PDF", command=self._generate_nutrition_sheet
        )

        # Show first step
        self._show_step(1)

    def populate_from_client(self):
        """Pre-populate form with existing client data"""
        if not self.client_data:
            return

        # Personal info
        if hasattr(self.steps[1], 'nom_entry') and self.client_data.get('nom'):
            self.steps[1].nom_entry.insert(0, self.client_data['nom'])
        if hasattr(self.steps[1], 'prenom_entry') and self.client_data.get('prenom'):
            self.steps[1].prenom_entry.insert(0, self.client_data['prenom'])

        # Morphology
        if hasattr(self.steps[2], 'taille_entry') and self.client_data.get('taille_cm'):
            self.steps[2].taille_entry.insert(0, str(self.client_data['taille_cm']))
        if hasattr(self.steps[2], 'poids_entry') and self.client_data.get('poids_kg'):
            self.steps[2].poids_entry.insert(0, str(self.client_data['poids_kg']))

    def _show_step(self, step: int):
        """Show specific step and hide others"""
        for step_num, step_widget in self.steps.items():
            if step_num == step:
                step_widget.pack(fill="both", expand=True)
            else:
                step_widget.pack_forget()

        # Update progress indicator
        self.progress_indicator.update_progress(step)

        # Update navigation buttons
        self.prev_button.configure(state="normal" if step > 1 else "disabled")

        if step == self.total_steps:
            self.next_button.pack_forget()
            self.generate_button.pack(side="right")
        else:
            self.generate_button.pack_forget()
            self.next_button.pack(side="right")

        # Update next button state
        current_step_widget = self.steps[step]
        is_valid = current_step_widget.is_valid() if hasattr(current_step_widget, 'is_valid') else True
        self.next_button.configure(state="normal" if is_valid else "disabled")

        self.current_step = step

    def _prev_step(self):
        if self.current_step > 1:
            self._show_step(self.current_step - 1)

    def _next_step(self):
        current_step_widget = self.steps[self.current_step]
        if hasattr(current_step_widget, 'is_valid') and not current_step_widget.is_valid():
            return

        if self.current_step < self.total_steps:
            self._show_step(self.current_step + 1)

            # Update macro step preview when reaching final step
            if self.current_step == self.total_steps:
                self._update_macro_preview()

    def _on_step_change(self):
        """Called when any step data changes"""
        # Update next button state
        current_step_widget = self.steps[self.current_step]
        is_valid = current_step_widget.is_valid() if hasattr(current_step_widget, 'is_valid') else True

        if hasattr(self, 'next_button'):
            self.next_button.configure(state="normal" if is_valid else "disabled")

        # Update macro preview if on final step
        if self.current_step == self.total_steps:
            self._update_macro_preview()

    def _update_macro_preview(self):
        """Update macro step with preview data"""
        try:
            personal_data = self._collect_personal_data()
            if personal_data:
                self.steps[5].update_preview_data(personal_data)
        except Exception:
            pass

    def _collect_personal_data(self) -> Optional[PersonalData]:
        """Collect data from all steps to create PersonalData object"""
        try:
            # Collect data from each step
            step1_data = self.steps[1].get_data()
            step2_data = self.steps[2].get_data()
            step3_data = self.steps[3].get_data()
            step4_data = self.steps[4].get_data()

            # Validate required data
            if not all([
                step1_data.get('nom'),
                step1_data.get('prenom'),
                step1_data.get('age'),
                step2_data.get('taille_cm'),
                step2_data.get('poids_kg')
            ]):
                return None

            return PersonalData(
                nom=step1_data['nom'],
                prenom=step1_data['prenom'],
                age=int(step1_data['age']),
                sexe=step1_data['sexe'],
                taille_cm=float(step2_data['taille_cm']),
                poids_kg=float(step2_data['poids_kg']),
                masse_grasse_pct=step2_data.get('masse_grasse_pct'),
                niveau_activite=step3_data['niveau_activite'],
                objectif=step4_data['objectif']
            )

        except Exception:
            return None

    def _generate_nutrition_sheet(self):
        """Generate complete nutrition sheet"""
        try:
            # Collect all data
            personal_data = self._collect_personal_data()
            if not personal_data:
                ctk.CTkMessagebox.show_error("Erreur", "Données incomplètes")
                return

            step5_data = self.steps[5].get_data()
            macro_targets = MacroTargets(
                proteines_g_par_kg=step5_data['proteines_g_par_kg'],
                glucides_pct=step5_data['glucides_pct'],
                lipides_pct=step5_data['lipides_pct']
            )

            # Calculate complete nutrition
            results = AdvancedNutritionCalculator.calculate_complete_nutrition(
                personal_data, macro_targets
            )

            # Call save callback if provided
            if self.save_callback:
                self.save_callback(results)

            self.destroy()

        except Exception as e:
            ctk.CTkMessagebox.show_error("Erreur", f"Erreur lors de la génération: {str(e)}")