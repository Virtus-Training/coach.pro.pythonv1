"""
Modern UI Kit - Composants d'interface avancés avec animations et effects
Inspiré de Discord, Notion, VS Code et Figma
"""

import customtkinter as ctk


# ===== Utils: Couleurs sûres pour tkinter (pas de RGBA) =====
def _hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _rgb_to_hex(rgb: tuple) -> str:
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"


def _get_app_bg_color() -> str:
    """Retourne la couleur d'arrière‑plan principale selon le thème courant."""
    try:
        fg = ctk.ThemeManager.theme.get("CTk", {}).get(
            "fg_color", ["#111827", "#111827"]
        )  # [light, dark]
        if isinstance(fg, (list, tuple)) and len(fg) >= 2:
            mode = ctk.get_appearance_mode()
            idx = 0 if str(mode).lower() == "light" else 1
            return fg[idx]
        if isinstance(fg, str):
            return fg
    except Exception:
        pass
    return "#111827"


def _blend_hex(bg_hex: str, fg_hex: str, alpha: float) -> str:
    """Mélange fg sur bg avec alpha (0..1) et retourne un #RRGGBB valide."""
    br, bg, bb = _hex_to_rgb(bg_hex)
    fr, fg_, fb = _hex_to_rgb(fg_hex)
    r = round((1 - alpha) * br + alpha * fr)
    g = round((1 - alpha) * bg + alpha * fg_)
    b = round((1 - alpha) * bb + alpha * fb)
    return _rgb_to_hex((r, g, b))


def _tint_primary(alpha: float) -> str:
    """Retourne une teinte de la couleur primaire mélangée au fond (simule la transparence)."""
    primary = ctk.ThemeManager.theme["color"].get("primary", "#6366F1")
    return _blend_hex(_get_app_bg_color(), primary, max(0.0, min(1.0, alpha)))


class AnimatedButton(ctk.CTkButton):
    """Bouton avec animation hover et click effects."""

    def __init__(self, master, **kwargs):
        # Configuration par défaut modern
        modern_defaults = {
            "corner_radius": 8,
            "border_width": 0,
            "height": 44,
            "font": ctk.CTkFont(size=14, weight="bold"),
            "cursor": "hand2",
        }

        # Merge avec les kwargs
        for key, value in modern_defaults.items():
            kwargs.setdefault(key, value)

        super().__init__(master, **kwargs)

        # États pour animation
        self._is_hovering = False
        self._animation_running = False

        # Bind des événements
        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)
        self.bind("<Button-1>", self._on_mouse_click)

    def _on_hover_enter(self, event):
        """Animation d'entrée hover."""
        if not self._animation_running:
            self._is_hovering = True
            self._animate_hover(True)

    def _on_hover_leave(self, event):
        """Animation de sortie hover."""
        if not self._animation_running:
            self._is_hovering = False
            self._animate_hover(False)

    def _on_mouse_click(self, event):
        """Effet de click avec pulse."""
        self._animate_click()

    def _animate_hover(self, entering: bool):
        """Animation smooth du hover effect."""
        if self._animation_running:
            return

        self._animation_running = True

        def animate():
            # Simule une transition smooth en modifiant l'opacité
            try:
                current_color = self.cget("fg_color")
                if entering:
                    # Slightly lighter on hover
                    if isinstance(current_color, str) and current_color.startswith("#"):
                        # Simple hover effect
                        self.configure(fg_color=self.cget("hover_color"))
                else:
                    # Back to original
                    self.configure(fg_color=current_color)

                # Simulate scale effect with padding
                if entering:
                    # 25% de teinte primaire (token si dispo)
                    border_col = ctk.ThemeManager.theme["color"].get(
                        "primary_t25", _tint_primary(0.25)
                    )
                    self.configure(border_width=1, border_color=border_col)
                else:
                    self.configure(border_width=0)

            except Exception:
                pass
            finally:
                self._animation_running = False

        # Lance l'animation dans un thread léger
        self.after(1, animate)

    def _animate_click(self):
        """Effet de pulse au click."""

        def pulse():
            try:
                # 50% de teinte primaire (token si dispo)
                border_col = ctk.ThemeManager.theme["color"].get(
                    "primary_t50", _tint_primary(0.5)
                )
                self.configure(border_width=2, border_color=border_col)
                self.after(100, lambda: self.configure(border_width=0))
            except Exception:
                pass

        self.after(1, pulse)


