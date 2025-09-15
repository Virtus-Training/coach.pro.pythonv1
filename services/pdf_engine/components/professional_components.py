"""
Professional PDF Components - Premium UI elements for commercial-grade templates
Includes data visualizations, progress indicators, and premium layouts
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from io import BytesIO
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.units import cm, inch
from reportlab.platypus import Flowable, Paragraph, Table, TableStyle
try:
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.lineplots import LinePlot
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False
from reportlab.graphics.shapes import Drawing, Rect, Circle, String
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class ProgressBarComponent(Flowable):
    """Premium progress bar with gradient and labels"""

    def __init__(self, value: float, max_value: float = 100, width: float = 200, height: float = 20,
                 color_start: str = "#4CAF50", color_end: str = "#81C784", bg_color: str = "#E0E0E0"):
        self.value = value
        self.max_value = max_value
        self.width = width
        self.height = height
        self.color_start = HexColor(color_start)
        self.color_end = HexColor(color_end)
        self.bg_color = HexColor(bg_color)

    def draw(self):
        progress_width = (self.value / self.max_value) * self.width if self.max_value > 0 else 0

        # Background
        self.canv.setFillColor(self.bg_color)
        self.canv.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)

        # Progress bar with gradient effect
        if progress_width > 0:
            self.canv.setFillColor(self.color_start)
            self.canv.roundRect(0, 0, progress_width, self.height, 5, fill=1, stroke=0)

        # Text overlay
        percentage = f"{(self.value/self.max_value)*100:.1f}%" if self.max_value > 0 else "0%"
        self.canv.setFillColor(HexColor("#FFFFFF"))
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.drawCentredText(self.width/2, self.height/2 - 3, percentage)


class MacronutrientWheelComponent(Flowable):
    """Premium macronutrient pie chart with custom styling"""

    def __init__(self, protein: float, carbs: float, fat: float,
                 width: float = 150, height: float = 150):
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.width = width
        self.height = height
        self.total = protein + carbs + fat

    def draw(self):
        if self.total == 0:
            return

        if not CHARTS_AVAILABLE:
            # Fallback to simple text representation
            self.canv.setFillColor(HexColor("#000000"))
            self.canv.setFont("Helvetica-Bold", 12)
            self.canv.drawCentredText(self.width/2, self.height/2 + 10, "MACROS")

            self.canv.setFont("Helvetica", 10)
            protein_pct = (self.protein / self.total * 100) if self.total > 0 else 0
            carbs_pct = (self.carbs / self.total * 100) if self.total > 0 else 0
            fat_pct = (self.fat / self.total * 100) if self.total > 0 else 0

            self.canv.drawCentredText(self.width/2, self.height/2 - 10, f"P: {protein_pct:.0f}%")
            self.canv.drawCentredText(self.width/2, self.height/2 - 25, f"C: {carbs_pct:.0f}%")
            self.canv.drawCentredText(self.width/2, self.height/2 - 40, f"L: {fat_pct:.0f}%")
            return

        drawing = Drawing(self.width, self.height)

        # Create pie chart
        pie = Pie()
        pie.x = 25
        pie.y = 25
        pie.width = 100
        pie.height = 100

        # Data and colors
        pie.data = [self.protein, self.carbs, self.fat]
        pie.labels = ['Protéines', 'Glucides', 'Lipides']
        pie.slices.strokeColor = HexColor("#FFFFFF")
        pie.slices.strokeWidth = 2

        # Custom colors
        pie.slices[0].fillColor = HexColor("#FF6B6B")  # Protein - Red
        pie.slices[1].fillColor = HexColor("#4ECDC4")  # Carbs - Teal
        pie.slices[2].fillColor = HexColor("#FFE66D")  # Fat - Yellow

        drawing.add(pie)
        drawing.drawOn(self.canv, 0, 0)


class WorkoutBlockComponent(Flowable):
    """Premium workout block with exercise visualization"""

    def __init__(self, block_data: Dict[str, Any], width: float = 400, theme: str = "professional"):
        self.block_data = block_data
        self.width = width
        self.theme = theme
        self.height = self._calculate_height()

    def _calculate_height(self) -> float:
        exercises = self.block_data.get("exercises", [])
        base_height = 60  # Header
        exercise_height = len(exercises) * 30 + 20  # Exercises + padding
        return base_height + exercise_height

    def draw(self):
        y_position = self.height - 20

        # Block header with gradient background
        self._draw_block_header(y_position)
        y_position -= 40

        # Exercise list
        exercises = self.block_data.get("exercises", [])
        for i, exercise in enumerate(exercises):
            self._draw_exercise_row(exercise, y_position - (i * 30))

    def _draw_block_header(self, y: float):
        """Draw premium block header with gradient"""
        # Header background
        self.canv.setFillColor(HexColor("#2563EB"))
        self.canv.roundRect(0, y-30, self.width, 30, 5, fill=1, stroke=0)

        # Title
        self.canv.setFillColor(HexColor("#FFFFFF"))
        self.canv.setFont("Helvetica-Bold", 14)
        title = self.block_data.get("title", "Bloc d'exercices")
        self.canv.drawString(15, y-20, title)

        # Duration/Format info
        duration = self.block_data.get("duration", "")
        format_type = self.block_data.get("format", "")
        info = f"{format_type} - {duration} min" if duration else format_type

        if info:
            self.canv.setFont("Helvetica", 10)
            self.canv.drawRightString(self.width - 15, y-20, info)

    def _draw_exercise_row(self, exercise: Dict[str, Any], y: float):
        """Draw individual exercise with professional styling"""
        # Alternating row background
        if hasattr(self, '_row_counter'):
            self._row_counter += 1
        else:
            self._row_counter = 0

        if self._row_counter % 2 == 0:
            self.canv.setFillColor(HexColor("#F8FAFC"))
            self.canv.rect(0, y-25, self.width, 25, fill=1, stroke=0)

        # Exercise name
        self.canv.setFillColor(HexColor("#1F2937"))
        self.canv.setFont("Helvetica-Bold", 11)
        name = exercise.get("name", "Exercise")
        self.canv.drawString(15, y-15, name)

        # Reps/Sets
        reps = exercise.get("reps", "")
        if reps:
            self.canv.setFont("Helvetica", 10)
            self.canv.setFillColor(HexColor("#6B7280"))
            self.canv.drawString(self.width * 0.6, y-15, reps)

        # Notes
        notes = exercise.get("notes", "")
        if notes:
            self.canv.setFont("Helvetica-Oblique", 9)
            self.canv.setFillColor(HexColor("#9CA3AF"))
            # Truncate long notes
            max_chars = int((self.width * 0.35) / 5)  # Approximate character width
            if len(notes) > max_chars:
                notes = notes[:max_chars-3] + "..."
            self.canv.drawString(15, y-5, notes)


class NutritionFactsComponent(Flowable):
    """FDA-style nutrition facts panel with professional styling"""

    def __init__(self, nutrition_data: Dict[str, Any], width: float = 200):
        self.nutrition_data = nutrition_data
        self.width = width
        self.height = 300  # Fixed height for consistency

    def draw(self):
        # Black border
        self.canv.setStrokeColor(HexColor("#000000"))
        self.canv.setLineWidth(2)
        self.canv.rect(0, 0, self.width, self.height, fill=0, stroke=1)

        y_pos = self.height - 20

        # Title
        self.canv.setFont("Helvetica-Bold", 14)
        self.canv.setFillColor(HexColor("#000000"))
        self.canv.drawString(10, y_pos, "Valeurs Nutritionnelles")
        y_pos -= 25

        # Serving size
        self.canv.setFont("Helvetica", 10)
        serving = self.nutrition_data.get("serving_size", "1 portion")
        self.canv.drawString(10, y_pos, f"Portion: {serving}")
        y_pos -= 20

        # Thick line
        self.canv.setLineWidth(3)
        self.canv.line(5, y_pos, self.width-5, y_pos)
        y_pos -= 15

        # Calories
        calories = self.nutrition_data.get("calories", 0)
        self.canv.setFont("Helvetica-Bold", 16)
        self.canv.drawString(10, y_pos, f"Calories: {calories}")
        y_pos -= 25

        # Macronutrients
        nutrients = [
            ("Protéines", self.nutrition_data.get("protein", 0), "g"),
            ("Glucides", self.nutrition_data.get("carbs", 0), "g"),
            ("Lipides", self.nutrition_data.get("fat", 0), "g"),
            ("Fibres", self.nutrition_data.get("fiber", 0), "g"),
            ("Sucres", self.nutrition_data.get("sugar", 0), "g"),
            ("Sodium", self.nutrition_data.get("sodium", 0), "mg")
        ]

        for name, value, unit in nutrients:
            self.canv.setFont("Helvetica", 10)
            self.canv.drawString(10, y_pos, f"{name}: {value}{unit}")
            y_pos -= 15


class MotivationalBadgeComponent(Flowable):
    """Gamification badges for motivation templates"""

    def __init__(self, badge_type: str, value: str = "", width: float = 80, height: float = 80):
        self.badge_type = badge_type
        self.value = value
        self.width = width
        self.height = height

        # Badge configurations
        self.badges = {
            "achievement": {"color": "#FFD700", "symbol": "★", "label": "Achievement"},
            "streak": {"color": "#FF6B35", "symbol": "🔥", "label": "Streak"},
            "personal_best": {"color": "#6B5B95", "symbol": "🏆", "label": "Personal Best"},
            "consistency": {"color": "#88D8B0", "symbol": "✓", "label": "Consistent"}
        }

    def draw(self):
        badge_config = self.badges.get(self.badge_type, self.badges["achievement"])

        # Badge circle
        center_x, center_y = self.width/2, self.height/2
        radius = min(self.width, self.height)/2 - 5

        self.canv.setFillColor(HexColor(badge_config["color"]))
        self.canv.setStrokeColor(HexColor("#FFFFFF"))
        self.canv.setLineWidth(3)
        self.canv.circle(center_x, center_y, radius, fill=1, stroke=1)

        # Symbol
        self.canv.setFillColor(HexColor("#FFFFFF"))
        self.canv.setFont("Helvetica-Bold", 24)
        symbol = badge_config["symbol"]
        self.canv.drawCentredText(center_x, center_y - 8, symbol)

        # Value
        if self.value:
            self.canv.setFont("Helvetica-Bold", 10)
            self.canv.drawCentredText(center_x, center_y - 25, self.value)


class AnatomyZoneComponent(Flowable):
    """Muscle group highlighting for elite workout templates"""

    def __init__(self, target_muscles: List[str], width: float = 150, height: float = 200):
        self.target_muscles = target_muscles
        self.width = width
        self.height = height

    def draw(self):
        # Simple body outline (simplified for demo)
        # In production, this would use detailed SVG or vector graphics

        # Body outline
        self.canv.setStrokeColor(HexColor("#000000"))
        self.canv.setLineWidth(1)

        # Head
        head_x, head_y = self.width/2, self.height - 30
        self.canv.circle(head_x, head_y, 15, fill=0, stroke=1)

        # Torso
        torso_width, torso_height = 60, 80
        torso_x = (self.width - torso_width) / 2
        torso_y = head_y - 95
        self.canv.rect(torso_x, torso_y, torso_width, torso_height, fill=0, stroke=1)

        # Highlight target muscles
        for muscle in self.target_muscles:
            self._highlight_muscle_group(muscle)

    def _highlight_muscle_group(self, muscle: str):
        """Highlight specific muscle groups"""
        highlights = {
            "chest": (self.width/2, self.height - 80, 25),
            "shoulders": (self.width/2, self.height - 60, 20),
            "arms": (self.width/2 + 35, self.height - 90, 15),
            "legs": (self.width/2, self.height - 160, 30)
        }

        if muscle.lower() in highlights:
            x, y, radius = highlights[muscle.lower()]
            self.canv.setFillColor(HexColor("#FF6B6B"))
            self.canv.setStrokeColor(HexColor("#FF6B6B"))
            self.canv.circle(x, y, radius, fill=1, stroke=1)


class DataVisualizationComponent(Flowable):
    """Advanced data visualization for science-based templates"""

    def __init__(self, data: Dict[str, Any], chart_type: str = "bar",
                 width: float = 300, height: float = 200):
        self.data = data
        self.chart_type = chart_type
        self.width = width
        self.height = height

    def draw(self):
        if self.chart_type == "bar":
            self._draw_bar_chart()
        elif self.chart_type == "line":
            self._draw_line_chart()
        elif self.chart_type == "pie":
            self._draw_pie_chart()

    def _draw_bar_chart(self):
        """Draw professional bar chart"""
        values = self.data.get("values", [])
        labels = self.data.get("labels", [])

        if not values:
            return

        max_value = max(values)
        bar_width = self.width / len(values) * 0.8
        spacing = self.width / len(values) * 0.2

        for i, (value, label) in enumerate(zip(values, labels)):
            x = i * (bar_width + spacing) + spacing/2
            bar_height = (value / max_value) * (self.height - 40)

            # Bar
            self.canv.setFillColor(HexColor("#4CAF50"))
            self.canv.rect(x, 20, bar_width, bar_height, fill=1, stroke=0)

            # Value label
            self.canv.setFillColor(HexColor("#000000"))
            self.canv.setFont("Helvetica", 8)
            self.canv.drawCentredText(x + bar_width/2, bar_height + 25, str(value))

            # Axis label
            self.canv.drawCentredText(x + bar_width/2, 10, label[:8])

    def _draw_line_chart(self):
        """Draw professional line chart for progress tracking"""
        points = self.data.get("points", [])
        if len(points) < 2:
            return

        # Normalize data
        min_val = min(p[1] for p in points)
        max_val = max(p[1] for p in points)
        range_val = max_val - min_val if max_val != min_val else 1

        # Draw axes
        self.canv.setStrokeColor(HexColor("#000000"))
        self.canv.setLineWidth(1)
        self.canv.line(30, 20, 30, self.height - 20)  # Y axis
        self.canv.line(30, 20, self.width - 20, 20)   # X axis

        # Plot line
        self.canv.setStrokeColor(HexColor("#2196F3"))
        self.canv.setLineWidth(2)

        prev_x, prev_y = None, None
        for i, (x_val, y_val) in enumerate(points):
            x = 30 + (i / (len(points) - 1)) * (self.width - 50)
            y = 20 + ((y_val - min_val) / range_val) * (self.height - 40)

            if prev_x is not None:
                self.canv.line(prev_x, prev_y, x, y)

            # Data point
            self.canv.setFillColor(HexColor("#2196F3"))
            self.canv.circle(x, y, 3, fill=1, stroke=0)

            prev_x, prev_y = x, y

    def _draw_pie_chart(self):
        """Draw professional pie chart"""
        # Implementation would use ReportLab's pie chart functionality
        # Simplified version for demo
        pass


class QRCodeComponent(Flowable):
    """QR Code component for video links and digital integration"""

    def __init__(self, data: str, width: float = 60, height: float = 60):
        self.data = data
        self.width = width
        self.height = height

    def draw(self):
        # Placeholder QR code (in production, use qrcode library)
        self.canv.setStrokeColor(HexColor("#000000"))
        self.canv.setFillColor(HexColor("#000000"))

        # Draw a grid pattern as QR code placeholder
        cell_size = self.width / 10
        for i in range(10):
            for j in range(10):
                if (i + j) % 2 == 0:
                    x = i * cell_size
                    y = j * cell_size
                    self.canv.rect(x, y, cell_size, cell_size, fill=1, stroke=0)


class PremiumHeaderComponent(Flowable):
    """Luxury header with branding and premium styling"""

    def __init__(self, title: str, subtitle: str = "", logo_path: str = "",
                 width: float = 400, height: float = 80):
        self.title = title
        self.subtitle = subtitle
        self.logo_path = logo_path
        self.width = width
        self.height = height

    def draw(self):
        # Premium gradient background
        self.canv.setFillColor(HexColor("#1a365d"))
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)

        # Title
        self.canv.setFillColor(HexColor("#FFFFFF"))
        self.canv.setFont("Helvetica-Bold", 20)
        self.canv.drawString(20, self.height - 30, self.title)

        # Subtitle
        if self.subtitle:
            self.canv.setFont("Helvetica", 12)
            self.canv.setFillColor(HexColor("#CBD5E0"))
            self.canv.drawString(20, self.height - 50, self.subtitle)

        # Logo placeholder (in production, load actual logo)
        if self.logo_path:
            logo_size = 40
            logo_x = self.width - logo_size - 20
            logo_y = (self.height - logo_size) / 2

            self.canv.setStrokeColor(HexColor("#FFFFFF"))
            self.canv.rect(logo_x, logo_y, logo_size, logo_size, fill=0, stroke=1)
            self.canv.drawCentredText(logo_x + logo_size/2, logo_y + logo_size/2, "LOGO")