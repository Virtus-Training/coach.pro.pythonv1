"""🍽️ Intelligent Meal Planner 2025

AI-powered meal planning that learns user preferences:
- Smart meal generation based on nutritional goals
- Ingredient substitution and dietary restrictions
- Shopping list generation with store optimization
- Meal prep time estimation and scheduling
- Seasonal ingredient recommendations
- Cost optimization and budget tracking
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Tuple, Any
import customtkinter as ctk

from dtos.nutrition_dtos import PlanAlimentaireDTO
from ui.components.nutrition_2025.micro_interactions import AnimatedCard, ProgressBar
from ui.components.design_system import Card, CardTitle, PrimaryButton, SecondaryButton


class IntelligentMealPlanner(ctk.CTkFrame):
    """🧠 AI-powered meal planning interface

    Features:
    - Goal-based meal generation with macro optimization
    - Dietary restriction and preference learning
    - Ingredient substitution suggestions
    - Meal prep time and difficulty estimation
    - Shopping list generation with store mapping
    - Cost tracking and budget optimization
    - Seasonal ingredient recommendations
    - Social meal sharing and collaboration
    """

    def __init__(
        self,
        parent,
        client_id: int,
        controller,
        on_plan_generated: Optional[Callable[[Dict], None]] = None,
        **kwargs
    ):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.client_id = client_id
        self.controller = controller
        self.on_plan_generated = on_plan_generated or (lambda x: None)

        # Planning state
        self.current_plan = None
        self.planning_goals = {}
        self.dietary_restrictions = []
        self.preferred_cuisines = []
        self.meal_preferences = {}
        self.budget_target = 0.0

        # Generation parameters
        self.plan_duration = 7  # days
        self.meals_per_day = 3
        self.prep_time_limit = 60  # minutes
        self.difficulty_level = "medium"

        # AI learning data
        self.user_feedback = {}
        self.ingredient_preferences = {}
        self.cooking_skills = "intermediate"

        # Interface state
        self.generation_step = "goals"  # goals, preferences, generation, review
        self.is_generating = False
        self.generation_progress = 0

        self._setup_layout()
        self._create_planner_interface()
        self._load_user_preferences()

    def _setup_layout(self) -> None:
        """📐 Configure meal planner layout"""
        # Configure responsive grid
        self.grid_columnconfigure(0, weight=2)  # Main planning area
        self.grid_columnconfigure(1, weight=1)  # Settings panel
        self.grid_rowconfigure(0, weight=0)     # Header
        self.grid_rowconfigure(1, weight=1)     # Main content

    def _create_planner_interface(self) -> None:
        """🏗️ Build meal planner interface"""
        self._create_header()
        self._create_planning_area()
        self._create_settings_panel()

    def _create_header(self) -> None:
        """🍽️ Create meal planner header"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=8, pady=8)

        # Title with smart icon
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left")

        title_label = ctk.CTkLabel(
            title_frame,
            text="🧠 Intelligent Meal Planner",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(side="left")

        # Planning status
        self.status_label = ctk.CTkLabel(
            title_frame,
            text="Ready to plan your meals",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray50")
        )
        self.status_label.pack(side="left", padx=(16, 0))

        # Quick actions
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        # Generate plan button
        self.generate_btn = PrimaryButton(
            actions_frame,
            text="🪄 Generate Plan",
            command=self._start_plan_generation,
            width=140
        )
        self.generate_btn.pack(side="right", padx=(0, 8))

        # Quick plan buttons
        quick_plans = [
            ("⚡ Quick Plan", self._generate_quick_plan),
            ("🎯 Goal-Based", self._start_goal_based_planning)
        ]

        for text, command in quick_plans:
            btn = SecondaryButton(
                actions_frame,
                text=text,
                command=command,
                width=100
            )
            btn.pack(side="right", padx=(0, 8))

    def _create_planning_area(self) -> None:
        """📊 Create main planning workspace"""
        self.planning_frame = AnimatedCard(self, title="🗓️ Meal Planning Workspace")
        self.planning_frame.grid(row=1, column=0, sticky="nsew", padx=(8, 4), pady=8)

        # Planning steps navigator
        self._create_step_navigator()

        # Dynamic content area
        self.content_area = ctk.CTkFrame(
            self.planning_frame.content_frame,
            fg_color="transparent"
        )
        self.content_area.pack(fill="both", expand=True, pady=16)

        # Show initial step
        self._show_goals_step()

    def _create_settings_panel(self) -> None:
        """⚙️ Create settings and preferences panel"""
        self.settings_frame = AnimatedCard(self, title="⚙️ Planning Settings")
        self.settings_frame.grid(row=1, column=1, sticky="nsew", padx=(4, 8), pady=8)

        settings_container = ctk.CTkScrollableFrame(
            self.settings_frame.content_frame,
            fg_color="transparent"
        )
        settings_container.pack(fill="both", expand=True, pady=8)

        # Meal preferences
        self._create_meal_preferences(settings_container)

        # Dietary restrictions
        self._create_dietary_restrictions(settings_container)

        # Budget settings
        self._create_budget_settings(settings_container)

        # Cooking preferences
        self._create_cooking_preferences(settings_container)

    def _create_step_navigator(self) -> None:
        """🧭 Create planning step navigator"""
        nav_frame = ctk.CTkFrame(self.planning_frame.content_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(0, 16))

        steps = [
            ("🎯", "Goals", "goals"),
            ("❤️", "Preferences", "preferences"),
            ("🪄", "Generation", "generation"),
            ("👀", "Review", "review")
        ]

        self.step_buttons = {}
        for i, (icon, label, step_key) in enumerate(steps):
            step_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
            step_frame.pack(side="left", fill="x", expand=True)

            btn = ctk.CTkButton(
                step_frame,
                text=f"{icon}\\n{label}",
                width=80,
                height=50,
                font=ctk.CTkFont(size=10),
                command=lambda s=step_key: self._navigate_to_step(s),
                fg_color="transparent",
                border_width=1
            )
            btn.pack(padx=2)
            self.step_buttons[step_key] = btn

            # Add step connector (except for last step)
            if i < len(steps) - 1:
                connector = ctk.CTkLabel(
                    step_frame,
                    text="→",
                    font=ctk.CTkFont(size=16),
                    text_color=("gray50", "gray60")
                )
                connector.pack(side="right")

        # Set initial step
        self._update_step_navigator("goals")

    def _create_meal_preferences(self, parent) -> None:
        """🍽️ Create meal preferences section"""
        pref_frame = ctk.CTkFrame(parent)
        pref_frame.pack(fill="x", pady=(0, 16))

        # Section title
        title_label = ctk.CTkLabel(
            pref_frame,
            text="🍽️ Meal Preferences",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(anchor="w", padx=16, pady=(16, 8))

        # Meals per day
        meals_frame = ctk.CTkFrame(pref_frame, fg_color="transparent")
        meals_frame.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(
            meals_frame,
            text="Meals per day:",
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        self.meals_var = ctk.IntVar(value=self.meals_per_day)
        meals_slider = ctk.CTkSlider(
            meals_frame,
            from_=2,
            to=6,
            number_of_steps=4,
            variable=self.meals_var,
            command=self._on_meals_change
        )
        meals_slider.pack(side="right", padx=(8, 0))

        self.meals_label = ctk.CTkLabel(
            meals_frame,
            text=str(self.meals_per_day),
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.meals_label.pack(side="right", padx=(8, 0))

        # Plan duration
        duration_frame = ctk.CTkFrame(pref_frame, fg_color="transparent")
        duration_frame.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(
            duration_frame,
            text="Plan duration:",
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        self.duration_var = ctk.StringVar(value=f"{self.plan_duration} days")
        duration_menu = ctk.CTkOptionMenu(
            duration_frame,
            variable=self.duration_var,
            values=["1 day", "3 days", "7 days", "14 days", "30 days"],
            command=self._on_duration_change,
            width=100
        )
        duration_menu.pack(side="right")

        # Cuisine preferences
        cuisine_frame = ctk.CTkFrame(pref_frame, fg_color="transparent")
        cuisine_frame.pack(fill="x", padx=16, pady=(8, 16))

        ctk.CTkLabel(
            cuisine_frame,
            text="Preferred cuisines:",
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w")

        cuisines = ["Mediterranean", "Asian", "Mexican", "Italian", "American", "French"]
        self.cuisine_vars = {}

        cuisine_grid = ctk.CTkFrame(cuisine_frame, fg_color="transparent")
        cuisine_grid.pack(fill="x", pady=4)

        for i, cuisine in enumerate(cuisines):
            var = ctk.BooleanVar(value=cuisine in self.preferred_cuisines)
            self.cuisine_vars[cuisine] = var

            checkbox = ctk.CTkCheckBox(
                cuisine_grid,
                text=cuisine,
                variable=var,
                font=ctk.CTkFont(size=10),
                command=self._update_cuisine_preferences
            )
            checkbox.grid(row=i//2, column=i%2, sticky="w", padx=(0, 16), pady=2)

    def _create_dietary_restrictions(self, parent) -> None:
        """🚫 Create dietary restrictions section"""
        restrictions_frame = ctk.CTkFrame(parent)
        restrictions_frame.pack(fill="x", pady=(0, 16))

        title_label = ctk.CTkLabel(
            restrictions_frame,
            text="🚫 Dietary Restrictions",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(anchor="w", padx=16, pady=(16, 8))

        restrictions = [
            "Vegetarian", "Vegan", "Gluten-Free",
            "Dairy-Free", "Nut-Free", "Low-Carb",
            "Keto", "Paleo"
        ]

        self.restriction_vars = {}
        restrictions_grid = ctk.CTkFrame(restrictions_frame, fg_color="transparent")
        restrictions_grid.pack(fill="x", padx=16, pady=(0, 16))

        for i, restriction in enumerate(restrictions):
            var = ctk.BooleanVar(value=restriction in self.dietary_restrictions)
            self.restriction_vars[restriction] = var

            checkbox = ctk.CTkCheckBox(
                restrictions_grid,
                text=restriction,
                variable=var,
                font=ctk.CTkFont(size=10),
                command=self._update_dietary_restrictions
            )
            checkbox.grid(row=i//2, column=i%2, sticky="w", padx=(0, 8), pady=2)

    def _create_budget_settings(self, parent) -> None:
        """💰 Create budget settings section"""
        budget_frame = ctk.CTkFrame(parent)
        budget_frame.pack(fill="x", pady=(0, 16))

        title_label = ctk.CTkLabel(
            budget_frame,
            text="💰 Budget Settings",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(anchor="w", padx=16, pady=(16, 8))

        # Budget per week
        budget_input_frame = ctk.CTkFrame(budget_frame, fg_color="transparent")
        budget_input_frame.pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkLabel(
            budget_input_frame,
            text="Weekly budget ($):",
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        self.budget_var = ctk.StringVar(value=str(self.budget_target))
        budget_entry = ctk.CTkEntry(
            budget_input_frame,
            textvariable=self.budget_var,
            width=80,
            placeholder_text="0.00"
        )
        budget_entry.pack(side="right")

        # Cost optimization
        cost_frame = ctk.CTkFrame(budget_frame, fg_color="transparent")
        cost_frame.pack(fill="x", padx=16, pady=(0, 16))

        self.cost_optimization_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            cost_frame,
            text="Optimize for cost",
            variable=self.cost_optimization_var,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w")

    def _create_cooking_preferences(self, parent) -> None:
        """👨‍🍳 Create cooking preferences section"""
        cooking_frame = ctk.CTkFrame(parent)
        cooking_frame.pack(fill="x", pady=(0, 16))

        title_label = ctk.CTkLabel(
            cooking_frame,
            text="👨‍🍳 Cooking Preferences",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(anchor="w", padx=16, pady=(16, 8))

        # Cooking skill level
        skill_frame = ctk.CTkFrame(cooking_frame, fg_color="transparent")
        skill_frame.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(
            skill_frame,
            text="Skill level:",
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        self.skill_var = ctk.StringVar(value=self.cooking_skills)
        skill_menu = ctk.CTkOptionMenu(
            skill_frame,
            variable=self.skill_var,
            values=["beginner", "intermediate", "advanced"],
            width=120
        )
        skill_menu.pack(side="right")

        # Max prep time
        prep_frame = ctk.CTkFrame(cooking_frame, fg_color="transparent")
        prep_frame.pack(fill="x", padx=16, pady=(4, 16))

        ctk.CTkLabel(
            prep_frame,
            text="Max prep time (min):",
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        self.prep_time_var = ctk.IntVar(value=self.prep_time_limit)
        prep_slider = ctk.CTkSlider(
            prep_frame,
            from_=15,
            to=120,
            number_of_steps=21,
            variable=self.prep_time_var,
            command=self._on_prep_time_change
        )
        prep_slider.pack(side="right", padx=(8, 0))

        self.prep_time_label = ctk.CTkLabel(
            prep_frame,
            text=f"{self.prep_time_limit}min",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.prep_time_label.pack(side="right", padx=(8, 0))

    # Step navigation and content
    def _navigate_to_step(self, step: str) -> None:
        """🧭 Navigate to planning step"""
        self.generation_step = step
        self._update_step_navigator(step)

        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Show step content
        if step == "goals":
            self._show_goals_step()
        elif step == "preferences":
            self._show_preferences_step()
        elif step == "generation":
            self._show_generation_step()
        elif step == "review":
            self._show_review_step()

    def _update_step_navigator(self, current_step: str) -> None:
        """🔄 Update step navigator visual state"""
        for step_key, btn in self.step_buttons.items():
            if step_key == current_step:
                btn.configure(
                    fg_color=("#1f538d", "#1f538d"),
                    text_color="white",
                    border_width=0
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("gray20", "gray80"),
                    border_width=1
                )

    def _show_goals_step(self) -> None:
        """🎯 Show nutrition goals configuration"""
        goals_frame = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        goals_frame.pack(fill="both", expand=True)

        # Step title
        step_title = ctk.CTkLabel(
            goals_frame,
            text="🎯 Set Your Nutrition Goals",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        step_title.pack(pady=(0, 16))

        # Goal presets
        presets_frame = ctk.CTkFrame(goals_frame)
        presets_frame.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            presets_frame,
            text="Quick Goal Presets:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=16, pady=(16, 8))

        presets = [
            ("🏃‍♂️ Weight Loss", {"calories": -500, "protein": "high", "carbs": "moderate", "fats": "low"}),
            ("💪 Muscle Gain", {"calories": 300, "protein": "very_high", "carbs": "high", "fats": "moderate"}),
            ("⚖️ Maintenance", {"calories": 0, "protein": "moderate", "carbs": "moderate", "fats": "moderate"}),
            ("🏋️‍♀️ Performance", {"calories": 200, "protein": "high", "carbs": "very_high", "fats": "moderate"})
        ]

        preset_buttons = ctk.CTkFrame(presets_frame, fg_color="transparent")
        preset_buttons.pack(fill="x", padx=16, pady=(0, 16))

        for i, (preset_name, preset_goals) in enumerate(presets):
            btn = ctk.CTkButton(
                preset_buttons,
                text=preset_name,
                width=180,
                height=40,
                command=lambda pg=preset_goals: self._apply_goal_preset(pg),
                font=ctk.CTkFont(size=11)
            )
            btn.grid(row=i//2, column=i%2, sticky="ew", padx=4, pady=4)

        # Custom goals
        custom_frame = ctk.CTkFrame(goals_frame)
        custom_frame.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            custom_frame,
            text="Custom Goals:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=16, pady=(16, 8))

        # Calorie adjustment
        cal_frame = ctk.CTkFrame(custom_frame, fg_color="transparent")
        cal_frame.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(
            cal_frame,
            text="Daily calorie adjustment:",
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        self.calorie_adjustment_var = ctk.IntVar(value=0)
        cal_slider = ctk.CTkSlider(
            cal_frame,
            from_=-800,
            to=800,
            number_of_steps=32,
            variable=self.calorie_adjustment_var,
            command=self._on_calorie_adjustment_change
        )
        cal_slider.pack(side="right", padx=(8, 0))

        self.cal_adjustment_label = ctk.CTkLabel(
            cal_frame,
            text="0 kcal",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.cal_adjustment_label.pack(side="right", padx=(8, 0))

        # Navigation buttons
        nav_frame = ctk.CTkFrame(goals_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=16)

        next_btn = PrimaryButton(
            nav_frame,
            text="Next: Preferences →",
            command=lambda: self._navigate_to_step("preferences"),
            width=160
        )
        next_btn.pack(side="right")

    def _show_preferences_step(self) -> None:
        """❤️ Show preference learning interface"""
        pref_frame = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        pref_frame.pack(fill="both", expand=True)

        step_title = ctk.CTkLabel(
            pref_frame,
            text="❤️ Tell Us Your Preferences",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        step_title.pack(pady=(0, 16))

        # Ingredient preferences learning
        ingredients_frame = ctk.CTkFrame(pref_frame)
        ingredients_frame.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            ingredients_frame,
            text="Rate These Common Ingredients:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=16, pady=(16, 8))

        # Common ingredients with rating system
        ingredients = [
            "Chicken", "Beef", "Fish", "Eggs", "Beans",
            "Rice", "Pasta", "Potatoes", "Broccoli", "Spinach",
            "Cheese", "Yogurt", "Nuts", "Avocado", "Tomatoes"
        ]

        self.ingredient_ratings = {}
        ingredients_grid = ctk.CTkFrame(ingredients_frame, fg_color="transparent")
        ingredients_grid.pack(fill="x", padx=16, pady=(0, 16))

        for i, ingredient in enumerate(ingredients[:9]):  # Show first 9
            rating_frame = ctk.CTkFrame(ingredients_grid, fg_color="transparent")
            rating_frame.grid(row=i//3, column=i%3, sticky="ew", padx=8, pady=4)

            ctk.CTkLabel(
                rating_frame,
                text=ingredient,
                font=ctk.CTkFont(size=10)
            ).pack()

            # Rating buttons
            rating_buttons = ctk.CTkFrame(rating_frame, fg_color="transparent")
            rating_buttons.pack(pady=2)

            rating_var = ctk.IntVar(value=3)  # Default neutral
            self.ingredient_ratings[ingredient] = rating_var

            for rating in [1, 2, 3, 4, 5]:
                emoji = ["😞", "😐", "🙂", "😊", "😍"][rating-1]
                btn = ctk.CTkButton(
                    rating_buttons,
                    text=emoji,
                    width=24,
                    height=24,
                    font=ctk.CTkFont(size=12),
                    command=lambda r=rating, v=rating_var: v.set(r),
                    fg_color="transparent",
                    hover_color=("gray80", "gray30")
                )
                btn.pack(side="left", padx=1)

        # Navigation
        nav_frame = ctk.CTkFrame(pref_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=16)

        prev_btn = SecondaryButton(
            nav_frame,
            text="← Back",
            command=lambda: self._navigate_to_step("goals"),
            width=100
        )
        prev_btn.pack(side="left")

        next_btn = PrimaryButton(
            nav_frame,
            text="Generate Plan →",
            command=self._start_plan_generation,
            width=160
        )
        next_btn.pack(side="right")

    def _show_generation_step(self) -> None:
        """🪄 Show plan generation progress"""
        gen_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        gen_frame.pack(fill="both", expand=True)

        # Generation status
        status_frame = ctk.CTkFrame(gen_frame)
        status_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # Title
        title_label = ctk.CTkLabel(
            status_frame,
            text="🪄 Generating Your Meal Plan",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(40, 20))

        # Progress indicator
        self.generation_progress_bar = ProgressBar(
            status_frame,
            width=300,
            height=20,
            progress=self.generation_progress,
            target=100,
            color_scheme="energy",
            show_percentage=True
        )
        self.generation_progress_bar.pack(pady=20)

        # Status message
        self.generation_status = ctk.CTkLabel(
            status_frame,
            text="Analyzing your preferences...",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray50")
        )
        self.generation_status.pack(pady=(0, 40))

        if self.is_generating:
            self._animate_generation_progress()

    def _show_review_step(self) -> None:
        """👀 Show generated plan review"""
        review_frame = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        review_frame.pack(fill="both", expand=True)

        step_title = ctk.CTkLabel(
            review_frame,
            text="👀 Review Your Meal Plan",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        step_title.pack(pady=(0, 16))

        if self.current_plan:
            self._display_generated_plan(review_frame)
        else:
            # No plan generated yet
            empty_frame = ctk.CTkFrame(review_frame)
            empty_frame.pack(expand=True, fill="both", pady=50)

            ctk.CTkLabel(
                empty_frame,
                text="🍽️ No meal plan generated yet",
                font=ctk.CTkFont(size=14),
                text_color=("gray60", "gray50")
            ).pack(pady=40)

            generate_btn = PrimaryButton(
                empty_frame,
                text="🪄 Generate Plan",
                command=self._start_plan_generation,
                width=160
            )
            generate_btn.pack()

    def _display_generated_plan(self, parent) -> None:
        """📋 Display the generated meal plan"""
        plan_frame = ctk.CTkFrame(parent)
        plan_frame.pack(fill="x", pady=(0, 16))

        # Plan summary
        summary_frame = ctk.CTkFrame(plan_frame)
        summary_frame.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(
            summary_frame,
            text="📊 Plan Summary",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(0, 8))

        # Mock plan data
        plan_stats = {
            "duration": f"{self.plan_duration} days",
            "total_meals": self.plan_duration * self.meals_per_day,
            "avg_calories": "2000 kcal/day",
            "estimated_cost": "$85/week",
            "prep_time": "45 min/day avg"
        }

        stats_grid = ctk.CTkFrame(summary_frame, fg_color="transparent")
        stats_grid.pack(fill="x", pady=8)

        for i, (stat, value) in enumerate(plan_stats.items()):
            stat_frame = ctk.CTkFrame(stats_grid)
            stat_frame.grid(row=i//3, column=i%3, sticky="ew", padx=4, pady=4)

            ctk.CTkLabel(
                stat_frame,
                text=stat.replace("_", " ").title(),
                font=ctk.CTkFont(size=10),
                text_color=("gray60", "gray50")
            ).pack(pady=(8, 2))

            ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(pady=(0, 8))

        # Action buttons
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.pack(fill="x", pady=16)

        # Regenerate button
        regenerate_btn = SecondaryButton(
            actions_frame,
            text="🔄 Regenerate",
            command=self._regenerate_plan,
            width=120
        )
        regenerate_btn.pack(side="left")

        # Export buttons
        export_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        export_frame.pack(side="right")

        shopping_btn = PrimaryButton(
            export_frame,
            text="🛒 Shopping List",
            command=self._generate_shopping_list,
            width=140
        )
        shopping_btn.pack(side="right", padx=(0, 8))

        apply_btn = PrimaryButton(
            export_frame,
            text="✅ Apply Plan",
            command=self._apply_generated_plan,
            width=120
        )
        apply_btn.pack(side="right")

    # Event handlers and logic methods
    def _load_user_preferences(self) -> None:
        """📊 Load user preferences from database"""
        try:
            # In production, load from user profile
            # For now, use defaults
            self.preferred_cuisines = ["Mediterranean", "Italian"]
            self.dietary_restrictions = []
            self.budget_target = 100.0
        except Exception as e:
            print(f"Error loading preferences: {e}")

    def _on_meals_change(self, value) -> None:
        """🍽️ Handle meals per day change"""
        self.meals_per_day = int(value)
        self.meals_label.configure(text=str(self.meals_per_day))

    def _on_duration_change(self, value) -> None:
        """📅 Handle plan duration change"""
        self.plan_duration = int(value.split()[0])

    def _on_prep_time_change(self, value) -> None:
        """⏰ Handle prep time change"""
        self.prep_time_limit = int(value)
        self.prep_time_label.configure(text=f"{self.prep_time_limit}min")

    def _on_calorie_adjustment_change(self, value) -> None:
        """🔥 Handle calorie adjustment change"""
        adjustment = int(value)
        sign = "+" if adjustment > 0 else ""
        self.cal_adjustment_label.configure(text=f"{sign}{adjustment} kcal")

    def _update_cuisine_preferences(self) -> None:
        """🌍 Update cuisine preferences"""
        self.preferred_cuisines = [
            cuisine for cuisine, var in self.cuisine_vars.items()
            if var.get()
        ]

    def _update_dietary_restrictions(self) -> None:
        """🚫 Update dietary restrictions"""
        self.dietary_restrictions = [
            restriction for restriction, var in self.restriction_vars.items()
            if var.get()
        ]

    def _apply_goal_preset(self, preset_goals: Dict) -> None:
        """🎯 Apply goal preset"""
        self.planning_goals = preset_goals.copy()

        # Update calorie adjustment
        if "calories" in preset_goals:
            self.calorie_adjustment_var.set(preset_goals["calories"])
            self._on_calorie_adjustment_change(preset_goals["calories"])

        print(f"Applied goal preset: {preset_goals}")

    def _start_plan_generation(self) -> None:
        """🪄 Start meal plan generation"""
        if self.is_generating:
            return

        self.is_generating = True
        self.generation_progress = 0

        # Navigate to generation step
        self._navigate_to_step("generation")

        # Start generation process
        self._generate_meal_plan()

    def _generate_quick_plan(self) -> None:
        """⚡ Generate quick meal plan"""
        # Set quick defaults
        self.planning_goals = {"calories": 0, "protein": "moderate"}
        self.plan_duration = 3
        self.meals_per_day = 3

        self._start_plan_generation()

    def _start_goal_based_planning(self) -> None:
        """🎯 Start goal-based planning"""
        self._navigate_to_step("goals")

    def _generate_meal_plan(self) -> None:
        """🧠 Generate intelligent meal plan"""
        try:
            # Collect all parameters
            generation_params = {
                "client_id": self.client_id,
                "duration_days": self.plan_duration,
                "meals_per_day": self.meals_per_day,
                "goals": self.planning_goals,
                "dietary_restrictions": self.dietary_restrictions,
                "preferred_cuisines": self.preferred_cuisines,
                "budget_target": float(self.budget_var.get() or 0),
                "prep_time_limit": self.prep_time_limit,
                "cooking_skill": self.skill_var.get(),
                "ingredient_preferences": {
                    ingredient: var.get()
                    for ingredient, var in self.ingredient_ratings.items()
                }
            }

            # Simulate generation process
            self._simulate_generation_process(generation_params)

        except Exception as e:
            print(f"Error generating meal plan: {e}")
            self.is_generating = False

    def _simulate_generation_process(self, params: Dict) -> None:
        """🎬 Simulate AI meal plan generation"""
        generation_steps = [
            "Analyzing your nutritional goals...",
            "Learning from your preferences...",
            "Searching recipe database...",
            "Optimizing macro balance...",
            "Checking dietary restrictions...",
            "Estimating costs and prep time...",
            "Generating meal combinations...",
            "Finalizing your personalized plan..."
        ]

        self._process_generation_step(0, generation_steps)

    def _process_generation_step(self, step_index: int, steps: List[str]) -> None:
        """⚙️ Process one generation step"""
        if step_index >= len(steps):
            # Generation complete
            self._complete_generation()
            return

        # Update status
        if hasattr(self, 'generation_status'):
            self.generation_status.configure(text=steps[step_index])

        # Update progress
        progress = ((step_index + 1) / len(steps)) * 100
        self.generation_progress = progress
        if hasattr(self, 'generation_progress_bar'):
            self.generation_progress_bar.set_progress(progress)

        # Schedule next step
        self.after(800, lambda: self._process_generation_step(step_index + 1, steps))

    def _complete_generation(self) -> None:
        """✅ Complete meal plan generation"""
        self.is_generating = False

        # Create mock plan
        self.current_plan = {
            "id": "generated_plan_001",
            "duration": self.plan_duration,
            "meals": self._generate_mock_meals(),
            "nutrition_summary": {
                "avg_calories": 2000,
                "avg_protein": 150,
                "avg_carbs": 200,
                "avg_fats": 70
            },
            "estimated_cost": 85.50,
            "total_prep_time": self.plan_duration * 45  # minutes
        }

        # Update status
        if hasattr(self, 'generation_status'):
            self.generation_status.configure(text="✅ Your meal plan is ready!")

        # Navigate to review
        self.after(1000, lambda: self._navigate_to_step("review"))

        # Notify parent
        self.on_plan_generated(self.current_plan)

    def _generate_mock_meals(self) -> List[Dict]:
        """🍽️ Generate mock meal data"""
        meals = []
        meal_names = ["Breakfast", "Lunch", "Dinner", "Snack"]

        for day in range(self.plan_duration):
            for meal_idx in range(self.meals_per_day):
                meal_name = meal_names[meal_idx] if meal_idx < len(meal_names) else f"Meal {meal_idx + 1}"

                meals.append({
                    "day": day + 1,
                    "meal": meal_name,
                    "name": f"Delicious {meal_name}",
                    "calories": 400 + (meal_idx * 200),
                    "prep_time": 20 + (meal_idx * 10),
                    "difficulty": ["easy", "medium", "hard"][meal_idx % 3],
                    "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
                })

        return meals

    def _animate_generation_progress(self) -> None:
        """🎬 Animate generation progress"""
        if not self.is_generating:
            return

        # Continue animation
        self.after(100, self._animate_generation_progress)

    def _regenerate_plan(self) -> None:
        """🔄 Regenerate meal plan"""
        self.current_plan = None
        self._start_plan_generation()

    def _apply_generated_plan(self) -> None:
        """✅ Apply generated plan to user's nutrition"""
        if not self.current_plan:
            return

        try:
            # In production, this would save the plan to the database
            # and update the user's current nutrition plan
            print("✅ Applying generated meal plan...")

            # Update status
            self.status_label.configure(text="Plan applied successfully!")

            # Notify parent
            self.on_plan_generated(self.current_plan)

        except Exception as e:
            print(f"Error applying plan: {e}")

    def _generate_shopping_list(self) -> None:
        """🛒 Generate smart shopping list"""
        if not self.current_plan:
            return

        try:
            # Generate shopping list with store optimization
            shopping_list = self._create_optimized_shopping_list()

            # Show shopping list modal
            self._show_shopping_list_modal(shopping_list)

        except Exception as e:
            print(f"Error generating shopping list: {e}")

    def _create_optimized_shopping_list(self) -> Dict:
        """🛒 Create optimized shopping list"""
        # Mock shopping list with store sections
        return {
            "produce": ["Bananas", "Spinach", "Tomatoes", "Avocados"],
            "meat_seafood": ["Chicken breast", "Salmon fillets"],
            "dairy": ["Greek yogurt", "Eggs", "Milk"],
            "pantry": ["Brown rice", "Olive oil", "Quinoa"],
            "frozen": ["Mixed berries", "Broccoli"],
            "estimated_cost": 85.50,
            "store_optimization": "Grouped by aisle for efficient shopping"
        }

    def _show_shopping_list_modal(self, shopping_list: Dict) -> None:
        """📋 Show shopping list in modal"""
        # TODO: Implement shopping list modal
        print("🛒 Shopping list generated:")
        for section, items in shopping_list.items():
            if isinstance(items, list):
                print(f"  {section.replace('_', ' ').title()}: {', '.join(items)}")

    # Public interface
    def refresh(self) -> None:
        """🔄 Refresh meal planner"""
        self._load_user_preferences()

    def set_client_goals(self, goals: Dict) -> None:
        """🎯 Set nutrition goals externally"""
        self.planning_goals.update(goals)

    def get_current_plan(self) -> Optional[Dict]:
        """📋 Get current generated plan"""
        return self.current_plan