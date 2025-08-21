import customtkinter as ctk

from controllers.nutrition_controller import NutritionController


class FoodSearchBar(ctk.CTkFrame):
    def __init__(
        self,
        master,
        controller: NutritionController,
        on_food_selected_callback,
    ):
        super().__init__(master)
        self.on_food_selected_callback = on_food_selected_callback
        self.controller = controller

        self.search_var = ctk.StringVar()
        entry = ctk.CTkEntry(self, textvariable=self.search_var)
        entry.pack(fill="x", padx=5, pady=5)
        self.search_var.trace_add("write", lambda *args: self.on_search_change())

        self.results_frame = ctk.CTkScrollableFrame(self)
        self.results_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def on_search_change(self) -> None:
        query = self.search_var.get().strip()
        results = []
        if query:
            results = self.controller.search_aliments(query)
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        for aliment in results:
            btn = ctk.CTkButton(
                self.results_frame,
                text=aliment.nom,
                anchor="w",
                command=lambda a=aliment: self.on_food_selected_callback(a),
            )
            btn.pack(fill="x", padx=2, pady=2)
