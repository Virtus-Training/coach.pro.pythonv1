# app.py

import customtkinter as ctk

from controllers.client_controller import ClientController
from controllers.nutrition_controller import NutritionController
from repositories.aliment_repo import AlimentRepository
from repositories.client_repo import ClientRepository
from repositories.fiche_nutrition_repo import FicheNutritionRepository
from repositories.plan_alimentaire_repo import PlanAlimentaireRepository
from services.client_service import ClientService
from services.nutrition_service import NutritionService
from services.plan_alimentaire_service import PlanAlimentaireService
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
        self.title("CoachPro – Virtus Training")
        self.geometry("1280x800")
        self.minsize(1000, 700)
        self.configure(fg_color="#0f0f0f")

        self.shell = AppShell(self, self.switch_page, active_module="dashboard")
        self.shell.pack(fill="both", expand=True)

        self.current_page = None

        client_repo = ClientRepository()
        client_service = ClientService(client_repo)
        self.client_controller = ClientController(client_service)

        fiche_repo = FicheNutritionRepository()
        aliment_repo = AlimentRepository()
        plan_repo = PlanAlimentaireRepository()
        nutrition_service = NutritionService(fiche_repo, aliment_repo)
        plan_service = PlanAlimentaireService(plan_repo)
        self.nutrition_controller = NutritionController(
            nutrition_service, plan_service, client_service
        )

        self.page_titles = {
            "dashboard": "Tableau de bord",
            "programs": "Programmes",
            "calendar": "Calendrier",
            "sessions": "Séances",
            "progress": "Progression",
            "pdf": "PDF",
            "nutrition": "Nutrition",
            "database": "Base de données",
            "clients": "Gestion des Clients",
            "messaging": "Messagerie",
            "billing": "Facturation",
            "settings": "Paramètres",
        }

        self.switch_page("dashboard")

    def switch_page(self, page_name: str, title: str | None = None):
        if self.current_page:
            self.current_page.destroy()

        match page_name:
            case "dashboard":
                self.current_page = DashboardPage(self.shell.content_area)
            case "programs":
                self.current_page = ProgramPage(self.shell.content_area)
            case "sessions":
                self.current_page = SessionPage(self.shell.content_area)
            case "calendar":
                self.current_page = CalendarPage(self.shell.content_area)
            case "nutrition":
                self.current_page = NutritionPage(
                    self.shell.content_area, self.nutrition_controller, client_id=1
                )
            case "database":
                self.current_page = DatabasePage(self.shell.content_area)
            case "progress":
                self.current_page = ProgressPage(self.shell.content_area)
            case "pdf":
                self.current_page = PdfPage(self.shell.content_area)
            case "clients":
                self.current_page = ClientsPage(self.shell.content_area, self.client_controller)
            case "messaging":
                self.current_page = MessagingPage(self.shell.content_area)
            case "billing":
                self.current_page = BillingPage(self.shell.content_area)
            case _:
                self.current_page = DashboardPage(self.shell.content_area)

        self.shell.set_content(self.current_page)
        self.shell.header.update_title(title or self.page_titles.get(page_name, ""))
        self.shell.sidebar.set_active(page_name)

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
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = CoachApp()
    app.mainloop()
