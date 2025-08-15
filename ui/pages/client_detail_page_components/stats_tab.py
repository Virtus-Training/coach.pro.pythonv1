import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from repositories.seance_repo import SeanceRepository
from repositories.exercices_repo import ExerciseRepository
from ui.theme.colors import DARK_BG, DARK_PANEL, PRIMARY, TEXT


class StatsTab(ctk.CTkFrame):
    def __init__(self, master, client_id: int):
        super().__init__(master, fg_color="transparent")
        self.client_id = client_id
        self.seance_repo = SeanceRepository()
        self.exercice_repo = ExerciseRepository()
        self.canvas: FigureCanvasTkAgg | None = None

        control = ctk.CTkFrame(self, fg_color="transparent")
        control.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            control,
            text="Sélectionner un exercice pour voir la progression",
            text_color=TEXT,
        ).pack(anchor="w")

        exercices = self.exercice_repo.list_all_exercices()
        self.ex_options = {ex.nom: ex.id for ex in exercices}
        self.var = ctk.StringVar(value="Sélectionner un exercice")
        ctk.CTkOptionMenu(
            control,
            values=list(self.ex_options.keys()),
            variable=self.var,
            command=self._on_select,
            fg_color=DARK_PANEL,
            button_color=DARK_PANEL,
            button_hover_color=PRIMARY,
            text_color=TEXT,
        ).pack(anchor="w", pady=(5, 0))

        self.graph_frame = ctk.CTkFrame(self, fg_color=DARK_PANEL)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self._show_message(
            "Sélectionnez un exercice pour afficher le graphique de progression"
        )

    def _clear_graph(self) -> None:
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        for w in self.graph_frame.winfo_children():
            w.destroy()

    def _show_message(self, message: str) -> None:
        self._clear_graph()
        ctk.CTkLabel(
            self.graph_frame, text=message, text_color=TEXT
        ).pack(expand=True)

    def _on_select(self, choice: str) -> None:
        ex_id = self.ex_options.get(choice)
        if not ex_id:
            self._show_message(
                "Sélectionnez un exercice pour afficher le graphique de progression"
            )
            return

        history = self.seance_repo.get_exercice_history(self.client_id, ex_id)
        if not history:
            self._show_message("Aucune donnée disponible pour cet exercice")
            return

        self._clear_graph()
        dates = [h["date"] for h in history]
        charges = [h["max_charge"] for h in history]

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(DARK_PANEL)
        ax = fig.add_subplot(111)
        ax.set_facecolor(DARK_BG)
        ax.plot(dates, charges, color=PRIMARY, marker="o")
        ax.set_title(f"Évolution de la charge - {choice}", color=TEXT)
        ax.set_xlabel("Date de séance", color=TEXT)
        ax.set_ylabel("Charge max (kg)", color=TEXT)
        ax.tick_params(axis="x", colors=TEXT, rotation=45)
        ax.tick_params(axis="y", colors=TEXT)
        for spine in ax.spines.values():
            spine.set_color(TEXT)

        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
