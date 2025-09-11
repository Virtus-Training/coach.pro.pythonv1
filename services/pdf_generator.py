from io import BytesIO
from pathlib import Path
from typing import Optional

from matplotlib.figure import Figure
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from dtos.nutrition_dtos import NutritionPageDTO
from models.client import Client
from pdf_templates.nutrition_template import NutritionPDFTemplate
from pdf_templates.session_template import SessionPDFTemplate

# Palette (ui/theme/theme.json)
PRIMARY = "#22D3EE"
DARK_PANEL = "#1F2937"
TEXT_MUTED = "#9CA3AF"
ICON_DIR = Path(__file__).resolve().parent.parent / "assets" / "icons"


def _compute_age(date_naissance: Optional[str]) -> int:
    """Compute age from 'YYYY-MM-DD' or 'DD/MM/YYYY'."""
    if not date_naissance:
        return 0
    try:
        import datetime as _dt

        try:
            birth = _dt.date.fromisoformat(date_naissance)
        except Exception:
            birth = _dt.datetime.strptime(date_naissance, "%d/%m/%Y").date()
        today = _dt.date.today()
        return today.year - birth.year - (
            (today.month, today.day) < (birth.month, birth.day)
        )
    except Exception:
        return 0


def _draw_label_value(c: canvas.Canvas, x: float, y: float, label: str, value: str) -> None:
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    c.drawString(x, y, label)
    c.drawRightString(x + 9.5 * cm, y, value)


def _try_image(path: Path) -> Optional[ImageReader]:
    try:
        if path.exists():
            return ImageReader(str(path))
    except Exception:
        pass
    return None


