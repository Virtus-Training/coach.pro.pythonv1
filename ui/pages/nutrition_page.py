from tkinter import filedialog
from typing import Dict

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
from ui.components.food_search_bar import FoodSearchBar
from ui.components.meal_card import MealCard
from ui.pages.client_detail_page_components.fiche_nutrition_tab import (
    GenerateFicheModal,
)


class NutritionPage(ctk.CTkFrame):
    def __init__(self, parent, controller: NutritionController, client_id: int):
        super().__init__(parent)
        self.controller = controller
        self.nutrition_controller = controller  # used by GenerateFicheModal
        self.client_id = client_id

        data = self.controller.get_nutrition_page_data(client_id)
        self.client = data.client
        self.fiche = data.fiche
        self.plan: PlanAlimentaireDTO = data.plan
        self.active_repas_id = self.plan.repas[0].id if self.plan.repas else None

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        self._create_top_bar()
        self._create_left_panel()
        self._create_center_panel()
        self._create_right_panel()
        self._refresh()

    # Left panel
    def _create_left_panel(self) -> None:
        self.left_card = Card(self)
        self.left_card.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        name = f"{self.client.prenom} {self.client.nom}" if self.client else "Client"
        CardTitle(self.left_card, text=name).pack(padx=10, pady=(10, 5))
        self.cal_lbl = ctk.CTkLabel(self.left_card, text="Calories: 0 / 0")
        self.prot_lbl = ctk.CTkLabel(self.left_card, text="Protéines: 0 / 0")
        self.carb_lbl = ctk.CTkLabel(self.left_card, text="Glucides: 0 / 0")
        self.fat_lbl = ctk.CTkLabel(self.left_card, text="Lipides: 0 / 0")
        for lbl in [self.cal_lbl, self.prot_lbl, self.carb_lbl, self.fat_lbl]:
            lbl.pack(anchor="w", padx=10)

    # Center panel
    def _create_center_panel(self) -> None:
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.center_frame.columnconfigure(0, weight=1)
        self.meal_cards: Dict[int, MealCard] = {}
        for repas in self.plan.repas:
            card = MealCard(
                self.center_frame,
                repas.nom,
                on_select=lambda rid=repas.id: self._set_active_meal(rid),
                on_delete_item=self._delete_item,
            )
            card.pack(fill="x", pady=5)
            self.meal_cards[repas.id] = card

    # Right panel
    def _create_right_panel(self) -> None:
        self.search_bar = FoodSearchBar(self, self.controller, self._on_food_selected, client_id=self.client_id)
        self.search_bar.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

    def _create_top_bar(self) -> None:
        subtitle = (
            f"Plan alimentaire de {self.client.prenom} {self.client.nom}"
            if self.client
            else "Plan alimentaire"
        )
        hero = HeroBanner(
            self,
            title="Nutrition",
            subtitle=subtitle,
            icon_path="assets/icons/meal-plan.png",
        )
        hero.grid(row=0, column=0, columnspan=3, sticky="ew", padx=8, pady=(6, 6))
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=0, column=0, columnspan=3, sticky="e", padx=16, pady=(0, 0))
        
        # Nouvelles fonctionnalités intelligentes
        PrimaryButton(
            bar, 
            text="🤖 Générer Plan Auto", 
            command=self._generate_automatic_plan,
            width=180
        ).pack(side="right", padx=(0, 8))
        
        SecondaryButton(
            bar,
            text="📊 Analyser Plan",
            command=self._analyze_plan,
            width=140,
        ).pack(side="right", padx=(0, 8))
        
        SecondaryButton(
            bar,
            text="Fiche nutrition",
            command=self._open_fiche_modal,
            width=160,
        ).pack(side="right", padx=(0, 8))
        
        PrimaryButton(bar, text="Exporter en PDF", command=self._export_pdf).pack(
            side="right"
        )

    # Callbacks
    def _set_active_meal(self, repas_id: int) -> None:
        self.active_repas_id = repas_id
        for rid, card in self.meal_cards.items():
            card.set_active(rid == repas_id)

    def _on_food_selected(self, aliment) -> None:
        if self.active_repas_id is None:
            return
        self._open_add_item_popup(aliment)

    def _delete_item(self, item_id: int) -> None:
        self.plan = self.controller.delete_item_from_repas(item_id)
        self._refresh()

    # Add item popup
    def _open_add_item_popup(self, aliment) -> None:
        portions = self.controller.get_portions_for_aliment(aliment.id)
        popup = ctk.CTkToplevel(self)
        popup.title(aliment.nom)
        popup.grab_set()
        try:
            from utils.ui_helpers import bring_to_front
            bring_to_front(popup, make_modal=True)
        except Exception:
            pass

        gram_var = ctk.StringVar(value="100")
        gram_entry = ctk.CTkEntry(popup, textvariable=gram_var)
        gram_entry.pack(padx=10, pady=10)

        portion_names = [p.description for p in portions]
        portion_var = ctk.StringVar(value=portion_names[0] if portion_names else "")

        def on_portion_change(choice):
            idx = portion_names.index(choice)
            gram_var.set(str(portions[idx].grammes_equivalents))

        if portion_names:
            portion_menu = ctk.CTkOptionMenu(
                popup,
                values=portion_names,
                variable=portion_var,
                command=on_portion_change,
            )
            portion_menu.pack(padx=10, pady=10)

        def add_action():
            try:
                grams = float(gram_var.get())
            except ValueError:
                grams = 0.0
            self.plan = self.controller.add_aliment_to_repas(
                self.active_repas_id, aliment.id, grams
            )
            self._refresh()
            popup.destroy()

        ctk.CTkButton(
            popup,
            text="Ajouter",
            command=add_action,
            font=ctk.CTkFont(**ctk.ThemeManager.theme["font"]["Button"]),
        ).pack(pady=10)

    def _export_pdf(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")]
        )
        if path:
            dto = NutritionPageDTO(client=self.client, fiche=self.fiche, plan=self.plan)
            self.controller.export_plan_to_pdf(dto, path)

    def _open_fiche_modal(self) -> None:
        GenerateFicheModal(self)

    def refresh(self) -> None:
        self._refresh()

    # Refresh UI
    def _refresh(self) -> None:
        for repas in self.plan.repas:
            items = [
                {
                    "id": item.id,
                    "label": f"{item.nom} - {item.quantite:.0f}{item.unite}",
                }
                for item in repas.items
            ]
            totals = {
                "kcal": repas.totals_kcal,
                "proteines": repas.totals_proteines,
                "glucides": repas.totals_glucides,
                "lipides": repas.totals_lipides,
            }
            card = self.meal_cards.get(repas.id)
            if card:
                card.update(items, totals)
                card.set_active(repas.id == self.active_repas_id)
        self._update_totals()

    def _update_totals(self) -> None:
        totals = {
            "kcal": self.plan.totals_kcal,
            "proteines": self.plan.totals_proteines,
            "glucides": self.plan.totals_glucides,
            "lipides": self.plan.totals_lipides,
        }
        cible_kcal = self.fiche.objectif_kcal if self.fiche else 0
        cible_p = self.fiche.proteines_g if self.fiche else 0
        cible_g = self.fiche.glucides_g if self.fiche else 0
        cible_l = self.fiche.lipides_g if self.fiche else 0
        self.cal_lbl.configure(text=f"Calories: {totals['kcal']:.0f} / {cible_kcal}")
        self.prot_lbl.configure(
            text=f"Protéines: {totals['proteines']:.1f} / {cible_p}"
        )
        self.carb_lbl.configure(text=f"Glucides: {totals['glucides']:.1f} / {cible_g}")
        self.fat_lbl.configure(text=f"Lipides: {totals['lipides']:.1f} / {cible_l}")

    # --- Nouvelles fonctionnalités intelligentes ---
    
    def _generate_automatic_plan(self) -> None:
        """Génère automatiquement un plan alimentaire intelligent"""
        try:
            # Confirmation avec l'utilisateur
            import tkinter.messagebox as messagebox
            
            confirm = messagebox.askyesno(
                "Génération automatique",
                "Cette action va générer un plan alimentaire personnalisé basé sur votre profil.\n\n"
                "Voulez-vous continuer ?"
            )
            
            if not confirm:
                return
            
            # Génération via le contrôleur
            self.plan = self.controller.generate_automatic_meal_plan(
                client_id=self.client_id,
                nom_plan=f"Plan auto pour {self.client.prenom} {self.client.nom}" if self.client else "Plan automatique"
            )
            
            # Mise à jour de l'interface
            self._refresh()
            
            messagebox.showinfo(
                "Succès",
                "Plan alimentaire généré avec succès !\n\n"
                "Vous pouvez maintenant personnaliser ce plan en ajoutant/supprimant des aliments."
            )
            
        except Exception as e:
            import tkinter.messagebox as messagebox
            print(f"Erreur génération automatique: {e}")
            messagebox.showerror(
                "Erreur", 
                f"Impossible de générer le plan automatique :\n{e}\n\n"
                "Assurez-vous que la base d'aliments contient suffisamment de données."
            )
    
    def _analyze_plan(self) -> None:
        """Analyse le plan alimentaire actuel"""
        try:
            # Analyse via le contrôleur
            analyse = self.controller.analyze_current_plan(self.client_id)
            
            if "erreur" in analyse:
                import tkinter.messagebox as messagebox
                messagebox.showerror("Erreur d'analyse", analyse["erreur"])
                return
            
            # Formatage des résultats
            totaux = analyse.get("totaux", {})
            score = analyse.get("score_equilibre", 0)
            
            # Détermination de la couleur du score
            if score >= 80:
                score_status = "Excellent 🟢"
            elif score >= 60:
                score_status = "Bon 🟡"
            else:
                score_status = "À améliorer 🔴"
            
            # Affichage des résultats
            result_message = f"""📊 ANALYSE NUTRITIONNELLE
            
🔥 Calories totales: {totaux.get('kcal', 0):.0f} kcal
🥩 Protéines: {totaux.get('proteines', 0):.1f}g
🌾 Glucides: {totaux.get('glucides', 0):.1f}g  
🧈 Lipides: {totaux.get('lipides', 0):.1f}g
🌿 Fibres: {totaux.get('fibres', 0):.1f}g

📈 Score d'équilibre: {score}/100 - {score_status}
🍽️ Nombre de repas: {analyse.get('nombre_repas', 0)}

💡 Recommandations:
• Ajoutez plus d'aliments variés pour améliorer l'équilibre
• Privilégiez les aliments riches en fibres
• Équilibrez les sources de protéines"""

            import tkinter.messagebox as messagebox
            messagebox.showinfo("Analyse du Plan", result_message)
            
        except Exception as e:
            import tkinter.messagebox as messagebox
            print(f"Erreur analyse: {e}")
            messagebox.showerror("Erreur", f"Impossible d'analyser le plan :\n{e}")
    
    def _show_nutritional_profile(self) -> None:
        """Affiche ou crée le profil nutritionnel du client"""
        try:
            profil = self.controller.get_nutritional_profile(self.client_id)
            
            if profil:
                # Affichage du profil existant
                profile_info = f"""👤 PROFIL NUTRITIONNEL
                
Informations de base:
• Âge: {profil.age} ans
• Sexe: {profil.sexe}
• Poids: {profil.poids_kg} kg
• Taille: {profil.taille_cm} cm

Objectifs:
• Objectif principal: {profil.objectif_principal}
• Niveau d'activité: {profil.niveau_activite}
• Nombre de repas souhaité: {profil.nombre_repas_souhaite}

Besoins calculés:
• Métabolisme basal: {profil.metabolism_basal or 0:.0f} kcal
• Besoins totaux: {profil.besoins_caloriques or 0:.0f} kcal/jour

Dernière mise à jour: {profil.date_mise_a_jour.strftime('%d/%m/%Y') if profil.date_mise_a_jour else 'N/A'}"""
                
                import tkinter.messagebox as messagebox
                messagebox.showinfo("Profil Nutritionnel", profile_info)
            else:
                # Proposition de créer un profil
                import tkinter.messagebox as messagebox
                create_profile = messagebox.askyesno(
                    "Profil non trouvé",
                    "Aucun profil nutritionnel trouvé pour ce client.\n\n"
                    "Souhaitez-vous créer un profil pour des recommandations personnalisées ?"
                )
                
                if create_profile:
                    self._create_basic_profile()
                    
        except Exception as e:
            import tkinter.messagebox as messagebox
            print(f"Erreur profil: {e}")
            messagebox.showerror("Erreur", f"Impossible d'accéder au profil :\n{e}")
    
    def _create_basic_profile(self) -> None:
        """Crée un profil nutritionnel basique via une interface simple"""
        try:
            # Modal simple pour saisie des données de base
            profile_modal = ctk.CTkToplevel(self)
            profile_modal.title("Création Profil Nutritionnel")
            profile_modal.geometry("400x500")
            profile_modal.grab_set()
            
            # Variables pour la saisie
            age_var = ctk.StringVar(value="30")
            sexe_var = ctk.StringVar(value="M")
            poids_var = ctk.StringVar(value="70")
            taille_var = ctk.StringVar(value="175")
            objectif_var = ctk.StringVar(value="Maintenance")
            activite_var = ctk.StringVar(value="Activité modérée")
            
            # Interface de saisie
            ctk.CTkLabel(profile_modal, text="Création du Profil Nutritionnel", font=("Arial", 16, "bold")).pack(pady=10)
            
            # Âge
            ctk.CTkLabel(profile_modal, text="Âge:").pack(anchor="w", padx=20)
            ctk.CTkEntry(profile_modal, textvariable=age_var, width=100).pack(pady=5)
            
            # Sexe
            ctk.CTkLabel(profile_modal, text="Sexe:").pack(anchor="w", padx=20, pady=(10,0))
            ctk.CTkOptionMenu(profile_modal, variable=sexe_var, values=["M", "F"]).pack(pady=5)
            
            # Poids
            ctk.CTkLabel(profile_modal, text="Poids (kg):").pack(anchor="w", padx=20, pady=(10,0))
            ctk.CTkEntry(profile_modal, textvariable=poids_var, width=100).pack(pady=5)
            
            # Taille
            ctk.CTkLabel(profile_modal, text="Taille (cm):").pack(anchor="w", padx=20, pady=(10,0))
            ctk.CTkEntry(profile_modal, textvariable=taille_var, width=100).pack(pady=5)
            
            # Objectif
            ctk.CTkLabel(profile_modal, text="Objectif principal:").pack(anchor="w", padx=20, pady=(10,0))
            ctk.CTkOptionMenu(
                profile_modal, 
                variable=objectif_var, 
                values=["Perte de poids", "Prise de muscle", "Maintenance", "Performance sportive"]
            ).pack(pady=5)
            
            # Niveau d'activité
            ctk.CTkLabel(profile_modal, text="Niveau d'activité:").pack(anchor="w", padx=20, pady=(10,0))
            ctk.CTkOptionMenu(
                profile_modal, 
                variable=activite_var, 
                values=["Sédentaire", "Activité légère", "Activité modérée", "Activité intense", "Très intense"]
            ).pack(pady=5)
            
            # Boutons
            button_frame = ctk.CTkFrame(profile_modal, fg_color="transparent")
            button_frame.pack(pady=20)
            
            def save_profile():
                try:
                    profile_data = {
                        "age": int(age_var.get()),
                        "sexe": sexe_var.get(),
                        "poids_kg": float(poids_var.get()),
                        "taille_cm": float(taille_var.get()),
                        "objectif_principal": objectif_var.get(),
                        "niveau_activite": activite_var.get(),
                        "nombre_repas_souhaite": 3
                    }
                    
                    profil = self.controller.create_or_update_nutritional_profile(self.client_id, profile_data)
                    
                    if profil:
                        profile_modal.destroy()
                        import tkinter.messagebox as messagebox
                        messagebox.showinfo("Succès", "Profil nutritionnel créé avec succès !")
                    else:
                        import tkinter.messagebox as messagebox
                        messagebox.showerror("Erreur", "Impossible de créer le profil.")
                        
                except ValueError as e:
                    import tkinter.messagebox as messagebox
                    messagebox.showerror("Erreur de saisie", "Veuillez vérifier les valeurs saisies.")
            
            ctk.CTkButton(button_frame, text="Créer", command=save_profile).pack(side="left", padx=10)
            ctk.CTkButton(button_frame, text="Annuler", command=profile_modal.destroy).pack(side="left")
            
        except Exception as e:
            import tkinter.messagebox as messagebox
            print(f"Erreur création profil: {e}")
            messagebox.showerror("Erreur", f"Impossible de créer le profil :\n{e}")

