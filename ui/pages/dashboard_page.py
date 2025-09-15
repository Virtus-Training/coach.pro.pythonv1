#!/usr/bin/env python3
# ui/pages/dashboard_page.py

import customtkinter as ctk
from PIL import Image

from controllers.dashboard_controller import DashboardController
from ui.components.card import IconCard
from ui.components.design_system import HeroBanner, PrimaryButton
from ui.components.title import SectionTitle


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller: DashboardController):
        super().__init__(parent)
        self.controller = controller
        colors = ctk.ThemeManager.theme["color"]
        fonts = ctk.ThemeManager.theme["font"]
        self.configure(fg_color=colors["surface_dark"])

        data = self.controller.get_dashboard_data()

        # Header hero
        hero = HeroBanner(
            self,
            title="Tableau de bord",
            subtitle="Vue d’ensemble des activités et raccourcis.",
            icon_path="assets/icons/layout-dashboard.png",
        )
        hero.pack(fill="x", padx=12, pady=(6, 8))

        # Scrollable container
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # === SECTION HAUTE : Rappel + KPI + Raccourcis ===

        # Bloc Rappel du jour
        reminder_frame = ctk.CTkFrame(
            scroll, fg_color=colors["surface_light"], corner_radius=10
        )
        reminder_frame.pack(fill="x", padx=10, pady=(0, 20))
        ctk.CTkLabel(
            reminder_frame,
            text="🗓️ Aujourd’hui : 3 séances prévues, 2 suivis clients, 1 export PDF",
            font=ctk.CTkFont(**fonts["Body"]),
            text_color=colors["primary_text"],
            anchor="w",
        ).pack(padx=20, pady=10, anchor="w")

        # Bloc KPI horizontal
        quick_kpi = ctk.CTkFrame(scroll, fg_color="transparent")
        quick_kpi.pack(fill="x", padx=10, pady=(0, 10))

        def mini_kpi(title, value):
            box = ctk.CTkFrame(
                quick_kpi,
                fg_color=colors["surface_light"],
                corner_radius=8,
                width=180,
            )
            box.pack(side="left", expand=True, fill="both", padx=6)
            ctk.CTkLabel(
                box,
                text=title,
                text_color=colors["secondary_text"],
                font=ctk.CTkFont(**fonts["Small"]),
            ).pack(pady=(10, 2))
            ctk.CTkLabel(
                box,
                text=value,
                font=ctk.CTkFont(**fonts["H1"]),
                text_color=colors["primary"],
            ).pack(pady=(0, 10))

        mini_kpi("Clients actifs", str(data.active_clients))
        mini_kpi("Séances ce mois", str(data.sessions_this_month))
        mini_kpi(
            "Taux de complétion",
            f"{int(data.average_session_completion_rate * 100)}%",
        )

        # Boutons d’action rapide
        shortcuts = ctk.CTkFrame(scroll, fg_color="transparent")
        shortcuts.pack(fill="x", padx=10, pady=20)

        def shortcut_btn(text, emoji=""):
            return ctk.CTkButton(
                shortcuts,
                text=f"{emoji} {text}",
                font=ctk.CTkFont(**fonts["Body"]),
                fg_color=colors["primary"],
                hover_color="#06B6D4",
                corner_radius=6,
                height=36,
                text_color=colors["surface_dark"],
            )

        btn_session = shortcut_btn("Nouvelle séance", "➕")
        btn_session.configure(
            command=lambda: self.winfo_toplevel().switch_page("sessions")
        )
        btn_session.pack(side="left", padx=5)
        btn_client = shortcut_btn("Importer client", "📥")
        btn_client.configure(
            command=lambda: self.winfo_toplevel().switch_page("clients")
        )
        btn_client.pack(side="left", padx=5)
        shortcut_btn("Exporter PDF", "📄").pack(side="left", padx=5)
        shortcut_btn("Paramètres", "⚙️").pack(side="left", padx=5)
        shortcut_btn("Suivi progression", "📈").pack(side="left", padx=5)
        shortcut_btn("Plan nutrition", "🥗").pack(side="left", padx=5)
        shortcut_btn("Planning", "🗓️").pack(side="left", padx=5)

        grid_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        grid_frame.pack(pady=10)

        for col in range(4):
            grid_frame.grid_columnconfigure(col, weight=1)

        cards = [
            ("Programmes", "dumbbell.png"),
            ("Séances", "clock.png"),
            ("Calendrier", "calendar.png"),
            ("Clients", "users.png"),
            ("Nutrition", "apple.png"),
            ("Facturation", "billing.png"),
            ("Exercices", "database.png"),
            ("Export PDF", "pdf.png"),
            ("Progression", "chart.png"),
            ("Messagerie", "chat.png"),
            ("Assistant IA", "spark.png"),
            ("Paramètres", "settings.png"),
        ]

        columns = 4  # Nombre de colonnes désirées

        for i, (label, icon) in enumerate(cards):
            row = i // columns
            col = i % columns
            card = IconCard(grid_frame, text=label, icon_path=f"assets/icons/{icon}")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        PrimaryButton(scroll, text="Créer un nouveau programme").pack(pady=30)

        # === SECTION 2 : Statistiques visuelles stylisées ===

        SectionTitle(scroll, "Statistiques de la semaine").pack(pady=(30, 10))

        stats_card = ctk.CTkFrame(
            scroll, fg_color=colors["surface_light"], corner_radius=10
        )
        stats_card.pack(fill="x", padx=20, pady=10)

        title_row = ctk.CTkFrame(stats_card, fg_color="transparent")
        title_row.pack(fill="x", pady=(10, 5), padx=10)
        ctk.CTkLabel(
            title_row,
            text="📊 Répartition des séances",
            font=ctk.CTkFont(**fonts["H2"]),
            text_color=colors["primary_text"],
        ).pack(side="left")

        stats_content = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_content.pack(padx=20, pady=10, fill="x")

        # --- Fake Graphe stylisé (donut statique dessiné)
        graph_canvas = ctk.CTkCanvas(
            stats_content,
            width=200,
            height=200,
            bg=colors["surface_light"],
            highlightthickness=0,
        )
        graph_canvas.grid(row=0, column=0, padx=(0, 40))

        # Donut stylisé
        graph_canvas.create_oval(20, 20, 180, 180, fill="#333333", outline="")
        graph_canvas.create_arc(
            20, 20, 180, 180, start=0, extent=90, fill="#3b82f6", outline=""
        )
        graph_canvas.create_arc(
            20, 20, 180, 180, start=90, extent=80, fill="#22c55e", outline=""
        )
        graph_canvas.create_arc(
            20, 20, 180, 180, start=170, extent=70, fill="#f59e0b", outline=""
        )
        graph_canvas.create_arc(
            20, 20, 180, 180, start=240, extent=120, fill="#ef4444", outline=""
        )
        graph_canvas.create_oval(
            60, 60, 140, 140, fill=colors["surface_light"], outline=""
        )  # Centre du donut

        # --- Détails à droite du graphe
        stat_labels = ctk.CTkFrame(stats_content, fg_color="transparent")
        stat_labels.grid(row=0, column=1, sticky="nw")

        def stat_line(label, color, percent, total):
            row = ctk.CTkFrame(stat_labels, fg_color="transparent")
            row.pack(anchor="w", pady=4)
            dot = ctk.CTkLabel(
                row,
                text="●",
                text_color=color,
                font=ctk.CTkFont(**fonts["Body"]),
            )
            dot.pack(side="left", padx=(0, 6))
            name = ctk.CTkLabel(
                row,
                text=f"{label}",
                font=ctk.CTkFont(**fonts["Body"]),
                text_color=colors["primary_text"],
            )
            name.pack(side="left", padx=(0, 10))
            value = ctk.CTkLabel(
                row,
                text=f"{percent} • {total} séances",
                font=ctk.CTkFont(**fonts["Small"]),
                text_color=colors["secondary_text"],
            )
            value.pack(side="left")

        stat_line("Push", "#3b82f6", "35%", "14")
        stat_line("Pull", "#22c55e", "20%", "8")
        stat_line("Legs", "#f59e0b", "15%", "6")
        stat_line("Repos", "#ef4444", "30%", "12")

        # KPI
        kpi_frame = ctk.CTkFrame(
            scroll, fg_color=colors["surface_light"], corner_radius=10
        )
        kpi_frame.pack(pady=30, padx=20, fill="x")

        ctk.CTkLabel(
            kpi_frame,
            text="Indicateurs clés",
            font=ctk.CTkFont(**fonts["H2"]),
            text_color=colors["primary_text"],
        ).pack(anchor="w", padx=20, pady=(10, 0))

        kpi_grid = ctk.CTkFrame(kpi_frame, fg_color="transparent")
        kpi_grid.pack(padx=20, pady=10, fill="x")

        def kpi(label, value):
            box = ctk.CTkFrame(
                kpi_grid, fg_color=colors["surface_light"], corner_radius=8
            )
            box.pack(side="left", expand=True, fill="both", padx=5)
            ctk.CTkLabel(
                box,
                text=label,
                text_color=colors["primary_text"],
                font=ctk.CTkFont(**fonts["Small"]),
            ).pack(pady=(10, 2))
            ctk.CTkLabel(
                box,
                text=value,
                font=ctk.CTkFont(**fonts["H2"]),
                text_color=colors["primary"],
            ).pack(pady=(0, 10))

        kpi("Clients actifs", str(data.active_clients))
        kpi("Séances ce mois", str(data.sessions_this_month))
        kpi(
            "Taux de complétion",
            f"{int(data.average_session_completion_rate * 100)}%",
        )

        # === SECTION 3 : Clients récents ===
        SectionTitle(scroll, "Clients récents").pack(pady=(30, 10))

        clients_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        clients_frame.pack(pady=10, fill="x")

        clients = [
            ("Pauline C.", "user1.png", "il y a 2 jours"),
            ("Thomas B.", "user2.png", "hier"),
            ("Chloé D.", "user3.png", "il y a 4 jours"),
        ]

        for name, avatar_file, date in clients:
            row = ctk.CTkFrame(
                clients_frame, fg_color=colors["surface_light"], corner_radius=10
            )
            row.pack(pady=5, fill="x", padx=10)

            avatar_img = ctk.CTkImage(
                Image.open(f"assets/icons/{avatar_file}"), size=(40, 40)
            )
            ctk.CTkLabel(row, image=avatar_img, text="", width=50).pack(
                side="left", padx=10
            )
            ctk.CTkLabel(
                row,
                text=name,
                font=ctk.CTkFont(**fonts["Body"]),
                text_color=colors["primary_text"],
            ).pack(side="left")
            ctk.CTkLabel(
                row,
                text=date,
                font=ctk.CTkFont(**fonts["Small"]),
                text_color=colors["secondary_text"],
            ).pack(side="right", padx=20)
