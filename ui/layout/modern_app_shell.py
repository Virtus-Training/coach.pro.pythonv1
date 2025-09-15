"""
App Shell moderne avec layout fluide et transitions animées.
Combine ModernSidebar et ModernHeader pour une expérience immersive.
"""

from typing import Dict

import customtkinter as ctk

from ui.components.modern_ui_kit import show_toast
from ui.layout.modern_header import ModernHeader, setup_global_shortcuts
from ui.layout.modern_sidebar import ModernSidebar


class ModernAppShell(ctk.CTkFrame):
    """Shell d'application moderne avec layout adaptatif."""

    def __init__(
        self,
        parent,
        switch_page_callback,
        page_registry: Dict[str, Dict],
        active_module: str = "dashboard",
    ):
        super().__init__(
            parent,
            fg_color=ctk.ThemeManager.theme["color"]["surface_dark"],
            corner_radius=0,
        )

        self.switch_page_callback = switch_page_callback
        self.page_registry = page_registry
        self.active_module = active_module
        self.current_content = None

        # Configuration du grid pour layout responsive
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_interface()
        self._setup_animations()

        # Configuration des raccourcis globaux
        setup_global_shortcuts(parent)

    def _build_interface(self):
        """Construit l'interface principale."""
        # === SIDEBAR ===
        self.sidebar = ModernSidebar(
            self, self._on_page_switch, self.page_registry, self.active_module
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsw")

        # === HEADER ===
        self.header = ModernHeader(self)
        self.header.grid(row=0, column=1, sticky="ew")

        # Mise à jour du titre initial
        initial_page = self.page_registry.get(self.active_module, {})
        if initial_page:
            self.header.update_page(initial_page.get("label", "Dashboard"))

        # === CONTENT AREA ===
        self._create_content_area()

    def _create_content_area(self):
        """Crée la zone de contenu principale avec effets."""
        # Container principal avec padding moderne
        self.content_container = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.content_container.grid(row=1, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Zone de contenu avec effet d'ombre subtile
        self.content_area = ctk.CTkFrame(
            self.content_container,
            fg_color=ctk.ThemeManager.theme["color"]["surface_medium"],
            corner_radius=20,
            border_width=1,
            border_color=ctk.ThemeManager.theme["color"]["subtle_border"],
        )
        self.content_area.grid(
            row=0, column=0, sticky="nsew", padx=(8, 12), pady=(0, 12)
        )

        # Loading indicator par défaut
        self._show_loading_state()

    def _show_loading_state(self):
        """Affiche un état de chargement élégant."""
        loading_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        loading_frame.pack(expand=True)

        # Animation de chargement
        loading_label = ctk.CTkLabel(
            loading_frame,
            text="⚡",
            font=ctk.CTkFont(size=48),
            text_color=ctk.ThemeManager.theme["color"]["primary"],
        )
        loading_label.pack(expand=True, pady=(0, 16))

        status_label = ctk.CTkLabel(
            loading_frame,
            text="Initialisation...",
            font=ctk.CTkFont(size=16),
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
        )
        status_label.pack(expand=True)

        # Animation du loading
        self._animate_loading(loading_label)

    def _animate_loading(self, label):
        """Animation du symbole de chargement."""
        # Stop if label has been destroyed
        try:
            if not label.winfo_exists():
                return
        except Exception:
            return
        symbols = ["⚡", "✨", "💫", "⭐"]
        current_symbol = label.cget("text")
        try:
            current_index = symbols.index(current_symbol)
            next_index = (current_index + 1) % len(symbols)
        except ValueError:
            next_index = 0

        try:
            label.configure(text=symbols[next_index])
        except Exception:
            return
        # Schedule next step only if label still exists at execution
        self.after(500, lambda: (label.winfo_exists() and self._animate_loading(label)))

    def _setup_animations(self):
        """Configure les animations et transitions."""
        self._transition_active = False

        # Bind pour détecter les redimensionnements
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        """Gestion du redimensionnement avec animations."""
        if event.widget == self:
            # Adaptation responsive
            width = self.winfo_width()
            if width < 800:
                # Mode compact
                self._set_compact_mode(True)
            else:
                # Mode normal
                self._set_compact_mode(False)

    def _set_compact_mode(self, compact: bool):
        """Bascule en mode compact pour petits écrans."""
        if compact:
            # Sidebar plus étroite
            self.sidebar.configure(width=200)
        else:
            # Sidebar normale
            self.sidebar.configure(width=280)

    def _on_page_switch(self, module_id: str):
        """Gestion du changement de page avec transitions."""
        if self._transition_active or module_id == self.active_module:
            return

        self._transition_active = True

        # Animation de sortie du contenu actuel
        if self.current_content:
            self._animate_content_out(lambda: self._load_new_content(module_id))
        else:
            self._load_new_content(module_id)

    def _load_new_content(self, module_id: str):
        """Charge le nouveau contenu."""
        # Mise à jour de l'état
        self.active_module = module_id

        # Mise à jour du header
        page_info = self.page_registry.get(module_id, {})
        if page_info:
            self.header.update_page(page_info.get("label", module_id))

        # Callback vers l'application principale
        self.switch_page_callback(module_id)

    def _animate_content_out(self, callback):
        """Animation de sortie du contenu."""
        if not self.current_content:
            callback()
            return

        def fade_out(alpha=1.0):
            if alpha > 0.0:
                alpha -= 0.2
                try:
                    # Simule un fade out en modifiant l'opacité via les couleurs
                    self.content_area.configure(
                        fg_color=ctk.ThemeManager.theme["color"]["surface_dark"]
                    )
                    self.after(50, lambda: fade_out(alpha))
                except:
                    callback()
            else:
                callback()

        fade_out()

    def _animate_content_in(self):
        """Animation d'entrée du nouveau contenu."""

        def fade_in():
            try:
                self.content_area.configure(
                    fg_color=ctk.ThemeManager.theme["color"]["surface_medium"]
                )
            except:
                pass
            finally:
                self._transition_active = False

        self.after(100, fade_in)

    def set_content(self, new_content):
        """Définit le nouveau contenu avec animation."""
        # Clear loading state, but do not destroy incoming widget if already child
        for widget in list(self.content_area.winfo_children()):
            if widget is new_content:
                continue
            widget.destroy()

        # Hide current content
        if self.current_content:
            try:
                self.current_content.pack_forget()
            except:
                pass

        # Set new content
        self.current_content = new_content
        if new_content:
            try:
                new_content.pack_configure(fill="both", expand=True, padx=16, pady=10)
            except Exception:
                new_content.pack(fill="both", expand=True, padx=16, pady=10)

            # Animation d'entrée
            self._animate_content_in()

            # Toast de notification
            page_info = self.page_registry.get(self.active_module, {})
            if page_info:
                show_toast(
                    self,
                    f"Page chargée: {page_info.get('label', self.active_module)}",
                    "success",
                    1500,
                )

    def update_page_title(self, title: str, breadcrumbs: list = None):
        """Met à jour le titre de page et breadcrumbs."""
        self.header.update_page(title, breadcrumbs)

    def get_search_callback(self):
        """Retourne le callback de recherche du header."""
        return getattr(self.header, "search_callback", None)

    def set_search_callback(self, callback):
        """Définit le callback de recherche."""
        self.header.set_search_callback(callback)
