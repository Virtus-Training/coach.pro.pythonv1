"""✨ Micro-Interactions & Animations 2025

Delightful micro-interactions that enhance user experience:
- Smooth card animations with hover effects
- Progress bars with easing functions
- Score indicators with celebration animations
- Loading states with skeleton screens
- Touch feedback and haptic-like responses
"""

import math
from datetime import datetime
from typing import Optional, Callable, Dict, Any
import customtkinter as ctk


class AnimatedCard(ctk.CTkFrame):
    """🎴 Animated card with smooth hover effects and state transitions

    Features:
    - Hover elevation and scale effects
    - Smooth color transitions
    - Loading states with skeleton animations
    - Click feedback with spring animations
    - Accessibility-friendly focus indicators
    """

    def __init__(
        self,
        parent,
        title: str = "",
        hover_scale: float = 1.02,
        animation_duration: int = 200,
        **kwargs
    ):
        # Set default colors if not provided
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = ("white", "gray20")
        if "corner_radius" not in kwargs:
            kwargs["corner_radius"] = 12

        super().__init__(parent, **kwargs)

        self.title = title
        self.hover_scale = hover_scale
        self.animation_duration = animation_duration

        # Animation state
        self.is_hovered = False
        self.is_pressed = False
        self.is_loading = False
        self.animation_frame = 0
        self.scale_factor = 1.0
        self.target_scale = 1.0

        # Elevation shadow simulation
        self.elevation = 0
        self.target_elevation = 0

        self._create_content()
        self._setup_animations()
        self._bind_interactions()

    def _create_content(self) -> None:
        """🏗️ Create card content"""
        if self.title:
            self.title_label = ctk.CTkLabel(
                self,
                text=self.title,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            self.title_label.pack(anchor="w", padx=16, pady=(16, 8))

        # Content area for child widgets
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _setup_animations(self) -> None:
        \"\"\"🎬 Setup animation system\"\"\"
        self._animate_frame()

    def _bind_interactions(self) -> None:
        \"\"\"🖱️ Bind hover and click interactions\"\"\"
        # Bind to self and all child widgets
        self._bind_recursive(self)

    def _bind_recursive(self, widget) -> None:
        \"\"\"🔄 Recursively bind events to all child widgets\"\"\"
        widget.bind("<Enter>", self._on_hover_enter)
        widget.bind("<Leave>", self._on_hover_leave)
        widget.bind("<Button-1>", self._on_click_down)
        widget.bind("<ButtonRelease-1>", self._on_click_up)

        # Bind to children
        for child in widget.winfo_children():
            try:
                self._bind_recursive(child)
            except:
                pass  # Some widgets don't support binding

    def _on_hover_enter(self, event=None) -> None:
        \"\"\"🖱️ Handle hover enter with smooth scale animation\"\"\"
        if not self.is_hovered:
            self.is_hovered = True
            self.target_scale = self.hover_scale
            self.target_elevation = 2

    def _on_hover_leave(self, event=None) -> None:
        \"\"\"🖱️ Handle hover leave with smooth return animation\"\"\"
        if self.is_hovered:
            self.is_hovered = False
            self.target_scale = 1.0
            self.target_elevation = 0

    def _on_click_down(self, event=None) -> None:
        \"\"\"👆 Handle click down with press animation\"\"\"
        self.is_pressed = True
        self.target_scale = self.hover_scale * 0.98  # Slight scale down

    def _on_click_up(self, event=None) -> None:
        \"\"\"👆 Handle click up with spring back animation\"\"\"
        self.is_pressed = False
        if self.is_hovered:
            self.target_scale = self.hover_scale
        else:
            self.target_scale = 1.0

    def _animate_frame(self) -> None:
        \"\"\"🎨 Animate one frame\"\"\"
        # Smooth scale transition
        scale_diff = self.target_scale - self.scale_factor
        if abs(scale_diff) > 0.001:
            self.scale_factor += scale_diff * 0.2  # Easing factor
            self._apply_visual_effects()

        # Smooth elevation transition
        elevation_diff = self.target_elevation - self.elevation
        if abs(elevation_diff) > 0.1:
            self.elevation += elevation_diff * 0.3
            self._apply_visual_effects()

        self.animation_frame += 1

        # Schedule next frame
        self.after(16, self._animate_frame)  # ~60fps

    def _apply_visual_effects(self) -> None:
        \"\"\"✨ Apply current animation values\"\"\"
        # Scale simulation through slight size changes
        if abs(self.scale_factor - 1.0) > 0.001:
            # Subtle border color change for scale feedback
            base_color = self.cget("fg_color")
            if self.scale_factor > 1.0:
                # Slightly brighten on hover
                self.configure(border_width=1, border_color=("gray70", "gray60"))
            else:
                self.configure(border_width=0)

        # Elevation simulation through border and slight color changes
        if self.elevation > 0:
            elevation_color = ("gray60", "gray40") if self.elevation > 1 else ("gray80", "gray50")
            self.configure(border_width=1, border_color=elevation_color)

    def set_loading(self, loading: bool) -> None:
        \"\"\"⏳ Set loading state with skeleton animation\"\"\"
        self.is_loading = loading
        if loading:
            self._show_skeleton()
        else:
            self._hide_skeleton()

    def _show_skeleton(self) -> None:
        \"\"\"💀 Show skeleton loading animation\"\"\"
        # TODO: Implement skeleton loading
        pass

    def _hide_skeleton(self) -> None:
        \"\"\"✅ Hide skeleton and show content\"\"\"
        # TODO: Implement skeleton hiding
        pass


class ProgressBar(ctk.CTkFrame):
    \"\"\"📊 Animated progress bar with smooth filling and color transitions

    Features:
    - Smooth progress animations with easing
    - Color-coded progress states (green/orange/red)
    - Percentage labels with fade-in animations
    - Customizable styling and dimensions
    - Accessibility features with ARIA-like labels
    \"\"\"

    def __init__(
        self,
        parent,
        width: int = 200,
        height: int = 20,
        progress: float = 0.0,
        target: float = 100.0,
        color_scheme: str = "default",
        show_percentage: bool = True,
        animated: bool = True,
        **kwargs
    ):
        # Set frame styling
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = ("gray90", "gray25")
        if "corner_radius" not in kwargs:
            kwargs["corner_radius"] = height // 2

        super().__init__(parent, width=width, height=height, **kwargs)

        self.target = max(target, 1)
        self.show_percentage = show_percentage
        self.animated = animated

        # Progress state
        self.current_progress = 0.0
        self.target_progress = min(progress / self.target, 1.0)
        self.animation_speed = 0.05

        # Color schemes
        self.color_schemes = {
            "default": ["#2196F3", "#4CAF50", "#FF9800", "#F44336"],
            "health": ["#4CAF50", "#8BC34A", "#FF9800", "#F44336"],
            "energy": ["#FF6B35", "#FF8C42", "#FFA726", "#FF7043"]
        }
        self.colors = self.color_schemes.get(color_scheme, self.color_schemes["default"])

        self._create_progress_bar()
        if self.animated:
            self._start_animation()

    def _create_progress_bar(self) -> None:
        \"\"\"🏗️ Create progress bar components\"\"\"
        # Progress fill frame
        self.progress_fill = ctk.CTkFrame(
            self,
            width=0,
            height=self.cget("height") - 4,
            corner_radius=self.cget("corner_radius") - 2,
            fg_color=self._get_progress_color()
        )
        self.progress_fill.place(x=2, y=2)

        # Percentage label (if enabled)
        if self.show_percentage:
            self.percentage_label = ctk.CTkLabel(
                self,
                text="0%",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=("white", "white")
            )
            self.percentage_label.place(relx=0.5, rely=0.5, anchor="center")

    def _get_progress_color(self) -> str:
        \"\"\"🎨 Get color based on current progress\"\"\"
        if self.target_progress <= 0.25:
            return self.colors[0]  # Low progress
        elif self.target_progress <= 0.75:
            return self.colors[1]  # Medium progress
        elif self.target_progress <= 1.0:
            return self.colors[2]  # High progress
        else:
            return self.colors[3]  # Over target

    def _start_animation(self) -> None:
        \"\"\"🎬 Start progress animation\"\"\"
        self._animate_progress()

    def _animate_progress(self) -> None:
        \"\"\"📈 Animate progress filling\"\"\"
        if abs(self.current_progress - self.target_progress) > 0.001:
            # Smooth easing towards target
            diff = self.target_progress - self.current_progress
            self.current_progress += diff * self.animation_speed

            # Update visual progress
            self._update_visual_progress()

            # Continue animation
            self.after(16, self._animate_progress)
        else:
            # Animation complete
            self.current_progress = self.target_progress
            self._update_visual_progress()

    def _update_visual_progress(self) -> None:
        \"\"\"🎨 Update visual progress representation\"\"\"
        # Calculate fill width
        total_width = self.cget("width") - 4
        fill_width = max(0, total_width * self.current_progress)

        # Update progress fill
        self.progress_fill.configure(
            width=fill_width,
            fg_color=self._get_progress_color()
        )

        # Update percentage label
        if self.show_percentage:
            percentage = self.current_progress * 100
            self.percentage_label.configure(text=f"{percentage:.0f}%")

    def set_progress(self, progress: float, target: Optional[float] = None) -> None:
        \"\"\"📊 Set new progress value with animation\"\"\"
        if target is not None:
            self.target = max(target, 1)

        old_target = self.target_progress
        self.target_progress = min(progress / self.target, 1.0)

        if self.animated and abs(self.target_progress - old_target) > 0.001:
            self._start_animation()
        else:
            self.current_progress = self.target_progress
            self._update_visual_progress()

    def set_color_scheme(self, scheme: str) -> None:
        \"\"\"🎨 Set color scheme\"\"\"
        self.colors = self.color_schemes.get(scheme, self.color_schemes["default"])
        self._update_visual_progress()


class ScoreIndicator(ctk.CTkFrame):
    \"\"\"🎯 Animated score indicator with circular progress and celebrations

    Features:
    - Circular progress indicator with smooth animations
    - Score-based color transitions
    - Celebration animations for milestones
    - Trend indicators (up/down arrows)
    - Customizable score ranges and thresholds
    \"\"\"

    def __init__(
        self,
        parent,
        score: float = 0,
        max_score: float = 100,
        label: str = "Score",
        color_scheme: str = "health",
        size: int = 100,
        **kwargs
    ):
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = "transparent"

        super().__init__(parent, width=size, height=size + 40, **kwargs)

        self.max_score = max_score
        self.label = label
        self.size = size
        self.color_scheme = color_scheme

        # Score state
        self.current_score = 0.0
        self.target_score = min(score, max_score)
        self.previous_score = 0.0
        self.animation_speed = 0.1

        # Celebration state
        self.is_celebrating = False
        self.celebration_frame = 0

        self._create_indicator()
        self._start_animation()

    def _create_indicator(self) -> None:
        \"\"\"🏗️ Create score indicator components\"\"\"
        # Canvas for circular progress
        self.canvas = ctk.CTkCanvas(
            self,
            width=self.size,
            height=self.size,
            bg=self._get_bg_color(),
            highlightthickness=0
        )
        self.canvas.pack(pady=(10, 5))

        # Score label
        self.score_label = ctk.CTkLabel(
            self,
            text=f"{self.target_score:.0f}",
            font=ctk.CTkFont(size=self.size // 4, weight="bold")
        )
        self.score_label.pack()

        # Description label
        self.desc_label = ctk.CTkLabel(
            self,
            text=self.label,
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray50")
        )
        self.desc_label.pack()

    def _get_bg_color(self) -> str:
        \"\"\"🎨 Get background color\"\"\"
        try:
            return "#212121" if ctk.get_appearance_mode() == "Dark" else "#FAFAFA"
        except:
            return "#212121"

    def _get_score_color(self, score: float) -> str:
        \"\"\"🎨 Get color based on score\"\"\"
        ratio = score / self.max_score

        if self.color_scheme == "health":
            if ratio >= 0.8:
                return "#4CAF50"  # Excellent - Green
            elif ratio >= 0.6:
                return "#8BC34A"  # Good - Light Green
            elif ratio >= 0.4:
                return "#FF9800"  # Fair - Orange
            else:
                return "#F44336"  # Poor - Red
        else:
            # Default blue scheme
            if ratio >= 0.8:
                return "#2196F3"
            elif ratio >= 0.6:
                return "#03A9F4"
            elif ratio >= 0.4:
                return "#FF9800"
            else:
                return "#F44336"

    def _start_animation(self) -> None:
        \"\"\"🎬 Start score animation\"\"\"
        self._animate_score()

    def _animate_score(self) -> None:
        \"\"\"📈 Animate score counting up\"\"\"
        if abs(self.current_score - self.target_score) > 0.1:
            # Smooth easing towards target
            diff = self.target_score - self.current_score
            self.current_score += diff * self.animation_speed

            # Update visuals
            self._update_visual_score()

            # Continue animation
            self.after(16, self._animate_score)
        else:
            # Animation complete
            self.current_score = self.target_score
            self._update_visual_score()
            self._check_celebration()

    def _update_visual_score(self) -> None:
        \"\"\"🎨 Update visual score display\"\"\"
        # Clear canvas
        self.canvas.delete("all")

        # Draw circular progress
        self._draw_circular_progress()

        # Update score label
        self.score_label.configure(
            text=f"{self.current_score:.0f}",
            text_color=self._get_score_color(self.current_score)
        )

    def _draw_circular_progress(self) -> None:
        \"\"\"⭕ Draw circular progress indicator\"\"\"
        center = self.size // 2
        radius = center - 10
        width = 8

        # Background circle
        self.canvas.create_oval(
            center - radius,
            center - radius,
            center + radius,
            center + radius,
            outline=("#E0E0E0" if ctk.get_appearance_mode() == "Light" else "#404040"),
            width=width,
            style="arc",
            extent=360
        )

        # Progress arc
        if self.current_score > 0:
            progress_ratio = min(self.current_score / self.max_score, 1.0)
            extent = progress_ratio * 360

            color = self._get_score_color(self.current_score)

            # Add glow effect for high scores
            if progress_ratio > 0.8:
                # Outer glow
                self.canvas.create_oval(
                    center - radius - 2,
                    center - radius - 2,
                    center + radius + 2,
                    center + radius + 2,
                    outline=color,
                    width=2,
                    style="arc",
                    start=90,
                    extent=-extent
                )

            # Main progress arc
            self.canvas.create_oval(
                center - radius,
                center - radius,
                center + radius,
                center + radius,
                outline=color,
                width=width,
                style="arc",
                start=90,  # Start from top
                extent=-extent  # Clockwise
            )

    def _check_celebration(self) -> None:
        \"\"\"🎉 Check if celebration is needed\"\"\"
        # Celebrate milestones
        milestones = [25, 50, 75, 100]
        for milestone in milestones:
            if (self.previous_score < milestone <= self.target_score and
                self.target_score >= milestone):
                self._trigger_celebration()
                break

    def _trigger_celebration(self) -> None:
        \"\"\"🎉 Trigger celebration animation\"\"\"
        if not self.is_celebrating:
            self.is_celebrating = True
            self.celebration_frame = 0
            self._animate_celebration()

    def _animate_celebration(self) -> None:
        \"\"\"🎊 Animate celebration effects\"\"\"
        if self.celebration_frame < 30:  # 30 frames of celebration
            # Pulse effect
            scale = 1.0 + math.sin(self.celebration_frame * 0.5) * 0.1

            # Color flash effect
            if self.celebration_frame % 6 < 3:
                color = "#FFD700"  # Gold flash
            else:
                color = self._get_score_color(self.current_score)

            self.score_label.configure(text_color=color)

            self.celebration_frame += 1
            self.after(50, self._animate_celebration)
        else:
            # End celebration
            self.is_celebrating = False
            self.score_label.configure(
                text_color=self._get_score_color(self.current_score)
            )

    def update_score(self, new_score: float) -> None:
        \"\"\"📊 Update score with animation\"\"\"
        self.previous_score = self.target_score
        self.target_score = min(new_score, self.max_score)

        if abs(self.target_score - self.current_score) > 0.1:
            self._start_animation()
        else:
            self.current_score = self.target_score
            self._update_visual_score()


class StreakTracker(ctk.CTkFrame):
    \"\"\"🔥 Streak tracking widget with fire animations

    Features:
    - Fire emoji animations based on streak length
    - Streak milestone celebrations
    - Progress towards next milestone
    - Motivational messages
    - Social sharing integration ready
    \"\"\"

    def __init__(
        self,
        parent,
        streak_days: int = 0,
        streak_type: str = "nutrition",
        **kwargs
    ):
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = ("gray95", "gray15")
        if "corner_radius" not in kwargs:
            kwargs["corner_radius"] = 12

        super().__init__(parent, **kwargs)

        self.streak_days = streak_days
        self.streak_type = streak_type

        # Milestone definitions
        self.milestones = [1, 3, 7, 14, 21, 30, 60, 90, 100, 365]
        self.milestone_rewards = {
            1: "🌱 Getting started!",
            3: "🔥 Building momentum!",
            7: "💪 One week strong!",
            14: "⭐ Two weeks amazing!",
            21: "🏆 Habit formed!",
            30: "👑 Monthly champion!",
            60: "🎯 Consistency master!",
            90: "🚀 Unstoppable force!",
            100: "💎 Century achiever!",
            365: "🌟 Year-long legend!"
        }

        self._create_tracker()

    def _create_tracker(self) -> None:
        \"\"\"🏗️ Create streak tracker\"\"\"
        # Fire icon with animation
        self.fire_label = ctk.CTkLabel(
            self,
            text=self._get_fire_animation(),
            font=ctk.CTkFont(size=32)
        )
        self.fire_label.pack(pady=(16, 8))

        # Streak count
        self.streak_label = ctk.CTkLabel(
            self,
            text=f"{self.streak_days} day{'s' if self.streak_days != 1 else ''}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.streak_label.pack()

        # Streak type
        type_label = ctk.CTkLabel(
            self,
            text=f"{self.streak_type.title()} Streak",
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray50")
        )
        type_label.pack(pady=(0, 8))

        # Next milestone
        self._create_milestone_progress()

        # Motivational message
        self._create_motivation_message()

    def _get_fire_animation(self) -> str:
        \"\"\"🔥 Get fire emoji based on streak length\"\"\"
        if self.streak_days == 0:
            return "⭕"  # No streak
        elif self.streak_days < 3:
            return "🔥"  # Single fire
        elif self.streak_days < 7:
            return "🔥🔥"  # Double fire
        elif self.streak_days < 30:
            return "🔥🔥🔥"  # Triple fire
        else:
            return "🔥🔥🔥🔥"  # Quad fire for long streaks

    def _create_milestone_progress(self) -> None:
        \"\"\"🎯 Create next milestone progress\"\"\"
        next_milestone = self._get_next_milestone()
        if next_milestone:
            progress_frame = ctk.CTkFrame(self, fg_color="transparent")
            progress_frame.pack(fill="x", padx=16, pady=8)

            # Progress to next milestone
            progress = min(self.streak_days / next_milestone, 1.0)

            milestone_label = ctk.CTkLabel(
                progress_frame,
                text=f"Next milestone: {next_milestone} days",
                font=ctk.CTkFont(size=10),
                text_color=("gray60", "gray50")
            )
            milestone_label.pack()

            # Mini progress bar
            progress_bar = ProgressBar(
                progress_frame,
                width=120,
                height=6,
                progress=self.streak_days,
                target=next_milestone,
                color_scheme="energy",
                show_percentage=False
            )
            progress_bar.pack(pady=4)

    def _create_motivation_message(self) -> None:
        \"\"\"💪 Create motivational message\"\"\"
        message = self._get_motivation_message()
        if message:
            message_label = ctk.CTkLabel(
                self,
                text=message,
                font=ctk.CTkFont(size=10),
                text_color=("gray50", "gray60"),
                wraplength=150
            )
            message_label.pack(padx=16, pady=(0, 16))

    def _get_next_milestone(self) -> Optional[int]:
        \"\"\"🎯 Get next streak milestone\"\"\"
        for milestone in self.milestones:
            if milestone > self.streak_days:
                return milestone
        return None

    def _get_motivation_message(self) -> str:
        \"\"\"💪 Get motivational message based on streak\"\"\"
        if self.streak_days == 0:
            return "Start your streak today! 💪"
        elif self.streak_days in self.milestone_rewards:
            return self.milestone_rewards[self.streak_days]
        elif self.streak_days < 7:
            return f"Keep going! {7 - self.streak_days} days to your first week!"
        elif self.streak_days < 30:
            return f"Fantastic progress! {30 - self.streak_days} days to a month!"
        else:
            return "You're on fire! Keep the momentum! 🚀"

    def update_streak(self, new_streak: int) -> None:
        \"\"\"🔄 Update streak with celebration if needed\"\"\"
        old_streak = self.streak_days
        self.streak_days = new_streak

        # Check for milestone celebration
        if new_streak in self.milestone_rewards and new_streak > old_streak:
            self._celebrate_milestone()

        # Update visuals
        self.fire_label.configure(text=self._get_fire_animation())
        self.streak_label.configure(text=f"{self.streak_days} day{'s' if self.streak_days != 1 else ''}")

        # Recreate milestone progress
        for widget in self.winfo_children():
            if hasattr(widget, '_milestone_progress'):
                widget.destroy()
        self._create_milestone_progress()
        self._create_motivation_message()

    def _celebrate_milestone(self) -> None:
        \"\"\"🎉 Celebrate reaching a milestone\"\"\"
        # TODO: Implement milestone celebration animation
        print(f"🎉 Milestone reached: {self.streak_days} days!")