class GlassCard(ctk.CTkFrame):
    """Carte avec effet glassmorphism moderne."""

    def __init__(self, master, title: str = "", **kwargs):
        # Configuration glassmorphism
        glass_defaults = {
            "corner_radius": 16,
            "border_width": 1,
            "border_color": ctk.ThemeManager.theme["color"].get(
                "subtle_border", "#334155"
            ),
            "fg_color": ctk.ThemeManager.theme["color"].get(
                "surface_elevated", "#2D2F5F"
            ),
        }

        for key, value in glass_defaults.items():
            kwargs.setdefault(key, value)

        super().__init__(master, **kwargs)

        self.title = title
        self._hover_active = False

        if title:
            self._create_header()

        # Container pour le contenu
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        padding = 20 if title else 16
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=padding,
            pady=(0 if title else padding, padding),
        )

        # Hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _create_header(self):
        """Crée le header de la carte."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(16, 8))

        title_label = ctk.CTkLabel(
            header_frame,
            text=self.title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=ctk.ThemeManager.theme["color"]["primary_text"],
        )
        title_label.pack(anchor="w")

        # Ligne décorative
        divider = ctk.CTkFrame(
            header_frame,
            height=2,
            fg_color=ctk.ThemeManager.theme["color"].get("primary", "#6366F1"),
        )
        divider.pack(fill="x", pady=(8, 0))

    def _on_enter(self, event):
        """Hover effect - subtle glow."""
        if not self._hover_active:
            self._hover_active = True
            self.configure(
                border_color=ctk.ThemeManager.theme["color"].get(
                    "primary_light", "#A5B4FC"
                ),
                border_width=2,
            )

    def _on_leave(self, event):
        """Remove hover effect."""
        if self._hover_active:
            self._hover_active = False
            self.configure(
                border_color=ctk.ThemeManager.theme["color"].get(
                    "subtle_border", "#334155"
                ),
                border_width=1,
            )


class ModernTabView(ctk.CTkFrame):
    """TabView avec animations et style moderne."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._tabs = {}
        self._active_tab = None
        self._tab_buttons = {}

        # Header pour les tabs
        self.tab_header = ctk.CTkFrame(
            self,
            height=60,
            fg_color=ctk.ThemeManager.theme["color"].get("surface_light", "#252651"),
            corner_radius=12,
        )
        self.tab_header.pack(fill="x", pady=(0, 16))
        self.tab_header.pack_propagate(False)

        # Container pour les boutons de tabs
        self.tab_buttons_frame = ctk.CTkFrame(self.tab_header, fg_color="transparent")
        self.tab_buttons_frame.pack(expand=True, pady=12, padx=16)

        # Content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

    def add_tab(self, name: str, text: str) -> ctk.CTkFrame:
        """Ajoute un nouvel onglet."""
        # Bouton de tab
        # Couleur de hover sans alpha (simule un léger overlay clair)
        safe_hover_overlay = ctk.ThemeManager.theme["color"].get(
            "overlay_low", _blend_hex(_get_app_bg_color(), "#FFFFFF", 0.04)
        )

        tab_button = AnimatedButton(
            self.tab_buttons_frame,
            text=text,
            height=36,
            corner_radius=8,
            fg_color="transparent",
            text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            hover_color=safe_hover_overlay,
            command=lambda: self.set_active_tab(name),
        )
        tab_button.pack(side="left", padx=(0, 8))
        self._tab_buttons[name] = tab_button

        # Content frame
        tab_content = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self._tabs[name] = tab_content

        # Si premier tab, le rendre actif
        if not self._active_tab:
            self.set_active_tab(name)

        return tab_content

    def set_active_tab(self, name: str):
        """Change l'onglet actif avec animation."""
        if name not in self._tabs or name == self._active_tab:
            return

        # Hide current tab
        if self._active_tab and self._active_tab in self._tabs:
            self._tabs[self._active_tab].pack_forget()
            # Reset button style
            self._tab_buttons[self._active_tab].configure(
                fg_color="transparent",
                text_color=ctk.ThemeManager.theme["color"]["secondary_text"],
            )

        # Show new tab with animation
        self._active_tab = name
        self._tabs[name].pack(fill="both", expand=True)

        # Update button style
        self._tab_buttons[name].configure(
            fg_color=ctk.ThemeManager.theme["color"]["primary"], text_color="white"
        )

        # Subtle animation effect
        self._animate_tab_transition(name)

    def _animate_tab_transition(self, tab_name: str):
        """Animation de transition entre tabs."""
        tab_frame = self._tabs[tab_name]

        def fade_in():
            try:
                # Simulate fade in with alpha changes
                local_overlay = ctk.ThemeManager.theme["color"].get(
                    "overlay_low", _blend_hex(_get_app_bg_color(), "#FFFFFF", 0.04)
                )
                tab_frame.configure(fg_color=local_overlay)
                self.after(150, lambda: tab_frame.configure(fg_color="transparent"))
            except Exception:
                pass

        self.after(50, fade_in)


