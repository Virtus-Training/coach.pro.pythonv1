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
from ui.layout.app_shell import AppShell
from ui.pages.billing_page import BillingPage
from ui.pages.calendar_page import CalendarPage
from ui.pages.client_detail_page import ClientDetailPage
from ui.pages.clients_page import ClientsPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.database_page import DatabasePage
from ui.pages.messaging_page import MessagingPage
from ui.pages.nutrition_page import NutritionPage
from ui.pages.pdf_page import PdfPage
from ui.pages.program_page import ProgramPage
from ui.pages.progress_page import ProgressPage
from ui.pages.session_page import SessionPage


class CoachApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("ui/theme/theme.json")

        self.title("CoachPro – Virtus Training")
        self.geometry("1280x800")
        self.minsize(1000, 700)

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
                "factory": lambda parent: DashboardPage(
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
                "label": "Séances",
                "icon": "clock.png",
                "factory": lambda parent: SessionPage(parent, self.session_controller),
            },
            "progress": {
                "label": "Progression",
                "icon": "chart.png",
                "factory": lambda parent: ProgressPage(parent),
            },
            "pdf": {
                "label": "PDF",
                "icon": "pdf.png",
                "factory": lambda parent: PdfPage(parent),
            },
            "nutrition": {
                "label": "Nutrition",
                "icon": "meal-plan.png",
                "factory": lambda parent: NutritionPage(
                    parent, self.nutrition_controller, client_id=1
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

        self.shell = AppShell(
            self, self.switch_page, self.page_registry, active_module="dashboard"
        )
        self.shell.pack(fill="both", expand=True)

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
        self.shell.header.update_title(title or entry["label"])
        active_name = page_name if page_name in self.page_registry else "dashboard"
        self.shell.sidebar.set_active(active_name)

    def show_client_detail(self, client_id: int) -> None:
        page = ClientDetailPage(
            self.shell.content_area,
            self.client_controller,
            self.nutrition_controller,
            client_id,
        )
        self.shell.set_content(page)
        self.current_page = page
        self.shell.header.update_title("Fiche Client")

    def show_clients_page(self) -> None:
        self.switch_page("clients")


def launch_app():
    app = CoachApp()
    app.mainloop()