def generate_nutrition_sheet_pdf(
    fiche_data: dict, client_data: Client, file_path: str
) -> None:
    """Generate a styled, single-page nutrition sheet PDF."""

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    margin = 1.2 * cm

    c.setTitle("Fiche Nutrition")

    # Header bar
    c.setFillColor(colors.HexColor(DARK_PANEL))
    c.rect(0, height - 3 * cm, width, 3 * cm, stroke=0, fill=1)
    c.setFillColor(colors.HexColor(PRIMARY))
    c.rect(0, height - 3 * cm, width, 0.25 * cm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    full_name = f"{client_data.prenom} {client_data.nom}".strip()
    c.drawString(margin, height - 1.6 * cm, f"Fiche Nutrition – {full_name}")
    logo = _try_image(Path(__file__).resolve().parent.parent / "assets" / "Logo.png")
    if logo:
        c.drawImage(logo, width - margin - 2.8 * cm, height - 2.8 * cm, 2.4 * cm, 2.4 * cm, mask='auto')

    # Origin for body
    x = margin
    y = height - 4.2 * cm

    # Personal info
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Informations personnelles")
    y -= 0.7 * cm
    age = _compute_age(getattr(client_data, "date_naissance", None))
    poids = fiche_data.get("poids_kg_mesure") or getattr(client_data, "poids_kg", None) or ""
    taille = getattr(client_data, "taille_cm", None) or fiche_data.get("taille_cm", "")
    sexe = getattr(client_data, "sexe", "") or fiche_data.get("sexe", "")
    activite = getattr(client_data, "niveau_activite", "") or fiche_data.get("niveau_activite", "")
    objectif = fiche_data.get("objectif", getattr(client_data, "objectifs", ""))
    _draw_label_value(c, x, y, "Âge", f"{age} ans" if age else "—")
    y -= 0.55 * cm
    _draw_label_value(c, x, y, "Poids", f"{poids} kg" if poids != "" else "—")
    y -= 0.55 * cm
    _draw_label_value(c, x, y, "Taille", f"{taille} cm" if taille != "" else "—")
    y -= 0.55 * cm
    _draw_label_value(c, x, y, "Sexe", sexe or "—")
    y -= 0.55 * cm
    _draw_label_value(c, x, y, "Activité", activite or "—")
    y -= 0.55 * cm
    _draw_label_value(c, x, y, "Objectif", objectif or "—")

    # Nutrition targets
    y -= 0.8 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Données nutritionnelles")
    y -= 0.7 * cm
    c.setFont("Helvetica", 12)
    maintenance = int(fiche_data.get("maintenance_kcal", 0))
    objectif_kcal = int(fiche_data.get("objectif_kcal", 0))
    c.drawString(x, y, f"Maintenance : {maintenance} kcal")
    y -= 0.55 * cm
    c.drawString(x, y, f"Objectif calorique : {objectif_kcal} kcal")
    y -= 0.8 * cm

    # Macros
    prot_g = int(fiche_data.get("proteines_g", 0))
    gluc_g = int(fiche_data.get("glucides_g", 0))
    lip_g = int(fiche_data.get("lipides_g", 0))
    prot_cal, gluc_cal, lip_cal = prot_g * 4, gluc_g * 4, lip_g * 9

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#3C91E6")); c.rect(x, y - 0.25 * cm, 0.3 * cm, 0.3 * cm, stroke=0, fill=1)
    c.setFillColor(colors.black); c.drawString(x + 0.5 * cm, y, f"Protéines : {prot_g} g / {prot_cal} kcal")
    y -= 0.6 * cm
    c.setFillColor(colors.HexColor("#FFAD05")); c.rect(x, y - 0.25 * cm, 0.3 * cm, 0.3 * cm, stroke=0, fill=1)
    c.setFillColor(colors.black); c.drawString(x + 0.5 * cm, y, f"Glucides : {gluc_g} g / {gluc_cal} kcal")
    y -= 0.6 * cm
    c.setFillColor(colors.HexColor("#E4572E")); c.rect(x, y - 0.25 * cm, 0.3 * cm, 0.3 * cm, stroke=0, fill=1)
    c.setFillColor(colors.black); c.drawString(x + 0.5 * cm, y, f"Lipides : {lip_g} g / {lip_cal} kcal")
    y -= 0.9 * cm

    # Pie chart (right) with higher DPI and styled wedges
    try:
        fig = Figure(figsize=(3.0, 3.0), dpi=300)
        ax = fig.add_subplot(111)
        ax.set_facecolor("white")
        vals = [max(prot_cal, 0), max(gluc_cal, 0), max(lip_cal, 0)]
        labels = ["P", "G", "L"]
        colors_pie = ["#3C91E6", "#FFAD05", "#E4572E"]
        wedges, texts, autotexts = ax.pie(
            vals,
            colors=colors_pie,
            labels=labels,
            autopct=lambda p: f"{p:.0f}%" if p >= 3 else "",
            startangle=90,
            wedgeprops={"linewidth": 1, "edgecolor": "#FFFFFF"},
            textprops={"fontsize": 9, "weight": "bold"},
            pctdistance=0.72,
        )
        for t in autotexts:
            t.set_color("black"); t.set_fontsize(9); t.set_weight("bold")
        ax.axis("equal")
        buf = BytesIO(); fig.savefig(buf, format="PNG", transparent=True, bbox_inches="tight", pad_inches=0)
        buf.seek(0)
        c.drawImage(ImageReader(buf), width - margin - 6 * cm, y - 1.2 * cm, 5.5 * cm, 5.5 * cm, mask='auto')
    except Exception:
        pass

    # Estimated monthly variation
    delta = objectif_kcal - maintenance
    variation_kg = round((delta * 30) / 7700.0, 1) if maintenance and objectif_kcal else 0.0
    signe = "+" if variation_kg > 0 else ""
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, f"Estimation mensuelle : {signe}{variation_kg} kg")
    y -= 1.0 * cm

    # Recommendations block
    block_h = 6.2 * cm
    block_y = margin
    c.setFillColor(colors.HexColor("#F3F6FA"))
    c.rect(x, block_y, width - 2 * margin, block_h, stroke=0, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x + 0.5 * cm, block_y + block_h - 0.9 * cm, "Recommandations personnalisées")

    conseils = [
        f"Hydratation : env. {int((poids or 0) * 35)} mL / jour" if poids else "Hydratation : viser ~2 L / jour",
        "Sommeil : 7 à 9h / nuit",
        "Privilégier les aliments bruts, limiter l'ultra-transformé",
        "Manger lentement et à satiété, sans distraction",
        "Respecter des horaires de repas réguliers",
        "Inclure de la marche active chaque jour",
    ]
    obj = (objectif or "").lower()
    if "perte" in obj:
        conseils += [
            "Augmenter les légumes pour la satiété",
            "Favoriser les protéines maigres",
            "Déficit progressif (≤ 500 kcal/jour)",
        ]
    elif "masse" in obj:
        conseils += [
            "Augmenter progressivement les glucides",
            "Encas post-entraînement (P + G)",
            "Suivre la prise de poids (200–400 g/sem)",
        ]

    c.setFont("Helvetica", 11)
    text_y = block_y + block_h - 1.6 * cm
    for line in conseils:
        if text_y < block_y + 0.7 * cm:
            break
        c.drawString(x + 0.5 * cm, text_y, f"• {line}")
        text_y -= 0.55 * cm

    # Footer
    c.setFillColor(colors.HexColor(TEXT_MUTED))
    c.setFont("Helvetica-Oblique", 9)
    c.drawRightString(width - margin, 0.9 * cm, "Fiche Personnalisée - Virtus Training")

    c.showPage(); c.save()


def generate_session_pdf(
    session_dto: dict, client_name: str | None, file_path: str
) -> None:
    template = SessionPDFTemplate(session_dto, client_name)
    template.build(file_path)


def generate_session_pdf_with_style(
    session_dto: dict,
    client_name: str | None,
    file_path: str,
    style: dict,
) -> None:
    template = SessionPDFTemplate(session_dto, client_name, style=style)
    template.build(file_path)


def generate_nutrition_pdf(nutrition_dto: NutritionPageDTO, file_path: str) -> None:
    template = NutritionPDFTemplate(nutrition_dto)
    template.build(file_path)