class StatusIndicator(ctk.CTkFrame):
    """Indicateur de status avec couleur et animation."""

    def __init__(self, master, status: str = "success", text: str = "", **kwargs):
        self.status_colors = {
            "success": ctk.ThemeManager.theme["color"].get("success", "#22C55E"),
            "warning": ctk.ThemeManager.theme["color"].get("warning", "#F59E0B"),
            "error": ctk.ThemeManager.theme["color"].get("error", "#EF4444"),
            "info": ctk.ThemeManager.theme["color"].get("primary", "#6366F1"),
            "neutral": ctk.ThemeManager.theme["color"].get("muted_text", "#64748B"),
        }

        super().__init__(
            master,
            fg_color=self.status_colors.get(status, self.status_colors["neutral"]),
            corner_radius=12,
            height=32,
            **kwargs,
        )
        self.pack_propagate(False)

        self.status = status
        self._create_content(text)

    def _create_content(self, text: str):
        """Crée le contenu de l'indicateur."""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True, padx=12, pady=6)

        # Status dot
        dot = ctk.CTkLabel(
            content_frame, text="●", font=ctk.CTkFont(size=16), text_color="white"
        )
        dot.pack(side="left")

        if text:
            text_label = ctk.CTkLabel(
                content_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
            )
            text_label.pack(side="left", padx=(4, 0))

    def update_status(self, status: str, text: str = ""):
        """Met à jour le status avec animation."""
        new_color = self.status_colors.get(status, self.status_colors["neutral"])

        # Animation de changement
        def transition():
            try:
                self.configure(fg_color=new_color)
                # Pulse effect
                self.configure(corner_radius=16)
                self.after(200, lambda: self.configure(corner_radius=12))
            except Exception:
                pass

        self.after(1, transition)

        if text:
            # Update text content
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for child in widget.winfo_children():
                        if (
                            isinstance(child, ctk.CTkLabel)
                            and child.cget("text") != "●"
                        ):
                            child.configure(text=text)
                            break


class FloatingActionButton(ctk.CTkButton):
    """Bouton d'action flottant avec effet d'ombre."""

    def __init__(self, master, icon_text: str = "➕", **kwargs):
        fab_defaults = {
            "width": 56,
            "height": 56,
            "corner_radius": 28,
            "text": icon_text,
            "font": ctk.CTkFont(size=20),
            "fg_color": ctk.ThemeManager.theme["color"]["primary"],
            "hover_color": ctk.ThemeManager.theme["color"].get(
                "primary_hover", "#4F46E5"
            ),
            "cursor": "hand2",
        }

        for key, value in fab_defaults.items():
            kwargs.setdefault(key, value)

        super().__init__(master, **kwargs)

        # Hover effects
        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)

    def _on_hover_enter(self, event):
        """Scale up effect on hover."""
        self.configure(width=60, height=60, corner_radius=30)

    def _on_hover_leave(self, event):
        """Scale back to normal."""
        self.configure(width=56, height=56, corner_radius=28)


