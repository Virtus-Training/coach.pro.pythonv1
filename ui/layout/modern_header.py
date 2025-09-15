"""
Header moderne avec breadcrumbs, search et actions contextuelles.
Inspiré de Notion, Linear et GitHub.
"""

from typing import Callable, List, Optional

import customtkinter as ctk

from ui.components.modern_ui_kit import AnimatedButton, StatusIndicator, show_toast
from utils.icon_loader import load_icon


class ModernHeader(ctk.CTkFrame):
    """Header moderne avec navigation contextuelle."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            height=56,
            corner_radius=0,
            fg_color=ctk.ThemeManager.theme["color"]["surface_light"],
            **kwargs
        )

        # Empêcher la frame header de grandir selon ses enfants (grid)
        self.pack_propagate(False)
        try:
            self.grid_propagate(False)
        except Exception:
            pass
        self.grid_columnconfigure(1, weight=1)  # Center section expands

        self.current_page = ""
        self.breadcrumbs = []

        self._build_interface()

    def _build_interface(self):
        """Construit l'interface du header."""
        # === LEFT SECTION: Breadcrumbs ===
        self._create_breadcrumbs_section()

        # === CENTER SECTION: Search & Quick Actions ===
        self._create_center_section()

        # === RIGHT SECTION: User & System ===
        self._create_right_section()

    def _create_breadcrumbs_section(self):
        """Section breadcrumbs et titre de page."""
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="w", padx=20, pady=8)

        # Container pour breadcrumbs
        self.breadcrumbs_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.breadcrumbs_frame.pack(anchor="w")

        # Titre principal par défaut
        self.page_title = ctk.CTkLabel(
            self.left_frame,
            text="Tableau de bord",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"]
        )
        self.page_title.pack(anchor="w", pady=(2, 0))

    def _create_center_section(self):
        """Section centrale avec recherche et actions rapides."""
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.grid(row=0, column=1, sticky="ew", padx=20, pady=8)

        # Barre de recherche moderne
        search_container = ctk.CTkFrame(
            self.center_frame,
            fg_color=ctk.ThemeManager.theme["color"]["surface_dark"],
            corner_radius=18,
            height=36
        )
        search_container.pack(expand=True, pady=4)
        search_container.pack_propagate(False)

        # Icône de recherche
        try:
            search_icon = load_icon("search.png", 18)
        except:
            search_icon = None

        search_icon_label = ctk.CTkLabel(
            search_container,
            text="🔍" if not search_icon else "",
            image=search_icon,
            text_color=ctk.ThemeManager.theme["color"]["muted_text"]
        )
        search_icon_label.pack(side="left", padx=(16, 8), pady=8)

        # Entry de recherche
        self.search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="Rechercher clients, exercices...",
            border_width=0,
            fg_color="transparent",
            font=ctk.CTkFont(size=14),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"]
        )
        self.search_entry.pack(side="left", expand=True, fill="both", pady=8, padx=(0, 16))

        # Raccourci clavier
        self.search_entry.bind("<Return>", self._on_search)

        # Keyboard shortcut hint
        shortcut_label = ctk.CTkLabel(
            search_container,
            text="Ctrl+K",
            font=ctk.CTkFont(size=10),
            text_color=ctk.ThemeManager.theme["color"]["muted_text"],
            fg_color=ctk.ThemeManager.theme["color"]["surface_elevated"],
            corner_radius=4,
            padx=6, pady=2
        )
        shortcut_label.pack(side="right", padx=(0, 12), pady=8)

    def _create_right_section(self):
        """Section droite avec notifications et profil utilisateur."""
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=2, sticky="e", padx=20, pady=8)

        # Quick actions toolbar
        toolbar = ctk.CTkFrame(
            self.right_frame,
            fg_color=ctk.ThemeManager.theme["color"]["surface_dark"],
            corner_radius=12
        )
        toolbar.pack(side="left", padx=(0, 16))

        # Bouton notifications
        notif_btn = AnimatedButton(
            toolbar,
            text="🔔",
            width=40,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color=ctk.ThemeManager.theme["color"]["surface_elevated"],
            font=ctk.CTkFont(size=16),
            command=self._show_notifications
        )
        notif_btn.pack(side="left", padx=4, pady=4)

        # Status indicator
        status_btn = AnimatedButton(
            toolbar,
            text="📊",
            width=40,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color=ctk.ThemeManager.theme["color"]["surface_elevated"],
            font=ctk.CTkFont(size=16),
            command=self._show_status
        )
        status_btn.pack(side="left", padx=4, pady=4)

        # Paramètres
        settings_btn = AnimatedButton(
            toolbar,
            text="⚙️",
            width=40,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color=ctk.ThemeManager.theme["color"]["surface_elevated"],
            font=ctk.CTkFont(size=16),
            command=self._show_settings
        )
        settings_btn.pack(side="left", padx=4, pady=4)

        # Profile section
        self._create_profile_section()

    def _create_profile_section(self):
        """Section profil utilisateur avec avatar."""
        profile_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color=ctk.ThemeManager.theme["color"]["surface_dark"],
            corner_radius=18,
            height=36
        )
        profile_frame.pack(side="left")
        profile_frame.pack_propagate(False)

        # Avatar
        avatar_btn = AnimatedButton(
            profile_frame,
            text="👤",
            width=32,
            height=32,
            corner_radius=16,
            fg_color=ctk.ThemeManager.theme["color"]["primary"],
            hover_color=ctk.ThemeManager.theme["color"]["primary_hover"],
            font=ctk.CTkFont(size=14),
            command=self._show_profile_menu
        )
        avatar_btn.pack(side="left", padx=(8, 4), pady=8)

        # Nom utilisateur
        user_info_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
        user_info_frame.pack(side="left", padx=(4, 12), pady=8)

        name_label = ctk.CTkLabel(
            user_info_frame,
            text="Coach Pro",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"]
        )
        name_label.pack(anchor="w")

        # Status en ligne
        online_indicator = StatusIndicator(
            user_info_frame,
            status="success",
            text=""
        )
        online_indicator.pack(anchor="w")
        online_indicator.configure(width=8, height=8)

    def update_page(self, page_name: str, breadcrumbs: Optional[List[str]] = None):
        """Met à jour la page courante et les breadcrumbs."""
        self.current_page = page_name
        self.breadcrumbs = breadcrumbs or []

        # Met à jour le titre
        self.page_title.configure(text=page_name)

        # Met à jour les breadcrumbs
        self._update_breadcrumbs()

        # Animation de transition
        self._animate_page_change()

    def _update_breadcrumbs(self):
        """Met à jour l'affichage des breadcrumbs."""
        # Clear existing breadcrumbs
        for widget in self.breadcrumbs_frame.winfo_children():
            widget.destroy()

        if not self.breadcrumbs:
            return

        # Create breadcrumb trail
        for i, crumb in enumerate(self.breadcrumbs):
            # Breadcrumb button
            crumb_btn = AnimatedButton(
                self.breadcrumbs_frame,
                text=crumb,
                height=24,
                corner_radius=4,
                fg_color="transparent",
                hover_color=ctk.ThemeManager.theme["color"]["glass_overlay"],
                text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
                font=ctk.CTkFont(size=11),
                command=lambda c=crumb: self._on_breadcrumb_click(c)
            )
            crumb_btn.pack(side="left", padx=2)

            # Separator (except for last item)
            if i < len(self.breadcrumbs) - 1:
                separator = ctk.CTkLabel(
                    self.breadcrumbs_frame,
                    text="›",
                    font=ctk.CTkFont(size=12),
                    text_color=ctk.ThemeManager.theme["color"]["muted_text"]
                )
                separator.pack(side="left", padx=4)

    def _animate_page_change(self):
        """Animation lors du changement de page."""
        # Subtle fade effect on title
        def fade_effect():
            try:
                original_color = self.page_title.cget("text_color")
                self.page_title.configure(text_color=ctk.ThemeManager.theme["color"]["primary"])
                self.after(200, lambda: self.page_title.configure(text_color=original_color))
            except Exception:
                pass

        self.after(50, fade_effect)

    def _on_search(self, event=None):
        """Gestion de la recherche."""
        query = self.search_entry.get().strip()
        if query:
            show_toast(self, f"Recherche: {query}", "info", 2000)
            # TODO: Implémenter la logique de recherche réelle

    def _on_breadcrumb_click(self, crumb: str):
        """Navigation via breadcrumb."""
        show_toast(self, f"Navigation vers: {crumb}", "info", 1500)
        # TODO: Implémenter la navigation réelle

    def _show_notifications(self):
        """Affiche le panneau des notifications."""
        show_toast(self, "Aucune nouvelle notification", "info", 2000)

    def _show_status(self):
        """Affiche les statistiques système."""
        show_toast(self, "Système opérationnel", "success", 2000)

    def _show_settings(self):
        """Ouvre les paramètres."""
        show_toast(self, "Paramètres (à implémenter)", "info", 2000)

    def _show_profile_menu(self):
        """Affiche le menu profil."""
        show_toast(self, "Menu profil (à implémenter)", "info", 2000)

    def set_search_callback(self, callback: Callable[[str], None]):
        """Définit le callback pour la recherche."""
        self.search_callback = callback

    def focus_search(self):
        """Met le focus sur la barre de recherche."""
        self.search_entry.focus_set()


# Fonction utilitaire pour les raccourcis clavier globaux
def setup_global_shortcuts(app):
    """Configure les raccourcis clavier globaux."""
    def on_ctrl_k(event):
        # Focus sur la recherche
        try:
            header = getattr(app, 'header', None)
            if header and hasattr(header, 'focus_search'):
                header.focus_search()
        except Exception:
            pass

    # Bind Ctrl+K pour la recherche
    app.bind_all("<Control-k>", on_ctrl_k)
    app.bind_all("<Control-K>", on_ctrl_k)
