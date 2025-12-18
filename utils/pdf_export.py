# utils/pdf_export.py
from io import BytesIO
from dataclasses import dataclass
from typing import List, Optional, Tuple
import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)

from utils.signature_block import make_signature_block

# Single source for headers; stored as unicode escapes to avoid encoding issues
HEADERS = ["\u2116", "\u041d\u043e\u043c\u0435\u0440 \u0441\u0435\u0440\u0438\u0438", "\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435"]
FONT_PATH = os.path.join(os.getcwd(), "DejaVuSans.ttf")
pdfmetrics.registerFont(TTFont("DejaVu", FONT_PATH))


@dataclass
class PdfSection:
    heading: str
    body_html: Optional[str] = None
    table_df: Optional[pd.DataFrame] = None
    show_heading: bool = True


def _fig_to_png_bytes(fig) -> BytesIO:
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    buf.seek(0)
    return buf


def _strip_spans(html: str) -> str:
    """Remove span tags and inline styles unsupported by ReportLab's mini-HTML."""
    return html.replace("<span", "<dummy-span").replace("</span>", "</dummy-span>")


def _prepare_paragraph_html(html: str) -> str:
    """
    Normalize HTML for ReportLab Paragraph:
    - remove span tags
    - normalize <br> / <br /> to self-closing <br/>
    - replace paragraph wrappers with line breaks
    """
    safe = _strip_spans(html)
    safe = safe.replace("<p>", "").replace("</p>", "<br/>")
    # ensure break tags are self-closing
    safe = safe.replace("<br>", "<br/>").replace("<br />", "<br/>")
    return safe


