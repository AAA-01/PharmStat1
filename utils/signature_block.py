# utils/signature_block.py
from typing import List, Optional, Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

DEFAULT_ROLES = ["Утверждено:", "Согласовано:", "Проверено:", "Подготовлено:"]
HEADER_TEXT = ("<b>Ф.И.О.</b><br/>Должность", "Подпись, дата / ЭЦП")


def make_signature_block(
    styles,
    signatures: Optional[List[Dict[str, str]]] = None,
    roles: Optional[List[str]] = None,
) -> Table:
    """
    Build a 3-column signature table:
    [Role] | [Name + Position] | [Signature/date].
    If signatures are missing, cells stay empty so they can be filled later.
    """
    roles = roles or DEFAULT_ROLES
    signatures = signatures or []

    def clean_text(value: Optional[str]) -> str:
        return "" if value is None else str(value)

    header_style = ParagraphStyle(
        "sig_header",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=10,
        leading=12,
        alignment=1,  # center
        spaceAfter=4,
    )
    cell_style = ParagraphStyle(
        "sig_cell",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=9,
        leading=11,
    )

    data = [
        ["", Paragraph(HEADER_TEXT[0], header_style), Paragraph(HEADER_TEXT[1], header_style)],
    ]

    max_len = max(len(roles), len(signatures))
    for idx in range(max_len):
        role = clean_text(roles[idx]) if idx < len(roles) else ""
        payload = signatures[idx] if idx < len(signatures) else {}
        name = clean_text(payload.get("name", ""))
        position = clean_text(payload.get("position", ""))
        sign = clean_text(payload.get("signature", ""))

        # Skip rows that are entirely empty (for flexible removal)
        if not any([role.strip(), name.strip(), position.strip(), sign.strip()]):
            continue

        full = "<br/>".join([p for p in [name, position] if p.strip()])
        data.append([
            Paragraph(role, cell_style),
            Paragraph(full, cell_style),
            Paragraph(sign, cell_style),
        ])

    usable_w = A4[0] - 60  # same margins as pdf_export
    col_widths = [0.18 * usable_w, 0.46 * usable_w, 0.36 * usable_w]

    tbl = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.75, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (0, 1), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl
