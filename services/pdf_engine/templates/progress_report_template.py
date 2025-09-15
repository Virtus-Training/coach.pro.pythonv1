"""
Progress Report Template - Professional progress tracking PDF generation
Client progress visualization with charts, photos, and measurements
"""

from __future__ import annotations

import io
from typing import Any, Dict, List

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Image, PageBreak, Paragraph, Spacer, Table, TableStyle

from .base_template import BaseTemplate


class ProgressReportTemplate(BaseTemplate):
    """
    Professional progress report template with data visualization
    Supports progress charts, before/after photos, and detailed measurements
    """

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "header": {
                "enabled": True,
                "show_logo": True,
                "show_metadata": True,
            },
            "footer": {
                "enabled": True,
                "show_branding": True,
                "show_page_numbers": True,
                "text": "Rapport de progression généré avec CoachPro",
            },
            "colors": {
                "primary": "#DC3545",
                "secondary": "#6F42C1",
                "accent": "#20C997",
                "background": "#FFFFFF",
                "surface": "#F8F9FA",
                "text_primary": "#212529",
                "text_secondary": "#6C757D",
                "border": "#DEE2E6",
                "improvement": "#28A745",
                "regression": "#DC3545",
                "stable": "#FFC107",
                "chart_grid": "#E9ECEF",
            },
            "fonts": {
                "title": {"name": "Helvetica-Bold", "size": 22},
                "heading": {"name": "Helvetica-Bold", "size": 16},
                "subheading": {"name": "Helvetica-Bold", "size": 13},
                "body": {"name": "Helvetica", "size": 10},
                "caption": {"name": "Helvetica", "size": 8},
            },
            "show_charts": True,
            "show_photos": True,
            "show_measurements": True,
            "chart_style": "modern",  # modern, classic, minimal
        }

    @classmethod
    def get_data_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "client_name": {"type": "string"},
                "report_period": {"type": "string"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "summary": {
                    "type": "object",
                    "properties": {
                        "total_sessions": {"type": "number"},
                        "weight_change": {"type": "number"},
                        "body_fat_change": {"type": "number"},
                        "muscle_gain": {"type": "number"},
                        "achievements": {"type": "array"},
                    },
                },
                "measurements": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "date": {"type": "string"},
                            "weight": {"type": "number"},
                            "body_fat": {"type": "number"},
                            "muscle_mass": {"type": "number"},
                            "measurements": {
                                "type": "object",
                                "properties": {
                                    "chest": {"type": "number"},
                                    "waist": {"type": "number"},
                                    "hips": {"type": "number"},
                                    "arms": {"type": "number"},
                                    "thighs": {"type": "number"},
                                },
                            },
                        },
                    },
                },
                "performance_data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "exercise": {"type": "string"},
                            "data_points": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "date": {"type": "string"},
                                        "weight": {"type": "number"},
                                        "reps": {"type": "number"},
                                        "volume": {"type": "number"},
                                    },
                                },
                            },
                        },
                    },
                },
                "photos": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "date": {"type": "string"},
                            "type": {"type": "string"},
                            "front_photo": {"type": "string"},
                            "side_photo": {"type": "string"},
                            "back_photo": {"type": "string"},
                        },
                    },
                },
                "goals": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "target_date": {"type": "string"},
                            "status": {"type": "string"},
                            "progress_percentage": {"type": "number"},
                        },
                    },
                },
            },
            "required": ["title", "client_name", "summary"],
        }

    def _build_content(self) -> List[Any]:
        """Build progress report content"""
        elements = []

        # Executive summary
        elements.extend(self._build_executive_summary())
        elements.append(Spacer(1, 0.5 * cm))

        # Key metrics overview
        elements.extend(self._build_key_metrics())
        elements.append(Spacer(1, 0.5 * cm))

        # Progress charts
        if self.merged_config.get("show_charts", True) and not self.preview_mode:
            elements.extend(self._build_progress_charts())
            elements.append(Spacer(1, 0.5 * cm))

        # Measurements tracking
        if self.merged_config.get("show_measurements", True):
            elements.extend(self._build_measurements_section())
            elements.append(Spacer(1, 0.5 * cm))

        # Before/After photos
        if self.merged_config.get("show_photos", True) and not self.preview_mode:
            elements.extend(self._build_photos_section())
            elements.append(PageBreak())

        # Performance analysis
        if not self.preview_mode:
            elements.extend(self._build_performance_analysis())
            elements.append(Spacer(1, 0.5 * cm))

        # Goals tracking
        elements.extend(self._build_goals_section())

        return elements

    def _build_executive_summary(self) -> List[Any]:
        """Build executive summary section"""
        elements = []
        summary = self.data.get("summary", {})

        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>📊 Résumé exécutif</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Summary metrics
        summary_data = []

        period = self.data.get("report_period", "")
        if period:
            summary_data.append(f"📅 Période: {period}")

        total_sessions = summary.get("total_sessions")
        if total_sessions:
            summary_data.append(f"🎯 Séances: {total_sessions}")

        weight_change = summary.get("weight_change")
        if weight_change is not None:
            sign = "+" if weight_change > 0 else ""
            summary_data.append(f"⚖️ Poids: {sign}{weight_change:.1f} kg")

        body_fat_change = summary.get("body_fat_change")
        if body_fat_change is not None:
            sign = "+" if body_fat_change > 0 else ""
            summary_data.append(f"📉 Masse grasse: {sign}{body_fat_change:.1f}%")

        if summary_data:
            summary_text = " • ".join(summary_data)
            summary_paragraph = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}">{summary_text}</font>',
                self.styles["body"],
            )

            # Create highlight box
            summary_table_data = [[summary_paragraph]]
            summary_table = Table(summary_table_data, colWidths=[18 * cm])
            summary_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor(self.merged_config["colors"]["surface"]),
                        ),
                        (
                            "BORDER",
                            (0, 0),
                            (-1, -1),
                            2,
                            colors.HexColor(self.merged_config["colors"]["primary"]),
                        ),
                        ("PADDING", (0, 0), (-1, -1), 15),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]
                )
            )

            elements.append(summary_table)

        # Achievements
        achievements = summary.get("achievements", [])
        if achievements:
            elements.append(Spacer(1, 0.3 * cm))
            achievements_header = Paragraph(
                f'<font name="{self.merged_config["fonts"]["subheading"]["name"]}" '
                f'size="{self.merged_config["fonts"]["subheading"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}"><b>🏆 Accomplissements</b></font>',
                self.styles["heading"],
            )
            elements.append(achievements_header)

            achievements_text = []
            for achievement in achievements:
                achievements_text.append(f"✅ {achievement}")

            achievements_content = "<br/>".join(achievements_text)
            achievements_paragraph = Paragraph(
                f'<font name="{self.merged_config["fonts"]["body"]["name"]}" '
                f'size="{self.merged_config["fonts"]["body"]["size"]}" '
                f'color="{self.merged_config["colors"]["text_primary"]}">{achievements_content}</font>',
                self.styles["body"],
            )
            elements.append(achievements_paragraph)

        return elements

    def _build_key_metrics(self) -> List[Any]:
        """Build key metrics dashboard"""
        elements = []
        measurements = self.data.get("measurements", [])

        if len(measurements) < 2:
            return elements

        # Get first and last measurements
        first_measurement = measurements[0]
        last_measurement = measurements[-1]

        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>📈 Évolution des métriques clés</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Create metrics comparison table
        metrics_data = [["Métrique", "Début", "Actuel", "Évolution", "Statut"]]

        # Weight comparison
        weight_start = first_measurement.get("weight")
        weight_current = last_measurement.get("weight")
        if weight_start and weight_current:
            weight_change = weight_current - weight_start
            weight_status = self._get_change_status(weight_change, "weight")
            weight_icon = self._get_status_icon(weight_status)

            metrics_data.append(
                [
                    "Poids (kg)",
                    f"{weight_start:.1f}",
                    f"{weight_current:.1f}",
                    f"{weight_change:+.1f}",
                    weight_icon,
                ]
            )

        # Body fat comparison
        bf_start = first_measurement.get("body_fat")
        bf_current = last_measurement.get("body_fat")
        if bf_start and bf_current:
            bf_change = bf_current - bf_start
            bf_status = self._get_change_status(bf_change, "body_fat")
            bf_icon = self._get_status_icon(bf_status)

            metrics_data.append(
                [
                    "Masse grasse (%)",
                    f"{bf_start:.1f}",
                    f"{bf_current:.1f}",
                    f"{bf_change:+.1f}",
                    bf_icon,
                ]
            )

        # Muscle mass comparison
        muscle_start = first_measurement.get("muscle_mass")
        muscle_current = last_measurement.get("muscle_mass")
        if muscle_start and muscle_current:
            muscle_change = muscle_current - muscle_start
            muscle_status = self._get_change_status(muscle_change, "muscle")
            muscle_icon = self._get_status_icon(muscle_status)

            metrics_data.append(
                [
                    "Masse musculaire (kg)",
                    f"{muscle_start:.1f}",
                    f"{muscle_current:.1f}",
                    f"{muscle_change:+.1f}",
                    muscle_icon,
                ]
            )

        if len(metrics_data) > 1:
            metrics_table = Table(
                metrics_data, colWidths=[4 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 2 * cm]
            )
            metrics_table.setStyle(self._get_metrics_table_style())
            elements.append(metrics_table)

        return elements

    def _build_progress_charts(self) -> List[Any]:
        """Build progress visualization charts"""
        elements = []
        measurements = self.data.get("measurements", [])

        if len(measurements) < 2:
            return elements

        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>📊 Graphiques de progression</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Weight progression chart
        weight_chart = self._create_weight_chart(measurements)
        if weight_chart:
            elements.append(weight_chart)
            elements.append(Spacer(1, 0.3 * cm))

        # Body composition chart
        composition_chart = self._create_composition_chart(measurements)
        if composition_chart:
            elements.append(composition_chart)

        return elements

    def _build_measurements_section(self) -> List[Any]:
        """Build body measurements tracking section"""
        elements = []
        measurements = self.data.get("measurements", [])

        if not measurements:
            return elements

        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>📏 Suivi des mensurations</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Create measurements table
        measurements_data = [
            ["Date", "Poitrine", "Taille", "Hanches", "Bras", "Cuisses"]
        ]

        for measurement in measurements:
            date = measurement.get("date", "")
            body_measurements = measurement.get("measurements", {})

            row = [
                date,
                f"{body_measurements.get('chest', '')}"
                + (" cm" if body_measurements.get("chest") else ""),
                f"{body_measurements.get('waist', '')}"
                + (" cm" if body_measurements.get("waist") else ""),
                f"{body_measurements.get('hips', '')}"
                + (" cm" if body_measurements.get("hips") else ""),
                f"{body_measurements.get('arms', '')}"
                + (" cm" if body_measurements.get("arms") else ""),
                f"{body_measurements.get('thighs', '')}"
                + (" cm" if body_measurements.get("thighs") else ""),
            ]
            measurements_data.append(row)

        measurements_table = Table(
            measurements_data,
            colWidths=[3 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm],
        )
        measurements_table.setStyle(self._get_standard_table_style())
        elements.append(measurements_table)

        return elements

    def _build_photos_section(self) -> List[Any]:
        """Build before/after photos section"""
        elements = []
        photos = self.data.get("photos", [])

        if not photos:
            return elements

        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>📸 Photos de progression</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.4 * cm))

        # Display before and after photos
        if len(photos) >= 2:
            before_photos = photos[0]
            after_photos = photos[-1]

            elements.extend(self._build_photo_comparison(before_photos, after_photos))

        return elements

    def _build_photo_comparison(
        self, before: Dict[str, Any], after: Dict[str, Any]
    ) -> List[Any]:
        """Build before/after photo comparison"""
        elements = []

        before_date = before.get("date", "Avant")
        after_date = after.get("date", "Après")

        # Comparison header
        comparison_data = [[f"📅 {before_date}", f"📅 {after_date}"]]

        # Front view comparison
        before_front = before.get("front_photo")
        after_front = after.get("front_photo")

        if before_front and after_front:
            try:
                from pathlib import Path

                before_img = None
                after_img = None

                if Path(before_front).exists():
                    before_img = Image(before_front, width=6 * cm, height=8 * cm)

                if Path(after_front).exists():
                    after_img = Image(after_front, width=6 * cm, height=8 * cm)

                if before_img and after_img:
                    comparison_data.append([before_img, after_img])

            except Exception:
                # If image loading fails, show placeholder
                comparison_data.append(["Photo non disponible", "Photo non disponible"])

        comparison_table = Table(comparison_data, colWidths=[9 * cm, 9 * cm])
        comparison_table.setStyle(
            TableStyle(
                [
                    # Header
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor(self.merged_config["colors"]["primary"]),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        self.merged_config["fonts"]["subheading"]["name"],
                    ),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    # Photos
                    ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    (
                        "BORDER",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.HexColor(self.merged_config["colors"]["border"]),
                    ),
                    ("PADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        elements.append(comparison_table)
        return elements

    def _build_performance_analysis(self) -> List[Any]:
        """Build performance analysis section"""
        elements = []
        performance_data = self.data.get("performance_data", [])

        if not performance_data:
            return elements

        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>💪 Analyse des performances</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Performance summary table
        performance_summary = [
            ["Exercice", "Performance initiale", "Performance actuelle", "Progression"]
        ]

        for exercise_data in performance_data:
            exercise_name = exercise_data.get("exercise", "")
            data_points = exercise_data.get("data_points", [])

            if len(data_points) < 2:
                continue

            first_point = data_points[0]
            last_point = data_points[-1]

            # Calculate progression
            first_volume = first_point.get("volume", 0)
            last_volume = last_point.get("volume", 0)

            if first_volume > 0:
                progression = ((last_volume - first_volume) / first_volume) * 100
                progression_text = f"{progression:+.1f}%"
            else:
                progression_text = "N/A"

            performance_summary.append(
                [
                    exercise_name,
                    f"{first_point.get('weight', 0)}kg × {first_point.get('reps', 0)}",
                    f"{last_point.get('weight', 0)}kg × {last_point.get('reps', 0)}",
                    progression_text,
                ]
            )

        if len(performance_summary) > 1:
            performance_table = Table(
                performance_summary, colWidths=[5 * cm, 4 * cm, 4 * cm, 4 * cm, 1 * cm]
            )
            performance_table.setStyle(self._get_standard_table_style())
            elements.append(performance_table)

        return elements

    def _build_goals_section(self) -> List[Any]:
        """Build goals tracking section"""
        elements = []
        goals = self.data.get("goals", [])

        if not goals:
            return elements

        header = Paragraph(
            f'<font name="{self.merged_config["fonts"]["heading"]["name"]}" '
            f'size="{self.merged_config["fonts"]["heading"]["size"]}" '
            f'color="{self.merged_config["colors"]["primary"]}"><b>🎯 Suivi des objectifs</b></font>',
            self.styles["heading"],
        )
        elements.append(header)
        elements.append(Spacer(1, 0.3 * cm))

        # Goals table
        goals_data = [["Objectif", "Date cible", "Progression", "Statut"]]

        for goal in goals:
            description = goal.get("description", "")
            target_date = goal.get("target_date", "")
            progress = goal.get("progress_percentage", 0)
            status = goal.get("status", "En cours")

            # Progress bar representation
            progress_bar = self._create_text_progress_bar(progress)

            goals_data.append([description, target_date, progress_bar, status])

        goals_table = Table(goals_data, colWidths=[6 * cm, 3 * cm, 5 * cm, 4 * cm])
        goals_table.setStyle(self._get_standard_table_style())
        elements.append(goals_table)

        return elements

    def _create_weight_chart(self, measurements: List[Dict[str, Any]]) -> Any:
        """Create weight progression line chart"""
        try:
            from datetime import datetime

            import matplotlib
            import matplotlib.dates as mdates
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_agg import FigureCanvasAgg

            matplotlib.use("Agg")

            # Extract weight data
            dates = []
            weights = []

            for measurement in measurements:
                date_str = measurement.get("date", "")
                weight = measurement.get("weight")

                if date_str and weight:
                    try:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        dates.append(date_obj)
                        weights.append(weight)
                    except:
                        continue

            if len(dates) < 2:
                return None

            # Create chart
            fig, ax = plt.subplots(figsize=(8, 4), dpi=150)
            fig.patch.set_facecolor("white")

            ax.plot(
                dates,
                weights,
                color=self.merged_config["colors"]["primary"],
                linewidth=2,
                marker="o",
                markersize=6,
            )

            ax.set_title("Évolution du poids", fontsize=14, fontweight="bold", pad=20)
            ax.set_xlabel("Date", fontsize=10)
            ax.set_ylabel("Poids (kg)", fontsize=10)

            # Format dates on x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

            # Grid styling
            ax.grid(
                True,
                color=self.merged_config["colors"]["chart_grid"],
                linestyle="--",
                alpha=0.7,
            )
            ax.set_axisbelow(True)

            # Styling
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            plt.tight_layout()

            # Save to buffer
            canvas = FigureCanvasAgg(fig)
            buffer = io.BytesIO()
            canvas.print_png(buffer)
            buffer.seek(0)

            plt.close(fig)

            return Image(buffer, width=12 * cm, height=6 * cm)

        except ImportError:
            # Matplotlib not available - create simple text representation
            if len(dates) >= 2:
                weight_change = weights[-1] - weights[0]
                sign = "+" if weight_change > 0 else ""

                chart_text = f"""
                📊 Évolution du poids:
                Début: {weights[0]:.1f} kg
                Actuel: {weights[-1]:.1f} kg
                Variation: {sign}{weight_change:.1f} kg
                """

                chart_paragraph = Paragraph(
                    f'<font name="Helvetica" size="10">{chart_text}</font>',
                    self.styles["body"],
                )
                return chart_paragraph
            return None
        except Exception:
            return None

    def _create_composition_chart(self, measurements: List[Dict[str, Any]]) -> Any:
        """Create body composition chart"""
        try:
            import matplotlib
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_agg import FigureCanvasAgg

            matplotlib.use("Agg")

            # Get latest measurement for pie chart
            latest = measurements[-1]
            body_fat = latest.get("body_fat", 0)
            muscle_mass = latest.get("muscle_mass", 0)
            weight = latest.get("weight", 0)

            if not all([body_fat, muscle_mass, weight]):
                return None

            # Calculate components
            fat_mass = (body_fat / 100) * weight
            other_mass = weight - muscle_mass - fat_mass

            if other_mass < 0:
                other_mass = 0

            # Create pie chart
            fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
            fig.patch.set_facecolor("white")

            sizes = [muscle_mass, fat_mass, other_mass]
            labels = ["Muscle", "Graisse", "Autres"]
            colors_chart = [
                self.merged_config["colors"]["improvement"],
                self.merged_config["colors"]["regression"],
                self.merged_config["colors"]["stable"],
            ]

            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                colors=colors_chart,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"linewidth": 2, "edgecolor": "white"},
            )

            for text in texts:
                text.set_fontsize(10)
                text.set_fontweight("bold")

            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontsize(9)
                autotext.set_fontweight("bold")

            ax.set_title(
                "Composition corporelle actuelle",
                fontsize=12,
                fontweight="bold",
                pad=20,
            )

            # Save to buffer
            canvas = FigureCanvasAgg(fig)
            buffer = io.BytesIO()
            canvas.print_png(buffer)
            buffer.seek(0)

            plt.close(fig)

            return Image(buffer, width=6 * cm, height=6 * cm)

        except ImportError:
            # Matplotlib not available - create simple text representation
            chart_text = f"""
            📊 Composition corporelle:
            💪 Muscle: {muscle_mass:.1f} kg
            📉 Graisse: {fat_mass:.1f} kg
            ⚖️ Total: {weight:.1f} kg
            """

            chart_paragraph = Paragraph(
                f'<font name="Helvetica" size="10">{chart_text}</font>',
                self.styles["body"],
            )
            return chart_paragraph
        except Exception:
            return None

    def _create_text_progress_bar(self, progress: float) -> str:
        """Create text-based progress bar"""
        bar_length = 10
        filled_length = int(bar_length * (progress / 100))

        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"{bar} {progress:.0f}%"

    def _get_change_status(self, change: float, metric_type: str) -> str:
        """Get status based on change value and metric type"""
        if abs(change) < 0.1:
            return "stable"

        if metric_type in ["weight", "body_fat"]:
            # For weight/body fat, negative change might be good
            return "improvement" if change < 0 else "regression"
        elif metric_type == "muscle":
            # For muscle, positive change is good
            return "improvement" if change > 0 else "regression"
        else:
            return "stable"

    def _get_status_icon(self, status: str) -> str:
        """Get icon for status"""
        icons = {"improvement": "📈", "regression": "📉", "stable": "➡️"}
        return icons.get(status, "➡️")

    def _get_metrics_table_style(self) -> TableStyle:
        """Get styling for metrics table"""
        return TableStyle(
            [
                # Header
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(self.merged_config["colors"]["primary"]),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    self.merged_config["fonts"]["subheading"]["name"],
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    self.merged_config["fonts"]["subheading"]["size"],
                ),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                # Body
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    self.merged_config["fonts"]["body"]["name"],
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    self.merged_config["fonts"]["body"]["size"],
                ),
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor(self.merged_config["colors"]["text_primary"]),
                ),
                ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                # Grid and padding
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.HexColor(self.merged_config["colors"]["border"]),
                ),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )

    def _get_standard_table_style(self) -> TableStyle:
        """Get standard table styling"""
        return TableStyle(
            [
                # Header
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(self.merged_config["colors"]["primary"]),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    self.merged_config["fonts"]["subheading"]["name"],
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    self.merged_config["fonts"]["subheading"]["size"],
                ),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                # Body
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    self.merged_config["fonts"]["body"]["name"],
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    self.merged_config["fonts"]["body"]["size"],
                ),
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor(self.merged_config["colors"]["text_primary"]),
                ),
                # Alternating backgrounds
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor(self.merged_config["colors"]["surface"]),
                    ],
                ),
                # Grid and padding
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.HexColor(self.merged_config["colors"]["border"]),
                ),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
