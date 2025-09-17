"""🍽️ Générateur de Plans Alimentaires Automatique

Générateur intelligent qui crée des plans alimentaires personnalisés
basés sur les fiches nutrition et utilisant la base d'aliments.
"""

import customtkinter as ctk
from typing import Optional, Dict, List, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import random

from models.aliment import Aliment, CategorieAliment


@dataclass
class MealPlanConfig:
    """Configuration pour la génération de plan"""
    duree_jours: int = 7
    nb_repas_jour: int = 4
    variete_score: float = 0.8  # 0-1, plus élevé = plus de variété
    regime_alimentaire: str = "Omnivore"
    exclure_categories: List[str] = None
    tolerance_macro: float = 0.1  # ±10% par défaut


class MealPlanGenerator(ctk.CTkFrame):
    """🧬 Générateur de Plans Alimentaires Intelligent"""

    def __init__(self, parent, controller, client_id: Optional[int] = None,
                 on_plan_generated: Optional[Callable] = None, **kwargs):
        super().__init__(parent, **kwargs)

        self.controller = controller
        self.client_id = client_id
        self.on_plan_generated = on_plan_generated

        # État interne
        self.fiche_nutrition = None
        self.aliments_disponibles = []
        self.plan_genere = None

        # Charger les données
        self._load_nutrition_data()
        self._load_available_foods()

        # Construire l'interface
        self._create_generator_interface()

    def _load_nutrition_data(self) -> None:
        """📊 Charger la fiche nutrition du client"""
        try:
            if self.client_id:
                # Récupérer la fiche nutrition via le controller
                data = self.controller.get_nutrition_page_data(self.client_id)
                self.fiche_nutrition = data.fiche if data else None
        except Exception as e:
            print(f"❌ Erreur chargement fiche nutrition: {e}")

    def _load_available_foods(self) -> None:
        """🍎 Charger la base d'aliments disponibles"""
        try:
            # Récupérer tous les aliments de la base
            self.aliments_disponibles = self.controller.search_aliments("") or []
            print(f"✅ {len(self.aliments_disponibles)} aliments chargés")
        except Exception as e:
            print(f"❌ Erreur chargement aliments: {e}")
            self.aliments_disponibles = []

    def _create_generator_interface(self) -> None:
        """🎨 Interface de configuration du générateur"""
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Titre
        title = ctk.CTkLabel(
            self,
            text="🍽️ Générateur de Plan Alimentaire",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(16, 24))

        # Vérification fiche nutrition
        if not self.fiche_nutrition:
            self._create_no_nutrition_warning()
            return

        # Info fiche nutrition
        self._create_nutrition_info()

        # Formulaire de configuration
        self._create_config_form()

        # Bouton génération
        self._create_generate_button()

        # Zone d'affichage du plan
        self._create_plan_display()

    def _create_no_nutrition_warning(self) -> None:
        """⚠️ Avertissement si pas de fiche nutrition"""
        warning = ctk.CTkFrame(self, fg_color="#EF4444")
        warning.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=16)

        ctk.CTkLabel(
            warning,
            text="⚠️ Aucune Fiche Nutrition Trouvée",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(pady=8)

        ctk.CTkLabel(
            warning,
            text="Créez d'abord une fiche nutrition pour ce client",
            font=ctk.CTkFont(size=12),
            text_color="white"
        ).pack(pady=(0, 8))

    def _create_nutrition_info(self) -> None:
        """📊 Affichage des informations de la fiche nutrition"""
        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=8)

        # Titre info
        ctk.CTkLabel(
            info_frame,
            text="📊 Objectifs Nutritionnels",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(12, 8))

        # Macros en ligne
        macros_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        macros_frame.pack(fill="x", padx=16, pady=8)

        # Objectifs de la fiche
        objectives = [
            ("🔥", "Calories", f"{self.fiche_nutrition.objectif_kcal} kcal"),
            ("💪", "Protéines", f"{self.fiche_nutrition.proteines_g}g"),
            ("🌾", "Glucides", f"{self.fiche_nutrition.glucides_g}g"),
            ("🧈", "Lipides", f"{self.fiche_nutrition.lipides_g}g")
        ]

        for i, (icon, label, value) in enumerate(objectives):
            obj_frame = ctk.CTkFrame(macros_frame, width=120, height=60)
            obj_frame.grid(row=0, column=i, padx=4, pady=4)

            ctk.CTkLabel(obj_frame, text=icon, font=ctk.CTkFont(size=16)).pack(pady=(8, 2))
            ctk.CTkLabel(obj_frame, text=value, font=ctk.CTkFont(size=11, weight="bold")).pack()
            ctk.CTkLabel(obj_frame, text=label, font=ctk.CTkFont(size=9)).pack(pady=(0, 8))

        # Configurer les colonnes
        for i in range(4):
            macros_frame.grid_columnconfigure(i, weight=1)

    def _create_config_form(self) -> None:
        """⚙️ Formulaire de configuration du plan"""
        config_frame = ctk.CTkFrame(self)
        config_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=16, pady=8)

        # Titre
        ctk.CTkLabel(
            config_frame,
            text="⚙️ Configuration du Plan",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(12, 16))

        # Conteneur pour 2 colonnes
        form_container = ctk.CTkFrame(config_frame, fg_color="transparent")
        form_container.pack(fill="x", padx=16, pady=(0, 16))
        form_container.grid_columnconfigure(0, weight=1)
        form_container.grid_columnconfigure(1, weight=1)

        # Colonne gauche
        left_col = ctk.CTkFrame(form_container, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        # Durée du plan (slider)
        ctk.CTkLabel(left_col, text="📅 Durée du plan (jours)",
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 4))

        self.duree_var = ctk.IntVar(value=7)
        self.duree_slider = ctk.CTkSlider(left_col, from_=3, to=21, number_of_steps=18,
                                         variable=self.duree_var, width=200)
        self.duree_slider.pack(anchor="w", pady=(0, 4))

        self.duree_label = ctk.CTkLabel(left_col, text="7 jours",
                                       font=ctk.CTkFont(size=10), text_color="gray60")
        self.duree_label.pack(anchor="w", pady=(0, 12))

        # Callback pour mettre à jour le label
        self.duree_slider.configure(command=lambda v: self.duree_label.configure(text=f"{int(v)} jours"))

        # Nombre de repas par jour (slider)
        ctk.CTkLabel(left_col, text="🍽️ Repas par jour",
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 4))

        self.repas_var = ctk.IntVar(value=4)
        self.repas_slider = ctk.CTkSlider(left_col, from_=3, to=6, number_of_steps=3,
                                         variable=self.repas_var, width=200)
        self.repas_slider.pack(anchor="w", pady=(0, 4))

        self.repas_label = ctk.CTkLabel(left_col, text="4 repas",
                                       font=ctk.CTkFont(size=10), text_color="gray60")
        self.repas_label.pack(anchor="w", pady=(0, 12))

        self.repas_slider.configure(command=lambda v: self.repas_label.configure(text=f"{int(v)} repas"))

        # Colonne droite
        right_col = ctk.CTkFrame(form_container, fg_color="transparent")
        right_col.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        # Régime alimentaire (combobox)
        ctk.CTkLabel(right_col, text="🥗 Régime alimentaire",
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 4))

        self.regime_combo = ctk.CTkComboBox(right_col,
                                           values=["Omnivore", "Végétarien", "Vegan", "Sans gluten"],
                                           width=200, state="readonly")
        self.regime_combo.pack(anchor="w", pady=(0, 12))
        self.regime_combo.set("Omnivore")

        # Niveau de variété (slider)
        ctk.CTkLabel(right_col, text="🎯 Variété des aliments",
                    font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 4))

        self.variete_var = ctk.DoubleVar(value=0.8)
        self.variete_slider = ctk.CTkSlider(right_col, from_=0.3, to=1.0, number_of_steps=7,
                                           variable=self.variete_var, width=200)
        self.variete_slider.pack(anchor="w", pady=(0, 4))

        self.variete_label = ctk.CTkLabel(right_col, text="Élevée",
                                         font=ctk.CTkFont(size=10), text_color="gray60")
        self.variete_label.pack(anchor="w", pady=(0, 12))

        def update_variete_label(v):
            if v < 0.5:
                text = "Faible"
            elif v < 0.8:
                text = "Moyenne"
            else:
                text = "Élevée"
            self.variete_label.configure(text=text)

        self.variete_slider.configure(command=update_variete_label)

    def _create_generate_button(self) -> None:
        """🪄 Bouton de génération du plan"""
        self.generate_btn = ctk.CTkButton(
            self,
            text="🪄 Générer le Plan Alimentaire",
            command=self._generate_meal_plan,
            width=300,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#10B981",
            hover_color="#059669",
            corner_radius=25
        )
        self.generate_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def _create_plan_display(self) -> None:
        """📋 Zone d'affichage du plan généré"""
        self.plan_frame = ctk.CTkScrollableFrame(self, height=400)
        self.plan_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))

        # Message initial
        self.plan_status = ctk.CTkLabel(
            self.plan_frame,
            text="👆 Configurez et générez votre plan alimentaire",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        self.plan_status.pack(pady=40)

    def _generate_meal_plan(self) -> None:
        """🧬 Générer le plan alimentaire automatiquement"""
        if not self.fiche_nutrition or not self.aliments_disponibles:
            self._show_error("❌ Données insuffisantes pour générer le plan")
            return

        # Désactiver le bouton pendant la génération
        self.generate_btn.configure(state="disabled", text="🔄 Génération en cours...")

        # Configuration
        config = MealPlanConfig(
            duree_jours=int(self.duree_var.get()),
            nb_repas_jour=int(self.repas_var.get()),
            regime_alimentaire=self.regime_combo.get(),
            variete_score=self.variete_var.get(),
            tolerance_macro=0.1
        )

        try:
            # Générer le plan
            self.plan_genere = self._generate_plan_algorithm(config)

            # Afficher le plan
            self._display_generated_plan()

            # Callback si fourni
            if self.on_plan_generated:
                self.on_plan_generated(self.plan_genere)

        except Exception as e:
            self._show_error(f"❌ Erreur génération: {str(e)}")

        finally:
            # Réactiver le bouton
            self.generate_btn.configure(state="normal", text="🪄 Générer le Plan Alimentaire")

    def _generate_plan_algorithm(self, config: MealPlanConfig) -> Dict:
        """🤖 Algorithme de génération automatique du plan"""
        # Objectifs nutritionnels journaliers
        target_kcal = self.fiche_nutrition.objectif_kcal
        target_protein = self.fiche_nutrition.proteines_g
        target_carbs = self.fiche_nutrition.glucides_g
        target_fat = self.fiche_nutrition.lipides_g

        # Filtrer les aliments selon le régime
        aliments_compatibles = [
            aliment for aliment in self.aliments_disponibles
            if aliment.est_compatible_regime(config.regime_alimentaire)
        ]

        if not aliments_compatibles:
            raise ValueError("Aucun aliment compatible avec le régime sélectionné")

        # Générer le plan jour par jour
        plan = {
            "config": config,
            "objectifs_jour": {
                "kcal": target_kcal,
                "proteines_g": target_protein,
                "glucides_g": target_carbs,
                "lipides_g": target_fat
            },
            "jours": []
        }

        for jour in range(1, config.duree_jours + 1):
            plan_jour = self._generate_daily_plan(
                jour, config, aliments_compatibles,
                target_kcal, target_protein, target_carbs, target_fat
            )
            plan["jours"].append(plan_jour)

        return plan

    def _generate_daily_plan(self, jour_num: int, config: MealPlanConfig,
                           aliments: List[Aliment], target_kcal: float,
                           target_protein: float, target_carbs: float,
                           target_fat: float) -> Dict:
        """📅 Générer le plan d'une journée"""

        # Répartition des calories par repas
        repas_ratios = self._get_meal_ratios(config.nb_repas_jour)

        plan_jour = {
            "jour": jour_num,
            "repas": [],
            "totaux": {"kcal": 0, "proteines_g": 0, "glucides_g": 0, "lipides_g": 0}
        }

        noms_repas = ["Petit-déjeuner", "Déjeuner", "Dîner", "Collation", "Collation 2", "Collation 3"]

        for i, ratio in enumerate(repas_ratios):
            if i >= len(noms_repas):
                break

            repas = self._generate_meal(
                noms_repas[i], aliments, ratio,
                target_kcal, target_protein, target_carbs, target_fat, config
            )

            plan_jour["repas"].append(repas)

            # Cumuler les totaux
            for key in plan_jour["totaux"]:
                plan_jour["totaux"][key] += repas["totaux"][key]

        return plan_jour

    def _get_meal_ratios(self, nb_repas: int) -> List[float]:
        """⚖️ Répartition calorique par repas"""
        if nb_repas == 3:
            return [0.25, 0.45, 0.30]  # Petit-déj, Déj, Dîner
        elif nb_repas == 4:
            return [0.25, 0.35, 0.30, 0.10]  # + Collation
        elif nb_repas == 5:
            return [0.20, 0.30, 0.25, 0.15, 0.10]  # + 2 collations
        else:
            return [0.20, 0.25, 0.25, 0.15, 0.10, 0.05]  # 6 repas

    def _generate_meal(self, nom_repas: str, aliments: List[Aliment],
                      ratio_kcal: float, target_kcal: float,
                      target_protein: float, target_carbs: float,
                      target_fat: float, config: MealPlanConfig) -> Dict:
        """🍽️ Générer un repas individuel"""

        # Objectifs pour ce repas
        repas_kcal = target_kcal * ratio_kcal
        repas_protein = target_protein * ratio_kcal
        repas_carbs = target_carbs * ratio_kcal
        repas_fat = target_fat * ratio_kcal

        # Sélectionner 2-4 aliments pour ce repas
        nb_aliments = random.randint(2, min(4, len(aliments)))
        aliments_repas = random.sample(aliments, nb_aliments)

        # Optimiser les quantités pour atteindre les macros
        aliments_quantites = self._optimize_meal_quantities(
            aliments_repas, repas_kcal, repas_protein, repas_carbs, repas_fat
        )

        # Calculer les totaux réels
        totaux = {"kcal": 0, "proteines_g": 0, "glucides_g": 0, "lipides_g": 0}
        aliments_detail = []

        for aliment, quantite in aliments_quantites:
            valeurs = aliment.calculer_valeurs_nutritionnelles(quantite)
            aliments_detail.append({
                "aliment": aliment,
                "quantite_g": quantite,
                "valeurs": valeurs
            })

            totaux["kcal"] += valeurs["kcal"]
            totaux["proteines_g"] += valeurs["proteines_g"]
            totaux["glucides_g"] += valeurs["glucides_g"]
            totaux["lipides_g"] += valeurs["lipides_g"]

        return {
            "nom": nom_repas,
            "objectifs": {
                "kcal": repas_kcal,
                "proteines_g": repas_protein,
                "glucides_g": repas_carbs,
                "lipides_g": repas_fat
            },
            "aliments": aliments_detail,
            "totaux": totaux
        }

    def _optimize_meal_quantities(self, aliments: List[Aliment],
                                 target_kcal: float, target_protein: float,
                                 target_carbs: float, target_fat: float) -> List[tuple]:
        """🎯 Optimiser les quantités d'aliments pour atteindre les macros"""
        # Algorithme simple d'optimisation
        # Dans une version plus avancée, on pourrait utiliser une optimisation linéaire

        base_quantity = 80  # grammes de base par aliment
        quantities = [(aliment, base_quantity) for aliment in aliments]

        # Ajuster les quantités pour se rapprocher des objectifs
        for iteration in range(10):  # Max 10 itérations d'ajustement
            current_kcal = sum(aliment.kcal_100g * qty / 100 for aliment, qty in quantities)

            if abs(current_kcal - target_kcal) < target_kcal * 0.05:  # ±5%
                break

            # Ajuster proportionnellement
            factor = target_kcal / max(current_kcal, 1)
            quantities = [(aliment, max(20, min(200, qty * factor))) for aliment, qty in quantities]

        return quantities

    def _display_generated_plan(self) -> None:
        """📋 Afficher le plan généré sous forme de tableaux"""
        # Nettoyer l'affichage précédent
        for widget in self.plan_frame.winfo_children():
            widget.destroy()

        if not self.plan_genere:
            return

        # Titre du plan généré
        title = ctk.CTkLabel(
            self.plan_frame,
            text=f"✅ Plan Alimentaire Généré - {self.plan_genere['config'].duree_jours} jours",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#10B981"
        )
        title.pack(pady=(0, 16))

        # Résumé des objectifs
        objectifs = self.plan_genere["objectifs_jour"]
        summary = ctk.CTkFrame(self.plan_frame)
        summary.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(summary, text="🎯 Objectifs Journaliers",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(8, 4))

        obj_text = f"🔥 {objectifs['kcal']} kcal | 💪 {objectifs['proteines_g']}g protéines | 🌾 {objectifs['glucides_g']}g glucides | 🧈 {objectifs['lipides_g']}g lipides"
        ctk.CTkLabel(summary, text=obj_text, font=ctk.CTkFont(size=12)).pack(pady=(0, 8))

        # Afficher chaque jour
        for jour_data in self.plan_genere["jours"]:
            self._display_daily_plan(jour_data)

    def _display_daily_plan(self, jour_data: Dict) -> None:
        """📅 Afficher le plan d'une journée"""
        # Cadre du jour
        day_frame = ctk.CTkFrame(self.plan_frame)
        day_frame.pack(fill="x", pady=8)

        # Header du jour
        day_header = ctk.CTkFrame(day_frame, fg_color="#6366F1")
        day_header.pack(fill="x", padx=8, pady=8)

        ctk.CTkLabel(
            day_header,
            text=f"📅 Jour {jour_data['jour']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=12, pady=8)

        # Totaux du jour
        totaux = jour_data["totaux"]
        total_text = f"Total: {totaux['kcal']:.0f} kcal | {totaux['proteines_g']:.1f}g P | {totaux['glucides_g']:.1f}g G | {totaux['lipides_g']:.1f}g L"
        ctk.CTkLabel(
            day_header,
            text=total_text,
            font=ctk.CTkFont(size=11),
            text_color="white"
        ).pack(side="right", padx=12, pady=8)

        # Table des repas
        for repas_data in jour_data["repas"]:
            self._display_meal_table(day_frame, repas_data)

    def _display_meal_table(self, parent, repas_data: Dict) -> None:
        """🍽️ Afficher un repas sous forme de tableau"""
        meal_frame = ctk.CTkFrame(parent)
        meal_frame.pack(fill="x", padx=16, pady=4)

        # Header repas
        meal_header = ctk.CTkFrame(meal_frame, fg_color="transparent")
        meal_header.pack(fill="x", padx=8, pady=(8, 4))

        ctk.CTkLabel(
            meal_header,
            text=f"🍽️ {repas_data['nom']}",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left")

        totaux = repas_data["totaux"]
        meal_total = f"{totaux['kcal']:.0f} kcal | {totaux['proteines_g']:.1f}g P | {totaux['glucides_g']:.1f}g G | {totaux['lipides_g']:.1f}g L"
        ctk.CTkLabel(
            meal_header,
            text=meal_total,
            font=ctk.CTkFont(size=10),
            text_color="gray60"
        ).pack(side="right")

        # Tableau des aliments
        table_frame = ctk.CTkFrame(meal_frame, fg_color="transparent")
        table_frame.pack(fill="x", padx=8, pady=(0, 8))

        # En-têtes de colonnes
        headers = ["Aliment", "Quantité", "Kcal", "Protéines", "Glucides", "Lipides"]
        header_frame = ctk.CTkFrame(table_frame, fg_color="#374151")
        header_frame.pack(fill="x", pady=(0, 2))

        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="white"
            )
            header_label.grid(row=0, column=i, padx=4, pady=4, sticky="w")

        # Configurer les colonnes
        for i in range(len(headers)):
            header_frame.grid_columnconfigure(i, weight=1)

        # Lignes des aliments
        for aliment_data in repas_data["aliments"]:
            self._display_food_row(table_frame, aliment_data)

    def _display_food_row(self, parent, aliment_data: Dict) -> None:
        """🥕 Afficher une ligne d'aliment"""
        aliment = aliment_data["aliment"]
        quantite = aliment_data["quantite_g"]
        valeurs = aliment_data["valeurs"]

        row_frame = ctk.CTkFrame(parent, fg_color="#F9FAFB")
        row_frame.pack(fill="x", pady=1)

        # Données de la ligne
        row_data = [
            aliment.nom,
            f"{quantite:.0f}g",
            f"{valeurs['kcal']:.0f}",
            f"{valeurs['proteines_g']:.1f}g",
            f"{valeurs['glucides_g']:.1f}g",
            f"{valeurs['lipides_g']:.1f}g"
        ]

        for i, data in enumerate(row_data):
            cell_label = ctk.CTkLabel(
                row_frame,
                text=data,
                font=ctk.CTkFont(size=9),
                text_color="black" if i == 0 else "gray40"
            )
            cell_label.grid(row=0, column=i, padx=4, pady=2, sticky="w")

        # Configurer les colonnes
        for i in range(len(row_data)):
            row_frame.grid_columnconfigure(i, weight=1)

    def _show_error(self, message: str) -> None:
        """❌ Afficher un message d'erreur"""
        # Nettoyer l'affichage
        for widget in self.plan_frame.winfo_children():
            widget.destroy()

        error_label = ctk.CTkLabel(
            self.plan_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="#EF4444"
        )
        error_label.pack(pady=40)

    def get_generated_plan(self) -> Optional[Dict]:
        """📋 Récupérer le plan généré"""
        return self.plan_genere