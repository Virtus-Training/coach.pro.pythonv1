"""
Page Dashboard modernisée avec widgets interactifs et visualisations.
Inspiré de Linear, Notion, et modern SaaS dashboards.
"""

from typing import Dict

import customtkinter as ctk

from ui.components.modern_ui_kit import (
    AnimatedButton,
    FloatingActionButton,
    GlassCard,
    ModernProgressBar,
    ModernTabView,
    StatusIndicator,
    show_toast,
)


class ModernDashboardPage(ctk.CTkFrame):
    """Dashboard moderne avec layout en grid et widgets interactifs."""

    def __init__(self, parent, dashboard_controller=None):
        super().__init__(parent, fg_color="transparent")

        self.dashboard_controller = dashboard_controller
        self._create_interface()
        self._load_dashboard_data()

    def _create_interface(self):
        """Crée l'interface du dashboard."""
        # Container principal avec scroll
        self.main_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=ctk.ThemeManager.theme["color"]["surface_light"],
        )
        self.main_container.pack(fill="both", expand=True)

        # === WELCOME SECTION ===
        self._create_welcome_section()

        # === METRICS CARDS ROW ===
        self._create_metrics_section()

        # === MAIN CONTENT GRID ===
        self._create_main_content()

        # === FLOATING ACTION BUTTON ===
        self._create_fab()

    def _create_welcome_section(self):
        """Section d'accueil personnalisée."""
        # Eviter les couleurs RGBA (#RRGGBBAA) non supportées par tkinter
        # En remplacement: utiliser une couleur de surface élevée du thème
        welcome_card = GlassCard(
            self.main_container,
            fg_color=ctk.ThemeManager.theme["color"].get("surface_elevated", "#2D2F5F"),
        )
        welcome_card.pack(fill="x", padx=16, pady=(8, 12))

        welcome_content = ctk.CTkFrame(
            welcome_card.content_frame, fg_color="transparent"
        )
        welcome_content.pack(fill="both", expand=True)

        # Grid layout pour welcome
        welcome_content.grid_columnconfigure(0, weight=1)
        welcome_content.grid_columnconfigure(1, weight=0)

        # Texte de bienvenue
        left_frame = ctk.CTkFrame(welcome_content, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="w", padx=(0, 20))

        greeting_label = ctk.CTkLabel(
            left_frame,
            text="👋 Bonjour Coach !",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
        )
        greeting_label.pack(anchor="w")

        date_label = ctk.CTkLabel(
            left_frame,
            text="Voici un aperçu de votre activité aujourd'hui",
            font=ctk.CTkFont(size=14),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
        )
        date_label.pack(anchor="w", pady=(4, 0))

        # Actions rapides
        quick_actions = ctk.CTkFrame(left_frame, fg_color="transparent")
        quick_actions.pack(anchor="w", pady=(12, 0))

        new_client_btn = AnimatedButton(
            quick_actions,
            text="➕ Nouveau client",
            fg_color=ctk.ThemeManager.theme["color"]["primary"],
            hover_color=ctk.ThemeManager.theme["color"]["primary_hover"],
            command=lambda: show_toast(self, "Nouveau client", "info"),
        )
        new_client_btn.pack(side="left", padx=(0, 8))

        new_session_btn = AnimatedButton(
            quick_actions,
            text="🏃 Nouvelle séance",
            fg_color=ctk.ThemeManager.theme["color"]["secondary"],
            hover_color="#059669",
            command=lambda: show_toast(self, "Nouvelle séance", "info"),
        )
        new_session_btn.pack(side="left")

        # Status indicator
        right_frame = ctk.CTkFrame(welcome_content, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="e")

        system_status = StatusIndicator(
            right_frame, status="success", text="Système actif"
        )
        system_status.pack()

    def _create_metrics_section(self):
        """Cartes de métriques principales."""
        metrics_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Grid responsive pour les métriques
        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1)

        # Métriques factices (à remplacer par vraies données)
        metrics_data = [
            {
                "title": "Clients actifs",
                "value": "42",
                "change": "+5",
                "color": "primary",
                "icon": "👥",
            },
            {
                "title": "Séances cette semaine",
                "value": "18",
                "change": "+3",
                "color": "secondary",
                "icon": "🏃",
            },
            {
                "title": "Revenus du mois",
                "value": "2.4k€",
                "change": "+12%",
                "color": "accent",
                "icon": "💰",
            },
            {
                "title": "Taux de satisfaction",
                "value": "98%",
                "change": "+2%",
                "color": "success",
                "icon": "⭐",
            },
        ]

        for i, metric in enumerate(metrics_data):
            card = self._create_metric_card(metrics_frame, metric)
            card.grid(row=0, column=i, sticky="ew", padx=(0, 12 if i < 3 else 0))

    def _create_metric_card(self, parent, metric_data: Dict):
        """Crée une carte de métrique."""
        colors = {
            "primary": ctk.ThemeManager.theme["color"]["primary"],
            "secondary": ctk.ThemeManager.theme["color"]["secondary"],
            "accent": ctk.ThemeManager.theme["color"]["accent"],
            "success": ctk.ThemeManager.theme["color"]["success"],
        }

        card = GlassCard(parent)
        content = card.content_frame

        # Header avec icône
        header_frame = ctk.CTkFrame(content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 8))
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text=metric_data["title"],
            font=ctk.CTkFont(size=12),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            anchor="w",
        )
        title_label.grid(row=0, column=0, sticky="w")

        icon_label = ctk.CTkLabel(
            header_frame, text=metric_data["icon"], font=ctk.CTkFont(size=18)
        )
        icon_label.grid(row=0, column=1, sticky="e")

        # Valeur principale
        value_label = ctk.CTkLabel(
            content,
            text=metric_data["value"],
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
        )
        value_label.pack(anchor="w", pady=(0, 4))

        # Changement avec couleur
        change_color = colors.get(metric_data["color"], colors["primary"])
        change_label = ctk.CTkLabel(
            content,
            text=f"↗ {metric_data['change']}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=change_color,
        )
        change_label.pack(anchor="w")

        # Progress bar subtile
        progress = ModernProgressBar(content, max_value=100)
        progress.pack(fill="x", pady=(8, 0))
        progress.set_value(85, animate=True)  # Valeur exemple

        return card

    def _create_main_content(self):
        """Contenu principal avec tabs et widgets."""
        content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20)

        # Grid layout pour le contenu
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # === LEFT COLUMN: Activity & Charts ===
        left_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        # Tabview pour l'activité
        activity_tabs = ModernTabView(left_column)
        activity_tabs.pack(fill="both", expand=True)

        # Tab Activité récente
        recent_tab = activity_tabs.add_tab("recent", "📈 Activité récente")
        self._create_activity_feed(recent_tab)

        # Tab Statistiques
        stats_tab = activity_tabs.add_tab("stats", "📊 Statistiques")
        self._create_stats_widgets(stats_tab)

        # Tab Planning
        planning_tab = activity_tabs.add_tab("planning", "📅 Planning")
        self._create_planning_widget(planning_tab)

        # === RIGHT COLUMN: Quick Info & Actions ===
        right_column = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_column.grid(row=0, column=1, sticky="nsew")

        # Clients du jour
        self._create_today_clients(right_column)

        # Quick stats
        self._create_quick_stats(right_column)

        # Notifications
        self._create_notifications_widget(right_column)

    def _create_activity_feed(self, parent):
        """Feed d'activité récente."""
        feed_card = GlassCard(parent, title="Activité récente")
        feed_card.pack(fill="both", expand=True, padx=16, pady=16)

        # Liste d'activités
        activities = [
            {
                "icon": "👤",
                "text": "Nouveau client: Marie Dubois",
                "time": "Il y a 2h",
                "type": "success",
            },
            {
                "icon": "🏃",
                "text": "Séance terminée avec Jean Martin",
                "time": "Il y a 3h",
                "type": "info",
            },
            {
                "icon": "📊",
                "text": "Rapport mensuel généré",
                "time": "Il y a 1 jour",
                "type": "neutral",
            },
            {
                "icon": "💰",
                "text": "Paiement reçu - 85€",
                "time": "Il y a 1 jour",
                "type": "success",
            },
            {
                "icon": "📅",
                "text": "Séance planifiée pour demain",
                "time": "Il y a 2 jours",
                "type": "info",
            },
        ]

        for activity in activities:
            self._create_activity_item(feed_card.content_frame, activity)

    def _create_activity_item(self, parent, activity):
        """Item d'activité individuel."""
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=ctk.ThemeManager.theme["color"]["surface_elevated"],
            corner_radius=8,
            height=60,
        )
        item_frame.pack(fill="x", pady=4)
        item_frame.pack_propagate(False)
        item_frame.grid_columnconfigure(1, weight=1)

        # Icône
        icon_label = ctk.CTkLabel(
            item_frame, text=activity["icon"], font=ctk.CTkFont(size=20)
        )
        icon_label.grid(row=0, column=0, padx=(12, 8), pady=12)

        # Contenu
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=8)

        text_label = ctk.CTkLabel(
            content_frame,
            text=activity["text"],
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
            anchor="w",
        )
        text_label.pack(anchor="w")

        time_label = ctk.CTkLabel(
            content_frame,
            text=activity["time"],
            font=ctk.CTkFont(size=11),
            text_color=ctk.ThemeManager.theme["color"]["muted_text"],
            anchor="w",
        )
        time_label.pack(anchor="w")

    def _create_stats_widgets(self, parent):
        """Widgets de statistiques."""
        stats_card = GlassCard(parent, title="Graphiques de performance")
        stats_card.pack(fill="both", expand=True, padx=16, pady=16)

        # Placeholder pour graphiques
        chart_placeholder = ctk.CTkFrame(
            stats_card.content_frame,
            fg_color=ctk.ThemeManager.theme["color"]["surface_dark"],
            corner_radius=12,
            height=300,
        )
        chart_placeholder.pack(fill="both", expand=True, pady=8)

        placeholder_label = ctk.CTkLabel(
            chart_placeholder,
            text="📊\nGraphiques de performance\n(Intégration avec matplotlib à venir)",
            font=ctk.CTkFont(size=16),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
        )
        placeholder_label.pack(expand=True)

    def _create_planning_widget(self, parent):
        """Widget de planning."""
        planning_card = GlassCard(parent, title="Planning de la semaine")
        planning_card.pack(fill="both", expand=True, padx=16, pady=16)

        # Mini calendrier / planning
        days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        sessions = [3, 4, 2, 5, 3, 1, 0]  # Nombre de séances par jour

        for i, (day, session_count) in enumerate(zip(days, sessions)):
            day_frame = ctk.CTkFrame(
                planning_card.content_frame,
                fg_color=ctk.ThemeManager.theme["color"]["surface_elevated"],
                corner_radius=8,
                height=50,
            )
            day_frame.pack(fill="x", pady=2)
            day_frame.pack_propagate(False)
            day_frame.grid_columnconfigure(1, weight=1)

            # Jour
            day_label = ctk.CTkLabel(
                day_frame, text=day, font=ctk.CTkFont(size=12, weight="bold"), width=40
            )
            day_label.grid(row=0, column=0, padx=12, pady=12)

            # Nombre de séances
            sessions_text = (
                f"{session_count} séance{'s' if session_count > 1 else ''}"
                if session_count > 0
                else "Libre"
            )
            sessions_label = ctk.CTkLabel(
                day_frame,
                text=sessions_text,
                font=ctk.CTkFont(size=11),
                text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
                anchor="w",
            )
            sessions_label.grid(row=0, column=1, sticky="w", padx=(0, 12))

            # Progress bar pour charge de travail
            if session_count > 0:
                progress = ModernProgressBar(day_frame, max_value=5)
                progress.grid(row=0, column=2, sticky="ew", padx=(0, 12), pady=16)
                progress.configure(width=60)
                progress.set_value(session_count, animate=False)

    def _create_today_clients(self, parent):
        """Clients du jour."""
        clients_card = GlassCard(parent, title="Clients aujourd'hui")
        clients_card.pack(fill="x", pady=(0, 16))

        # Liste des clients du jour
        clients_today = [
            {"name": "Marie Dubois", "time": "09:00", "type": "Musculation"},
            {"name": "Jean Martin", "time": "14:30", "type": "Cardio"},
            {"name": "Sophie Leroux", "time": "17:00", "type": "Pilates"},
        ]

        for client in clients_today:
            client_frame = ctk.CTkFrame(
                clients_card.content_frame,
                fg_color=ctk.ThemeManager.theme["color"]["surface_elevated"],
                corner_radius=6,
                height=40,
            )
            client_frame.pack(fill="x", pady=2)
            client_frame.pack_propagate(False)

            time_label = ctk.CTkLabel(
                client_frame,
                text=client["time"],
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=ctk.ThemeManager.theme["color"]["primary"],
                width=50,
            )
            time_label.pack(side="left", padx=(8, 4), pady=8)

            info_frame = ctk.CTkFrame(client_frame, fg_color="transparent")
            info_frame.pack(side="left", expand=True, fill="both", padx=4)

            name_label = ctk.CTkLabel(
                info_frame,
                text=client["name"],
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
            )
            name_label.pack(anchor="w")

            type_label = ctk.CTkLabel(
                info_frame,
                text=client["type"],
                font=ctk.CTkFont(size=10),
                text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
                anchor="w",
            )
            type_label.pack(anchor="w")

    def _create_quick_stats(self, parent):
        """Statistiques rapides."""
        stats_card = GlassCard(parent, title="Stats rapides")
        stats_card.pack(fill="x", pady=(0, 16))

        quick_stats = [
            {"label": "Objectifs atteints", "value": "87%", "color": "success"},
            {"label": "Taux de présence", "value": "94%", "color": "primary"},
            {"label": "Satisfaction moyenne", "value": "4.8/5", "color": "accent"},
        ]

        for stat in quick_stats:
            stat_frame = ctk.CTkFrame(stats_card.content_frame, fg_color="transparent")
            stat_frame.pack(fill="x", pady=2)
            stat_frame.grid_columnconfigure(0, weight=1)

            label = ctk.CTkLabel(
                stat_frame,
                text=stat["label"],
                font=ctk.CTkFont(size=11),
                text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
                anchor="w",
            )
            label.grid(row=0, column=0, sticky="w")

            value = ctk.CTkLabel(
                stat_frame,
                text=stat["value"],
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=ctk.ThemeManager.theme["color"][stat["color"]],
                anchor="e",
            )
            value.grid(row=0, column=1, sticky="e")

    def _create_notifications_widget(self, parent):
        """Widget de notifications."""
        notif_card = GlassCard(parent, title="🔔 Notifications")
        notif_card.pack(fill="x")

        notifications = [
            {"text": "Rappel: Séance avec Marie à 9h", "type": "warning"},
            {"text": "Paiement en attente - Jean Martin", "type": "info"},
            {"text": "Nouveau message reçu", "type": "success"},
        ]

        for notif in notifications:
            notif_frame = ctk.CTkFrame(
                notif_card.content_frame,
                fg_color=ctk.ThemeManager.theme["color"]["surface_elevated"],
                corner_radius=6,
                height=35,
            )
            notif_frame.pack(fill="x", pady=1)
            notif_frame.pack_propagate(False)

            # Status dot
            colors = {
                "success": ctk.ThemeManager.theme["color"]["success"],
                "warning": ctk.ThemeManager.theme["color"]["warning"],
                "info": ctk.ThemeManager.theme["color"]["primary"],
            }

            dot = ctk.CTkLabel(
                notif_frame,
                text="●",
                font=ctk.CTkFont(size=12),
                text_color=colors.get(notif["type"], colors["info"]),
                width=20,
            )
            dot.pack(side="left", padx=(8, 4), pady=8)

            text_label = ctk.CTkLabel(
                notif_frame,
                text=notif["text"],
                font=ctk.CTkFont(size=10),
                text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
                anchor="w",
            )
            text_label.pack(side="left", expand=True, fill="x", padx=(0, 8), pady=8)

    def _create_fab(self):
        """Floating Action Button pour actions rapides."""
        fab = FloatingActionButton(
            self, icon_text="➕", command=self._show_quick_actions
        )
        fab.place(relx=1.0, rely=1.0, x=-80, y=-80, anchor="center")

    def _show_quick_actions(self):
        """Affiche les actions rapides."""
        show_toast(self, "Actions rapides (à implémenter)", "info", 2000)

    def _load_dashboard_data(self):
        """Charge les données du dashboard."""
        # TODO: Intégrer avec le controller réel
        if self.dashboard_controller:
            try:
                # Exemple d'intégration avec controller
                pass
            except Exception as e:
                show_toast(self, f"Erreur de chargement: {str(e)}", "error", 3000)