class ModernProgressBar(ctk.CTkFrame):
    """Barre de progression moderne avec animations."""

    def __init__(self, master, max_value: float = 100, **kwargs):
        super().__init__(
            master,
            height=8,
            fg_color=ctk.ThemeManager.theme["color"].get("surface_light", "#252651"),
            corner_radius=4,
            **kwargs,
        )

        self.max_value = max_value
        self.current_value = 0

        # Barre de progression
        self.progress_bar = ctk.CTkFrame(
            self,
            height=8,
            fg_color=ctk.ThemeManager.theme["color"]["primary"],
            corner_radius=4,
        )

        self.pack_propagate(False)

    def set_value(self, value: float, animate: bool = True):
        """Met à jour la valeur avec animation optionnelle."""
        if value > self.max_value:
            value = self.max_value
        elif value < 0:
            value = 0

        percentage = value / self.max_value

        if animate:
            self._animate_to_value(percentage)
        else:
            self._set_progress_width(percentage)

        self.current_value = value

    def _animate_to_value(self, target_percentage: float):
        """Animation fluide vers la valeur cible."""
        current_percentage = self.current_value / self.max_value
        steps = 20
        step_size = (target_percentage - current_percentage) / steps

        def animate_step(step: int):
            if step <= steps:
                new_percentage = current_percentage + (step_size * step)
                self._set_progress_width(new_percentage)
                self.after(20, lambda: animate_step(step + 1))

        animate_step(1)

    def _set_progress_width(self, percentage: float):
        """Définit la largeur de la barre de progression."""
        try:
            self.update_idletasks()
            total_width = self.winfo_width()
            if total_width > 0:
                progress_width = int(total_width * percentage)

                # Clear previous
                self.progress_bar.pack_forget()

                if progress_width > 0:
                    # Configure new width
                    self.progress_bar.configure(width=progress_width)
                    self.progress_bar.pack(anchor="w", fill="y")
        except Exception:
            pass


class NotificationToast(ctk.CTkToplevel):
    """Toast notification moderne avec auto-hide."""

    def __init__(self, master, message: str, type_: str = "info", duration: int = 3000):
        super().__init__(master)

        # Configuration de la fenêtre
        self.withdraw()  # Cacher au début
        self.overrideredirect(True)  # Pas de bordure
        self.attributes("-topmost", True)

        # Configuration des couleurs par type
        colors = {
            "success": ctk.ThemeManager.theme["color"]["success"],
            "warning": ctk.ThemeManager.theme["color"]["warning"],
            "error": ctk.ThemeManager.theme["color"]["error"],
            "info": ctk.ThemeManager.theme["color"]["primary"],
        }

        # Frame principal
        main_frame = GlassCard(
            self, fg_color=colors.get(type_, colors["info"]), corner_radius=12
        )
        main_frame.pack(padx=8, pady=8)

        # Message
        message_label = ctk.CTkLabel(
            main_frame.content_frame,
            text=message,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            wraplength=300,
        )
        message_label.pack(pady=(8, 8))

        # Position et animation
        self._position_toast()
        self._show_with_animation()

        # Auto-hide
        if duration > 0:
            self.after(duration, self._hide_with_animation)

    def _position_toast(self):
        """Positionne la notification en haut à droite."""
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        screen_width = self.winfo_screenwidth()
        self.winfo_screenheight()

        x = screen_width - width - 20
        y = 60

        self.geometry(f"{width}x{height}+{x}+{y}")

    def _show_with_animation(self):
        """Animation d'apparition (slide from right)."""
        self.deiconify()
        # Simple fade in effect
        self.attributes("-alpha", 0.0)

        def fade_in(alpha=0.0):
            if alpha < 1.0:
                alpha += 0.1
                self.attributes("-alpha", alpha)
                self.after(30, lambda: fade_in(alpha))

        fade_in()

    def _hide_with_animation(self):
        """Animation de disparition."""

        def fade_out(alpha=1.0):
            if alpha > 0.0:
                alpha -= 0.1
                try:
                    self.attributes("-alpha", alpha)
                    self.after(30, lambda: fade_out(alpha))
                except:
                    self.destroy()
            else:
                self.destroy()

        fade_out()


# Fonction utilitaire pour créer des notifications
def show_toast(parent, message: str, type_: str = "info", duration: int = 3000):
    """Affiche une notification toast."""
    return NotificationToast(parent, message, type_, duration)
