import customtkinter as ctk
from ui.components.tabbar import CustomTabBar
from ui.theme.fonts import get_title_font, get_section_font, get_text_font, get_small_font
from ui.theme.colors import PRIMARY, DARK_BG, DARK_PANEL, TEXT, TEXT_SECONDARY
from PIL import Image

class DatabasePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=DARK_BG)
        self.active_tab = "exercises"

        # Header
        header = ctk.CTkFrame(self, fg_color=PRIMARY, corner_radius=10)
        header.pack(fill="x", padx=20, pady=20)

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkLabel(title_row, text="🗃️", font=get_title_font()).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(title_row, text="Bases de Données", font=get_title_font(), text_color="white").pack(side="left")

        ctk.CTkLabel(header, text="Gérez vos bases de données d'exercices, d'aliments et de programmes.",
                     font=get_text_font(), text_color="#dbeafe").pack(anchor="w", padx=20, pady=(5, 15))

        # Tabs (Custom)
        self.tabs = [
            {"id": "exercises", "name": "Exercices", "icon": "dumbbell.png", "count": "150+"},
            {"id": "foods", "name": "Aliments", "icon": "apple.png", "count": "300+"},
            {"id": "training-programs", "name": "Programmes", "icon": "target.png", "count": "25+"},
            {"id": "nutrition-plans", "name": "Plans Nutrition", "icon": "meal-plan.png", "count": "15+"}
        ]


        self.tabbar = CustomTabBar(self, self.tabs, self.switch_tab, self.active_tab)
        self.tabbar.pack(fill="x", padx=20)

        # Contenu dynamique
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.update_content()

    def switch_tab(self, tab_id):
        self.active_tab = tab_id
        self.update_content()

    def update_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        match self.active_tab:
            case "exercises":
                self.init_exercises_tab(self.content_frame)
            case "foods":
                self.init_foods_tab(self.content_frame)
            case "training-programs":
                self.init_programs_tab(self.content_frame)
            case "nutrition-plans":
                self.init_nutrition_tab(self.content_frame)

    def init_exercises_tab(self, frame):
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for i in range(10):
            row = ctk.CTkFrame(scroll, fg_color=DARK_PANEL, corner_radius=8)
            row.pack(fill="x", padx=10, pady=4)
            ctk.CTkLabel(row, text=f"Exercice {i+1}", font=get_text_font(), text_color=TEXT).pack(side="left", padx=10)


    def init_foods_tab(self, frame):
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for i in range(10):
            row = ctk.CTkFrame(scroll, fg_color=DARK_PANEL, corner_radius=8)
            row.pack(fill="x", padx=10, pady=4)
            ctk.CTkLabel(row, text=f"Aliment {i+1}", font=get_text_font(), text_color=TEXT).pack(side="left", padx=10)
            

    def init_programs_tab(self, frame):
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for i in range(4):
            card = ctk.CTkFrame(scroll, fg_color=DARK_PANEL, corner_radius=10)
            card.pack(fill="x", pady=10, padx=10)
            ctk.CTkLabel(card, text=f"Programme {i+1}", font=get_section_font(), text_color=TEXT).pack(anchor="w", padx=20, pady=(10, 2))
            ctk.CTkLabel(card, text="Objectif : prise de masse - 4 semaines", font=get_text_font(), text_color=TEXT_SECONDARY).pack(anchor="w", padx=20, pady=(0, 10))
            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(anchor="e", padx=20, pady=(0, 10))
            ctk.CTkButton(actions, text="Modifier").pack(side="left", padx=5)
            ctk.CTkButton(actions, text="Supprimer").pack(side="left", padx=5)

    def init_nutrition_tab(self, frame):
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        for i in range(4):
            card = ctk.CTkFrame(scroll, fg_color=DARK_PANEL, corner_radius=10)
            card.pack(fill="x", pady=10, padx=10)
            ctk.CTkLabel(card, text=f"Plan Nutritionnel {i+1}", font=get_section_font(), text_color=TEXT).pack(anchor="w", padx=20, pady=(10, 2))
            ctk.CTkLabel(card, text="Type : perte de poids - 1800 kcal", font=get_text_font(), text_color=TEXT_SECONDARY).pack(anchor="w", padx=20, pady=(0, 10))
            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(anchor="e", padx=20, pady=(0, 10))
            ctk.CTkButton(actions, text="Modifier").pack(side="left", padx=5)
            ctk.CTkButton(actions, text="Supprimer").pack(side="left", padx=5)
