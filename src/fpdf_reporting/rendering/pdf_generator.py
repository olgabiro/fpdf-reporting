from pathlib import Path
from typing import Any, List, Optional, Tuple

from fpdf import FPDF, XPos, YPos

from fpdf_reporting.model.style import Style
from fpdf_reporting.model.ticket import Status, Ticket
from fpdf_reporting.rendering.graphs import build_pie_chart_bytes

FONT_FAMILY: str = "Inter"
HEADER_SIZE: int = 20
SECTION_TITLE_SIZE: int = 13
TEXT_SIZE: int = 10
LABEL_SIZE: int = 7
MARGIN_SIZE: int = 25

_SMALL_SPACING: float = 2
_MEDIUM_SPACING: float = 5
_LARGE_SPACING: float = 10

# Priority indicator
PRIORITY_COLORS = {
    "High": (252, 216, 212),  # red
    "Medium": (255, 232, 163),  # yellow
    "Low": (217, 241, 208),  # green
}

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "fonts"


class PDF(FPDF):
    style: Style

    def __init__(self, style: Style, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.style = style
        self.set_margin(MARGIN_SIZE)
        self.add_font(FONT_FAMILY, "", OUTPUT_DIR / "Inter-Regular.ttf")
        self.add_font(FONT_FAMILY, "B", OUTPUT_DIR / "Inter-Bold.ttf")
        self.add_font(FONT_FAMILY, "I", OUTPUT_DIR / "Inter-Italic.ttf")

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT_FAMILY, "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def document_header(self, text: str, centered: bool = False) -> None:
        self.set_font(FONT_FAMILY, "B", size=HEADER_SIZE)
        self.set_fill_color(*self.style.header_background)  # warm gray
        self.set_text_color(55, 53, 47)
        if centered:
            self.cell(
                0,
                HEADER_SIZE,
                text,
                align="C",
                fill=True,
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
        else:
            self.cell(_MEDIUM_SPACING, HEADER_SIZE, "", fill=True)
            self.cell(
                0,
                HEADER_SIZE,
                text,
                align="L",
                fill=True,
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
        self.set_y(self.get_y() + _LARGE_SPACING)

    def divider(self) -> None:
        self.set_draw_color(*self.style.border_color)
        x1, x2 = MARGIN_SIZE, self.w - MARGIN_SIZE
        y = self.get_y() + _MEDIUM_SPACING
        self.line(x1, y, x2, y)
        self.ln(_MEDIUM_SPACING)

    def section_title(self, text: str) -> None:
        self.set_font(FONT_FAMILY, "B", SECTION_TITLE_SIZE)
        self.set_text_color(*self.style.section_title_color)
        self.cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(self.get_x(), self.get_y() + _LARGE_SPACING)

    def summary_card(
        self,
        items: List[str],
        width: int = 80,
        x: Optional[float] = None,
        y: Optional[float] = None,
    ) -> tuple[float, float]:
        start_x = x or self.x
        start_y = y or self.y
        padding = _MEDIUM_SPACING
        row_height = 6
        card_height = (len(items) * row_height) + 2 * padding

        self.set_fill_color(*self.style.card_background)
        self.rect(
            start_x,
            start_y,
            width,
            card_height,
            style="F",
            round_corners=True,
            corner_radius=1.5,
        )
        self.set_font(FONT_FAMILY, "", TEXT_SIZE)
        self.set_text_color(*self.style.font_color)

        x = start_x + padding
        y = start_y + padding
        self.set_text_color(*self.style.card_details_color)
        for text in items:
            self.set_xy(x, y)
            self.cell(width - 2 * padding, row_height, text, align="L")
            y = y + row_height

        if start_x + width >= self.w - self.r_margin:
            self.set_xy(self.l_margin, start_y + card_height + padding)
        else:
            self.set_xy(start_x + width + padding, start_y)
        return start_x + width, start_y + card_height

    def styled_table(
        self,
        headers: list[str],
        rows: list[tuple[str, str, str, str]],
        col_widths: list[int],
    ) -> None:
        self.set_font(FONT_FAMILY, "B", TEXT_SIZE)
        self.set_fill_color(*self.style.table_header_color)
        self.set_text_color(*self.style.font_color)

        for i, h in enumerate(headers):
            self.cell(col_widths[i], 10, h, border="B", fill=True)
        self.ln(10)

        # rows
        self.set_font(FONT_FAMILY, "", LABEL_SIZE)

        for idx, row in enumerate(rows):
            self.set_fill_color(*self.style.table_row_colors[idx % 2])
            self.set_text_color(*self.style.font_color)

            for i, cell in enumerate(row):
                self.cell(col_widths[i], LABEL_SIZE, cell, border="B", fill=True)

            self.ln()
        self.set_y(self.get_y() + _LARGE_SPACING)

    def tag(self, text: str, status: Status) -> Tuple[float, float]:
        bg = self.style.status_colors.get(
            status, self.style.status_colors[Status.OTHER]
        )
        self.set_font(FONT_FAMILY, "", LABEL_SIZE)
        self.set_text_color(*self.style.font_color)

        text_w = self.get_string_width(text) + _SMALL_SPACING * 2
        text_h = _SMALL_SPACING + LABEL_SIZE * 25.4 / 72.0
        x, y = self.get_x(), self.get_y()

        self.set_fill_color(*bg)
        self.rect(
            x, y, text_w, text_h, style="F", round_corners=True, corner_radius=1.5
        )

        self.set_xy(x + _SMALL_SPACING - 1, y + 1)
        self.cell(text_w, text_h - _SMALL_SPACING, text, border=0)
        self.set_xy(x + text_w, y)  # end cell
        return text_w, text_h

    def detailed_tickets_table(self, tickets: list[Ticket]) -> None:
        self.set_font(FONT_FAMILY, "", TEXT_SIZE)

        for t in tickets:
            self.ticket_card_long(t)

    def ticket_card_long(
        self, ticket: Ticket, x: Optional[float] = None, y: Optional[float] = None
    ) -> None:
        start_x = x or self.x
        start_y = y or self.y
        width = self.w - self.r_margin - self.l_margin
        height = 22
        left_padding = 6
        top_padding = 2

        stripe_color: tuple[int, int, int] = self.style.category_colors.get(
            ticket.category, self.style.border_color
        )
        self.set_fill_color(*stripe_color)
        self.rect(
            start_x,
            start_y,
            2.5,
            height,
            style="F",
            round_corners=True,
            corner_radius=3,
        )
        self.set_draw_color(*self.style.border_color)
        self.rect(
            start_x, start_y, width, height, round_corners=True, corner_radius=1.5
        )

        self.set_xy(start_x + left_padding, start_y + top_padding)

        key_width = 15
        (_, line_height) = self.tag(ticket.status, ticket.status)
        self.set_font(FONT_FAMILY, "B", TEXT_SIZE)
        self.set_text_color(*self.style.font_color)
        self.set_x(self.get_x() + left_padding)
        self.cell(key_width, line_height, ticket.key)
        self.set_font(FONT_FAMILY, "", TEXT_SIZE)
        self.cell(width - key_width, line_height, ticket.summary, new_y=YPos.NEXT)

        self.set_xy(start_x + left_padding, start_y + line_height + 2 * top_padding)
        self.tag(ticket.issue_type, Status.OTHER)
        if ticket.priority:
            dot_color: tuple[int, int, int] = PRIORITY_COLORS.get(
                ticket.priority, (217, 241, 208)
            )
            dot_x = self.get_x() + left_padding
            dot_y = self.get_y() + (line_height - 3) / 2
            self.set_fill_color(*dot_color)
            self.ellipse(dot_x, dot_y, 3, 3, style="F")
            self.set_x(dot_x + 3)
            self.cell(10, line_height, ticket.priority)

        self.set_xy(start_x + left_padding, self.get_y() + line_height + top_padding)

        self.set_font(FONT_FAMILY, "", 9)
        self.cell(
            width - 12, 4, f"SP: {ticket.story_points}   Component: {ticket.component}"
        )

        self.set_y(start_y + height + _MEDIUM_SPACING)

    def _plot_bar_chart(self, values: list[float]) -> tuple[float, float]:
        spacing = 2
        bar_width = 3
        x = self.x
        start_y = self.y
        height = 30
        width = x + len(values) * (bar_width + spacing) + spacing
        max_value = max(values) if values else 0

        self.line(x, start_y, width, start_y)
        self.line(x, start_y + 5, width, start_y + 5)
        self.line(x, start_y + 10, width, start_y + 10)
        self.line(x, start_y + 15, width, start_y + 15)
        self.line(x, start_y + 20, width, start_y + 20)
        self.line(x, start_y + 25, width, start_y + 25)

        x += spacing

        for index, value in enumerate(values):
            self.set_fill_color(
                *self.style.chart_colors[index % len(self.style.chart_colors)]
            )
            bar_height = height * value / max_value
            y = start_y + height - bar_height
            self.rect(
                x,
                y,
                bar_width,
                bar_height,
                style="F",
                round_corners=True,
                corner_radius=1.5,
            )
            x += bar_width + spacing

        return x - spacing, start_y + height

    def bar_chart(
        self, data: dict[str, float], caption: Optional[str] = None
    ) -> tuple[float, float]:
        x = self.x
        y = self.y
        self._plot_bar_chart(list(data.values()))
        self.legend(list(data.keys()), x + 30, y + _SMALL_SPACING, caption=caption)
        self.set_xy(self.x + 15, y)
        return self.x, y + 30

    def pie_chart(
        self,
        data: dict[str, float],
        width: float = 70,
        caption: Optional[str] = None,
    ) -> None:
        """Generate a pie chart in-memory and insert it into the PDF."""
        img_buf = build_pie_chart_bytes(
            list(data.values()), colors=self.style.chart_colors
        )

        if img_buf is None:
            return

        x = self.get_x()
        y = self.get_y()

        self.image(img_buf, x=x, y=y, w=width)
        self.set_xy(x + width, y)

        legend_x = x + width + _MEDIUM_SPACING
        legend_y = y + _SMALL_SPACING
        self.legend(list(data.keys()), legend_x, legend_y, caption=caption)

    def legend(
        self, labels: list[str], x: float, y: float, caption: Optional[str] = None
    ) -> None:
        if caption:
            self.set_xy(x - 1, y)
            self.set_font(FONT_FAMILY, "", 9)
            self.cell(0, 5, caption, align="L")
            y += 5 + _SMALL_SPACING

        self.set_font(FONT_FAMILY, "", 9)
        legend_colors = self.style.chart_colors
        for idx, label in enumerate(labels):
            color = legend_colors[idx % len(legend_colors)]
            (_, y) = self.legend_label(color, label, x, y)

    def legend_label(
        self,
        color: tuple[int, int, int],
        label: str,
        x: Optional[float] = None,
        y: Optional[float] = None,
    ) -> tuple[float, float]:
        start_x = x or self.x
        start_y = y or self.y

        self.set_xy(start_x, start_y)
        self.set_fill_color(*color)
        self.ellipse(start_x, start_y + 0.5, 2, 2, style="F")
        self.set_x(start_x + 2)
        self.set_font(FONT_FAMILY, "", LABEL_SIZE)
        self.set_text_color(*self.style.font_color)
        self.cell(15, 3, label)
        self.set_font(FONT_FAMILY, "", TEXT_SIZE)
        return start_x + 15, start_y + 4
