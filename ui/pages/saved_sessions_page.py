"""Page pour afficher et gérer les séances sauvegardées."""

from datetime import date
from tkinter import messagebox

import customtkinter as ctk

from repositories.sessions_repo import SessionsRepository
from services.session_service import SessionService
from ui.components.design_system import CardTitle, PrimaryButton, SecondaryButton
from ui.pages.session_preview_panel import render_preview


class SavedSessionsPage(ctk.CTkFrame):
    """Page moderne pour afficher et gérer les séances sauvegardées."""

    def __init__(self, parent, session_controller, app=None):
        super().__init__(parent)
        self.session_controller = session_controller
        self.app = app  # Référence à l'app pour navigation
        self.session_service = SessionService(SessionsRepository())
        self.current_month = date.today().month
        self.current_year = date.today().year
        self.selected_session = None  # Stocker la séance sélectionnée pour l'export

        # Configuration du layout principal
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header avec titre et contrôles
        self._create_header()

        # Container principal avec sidebar et contenu
        self._create_main_container()

        # Charger les séances
        self._load_sessions()

    def _create_header(self):
        """Crée le header de la page."""
        header = ctk.CTkFrame(
            self, fg_color=("gray95", "gray20"), corner_radius=12, height=80
        )
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        header.grid_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=16)

        # Titre principal
        CardTitle(header_content, text="📚 Séances Sauvegardées").pack(
            side="left", anchor="w"
        )

        # Contrôles de navigation mensuelle
        nav_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        nav_frame.pack(side="right", anchor="e")

        # Boutons navigation mois
        SecondaryButton(
            nav_frame, text="◄", command=self._previous_month, width=40
        ).pack(side="left", padx=(0, 4))

        self.month_label = ctk.CTkLabel(
            nav_frame, text="", font=ctk.CTkFont(size=14, weight="bold")
        )
        self.month_label.pack(side="left", padx=8)

        SecondaryButton(nav_frame, text="►", command=self._next_month, width=40).pack(
            side="left", padx=(4, 0)
        )

    def _create_main_container(self):
        """Crée le container principal avec sidebar et contenu."""
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        # Donner plus de poids à la colonne de contenu pour l'aperçu
        main_container.grid_columnconfigure(0, weight=0)  # sidebar fixe (380px)
        main_container.grid_columnconfigure(1, weight=1)  # aperçu occupe tout le reste
        main_container.grid_rowconfigure(0, weight=1)

        # Sidebar avec liste des séances
        self._create_sidebar(main_container)

        # Zone de contenu pour l'aperçu
        self._create_content_area(main_container)

    def _create_sidebar(self, parent):
        """Crée la sidebar avec la liste des séances."""
        sidebar = ctk.CTkFrame(
            parent, fg_color=("gray98", "gray17"), corner_radius=8, width=350
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(1, weight=1)

        # Header de la sidebar
        sidebar_header = ctk.CTkFrame(sidebar, fg_color="transparent", height=50)
        sidebar_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        sidebar_header.grid_propagate(False)

        CardTitle(sidebar_header, text="📋 Liste des séances").pack(
            side="left", anchor="w"
        )

        self.sessions_count_label = ctk.CTkLabel(
            sidebar_header,
            text="0 séances",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        self.sessions_count_label.pack(side="right", anchor="e")

        # Liste scrollable des séances
        self.sessions_list = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
        self.sessions_list.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        # État vide
        self.empty_state = ctk.CTkFrame(self.sessions_list, fg_color="transparent")
        self.empty_state.pack(fill="both", expand=True, pady=40)

        ctk.CTkLabel(self.empty_state, text="📭", font=ctk.CTkFont(size=32)).pack(
            pady=(0, 8)
        )

        ctk.CTkLabel(
            self.empty_state,
            text="Aucune séance ce mois",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray50", "gray60"),
        ).pack(pady=(0, 4))

        ctk.CTkLabel(
            self.empty_state,
            text="Les séances sauvegardées apparaîtront ici",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray50"),
        ).pack()

    def _create_content_area(self, parent):
        """Crée la zone de contenu pour l'aperçu des séances."""
        self.content_area = ctk.CTkFrame(
            parent, fg_color=("gray98", "gray17"), corner_radius=8
        )
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(1, weight=1)

        # Header de la zone de contenu
        content_header = ctk.CTkFrame(
            self.content_area, fg_color="transparent", height=50
        )
        content_header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        content_header.grid_propagate(False)

        CardTitle(content_header, text="👁️ Aperçu détaillé").pack(
            side="left", anchor="w"
        )

        # Bouton Export PDF dans le header de l'aperçu
        export_btn = PrimaryButton(
            content_header,
            text="📄 Exporter en PDF",
            command=self._export_to_pdf,
            width=140,
        )
        export_btn.pack(side="right", anchor="e")

        # Zone d'aperçu
        self.preview_area = ctk.CTkScrollableFrame(
            self.content_area, fg_color="transparent"
        )
        self.preview_area.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        # État vide pour l'aperçu
        self.preview_empty_state = ctk.CTkFrame(
            self.preview_area, fg_color="transparent"
        )
        self.preview_empty_state.pack(fill="both", expand=True, pady=60)

        ctk.CTkLabel(
            self.preview_empty_state, text="👆", font=ctk.CTkFont(size=32)
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            self.preview_empty_state,
            text="Sélectionnez une séance",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray50", "gray60"),
        ).pack(pady=(0, 4))

        ctk.CTkLabel(
            self.preview_empty_state,
            text="Cliquez sur une séance pour voir les détails",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray50"),
        ).pack()

    def _load_sessions(self):
        """Charge les séances pour le mois courant."""
        try:
            sessions = self.session_service.repo.list_sessions_for_month(
                self.current_year, self.current_month
            )
            self._display_sessions(sessions)
            self._update_month_label()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les séances: {e}")

    def _display_sessions(self, sessions):
        """Affiche la liste des séances."""
        # Nettoyer la liste
        for widget in self.sessions_list.winfo_children():
            if widget != self.empty_state:
                widget.destroy()

        if not sessions:
            self.empty_state.pack(fill="both", expand=True, pady=40)
            self.sessions_count_label.configure(text="0 séances")
            return

        self.empty_state.pack_forget()
        self.sessions_count_label.configure(
            text=f"{len(sessions)} séance{'s' if len(sessions) > 1 else ''}"
        )

        # Afficher chaque séance
        for session in sessions:
            self._create_session_card(session)

    def _create_session_card(self, session):
        """Crée une carte pour une séance."""
        card = ctk.CTkFrame(
            self.sessions_list,
            fg_color=("gray92", "gray22"),
            corner_radius=8,
            cursor="hand2",
        )
        card.pack(fill="x", pady=4, padx=4)

        # Bind du clic
        card.bind("<Button-1>", lambda e: self._select_session(session))

        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="x", padx=12, pady=12)

        # Header de la carte
        header_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 8))

        # Icône et titre
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)

        session_icon = self._get_session_icon(session)
        title_label = ctk.CTkLabel(
            title_frame,
            text=f"{session_icon} {session.label}",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        title_label.pack(side="left")
        title_label.bind("<Button-1>", lambda e: self._select_session(session))

        # Date
        date_label = ctk.CTkLabel(
            header_frame,
            text=session.date_creation,
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
        )
        date_label.pack(side="right")
        date_label.bind("<Button-1>", lambda e: self._select_session(session))

        # Info supplémentaires
        info_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        info_frame.pack(fill="x")

        # Durée et blocs
        duration_text = f"⏱️ {session.duration_sec // 60} min"
        blocks_text = f"📋 {len(session.blocks)} blocs"
        mode_text = f"👥 {session.mode.title()}"

        info_text = f"{duration_text} • {blocks_text} • {mode_text}"
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray50"),
            anchor="w",
        )
        info_label.pack(side="left")
        info_label.bind("<Button-1>", lambda e: self._select_session(session))

        # Actions
        actions_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        # Bouton suppression
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=30,
            height=25,
            command=lambda: self._delete_session(session),
            fg_color="transparent",
            hover_color=("lightcoral", "darkred"),
        )
        delete_btn.pack(side="right")

    def _select_session(self, session):
        """Sélectionne et affiche une séance."""
        try:
            # Stocker la séance sélectionnée pour l'export
            self.selected_session = session

            # Construire le DTO pour l'aperçu
            session_dto = self.session_controller.build_preview_from_session(session)

            # Nettoyer l'aperçu
            for widget in self.preview_area.winfo_children():
                if widget != self.preview_empty_state:
                    widget.destroy()

            self.preview_empty_state.pack_forget()

            # Afficher l'aperçu
            render_preview(self.preview_area, session_dto)

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'afficher la séance: {e}")

    def _delete_session(self, session):
        """Supprime une séance après confirmation."""
        result = messagebox.askyesno(
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer la séance '{session.label}' ?\n\nCette action est irréversible.",
        )

        if result:
            try:
                self.session_service.repo.delete(session.session_id)
                self._load_sessions()  # Recharger la liste
                messagebox.showinfo(
                    "Succès", f"Séance '{session.label}' supprimée avec succès."
                )
            except Exception as e:
                messagebox.showerror(
                    "Erreur", f"Impossible de supprimer la séance: {e}"
                )

    def _get_session_icon(self, session):
        """Retourne l'icône appropriée pour une séance."""
        if session.mode == "COLLECTIF":
            return "👥"
        elif session.mode == "INDIVIDUEL":
            return "👤"
        else:
            return "🏋️"

    def _previous_month(self):
        """Navigue vers le mois précédent."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._load_sessions()

    def _next_month(self):
        """Navigue vers le mois suivant."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._load_sessions()

    def _update_month_label(self):
        """Met à jour le label du mois."""
        months = [
            "Janvier",
            "Février",
            "Mars",
            "Avril",
            "Mai",
            "Juin",
            "Juillet",
            "Août",
            "Septembre",
            "Octobre",
            "Novembre",
            "Décembre",
        ]
        month_name = months[self.current_month - 1]
        self.month_label.configure(text=f"{month_name} {self.current_year}")

    def _export_to_pdf(self):
        """Redirige vers la page PDF pour exporter la séance sélectionnée."""
        if not self.selected_session:
            messagebox.showwarning(
                "Aucune séance sélectionnée",
                "Veuillez d'abord sélectionner une séance à exporter.",
            )
            return

        if not self.app:
            messagebox.showerror(
                "Erreur",
                "Impossible d'accéder à la page PDF. Référence à l'application manquante.",
            )
            return

        try:
            # Naviguer vers la page PDF
            self.app.switch_page("pdf")

            # Info utilisateur
            messagebox.showinfo(
                "Redirection",
                f"Direction page PDF pour exporter la séance '{self.selected_session.label}'.\n\n"
                "Vous pouvez maintenant choisir un template et générer le PDF.",
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'accéder à la page PDF: {e}")
