"""⚡ Quick Action Bar 2025

Floating action bar with contextual shortcuts:
- Voice logging with real-time feedback
- Photo scanning with AI recognition
- Barcode scanning with instant lookup
- Smart export options
- Contextual suggestions based on time/usage
"""

from typing import Callable, Optional, Dict, List
from datetime import datetime
import customtkinter as ctk


class QuickActionBar(ctk.CTkFrame):
    """⚡ Floating quick action bar with smart contextual actions

    Features:
    - Context-aware action suggestions
    - Voice input with visual feedback
    - Photo capture with processing indicators
    - Barcode scanning with haptic feedback
    - Smart export options based on current data
    - Keyboard shortcuts for power users
    """

    def __init__(
        self,
        parent,
        on_voice_log: Optional[Callable] = None,
        on_photo_scan: Optional[Callable] = None,
        on_barcode_scan: Optional[Callable] = None,
        on_export: Optional[Callable] = None,
        compact_mode: bool = False,
        **kwargs
    ):
        # Floating action bar styling
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = ("gray95", "gray15")
        if "corner_radius" not in kwargs:
            kwargs["corner_radius"] = 20 if not compact_mode else 12
        if "height" not in kwargs:
            kwargs["height"] = 40 if compact_mode else 50

        super().__init__(parent, **kwargs)

        self.on_voice_log = on_voice_log or (lambda: None)
        self.on_photo_scan = on_photo_scan or (lambda: None)
        self.on_barcode_scan = on_barcode_scan or (lambda: None)
        self.on_export = on_export or (lambda: None)
        self.compact_mode = compact_mode

        # Action state tracking
        self.is_voice_active = False
        self.is_photo_active = False
        self.is_barcode_active = False
        self.last_action_time = None

        # Context awareness
        self.suggested_actions = []
        self.time_based_suggestions = []

        # Animation state
        self.pulse_frame = 0
        self.is_pulsing = False

        self._create_actions()
        self._setup_context_awareness()
        self._setup_keyboard_shortcuts()

    def _create_actions(self) -> None:
        """🎛️ Create action buttons with smart styling"""
        # Container for actions
        actions_container = ctk.CTkFrame(self, fg_color="transparent")
        actions_container.pack(fill="both", expand=True, padx=8, pady=4)

        # Action button size based on mode
        btn_size = 32 if self.compact_mode else 42
        icon_size = 12 if self.compact_mode else 14

        # Voice action
        self.voice_btn = self._create_action_button(
            actions_container,
            icon="🎤",
            tooltip="Voice log food (V)",
            command=self._handle_voice_action,
            size=btn_size,
            icon_size=icon_size
        )\n        self.voice_btn.pack(side="left", padx=2)\n        \n        # Photo action\n        self.photo_btn = self._create_action_button(\n            actions_container,\n            icon="📸",\n            tooltip="Scan meal photo (P)",\n            command=self._handle_photo_action,\n            size=btn_size,\n            icon_size=icon_size\n        )\n        self.photo_btn.pack(side="left", padx=2)\n        \n        # Barcode action\n        self.barcode_btn = self._create_action_button(\n            actions_container,\n            icon="📊",\n            tooltip="Scan barcode (B)",\n            command=self._handle_barcode_action,\n            size=btn_size,\n            icon_size=icon_size\n        )\n        self.barcode_btn.pack(side="left", padx=2)\n        \n        # Separator for secondary actions\n        if not self.compact_mode:\n            separator = ctk.CTkFrame(\n                actions_container,\n                width=1,\n                height=btn_size - 8,\n                fg_color=("gray70", "gray40")\n            )\n            separator.pack(side="left", padx=8)\n        \n        # Export action\n        self.export_btn = self._create_action_button(\n            actions_container,\n            icon="📤",\n            tooltip="Export data (E)",\n            command=self._handle_export_action,\n            size=btn_size,\n            icon_size=icon_size,\n            secondary=True\n        )\n        self.export_btn.pack(side="left", padx=2)\n        \n        # Context menu for more actions (if not compact)\n        if not self.compact_mode:\n            self.more_btn = self._create_action_button(\n                actions_container,\n                icon="⋯",\n                tooltip="More actions (M)",\n                command=self._show_more_actions,\n                size=btn_size,\n                icon_size=icon_size,\n                secondary=True\n            )\n            self.more_btn.pack(side="left", padx=2)\n            \n    def _create_action_button(\n        self,\n        parent,\n        icon: str,\n        tooltip: str,\n        command: Callable,\n        size: int,\n        icon_size: int,\n        secondary: bool = False\n    ) -> ctk.CTkButton:\n        \"\"\"🔘 Create styled action button\"\"\"\n        # Button styling based on type\n        if secondary:\n            fg_color = ("gray85", "gray30")\n            hover_color = ("gray75", "gray40")\n            text_color = ("gray40", "gray70")\n        else:\n            fg_color = ("#1f538d", "#1f538d")\n            hover_color = ("#1565C0", "#1976D2")\n            text_color = ("white", "white")\n            \n        btn = ctk.CTkButton(\n            parent,\n            text=icon,\n            width=size,\n            height=size,\n            font=ctk.CTkFont(size=icon_size),\n            fg_color=fg_color,\n            hover_color=hover_color,\n            text_color=text_color,\n            corner_radius=size // 2,\n            command=command\n        )\n        \n        # Store tooltip for hover effects\n        btn._tooltip = tooltip\n        \n        # Bind hover events for tooltip simulation\n        btn.bind("<Enter>", lambda e: self._show_tooltip(btn, tooltip))\n        btn.bind("<Leave>", lambda e: self._hide_tooltip())\n        \n        return btn\n        \n    def _show_tooltip(self, widget, text: str) -> None:\n        \"\"\"💬 Show tooltip (simplified version)\"\"\"\n        # TODO: Implement proper tooltip system\n        # For now, just print to console\n        if not self.compact_mode:\n            print(f\"💡 {text}\")\n            \n    def _hide_tooltip(self) -> None:\n        \"\"\"🫥 Hide tooltip\"\"\"\n        pass\n        \n    def _setup_context_awareness(self) -> None:\n        \"\"\"🧠 Setup context-aware suggestions\"\"\"\n        # Start context monitoring\n        self._update_context_suggestions()\n        \n    def _update_context_suggestions(self) -> None:\n        \"\"\"🔄 Update contextual suggestions based on time and usage\"\"\"\n        current_hour = datetime.now().hour\n        \n        # Time-based suggestions\n        self.time_based_suggestions = []\n        \n        if 6 <= current_hour <= 10:\n            # Morning: suggest breakfast logging\n            self.time_based_suggestions.append({\n                \"action\": \"voice\",\n                \"message\": \"🌅 Good morning! Log your breakfast\",\n                \"priority\": \"high\"\n            })\n        elif 11 <= current_hour <= 14:\n            # Lunch time: suggest quick photo scan\n            self.time_based_suggestions.append({\n                \"action\": \"photo\",\n                \"message\": \"🍽️ Lunch time! Quick photo scan?\",\n                \"priority\": \"medium\"\n            })\n        elif 18 <= current_hour <= 21:\n            # Dinner time: suggest comprehensive logging\n            self.time_based_suggestions.append({\n                \"action\": \"voice\",\n                \"message\": \"🌙 Dinner time! Voice log your meal\",\n                \"priority\": \"medium\"\n            })\n            \n        # Apply suggestions to UI\n        self._apply_suggestions()\n        \n        # Schedule next update\n        self.after(300000, self._update_context_suggestions)  # Every 5 minutes\n        \n    def _apply_suggestions(self) -> None:\n        \"\"\"✨ Apply contextual suggestions to buttons\"\"\"\n        # Reset all buttons to normal state\n        self._reset_button_states()\n        \n        # Apply high-priority suggestions\n        for suggestion in self.time_based_suggestions:\n            if suggestion[\"priority\"] == \"high\":\n                self._highlight_action_button(suggestion[\"action\"])\n                \n    def _highlight_action_button(self, action: str) -> None:\n        \"\"\"🌟 Highlight suggested action button\"\"\"\n        button_map = {\n            \"voice\": self.voice_btn,\n            \"photo\": self.photo_btn,\n            \"barcode\": self.barcode_btn,\n            \"export\": self.export_btn\n        }\n        \n        btn = button_map.get(action)\n        if btn:\n            # Add subtle glow effect\n            btn.configure(\n                border_width=2,\n                border_color=(\"#4CAF50\", \"#66BB6A\")\n            )\n            \n            # Start pulse animation\n            self._start_pulse_animation(btn)\n            \n    def _start_pulse_animation(self, button: ctk.CTkButton) -> None:\n        \"\"\"💓 Start pulse animation for suggested action\"\"\"\n        if not self.is_pulsing:\n            self.is_pulsing = True\n            self.pulse_frame = 0\n            self._animate_pulse(button)\n            \n    def _animate_pulse(self, button: ctk.CTkButton) -> None:\n        \"\"\"💫 Animate button pulse effect\"\"\"\n        if self.pulse_frame < 60:  # 1 second at 60fps\n            # Subtle scale effect simulation through border\n            intensity = abs(1.0 - (self.pulse_frame % 30) / 15.0)\n            alpha = int(255 * intensity * 0.3)  # Subtle effect\n            \n            # Update border color with alpha effect\n            if intensity > 0.5:\n                button.configure(border_color=(\"#4CAF50\", \"#66BB6A\"))\n            else:\n                button.configure(border_color=(\"#81C784\", \"#81C784\"))\n                \n            self.pulse_frame += 1\n            self.after(16, lambda: self._animate_pulse(button))\n        else:\n            self.is_pulsing = False\n            button.configure(border_width=0)\n            \n    def _reset_button_states(self) -> None:\n        \"\"\"🔄 Reset all buttons to normal state\"\"\"\n        buttons = [self.voice_btn, self.photo_btn, self.barcode_btn, self.export_btn]\n        for btn in buttons:\n            btn.configure(border_width=0)\n            \n    def _setup_keyboard_shortcuts(self) -> None:\n        \"\"\"⌨️ Setup keyboard shortcuts\"\"\"\n        # Bind keyboard events to parent window\n        try:\n            root = self.winfo_toplevel()\n            root.bind(\"<KeyPress-v>\", lambda e: self._handle_voice_action())\n            root.bind(\"<KeyPress-p>\", lambda e: self._handle_photo_action())\n            root.bind(\"<KeyPress-b>\", lambda e: self._handle_barcode_action())\n            root.bind(\"<KeyPress-e>\", lambda e: self._handle_export_action())\n            root.bind(\"<KeyPress-m>\", lambda e: self._show_more_actions())\n        except Exception:\n            # Keyboard shortcuts not available\n            pass\n            \n    # Action handlers with state management\n    def _handle_voice_action(self) -> None:\n        \"\"\"🎤 Handle voice logging action\"\"\"\n        if not self.is_voice_active:\n            self.is_voice_active = True\n            self.last_action_time = datetime.now()\n            \n            # Update button state\n            self.voice_btn.configure(\n                fg_color=\"#F44336\",  # Recording red\n                text=\"⏺️\"\n            )\n            \n            # Start voice session\n            try:\n                self.on_voice_log()\n            except Exception as e:\n                print(f\"Voice action error: {e}\")\n                self._reset_voice_state()\n        else:\n            # Stop voice recording\n            self._reset_voice_state()\n            \n    def _reset_voice_state(self) -> None:\n        \"\"\"🔄 Reset voice button state\"\"\"\n        self.is_voice_active = False\n        self.voice_btn.configure(\n            fg_color=(\"#1f538d\", \"#1f538d\"),\n            text=\"🎤\"\n        )\n        \n    def _handle_photo_action(self) -> None:\n        \"\"\"📸 Handle photo scanning action\"\"\"\n        if not self.is_photo_active:\n            self.is_photo_active = True\n            self.last_action_time = datetime.now()\n            \n            # Update button state\n            self.photo_btn.configure(\n                fg_color=\"#4CAF50\",  # Processing green\n                text=\"📷\"\n            )\n            \n            try:\n                self.on_photo_scan()\n                # Auto-reset after action\n                self.after(2000, self._reset_photo_state)\n            except Exception as e:\n                print(f\"Photo action error: {e}\")\n                self._reset_photo_state()\n        \n    def _reset_photo_state(self) -> None:\n        \"\"\"🔄 Reset photo button state\"\"\"\n        self.is_photo_active = False\n        self.photo_btn.configure(\n            fg_color=(\"#1f538d\", \"#1f538d\"),\n            text=\"📸\"\n        )\n        \n    def _handle_barcode_action(self) -> None:\n        \"\"\"📊 Handle barcode scanning action\"\"\"\n        if not self.is_barcode_active:\n            self.is_barcode_active = True\n            self.last_action_time = datetime.now()\n            \n            # Update button state\n            self.barcode_btn.configure(\n                fg_color=\"#FF9800\",  # Scanning orange\n                text=\"📱\"\n            )\n            \n            try:\n                self.on_barcode_scan()\n                # Auto-reset after action\n                self.after(3000, self._reset_barcode_state)\n            except Exception as e:\n                print(f\"Barcode action error: {e}\")\n                self._reset_barcode_state()\n                \n    def _reset_barcode_state(self) -> None:\n        \"\"\"🔄 Reset barcode button state\"\"\"\n        self.is_barcode_active = False\n        self.barcode_btn.configure(\n            fg_color=(\"#1f538d\", \"#1f538d\"),\n            text=\"📊\"\n        )\n        \n    def _handle_export_action(self) -> None:\n        \"\"\"📤 Handle export action\"\"\"\n        self.last_action_time = datetime.now()\n        \n        # Visual feedback\n        original_color = self.export_btn.cget(\"fg_color\")\n        self.export_btn.configure(fg_color=\"#2196F3\")\n        \n        try:\n            self.on_export()\n        except Exception as e:\n            print(f\"Export action error: {e}\")\n        finally:\n            # Reset button color after delay\n            self.after(1000, lambda: self.export_btn.configure(fg_color=original_color))\n            \n    def _show_more_actions(self) -> None:\n        \"\"\"⋯ Show additional actions menu\"\"\"\n        # TODO: Implement context menu with additional actions\n        more_actions = [\n            \"🗂️ Import from file\",\n            \"📋 Copy nutrition data\",\n            \"🔗 Share meal plan\",\n            \"⚙️ Quick settings\",\n            \"📊 View analytics\",\n            \"💡 Get suggestions\"\n        ]\n        \n        print(\"📱 More actions menu:\")\n        for action in more_actions:\n            print(f\"  {action}\")\n            \n    # Public interface methods\n    def set_voice_active(self, active: bool) -> None:\n        \"\"\"🎤 Set voice recording state externally\"\"\"\n        if active != self.is_voice_active:\n            if active:\n                self._handle_voice_action()\n            else:\n                self._reset_voice_state()\n                \n    def set_photo_processing(self, processing: bool) -> None:\n        \"\"\"📸 Set photo processing state externally\"\"\"\n        if processing and not self.is_photo_active:\n            self.is_photo_active = True\n            self.photo_btn.configure(\n                fg_color=\"#4CAF50\",\n                text=\"⏳\"\n            )\n        elif not processing and self.is_photo_active:\n            self._reset_photo_state()\n            \n    def set_barcode_scanning(self, scanning: bool) -> None:\n        \"\"\"📊 Set barcode scanning state externally\"\"\"\n        if scanning and not self.is_barcode_active:\n            self.is_barcode_active = True\n            self.barcode_btn.configure(\n                fg_color=\"#FF9800\",\n                text=\"🔍\"\n            )\n        elif not scanning and self.is_barcode_active:\n            self._reset_barcode_state()\n            \n    def update_context(self, context_data: Dict) -> None:\n        \"\"\"🧠 Update context for smarter suggestions\"\"\"\n        # Update suggestions based on new context\n        self.suggested_actions = context_data.get(\"suggestions\", [])\n        self._apply_suggestions()\n        \n    def get_usage_stats(self) -> Dict:\n        \"\"\"📊 Get usage statistics for analytics\"\"\"\n        return {\n            \"last_action_time\": self.last_action_time,\n            \"voice_active\": self.is_voice_active,\n            \"photo_active\": self.is_photo_active,\n            \"barcode_active\": self.is_barcode_active,\n            \"suggestions_count\": len(self.time_based_suggestions)\n        }