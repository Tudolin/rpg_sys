"""Geração da ficha de personagem em PDF.

Separado da camada web para que tanto a API quanto scripts possam usar.
Os campos vêm do sistema de jogo do personagem (game_systems.py), então a
ficha se adapta a Fantasia Medieval, Cthulhu, Velho Oeste ou Cyberpunk.
"""
import logging
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from game_systems import get_system

_FONT_NAME = "MedievalFont"
_FONT_PATH = "static/fonts/Enchanted Land.otf"
_font_ready = False


def _ensure_font():
    global _font_ready
    if _font_ready:
        return _FONT_NAME
    try:
        pdfmetrics.registerFont(TTFont(_FONT_NAME, _FONT_PATH))
        _font_ready = True
        return _FONT_NAME
    except Exception as e:  # fonte ausente não deve derrubar o download
        logging.warning("Fonte da ficha indisponível (%s); usando Helvetica.", e)
        return "Helvetica"


def build_character_sheet_pdf(buffer, character, class_info=None, race_info=None):
    font = _ensure_font()
    system = get_system(character.get("system_id"))

    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFillColorRGB(0.96, 0.87, 0.70)
    pdf.rect(0, 0, width, height, stroke=0, fill=1)

    pdf.setFont(font, 24)
    pdf.setFillColor(colors.darkred)
    pdf.drawCentredString(width / 2.0, height - 50, f"Ficha: {character['name']}")

    pdf.setFont(font, 13)
    pdf.setFillColor(colors.black)
    pdf.drawCentredString(width / 2.0, height - 72, f"{system['icon']} {system['name']}")

    image_path = (character.get("img_url") or "").lstrip("/")
    if image_path and os.path.exists(image_path):
        try:
            size = 140
            x, y = width - 200, height - 240
            pdf.setStrokeColor(colors.black)
            pdf.setLineWidth(2)
            pdf.rect(x - 8, y - 8, size + 16, size + 16)
            pdf.drawImage(ImageReader(image_path), x, y, width=size, height=size)
        except Exception as e:
            logging.warning("Não foi possível embutir o retrato no PDF: %s", e)

    text_x = 60
    y = height - 120
    line_height = 20

    def line(label, value):
        nonlocal y
        pdf.setFont(font, 15)
        pdf.setFillColor(colors.darkred)
        pdf.drawString(text_x, y, f"{label}:")
        pdf.setFillColor(colors.black)
        pdf.drawString(text_x + 150, y, str(value))
        y -= line_height

    def heading(text):
        nonlocal y
        y -= 6
        pdf.setFont(font, 18)
        pdf.setFillColor(colors.darkred)
        pdf.drawString(text_x, y, text)
        y -= line_height

    line(system["class_label"], class_info["name"] if class_info else "Desconhecido")
    if system["uses_race"]:
        line(system["race_label"], race_info["name"] if race_info else "Desconhecido")

    heading("Recursos")
    for resource in system["resources"]:
        values = character.get("resources", {}).get(resource["key"], {})
        line(resource["label"], f"{values.get('current', 0)} / {values.get('max', 0)}")

    heading("Atributos")
    for attribute in system["attributes"]:
        line(attribute["label"], character.get("attributes", {}).get(attribute["key"], 0))

    heading(system["ability_label"])
    pdf.setFont(font, 13)
    for ability in (character.get("habilidades") or {}).values():
        pdf.setFillColor(colors.black)
        pdf.drawString(text_x + 14, y, f"• {ability.get('name')}: {ability.get('description', '')}"[:96])
        y -= line_height - 4

    heading(system["skill_label"])
    pdf.setFont(font, 13)
    for skill, value in (character.get("pericias") or {}).items():
        pdf.setFillColor(colors.black)
        pdf.drawString(text_x + 14, y, f"• {skill}: +{value}")
        y -= line_height - 4

    if character.get("origem"):
        heading(system["history_label"])
        pdf.setFont(font, 13)
        for raw_line in str(character["origem"]).splitlines():
            for chunk in _wrap(raw_line, 88):
                pdf.setFillColor(colors.black)
                pdf.drawString(text_x + 14, y, chunk)
                y -= line_height - 5

    pdf.showPage()
    pdf.save()
    return buffer


def _wrap(text, width):
    words = text.split()
    if not words:
        return [""]
    lines, current = [], words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) <= width:
            current = f"{current} {word}"
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines
