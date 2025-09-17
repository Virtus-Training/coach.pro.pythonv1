# app.py

import customtkinter as ctk

from controllers.calendar_controller import CalendarController
from controllers.client_controller import ClientController
from controllers.dashboard_controller import DashboardController
from controllers.nutrition_controller import NutritionController
from controllers.session_controller import SessionController
from controllers.tracking_controller import TrackingController
from repositories.aliment_repo import AlimentRepository
from repositories.client_repo import ClientRepository
from repositories.exercices_repo import ExerciseRepository
from repositories.fiche_nutrition_repo import FicheNutritionRepository
from repositories.plan_alimentaire_repo import PlanAlimentaireRepository
from repositories.resultat_exercice_repo import ResultatExerciceRepository
from repositories.sessions_repo import SessionsRepository
from services.calendar_service import CalendarService
from services.client_service import ClientService
from services.dashboard_service import DashboardService
from services.exercise_service import ExerciseService
from services.nutrition_service import NutritionService
from services.plan_alimentaire_service import PlanAlimentaireService
from services.session_service import SessionService
from services.tracking_service import TrackingService
from ui.layout.modern_app_shell import ModernAppShell
from ui.pages.billing_page import BillingPage
from ui.pages.calendar_page import CalendarPage
from ui.pages.client_detail_page import ClientDetailPage
from ui.pages.clients_page import ClientsPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.database_page import DatabasePage
from ui.pages.messaging_page import MessagingPage
from ui.pages.modern_dashboard_page import ModernDashboardPage
from ui.pages.nutrition_page import NutritionPage
from ui.pages.nutrition_page_2025_simple import NutritionPage2025
from ui.pages.professional_pdf_templates_page import ProfessionalPdfTemplatesPage
from ui.pages.program_page import ProgramPage
from ui.pages.progress_page import ProgressPage
from ui.pages.saved_sessions_page import SavedSessionsPage
from ui.pages.session_page import SessionPage


class CoachApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("ui/theme/theme.json")

        # 🚀 Configuration interface nutrition - basculer entre ancienne et nouvelle version
        self.use_nutrition_2025 = True  # Mettre à False pour utiliser l'ancienne interface

        self.title("CoachPro – Virtus Training")
        self.geometry("1280x800")
        self.minsize(1000, 700)
        # Ensure clean window title (override any garbled text)
        try:
            self.title("CoachPro – Virtus Training")
        except Exception:
            self.title("CoachPro - Virtus Training")

        self.current_page = None

        client_repo = ClientRepository()
        client_service = ClientService(client_repo)
        self.client_controller = ClientController(client_service)

        sessions_repo = SessionsRepository()
        dashboard_service = DashboardService(client_repo, sessions_repo)
        self.dashboard_controller = DashboardController(dashboard_service)

        fiche_repo = FicheNutritionRepository()
        aliment_repo = AlimentRepository()
        plan_repo = PlanAlimentaireRepository()
        nutrition_service = NutritionService(fiche_repo, aliment_repo)
        plan_service = PlanAlimentaireService(plan_repo)
        self.nutrition_controller = NutritionController(
            nutrition_service, plan_service, client_service
        )

        session_service = SessionService(sessions_repo)
        exercise_repo = ExerciseRepository()
        exercise_service = ExerciseService(exercise_repo)
        self.session_controller = SessionController(
            session_service, client_service, exercise_service
        )

        result_repo = ResultatExerciceRepository()
        tracking_service = TrackingService(result_repo)
        self.tracking_controller = TrackingController(
            tracking_service, session_service, exercise_repo
        )

        calendar_service = CalendarService(sessions_repo)
        self.calendar_controller = CalendarController(calendar_service, session_service)

        self.page_registry = {
            "dashboard": {
                "label": "Tableau de bord",
                "icon": "layout-dashboard.png",
                "factory": lambda parent: ModernDashboardPage(
                    parent, self.dashboard_controller
                ),
            },
            "programs": {
                "label": "Programmes",
                "icon": "dumbbell.png",
                "factory": lambda parent: ProgramPage(parent),
            },
            "calendar": {
                "label": "Calendrier",
                "icon": "calendar.png",
                "factory": lambda parent: CalendarPage(
                    parent,
                    self.calendar_controller,
                    self.session_controller,
                    self.tracking_controller,
                ),
            },
            "sessions": {
                "label": "Créer Séance",
                "icon": "clock.png",
                "factory": lambda parent: SessionPage(parent, self.session_controller),
            },
            "saved_sessions": {
                "label": "Mes Séances",
                "icon": "chart.png",
                "factory": lambda parent: SavedSessionsPage(
                    parent, self.session_controller, self
                ),
            },
            "progress": {
                "label": "Progression",
                "icon": "chart.png",
                "factory": lambda parent: ProgressPage(parent),
            },
            "pdf": {
                "label": "PDF",
                "icon": "pdf.png",
                "factory": lambda parent: ProfessionalPdfTemplatesPage(parent),
            },
            "nutrition": {
                "label": "Nutrition" + (" 2025" if self.use_nutrition_2025 else ""),
                "icon": "meal-plan.png",
                "factory": lambda parent: (
                    NutritionPage2025(parent, self.nutrition_controller, client_id=1)
                    if self.use_nutrition_2025
                    else NutritionPage(parent, self.nutrition_controller, client_id=1)
                ),
            },
            "database": {
                "label": "Base de données",
                "icon": "database.png",
                "factory": lambda parent: DatabasePage(parent),
            },
            "clients": {
                "label": "Clients",
                "icon": "users.png",
                "factory": lambda parent: ClientsPage(parent, self.client_controller),
            },
            "messaging": {
                "label": "Messagerie",
                "icon": "chat.png",
                "factory": lambda parent: MessagingPage(parent),
            },
            "billing": {
                "label": "Facturation",
                "icon": "billing.png",
                "factory": lambda parent: BillingPage(parent),
            },
            "settings": {
                "label": "Paramètres",
                "icon": "settings.png",
                "factory": lambda parent: DashboardPage(
                    parent, self.dashboard_controller
                ),
            },
        }

        # Modern App shell with enhanced UI
        self.shell = ModernAppShell(
            self, self.switch_page, self.page_registry, active_module="dashboard"
        )
        self.shell.pack(fill="both", expand=True)

        # Enable modern theme and effects
        self.configure(fg_color=ctk.ThemeManager.theme["color"]["surface_dark"])

        self.switch_page("dashboard")

    def switch_page(self, page_name: str, title: str | None = None):
        # Détruit la page actuelle si elle existe
        if self.current_page:
            self.current_page.destroy()

        # Crée la nouvelle page et l'assigne à self.current_page
        entry = self.page_registry.get(page_name, self.page_registry["dashboard"])
        self.current_page = entry["factory"](self.shell.content_area)

        # Définit le contenu de la coquille (shell)
        self.shell.set_content(self.current_page)
        # ModernHeader expose update_page, pas update_title
        self.shell.header.update_page(title or entry["label"])
        active_name = page_name if page_name in self.page_registry else "dashboard"
        self.shell.sidebar.set_active(active_name)

    def show_client_detail(
        self, client_id: int, default_tab: str | None = None
    ) -> None:
        page = ClientDetailPage(
            self.shell.content_area,
            self.client_controller,
            self.nutrition_controller,
            client_id,
            default_tab=default_tab,
        )
        self.shell.set_content(page)
        self.current_page = page
        self.shell.header.update_title("Fiche Client")

    def show_clients_page(self) -> None:
        self.switch_page("clients")

    def toggle_nutrition_interface(self) -> None:
        """🔄 Bascule entre l'ancienne et la nouvelle interface nutrition"""
        self.use_nutrition_2025 = not self.use_nutrition_2025

        # Mettre à jour le label dans le registre
        self.page_registry["nutrition"]["label"] = "Nutrition" + (" 2025" if self.use_nutrition_2025 else "")

        # Si on est actuellement sur la page nutrition, la recharger
        if hasattr(self, 'current_page') and self.current_page:
            # Vérifier si c'est une page nutrition
            if isinstance(self.current_page, (NutritionPage, NutritionPage2025)):
                self.switch_page("nutrition")


def launch_app():
    app = CoachApp()
    app.mainloop()