class NumberedCanvas(canvas.Canvas):
    """Canvas with total page count for the footer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_page_number(total_pages)
            super().showPage()
        super().save()

    def _draw_page_number(self, total_pages: int):
        # Footer: "Page X of Y"
        self.saveState()
        self.setFont("DejaVu", 9)
        page_w, _ = A4
        y = 18
        current = self.getPageNumber()
        text = f"\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 {current} \u0438\u0437 {total_pages}"
        self.drawCentredString(page_w / 2, y, text)
        self.restoreState()


def _df_to_series_value_page(df: pd.DataFrame, styles, rows_per_col: int = 23, start_index: int = 1):
    """Render a single two-up page with exactly three columns: №, series id, value."""
    work = df.copy().reset_index(drop=True)
    if work.shape[1] != 2:
        raise ValueError(f"Expected 2 columns (Series, Value), got {work.shape[1]}")

    work.columns = HEADERS[1:]
    work.insert(0, HEADERS[0], range(start_index, start_index + len(work)))

    left = work.iloc[:rows_per_col].copy()
    right = work.iloc[rows_per_col: rows_per_col * 2].copy()

    cell_style = ParagraphStyle(
        "cell",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=9,
        leading=10,
        spaceAfter=0,
        spaceBefore=0,
    )

    def to_para(x):
        text = "" if pd.isna(x) else str(x)
        return Paragraph(text.replace("\n", "<br/>"), cell_style)

    def make_table(part: pd.DataFrame):
        data = [list(part.columns)] + [[to_para(v) for v in row] for row in part.values.tolist()]
        usable_half = (A4[0] - 60 - 10) / 2  # width per half-page minus 10 px gap
        col_widths = [
            0.12 * usable_half,  # №
            0.55 * usable_half,  # series id
            0.33 * usable_half,  # value
        ]
        t = Table(data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.75, colors.black),
            ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("ALIGN", (0, 1), (-1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        return t

    t_left = make_table(left)
    t_right = make_table(right)

    page_w = A4[0] - 60
    gap = 10  # расстояние между двумя таблицами
    col_w = (page_w - gap) / 2

    # Добавляем явный "пробел" между двумя таблицами, чтобы сетки не сливались
    container = Table([[t_left, "", t_right]], colWidths=[col_w, gap, col_w])
    container.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return container


def build_series_value_tables(df: pd.DataFrame, styles, rows_per_col: int = 23):
    """Split the dataframe across pages while keeping numbering continuous."""
    if df.shape[1] != 2:
        raise ValueError(f"Expected 2 columns (Series, Value), got {df.shape[1]}")

    flow = []
    rows_per_page = rows_per_col * 2
    start = 0

    while start < len(df):
        chunk = df.iloc[start:start + rows_per_page].copy()
        tbl = _df_to_series_value_page(chunk, styles, rows_per_col=rows_per_col, start_index=start + 1)
        flow.append(tbl)
        flow.append(Spacer(1, 12))
        start += rows_per_page
        if start < len(df):
            flow.append(PageBreak())

    return flow


def df_to_single_col_table(df: pd.DataFrame, styles):
    """Render a single-column table centered within page width."""
    work = df.copy().reset_index(drop=True)
    if work.shape[1] != 1:
        raise ValueError(f"Expected 1 column, got {work.shape[1]}")

    cell_style = ParagraphStyle(
        "cell_single",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=9,
        leading=11,
        alignment=1,  # center
        spaceAfter=0,
        spaceBefore=0,
    )

    def to_para(x):
        text = "" if pd.isna(x) else str(x)
        return Paragraph(text.replace("\n", "<br/>"), cell_style)

    data = [[to_para(v)] for v in work.iloc[:, 0].to_list()]
    tbl = Table(data, colWidths=[A4[0] - 60], repeatRows=0)
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.75, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return tbl


def build_pdf(
    title: str,
    sections: List[PdfSection],
    figures: List[Tuple[str, "matplotlib.figure.Figure"]],
    conclusions: str = "",
    show_title: bool = False,
    footer_left: str = "",
    footer_right: str = "",
    signatures: Optional[List[dict]] = None,
    signature_roles: Optional[List[str]] = None,
    after_figures_sections: Optional[List[PdfSection]] = None,
    cover_page: Optional[dict] = None,
    header: Optional[dict] = None,
) -> BytesIO:
    base_top_margin = 30
    header_height = header.get("height", 0) if header else 0
    top_margin = base_top_margin + header_height
    pdf_buf = BytesIO()
    doc = SimpleDocTemplate(
        pdf_buf,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=top_margin,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    for style in styles.byName.values():
        style.fontName = "DejaVu"

    story = []

    if cover_page:
        center_style = ParagraphStyle(
            "CoverCenter",
            parent=styles["Heading2"],
            alignment=1,  # center
            fontName="DejaVu",
            fontSize=12,
            leading=15,
            spaceAfter=4,
        )
        section_style = ParagraphStyle(
            "CoverSection",
            parent=styles["Heading2"],
            alignment=0,  # left
            fontName="DejaVu",
            fontSize=12,
            leading=14,
            spaceBefore=16,
            spaceAfter=16,
        )
        for line in cover_page.get("center_lines", []):
            story.append(Paragraph(f"<b>{line}</b>", center_style))
        if cover_page.get("section_heading"):
            story.append(Paragraph(f"<b>{cover_page['section_heading']}</b>", section_style))
            story.append(Spacer(1, 12))

    if show_title and title:
        story.append(Paragraph(title, styles["Title"]))
        story.append(Spacer(1, 12))

    def _render_section(sec: PdfSection):
        if sec.show_heading and sec.heading:
            story.append(Paragraph(sec.heading, styles["Heading2"]))
            story.append(Spacer(1, 6))

        if sec.body_html:
            safe_html = _prepare_paragraph_html(sec.body_html)
            story.append(Paragraph(safe_html, styles["BodyText"]))
            story.append(Spacer(1, 10))

        if sec.table_df is not None and not sec.table_df.empty:
            if sec.table_df.shape[1] == 2:
                tables = build_series_value_tables(sec.table_df, styles, rows_per_col=23)
                story.extend(tables)
            elif sec.table_df.shape[1] == 1:
                story.append(df_to_single_col_table(sec.table_df, styles))
                story.append(Spacer(1, 12))
            else:
                raise ValueError("Table must have 1 or 2 columns for PDF export")

            if story and not isinstance(story[-1], PageBreak):
                story.append(PageBreak())

    for s in sections:
        _render_section(s)

    if figures:
        story.append(Paragraph("\u0413\u0440\u0430\u0444\u0438\u043a\u0438", styles["Heading2"]))
        story.append(Spacer(1, 6))
        for item in figures:
            # allow (caption, fig) or (caption, fig, description_html)
            caption, fig = item[0], item[1]
            desc_html = item[2] if len(item) > 2 else None
            img_buf = _fig_to_png_bytes(fig)
            block = [
                Paragraph(caption, styles["BodyText"]),
                Image(img_buf, width=500, height=280),
            ]
            if desc_html:
                safe_desc = _prepare_paragraph_html(desc_html)
                block.append(Spacer(1, 6))
                block.append(Paragraph(safe_desc, styles["BodyText"]))
            block.append(Spacer(1, 12))
            story.append(KeepTogether(block))

    if conclusions:
        story.append(Paragraph("\u0412\u044b\u0432\u043e\u0434\u044b", styles["Heading2"]))
        story.append(Spacer(1, 6))
        safe_conc = _prepare_paragraph_html(conclusions.replace("\n", "<br/>"))
        story.append(Paragraph(safe_conc, styles["BodyText"]))

    if after_figures_sections:
        for s in after_figures_sections:
            _render_section(s)

    # Signature block at the end so approvals/sign-offs can be filled
    story.append(Spacer(1, 18))
    story.append(make_signature_block(styles, signatures, roles=signature_roles))

    def _draw_footer(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFont("DejaVu", 9)
        page_w, _ = A4
        y = 18
        if footer_left:
            canvas_obj.drawString(doc_obj.leftMargin, y, footer_left)
        if footer_right:
            canvas_obj.drawRightString(page_w - doc_obj.rightMargin, y, footer_right)
        canvas_obj.restoreState()

    def _draw_header(canvas_obj, doc_obj):
        if not header:
            return
        canvas_obj.saveState()
        canvas_obj.setFont("DejaVu", 12)
        page_w, page_h = A4
        left_x = doc_obj.leftMargin
        right_x = page_w - doc_obj.rightMargin
        top_y = page_h - base_top_margin - 8
        sub_y = top_y - 16

        left_title = header.get("left_title", "")
        left_subtitle = header.get("left_subtitle", "")
        right_lines = header.get("right_lines", [])

        if left_title:
            canvas_obj.drawString(left_x, top_y, left_title)
        if left_subtitle:
            canvas_obj.drawString(left_x, sub_y, left_subtitle)
        for idx, line in enumerate(right_lines):
            canvas_obj.drawRightString(right_x, top_y - idx * 14, line)

        line_y = A4[1] - top_margin + 12
        canvas_obj.setLineWidth(0.8)
        canvas_obj.line(left_x, line_y, right_x, line_y)
        canvas_obj.restoreState()

    def _decorate_page(canvas_obj, doc_obj):
        _draw_header(canvas_obj, doc_obj)
        _draw_footer(canvas_obj, doc_obj)

    doc.build(story, canvasmaker=NumberedCanvas, onFirstPage=_decorate_page, onLaterPages=_decorate_page)
    pdf_buf.seek(0)
    return pdf_buf
