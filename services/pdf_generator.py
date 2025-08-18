from io import BytesIO

from matplotlib.figure import Figure
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from models.client import Client
from ui.theme.colors import (
    NEUTRAL_100,
    NEUTRAL_300,
    NEUTRAL_700,
    NEUTRAL_800,
    NEUTRAL_900,
    PRIMARY,
)

# Mapping des anciennes couleurs vers le nouveau Design System
DARK_BG = NEUTRAL_900
DARK_PANEL = NEUTRAL_800
TEXT = NEUTRAL_100
TEXT_MUTED = NEUTRAL_300
# On choisit une couleur neutre pour remplacer l'ancienne 'SECONDARY'
SECONDARY = NEUTRAL_700


def generate_nutrition_sheet_pdf(
    fiche_data: dict, client_data: Client, file_path: str
) -> None:
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setTitle("Fiche Nutrition")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(
        30, height - 40, f"Fiche Nutrition - {client_data.prenom} {client_data.nom}"
    )

    c.setFont("Helvetica", 12)
    y = height - 80
    c.drawString(30, y, f"Poids mesuré : {fiche_data['poids_kg_mesure']} kg")
    y -= 20
    c.drawString(30, y, f"Objectif : {fiche_data['objectif']}")
    y -= 20
    c.drawString(30, y, f"Maintenance : {fiche_data['maintenance_kcal']} kcal")
    y -= 20
    c.drawString(30, y, f"Objectif calorique : {fiche_data['objectif_kcal']} kcal")
    y -= 30
    c.drawString(30, y, f"Protéines : {fiche_data['proteines_g']} g")
    y -= 20
    c.drawString(30, y, f"Glucides : {fiche_data['glucides_g']} g")
    y -= 20
    c.drawString(30, y, f"Lipides : {fiche_data['lipides_g']} g")

    # Pie chart
    fig = Figure(figsize=(2.5, 2.5), dpi=100)
    fig.patch.set_facecolor(DARK_PANEL)
    ax = fig.add_subplot(111)
    ax.set_facecolor(DARK_BG)
    protein_cal = fiche_data["proteines_g"] * 4
    carbs_cal = fiche_data["glucides_g"] * 4
    fats_cal = fiche_data["lipides_g"] * 9
    ax.pie(
        [protein_cal, carbs_cal, fats_cal],
        colors=[PRIMARY, SECONDARY, TEXT_MUTED],
        labels=["P", "G", "L"],
        textprops={"color": TEXT},
    )
    buf = BytesIO()
    fig.savefig(buf, format="PNG", facecolor=DARK_PANEL)
    buf.seek(0)
    c.drawImage(ImageReader(buf), width - 180, height - 220, 150, 150)

    c.showPage()
    c.save()
