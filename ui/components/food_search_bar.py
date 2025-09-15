import customtkinter as ctk

from controllers.nutrition_controller import NutritionController


class FoodSearchBar(ctk.CTkFrame):
    def __init__(
        self,
        master,
        controller: NutritionController,
        on_food_selected_callback,
        client_id: int = None,
    ):
        super().__init__(master)
        self.on_food_selected_callback = on_food_selected_callback
        self.controller = controller
        self.client_id = client_id

        # En-tête de recherche
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        ctk.CTkLabel(
            header_frame, 
            text="🔍 Recherche d'aliments", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")

        # Barre de recherche principale
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self, 
            textvariable=self.search_var,
            placeholder_text="Rechercher un aliment..."
        )
        self.search_entry.pack(fill="x", padx=5, pady=5)
        self.search_var.trace_add("write", lambda *args: self.on_search_change())

        # Options de filtrage rapide
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        self.filter_var = ctk.StringVar(value="Tous")
        self.filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.filter_var,
            values=["Tous", "Riches en protéines", "Faibles en calories", "Riches en fibres"],
            command=self.on_filter_change,
            width=150
        )
        self.filter_menu.pack(side="left", padx=(0, 5))

        # Suggestions personnalisées
        if self.client_id:
            self.suggestions_btn = ctk.CTkButton(
                filter_frame,
                text="💡 Suggestions",
                command=self.show_suggestions,
                width=100,
                height=28
            )
            self.suggestions_btn.pack(side="right")

        # Zone de résultats
        self.results_frame = ctk.CTkScrollableFrame(self, height=300)
        self.results_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Affichage initial des suggestions
        if self.client_id:
            self.show_suggestions()

    def on_search_change(self) -> None:
        """Déclenché lors de la modification de la recherche"""
        query = self.search_var.get().strip()
        
        # Annuler la recherche précédente s'il y en avait une
        if hasattr(self, '_search_job'):
            self.after_cancel(self._search_job)
        
        if len(query) < 2:
            # Afficher les suggestions si pas de recherche
            if self.client_id:
                self.show_suggestions()
            else:
                self.clear_results()
            return
        
        # Délai pour éviter trop de requêtes
        self._search_job = self.after(300, lambda: self.perform_search(query))
    
    def perform_search(self, query: str) -> None:
        """Effectue la recherche d'aliments"""
        try:
            # Construction des filtres basés sur l'option sélectionnée
            filters = self.get_current_filters()
            
            # Recherche avancée via le contrôleur
            results = self.controller.search_aliments_advanced(query, filters)
            
            self.display_results(results, f"Résultats pour '{query}'")
            
        except Exception as e:
            print(f"Erreur recherche: {e}")
            # Fallback sur la recherche basique
            results = self.controller.search_aliments(query)
            self.display_results(results, f"Résultats pour '{query}'")
    
    def get_current_filters(self) -> dict:
        """Construit les filtres basés sur la sélection actuelle"""
        filter_option = self.filter_var.get()
        
        filters = {}
        
        if filter_option == "Riches en protéines":
            filters["proteines_min"] = 15.0
        elif filter_option == "Faibles en calories":
            filters["kcal_max"] = 150.0
        elif filter_option == "Riches en fibres":
            # Utiliser une valeur par défaut raisonnable pour les fibres
            filters["limit"] = 20
        
        return filters
    
    def on_filter_change(self, value: str) -> None:
        """Déclenché lors du changement de filtre"""
        query = self.search_var.get().strip()
        if len(query) >= 2:
            self.perform_search(query)
        elif self.client_id:
            self.show_suggestions()
    
    def show_suggestions(self) -> None:
        """Affiche les suggestions personnalisées"""
        try:
            if not self.client_id:
                return
            
            suggestions = self.controller.get_food_suggestions(self.client_id, limit=8)
            self.display_results(suggestions, "💡 Suggestions pour vous")
            
        except Exception as e:
            print(f"Erreur suggestions: {e}")
            self.clear_results()
    
    def display_results(self, aliments: list, title: str = "Résultats") -> None:
        """Affiche les résultats de recherche"""
        # Nettoyer les résultats existants
        self.clear_results()
        
        if not aliments:
            no_result_label = ctk.CTkLabel(
                self.results_frame,
                text="Aucun résultat trouvé.\nEssayez d'élargir vos critères.",
                text_color=("gray60", "gray40")
            )
            no_result_label.pack(pady=20)
            return
        
        # Titre des résultats
        title_label = ctk.CTkLabel(
            self.results_frame,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        title_label.pack(anchor="w", padx=5, pady=(5, 10))
        
        # Affichage des aliments
        for aliment in aliments:
            self.create_food_item(aliment)
    
    def create_food_item(self, aliment) -> None:
        """Crée un élément d'aliment dans les résultats"""
        item_frame = ctk.CTkFrame(self.results_frame, fg_color=("gray90", "gray20"))
        item_frame.pack(fill="x", padx=2, pady=2)
        
        # Configuration du layout
        item_frame.grid_columnconfigure(0, weight=1)
        
        # Nom de l'aliment
        name_btn = ctk.CTkButton(
            item_frame,
            text=aliment.nom,
            anchor="w",
            fg_color="transparent",
            text_color=("black", "white"),
            hover_color=("gray80", "gray30"),
            command=lambda: self.on_food_selected_callback(aliment),
            font=ctk.CTkFont(size=11, weight="bold")
        )
        name_btn.grid(row=0, column=0, sticky="ew", padx=(8, 2), pady=(4, 2))
        
        # Informations nutritionnelles
        nutrition_text = f"{aliment.kcal_100g:.0f} kcal | {aliment.proteines_100g:.1f}g prot"
        if hasattr(aliment, 'categorie') and aliment.categorie:
            nutrition_text += f" | {aliment.categorie}"
        
        nutrition_label = ctk.CTkLabel(
            item_frame,
            text=nutrition_text,
            font=ctk.CTkFont(size=9),
            text_color=("gray60", "gray50"),
            anchor="w"
        )
        nutrition_label.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 4))
        
        # Score de qualité si disponible
        if hasattr(aliment, 'indice_healthy') and aliment.indice_healthy:
            score_color = "green" if aliment.indice_healthy >= 7 else "orange" if aliment.indice_healthy >= 4 else "red"
            score_label = ctk.CTkLabel(
                item_frame,
                text=f"⭐{aliment.indice_healthy}",
                font=ctk.CTkFont(size=9),
                text_color=score_color
            )
            score_label.grid(row=0, rowspan=2, column=1, padx=(2, 8), pady=4)
    
    def clear_results(self) -> None:
        """Nettoie les résultats affichés"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

