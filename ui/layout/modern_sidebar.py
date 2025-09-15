"""
Sidebar moderne avec animations, glassmorphism et micro-interactions.
Inspiré de Discord, VS Code et Notion.
"""

from typing import Callable, Dict

import customtkinter as ctk

from ui.components.modern_ui_kit import AnimatedButton, GlassCard, StatusIndicator
from utils.icon_loader import load_icon, load_square_image


class ModernSidebar(ctk.CTkFrame):
    """Sidebar moderne avec effets visuels avancés."""

    def __init__(
        self,
        parent,
        switch_page_callback: Callable,
        page_registry: Dict[str, Dict],
        active_module: str = "dashboard",
    ):
        super().__init__(
            parent,
            width=280,
            corner_radius=0,
            fg_color=ctk.ThemeManager.theme["color"]["surface_dark"],
        )

        self.switch_page_callback = switch_page_callback
        self.page_registry = page_registry
        self.active_module = active_module
        self._button_map = {}
        self._is_collapsed = False

        self.grid_propagate(False)
        # Faire grandir la zone de navigation (ligne 1) pour occuper l'espace disponible
        self.grid_rowconfigure(1, weight=1)

        self._build_interface()

    def _build_interface(self):
        """Construit l'interface de la sidebar."""
        # === HEADER SECTION ===
        self._create_header()

        # === NAVIGATION SECTION ===
        self._create_navigation()

        # === USER SECTION (bottom) ===
        self._create_user_section()

        # === COLLAPSE BUTTON ===
        self._create_collapse_button()

    def _create_header(self):
        """Crée la section header avec logo et titre."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=88)
        header_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 0))
        header_frame.grid_propagate(False)

        # Logo avec effet hover
        logo_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_container.pack(expand=True)

        try:
            logo = load_square_image("assets/Logo.png", 64)
            logo_label = ctk.CTkLabel(
                logo_container, image=logo, text="", cursor="hand2"
            )
            logo_label.pack(pady=(8, 6))

            # Effet hover sur le logo
            logo_label.bind("<Enter>", self._logo_hover_enter)
            logo_label.bind("<Leave>", self._logo_hover_leave)

        except Exception:
            # Fallback si logo introuvable
            fallback_logo = ctk.CTkLabel(
                logo_container, text="💪", font=ctk.CTkFont(size=32), cursor="hand2"
            )
            fallback_logo.pack(pady=(8, 6))

        # Titre de l'application
        title_label = ctk.CTkLabel(
            logo_container,
            text="CoachPro",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
        )
        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            logo_container,
            text="Virtus Training",
            font=ctk.CTkFont(size=12),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
        )
        subtitle_label.pack()

        # Ligne décorative avec gradient
        divider = ctk.CTkFrame(
            header_frame, height=2, fg_color=ctk.ThemeManager.theme["color"]["primary"]
        )
        divider.pack(fill="x", pady=(8, 0), padx=8)

    def _create_navigation(self):
        """Crée la section de navigation principale."""
        # Utiliser une frame simple (pas de scroll interne) afin d'afficher tous les boutons
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=16)

        # Titre de section
        section_title = ctk.CTkLabel(
            nav_frame,
            text="NAVIGATION",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["muted_text"],
            anchor="w",
        )
        section_title.pack(fill="x", padx=8, pady=(0, 12))

        # Création des boutons de navigation
        for item_id, data in self.page_registry.items():
            button = self._create_nav_button(
                nav_frame, item_id, data["label"], data["icon"]
            )
            self._button_map[item_id] = button

        # Spacer pour séparer les sections
        spacer = ctk.CTkFrame(nav_frame, fg_color="transparent", height=20)
        spacer.pack(fill="x")

        # Section utilitaires (si nécessaire)
        self._create_utility_section(nav_frame)

    def _create_nav_button(
        self, parent, item_id: str, label: str, icon_name: str
    ) -> AnimatedButton:
        """Crée un bouton de navigation moderne."""
        try:
            icon = load_icon(icon_name, 20)
        except Exception:
            icon = None

        button = AnimatedButton(
            parent,
            text=f"  {label}",
            image=icon,
            compound="left",
            anchor="w",
            height=40,
            corner_radius=12,
            fg_color="transparent",
            hover_color=ctk.ThemeManager.theme["color"].get("surface_light", "#252651"),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            font=ctk.CTkFont(size=14, weight="normal"),
            border_spacing=12,
            command=lambda i=item_id: self._on_nav_click(i),
        )
        button.pack(fill="x", padx=6, pady=2)

        return button

    def _create_utility_section(self, parent):
        """Crée une section avec outils utiles."""
        # Titre de section
        util_title = ctk.CTkLabel(
            parent,
            text="OUTILS",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["muted_text"],
            anchor="w",
        )
        util_title.pack(fill="x", padx=8, pady=(16, 12))

        # Status indicator
        status_card = GlassCard(
            parent, fg_color=ctk.ThemeManager.theme["color"]["surface_light"]
        )
        status_card.pack(fill="x", padx=4, pady=2)

        status_frame = ctk.CTkFrame(status_card.content_frame, fg_color="transparent")
        status_frame.pack(fill="x")

        ctk.CTkLabel(
            status_frame,
            text="Système",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
        ).pack(anchor="w")

        status_indicator = StatusIndicator(
            status_frame, status="success", text="Opérationnel"
        )
        status_indicator.pack(anchor="w", pady=(4, 0))

    def _create_user_section(self):
        """Crée la section utilisateur en bas."""
        user_frame = ctk.CTkFrame(
            self,
            fg_color=ctk.ThemeManager.theme["color"]["surface_light"],
            corner_radius=16,
            height=56,
        )
        user_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 12))
        user_frame.grid_propagate(False)

        content_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=12, pady=6)

        # Avatar et info utilisateur
        user_info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        user_info_frame.pack(side="left", expand=True, fill="both")

        # Avatar
        try:
            user_icon = load_icon("user1.png", 32)
        except:
            user_icon = None

        avatar_label = ctk.CTkLabel(
            user_info_frame,
            text="👤" if not user_icon else "",
            image=user_icon,
            font=ctk.CTkFont(size=20),
            text_color=ctk.ThemeManager.theme["color"]["primary"],
        )
        avatar_label.pack(side="left", padx=(0, 12))

        # Infos utilisateur
        info_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        info_frame.pack(side="left", expand=True, fill="both")

        name_label = ctk.CTkLabel(
            info_frame,
            text="Coach Pro",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
            anchor="w",
        )
        name_label.pack(anchor="w")

        status_label = ctk.CTkLabel(
            info_frame,
            text="En ligne",
            font=ctk.CTkFont(size=11),
            text_color=ctk.ThemeManager.theme["color"]["success"],
            anchor="w",
        )
        status_label.pack(anchor="w")

        # Menu utilisateur (icône)
        menu_button = AnimatedButton(
            content_frame,
            text="⋮",
            width=32,
            height=32,
            fg_color="transparent",
            hover_color=ctk.ThemeManager.theme["color"]["surface_dark"],
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._show_user_menu,
        )
        menu_button.pack(side="right")

    def _create_collapse_button(self):
        """Bouton pour réduire/agrandir la sidebar."""
        collapse_btn = AnimatedButton(
            self,
            text="◀",
            width=24,
            height=24,
            corner_radius=12,
            fg_color=ctk.ThemeManager.theme["color"]["surface_elevated"],
            hover_color=ctk.ThemeManager.theme["color"]["primary"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._toggle_collapse,
        )
        # Positionner en haut à droite
        collapse_btn.place(relx=1.0, x=-12, y=12, anchor="ne")

    def _on_nav_click(self, module_id: str):
        """Gestion du click sur navigation avec animation."""
        if module_id != self.active_module:
            # Animation de changement
            self._animate_page_change(module_id)
            self.switch_page_callback(module_id)

    def _animate_page_change(self, new_module_id: str):
        """Animation lors du changement de page."""
        # Désactive l'ancien bouton
        if self.active_module in self._button_map:
            old_button = self._button_map[self.active_module]
            old_button.configure(
                fg_color="transparent",
                text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            )

        # Active le nouveau bouton avec animation
        if new_module_id in self._button_map:
            new_button = self._button_map[new_module_id]

            # Animation de mise en surbrillance
            def highlight():
                new_button.configure(
                    fg_color=ctk.ThemeManager.theme["color"]["primary"],
                    text_color="white",
                )

                # Pulse effect
                new_button.configure(corner_radius=16)
                self.after(200, lambda: new_button.configure(corner_radius=12))

            self.after(50, highlight)

        self.active_module = new_module_id

    def _toggle_collapse(self):
        """Basculer entre sidebar étendue et réduite."""
        if self._is_collapsed:
            # Étendre
            self.configure(width=280)
            # Changer l'icône
            for widget in self.winfo_children():
                if isinstance(widget, AnimatedButton):
                    widget.configure(text="◀")
                    break
        else:
            # Réduire
            self.configure(width=80)
            # Changer l'icône
            for widget in self.winfo_children():
                if isinstance(widget, AnimatedButton):
                    widget.configure(text="▶")
                    break

        self._is_collapsed = not self._is_collapsed

    def _logo_hover_enter(self, event):
        """Effet hover sur le logo."""
        try:
            widget = event.widget
            # Petit effet de scale simulé
            widget.configure(cursor="hand2")
        except Exception:
            pass

    def _logo_hover_leave(self, event):
        """Sortie hover logo."""
        try:
            widget = event.widget
            widget.configure(cursor="")
        except Exception:
            pass

    def _show_user_menu(self):
        """Affiche le menu utilisateur."""
        # TODO: Implémenter menu contextuel
        pass

    def set_active(self, module_id: str):
        """Définit le module actif (appelé de l'extérieur)."""
        if module_id != self.active_module:
            self._animate_page_change(module_id)
