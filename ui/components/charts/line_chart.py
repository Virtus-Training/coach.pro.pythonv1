import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ui.theme.colors import DARK_BG, DARK_PANEL, PRIMARY, TEXT


class LineChart(ctk.CTkFrame):
    def __init__(
        self,
        master,
        dates: list[str],
        values: list[float],
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
    ) -> None:
        super().__init__(master, fg_color=DARK_PANEL)
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(DARK_PANEL)
        ax = fig.add_subplot(111)
        ax.set_facecolor(DARK_BG)
        ax.plot(dates, values, color=PRIMARY, marker="o")
        ax.set_title(title, color=TEXT)
        ax.set_xlabel(xlabel, color=TEXT)
        ax.set_ylabel(ylabel, color=TEXT)
        ax.tick_params(axis="x", colors=TEXT, rotation=45)
        ax.tick_params(axis="y", colors=TEXT)
        for spine in ax.spines.values():
            spine.set_color(TEXT)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
