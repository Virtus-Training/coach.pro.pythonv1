import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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
        colors = ctk.ThemeManager.theme["color"]
        super().__init__(master, fg_color=colors["surface_light"])
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(colors["surface_light"])
        ax = fig.add_subplot(111)
        ax.set_facecolor(colors["surface_dark"])
        ax.plot(dates, values, color=colors["primary"], marker="o")
        ax.set_title(title, color=colors["primary_text"])
        ax.set_xlabel(xlabel, color=colors["primary_text"])
        ax.set_ylabel(ylabel, color=colors["primary_text"])
        ax.tick_params(axis="x", colors=colors["primary_text"], rotation=45)
        ax.tick_params(axis="y", colors=colors["primary_text"])
        for spine in ax.spines.values():
            spine.set_color(colors["primary_text"])
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
