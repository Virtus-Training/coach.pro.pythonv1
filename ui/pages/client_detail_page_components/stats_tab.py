import customtkinter as ctk

from controllers.tracking_controller import TrackingController
from repositories.exercices_repo import ExerciseRepository
from repositories.resultat_exercice_repo import ResultatExerciceRepository
from repositories.sessions_repo import SessionsRepository
from services.session_service import SessionService
from services.tracking_service import TrackingService
from ui.components.charts.line_chart import LineChart


class StatsTab(ctk.CTkFrame):
    def __init__(self, master, client_id: int):
        super().__init__(master, fg_color="transparent")
        self.client_id = client_id
        self.tracking_controller = TrackingController(
            TrackingService(ResultatExerciceRepository()),
            SessionService(SessionsRepository()),
            ExerciseRepository(),
        )
        self.chart: LineChart | None = None

        control = ctk.CTkFrame(self, fg_color="transparent")
        control.pack(fill="x", padx=10, pady=10)

        self.colors = ctk.ThemeManager.theme["color"]
        ctk.CTkLabel(
            control,
            text="Sélectionner un exercice pour voir la progression",
            text_color=self.colors["primary_text"],
        ).pack(anchor="w")

        tracked = self.tracking_controller.get_tracked_exercises(self.client_id)
        self.ex_options = {ex.name: ex.id for ex in tracked}
        self.var = ctk.StringVar(value="Sélectionner un exercice")
        ctk.CTkComboBox(
            control,
            values=list(self.ex_options.keys()),
            variable=self.var,
            command=self._on_select,
            fg_color=self.colors["surface_light"],
            button_color=self.colors["surface_light"],
            button_hover_color=self.colors["primary"],
            text_color=self.colors["primary_text"],
            state="readonly",
        ).pack(anchor="w", pady=(5, 0))

        self.graph_frame = ctk.CTkFrame(self, fg_color=self.colors["surface_light"])
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self._show_message(
            "Sélectionnez un exercice pour afficher le graphique de progression"
        )

    def _clear_graph(self) -> None:
        if self.chart:
            self.chart.destroy()
            self.chart = None
        for w in self.graph_frame.winfo_children():
            w.destroy()

    def _show_message(self, message: str) -> None:
        self._clear_graph()
        ctk.CTkLabel(
            self.graph_frame, text=message, text_color=self.colors["primary_text"]
        ).pack(expand=True)

    def _on_select(self, choice: str) -> None:
        ex_id = self.ex_options.get(choice)
        if not ex_id:
            self._show_message(
                "Sélectionnez un exercice pour afficher le graphique de progression"
            )
            return

        progression = self.tracking_controller.get_exercise_progression(
            self.client_id, ex_id
        )
        if not progression.dates:
            self._show_message("Aucune donnée disponible pour cet exercice")
            return

        self._clear_graph()
        self.chart = LineChart(
            self.graph_frame,
            progression.dates,
            progression.poids,
            title=f"Évolution de la charge - {choice}",
            xlabel="Date de séance",
            ylabel="Charge (kg)",
        )
        self.chart.pack(fill="both", expand=True)
