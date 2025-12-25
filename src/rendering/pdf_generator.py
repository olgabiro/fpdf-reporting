from typing import List, Optional, Tuple

from fpdf import FPDF, XPos, YPos

from model.style import Style
from model.ticket import Status, Ticket

FONT_FAMILY: str = "Helvetica"
HEADER_SIZE: int = 20
SECTION_TITLE_SIZE: int = 13
TEXT_SIZE: int = 10
LABEL_SIZE: int = 7

# Priority indicator
PRIORITY_COLORS = {
    "High": (252, 216, 212),  # red
    "Medium": (255, 232, 163),  # yellow
    "Low": (217, 241, 208),  # green
}


class PDF(FPDF):
    style: Style

    def __init__(self, style: Style, **kwargs) -> None:
        super().__init__(**kwargs)
        self.style = style
        self.set_margin(25)

    def document_header(self, text: str, centered: bool = False) -> None:
        font = self.style.font
        self.set_font(font.font_family, "B", font.header_size)
        self.set_fill_color(*self.style.header_background)  # warm gray
        self.set_text_color(55, 53, 47)
        if centered:
            self.cell(
                0,
                font.header_size,
                text,
                align="C",
                fill=True,
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
        else:
            self.cell(self.style.padding, font.header_size, "", fill=True)
            self.cell(
                0,
                font.header_size,
                text,
                align="L",
                fill=True,
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
        self.set_y(self.get_y() + self.style.margin)

    def section_title(self, text: str) -> None:
        font = self.style.font
        self.set_font(font.font_family, "B", font.section_title_size)
        self.set_text_color(*self.style.section_title_color)
        self.cell(0, self.style.cell_height, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def summary_card(
            self,
            items: List[str],
            width: int = 80,
            x: Optional[float] = None,
            y: Optional[float] = None,
    ) -> tuple[float, float]:
        start_x = x or self.x
        start_y = y or self.y
        padding = self.style.padding
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

    def styled_table(self,
                     headers: list[str],
                     rows: list[tuple[str, str, str, str]],
                     col_widths: list[int]) -> None:
        font = self.style.font
        self.set_font(font.font_family, "B", font.table_header_size)
        self.set_fill_color(*self.style.table_header_color)
        self.set_text_color(*self.style.font_color)

        for i, h in enumerate(headers):
            self.cell(col_widths[i], 10, h, border="B", fill=True)
        self.ln(10)

        # rows
        self.set_font(font.font_family, "", font.table_content_size)

        for idx, row in enumerate(rows):
            self.set_fill_color(*self.style.table_row_colors[idx % 2])
            self.set_text_color(*self.style.font_color)

            for i, cell in enumerate(row):
                self.cell(
                    col_widths[i], font.table_content_size, cell, border="B", fill=True
                )

            self.ln()
        self.set_y(self.get_y() + self.style.margin)

    def tag(self,
            text: str,
            status: Status) -> Tuple[float, float]:
        bg = self.style.status_colors.get(
            status, self.style.status_colors[Status.OTHER]
        )
        self.set_font(self.style.font.font_family, "", self.style.font.tag_size)
        self.set_text_color(*self.style.font_color)

        text_w = self.get_string_width(text) + self.style.tag_padding * 2
        text_h = self.style.tag_padding + self.style.font.tag_size * 25.4 / 72.0
        x, y = self.get_x(), self.get_y()

        self.set_fill_color(*bg)
        self.rect(
            x, y, text_w, text_h, style="F", round_corners=True, corner_radius=1.5
        )

        self.set_xy(x + self.style.tag_padding - 1, y + 1)
        self.cell(text_w, text_h - self.style.tag_padding, text, border=0)
        self.set_xy(x + text_w, y)  # end cell
        return text_w, text_h

    def detailed_tickets_table(self, tickets: list[Ticket]) -> None:
        font = self.style.font
        self.set_font(font.font_family, "", font.font_size)

        for t in tickets:
            self.ticket_card_long(t)

    def ticket_card_long(self,
                         ticket: Ticket,
                         x: Optional[float] = None,
                         y: Optional[float] = None) -> None:
        start_x = x or self.x
        start_y = y or self.y
        width = self.w - self.r_margin - self.l_margin
        height = 22
        left_padding = 6
        top_padding = 2

        stripe_color: tuple[int, int, int] = self.style.category_colors.get(ticket.category)
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
            dot_color: tuple[int, int, int] | None = PRIORITY_COLORS.get(ticket.priority)
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

        self.set_y(start_y + height + self.style.padding)

    def bar_chart(self, values: list[int]) -> tuple[float, float]:
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
