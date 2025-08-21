# app.py

import customtkinter as ctk

from ui.layout.header import Header
from ui.layout.sidebar import Sidebar
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

from controllers.client_controller import ClientController
from repositories.client_repo import ClientRepository
from services.client_service import ClientService


class CoachApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CoachPro – Virtus Training")
        self.geometry("1280x800")
        self.minsize(1000, 700)
        self.configure(fg_color="#0f0f0f")

        # Layout de la fenêtre principale
        self.sidebar = Sidebar(self, self.switch_page, active_module="dashboard")
        self.sidebar.pack(side="left", fill="y")

        self.header = Header(self)
        self.header.pack(fill="x", side="top")

        self.main_frame = ctk.CTkFrame(self, fg_color="#1f1f1f")
        self.main_frame.pack(side="left", fill="both", expand=True)

        self.current_page = None
        self.clients_page = None
        self.client_detail_page = None

        repo = ClientRepository()
        service = ClientService(repo)
        self.client_controller = ClientController(service)

        self.switch_page("dashboard")  # Page par défaut

    def switch_page(self, page_name):
        # Détruire la page précédente
        if self.current_page:
            self.current_page.destroy()

        self.header.update_title("Nom de la page actuelle")

        # Sélectionner et afficher la bonne page
        match page_name:
            case "dashboard":
                self.current_page = DashboardPage(self.main_frame)
            case "programs":
                self.current_page = ProgramPage(self.main_frame)
            case "sessions":
                self.current_page = SessionPage(self.main_frame)
            case "calendar":
                self.current_page = CalendarPage(self.main_frame)
            case "nutrition":
                self.current_page = NutritionPage(self.main_frame, client_id=1)
                self.header.update_title("Nutrition")
            case "database":
                self.current_page = DatabasePage(self.main_frame)
            case "progress":
                self.current_page = ProgressPage(self.main_frame)
            case "pdf":
                self.current_page = PdfPage(self.main_frame)
            case "clients":
                self.clients_page = ClientsPage(self.main_frame, self.client_controller)
                self.current_page = self.clients_page
            case "messaging":
                self.current_page = MessagingPage(self.main_frame)
            case "billing":
                self.current_page = BillingPage(self.main_frame)
            case _:
                self.current_page = DashboardPage(self.main_frame)

        self.current_page.pack(fill="both", expand=True)

    def show_client_detail(self, client_id: int) -> None:
        """Affiche la page de détail d'un client."""
        if self.clients_page:
            self.clients_page.pack_forget()
        self.client_detail_page = ClientDetailPage(
            self.main_frame, self.client_controller, client_id
        )
        self.client_detail_page.pack(fill="both", expand=True)
        self.current_page = self.client_detail_page

    def show_clients_page(self) -> None:
        """Revient à la page de liste des clients."""
        if self.client_detail_page:
            self.client_detail_page.pack_forget()
            self.client_detail_page.destroy()
            self.client_detail_page = None
        if self.clients_page:
            self.clients_page.pack(fill="both", expand=True)
            self.current_page = self.clients_page


def launch_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = CoachApp()
    app.mainloop()
