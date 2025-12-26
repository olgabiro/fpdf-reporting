# Notion-style PDF Report Template using FPDF2
# You can replace FONT_FAMILY = "Helvetica" with "Inter" (or any other)
# once you add the font via pdf.add_font().

from fpdf import FPDF, XPos, YPos

FONT_FAMILY = "Helvetica"  # Change this to Inter later


class NotionPDF(FPDF):
    # Utility: draw a subtle Notion divider
    def divider(self, y_offset: float = 4) -> None:
        self.ln(y_offset)
        self.set_draw_color(230, 230, 230)
        x1, x2 = 10, self.w - 10
        y = self.get_y()
        self.line(x1, y, x2, y)
        self.ln(6)

    # Section title (Notion style)
    def section_title(self, text: str) -> None:
        self.set_font(FONT_FAMILY, "B", 13)
        self.set_text_color(55, 53, 47)
        self.cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    # Notion-like tag (rounded background)
    def tag(
        self,
        text: str,
        bg_color: tuple[int, int, int] = (217, 241, 208),
        padding_x: float = 2,
        padding_y: float = 1,
    ) -> None:
        self.set_font(FONT_FAMILY, "", 9)
        self.set_text_color(55, 53, 47)
        self.set_fill_color(*bg_color)
        # approximate rounded tag using cell
        self.cell(
            self.get_string_width(text) + padding_x * 2,
            6 + padding_y,
            text,
            border=0,
            ln=0,
            fill=True,
        )

    # Render Summary card style: light warm background + spacing
    def summary_card(self, items: list[tuple[str, str]]) -> None:
        self.set_fill_color(255, 238, 189)
        self.set_xy(10, self.get_y())

        # approximate a card block
        self.set_font(FONT_FAMILY, "", 10)
        self.set_text_color(80, 79, 75)
        start_y = self.get_y()

        # compute card height
        card_height = (len(items) * 8) + 3
        self.multi_cell(0, card_height, "", fill=True)

        # print content inside card
        self.set_xy(15, start_y + 5)
        for label, value in items:
            self.set_x(15)
            self.set_text_color(80, 79, 75)
            self.cell(50, 6, label)
            self.set_text_color(55, 53, 47)
            self.cell(30, 6, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(6)

    # Notion-style table
    def formatted_table(
        self,
        headers: list[str],
        rows: list[tuple[str, str, str, str]],
        col_widths: list[int],
    ) -> None:
        # header background
        self.set_font(FONT_FAMILY, "B", 11)
        self.set_fill_color(243, 242, 239)
        self.set_text_color(55, 53, 47)

        for i, h in enumerate(headers):
            self.cell(col_widths[i], 10, h, border="B", fill=True)
        self.ln(10)

        # rows
        self.set_font(FONT_FAMILY, "", 9)
        row_colors = [(255, 255, 255), (250, 249, 247)]

        for idx, row in enumerate(rows):
            self.set_fill_color(*row_colors[idx % 2])
            self.set_text_color(55, 53, 47)

            for i, cell in enumerate(row):
                self.cell(col_widths[i], 8, cell, border="B", fill=True)

            self.ln(8)


# EXAMPLE USAGE --------------------------------------------------------------


def generate_notion_pdf() -> None:
    pdf = NotionPDF()
    pdf.add_page()

    # Header block
    pdf.set_font(FONT_FAMILY, "B", 20)
    pdf.set_fill_color(247, 246, 243)  # warm gray
    pdf.set_text_color(55, 53, 47)
    pdf.cell(
        0,
        20,
        "Sprint 42 - JIRA Report",
        align="L",
        fill=True,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    pdf.ln(4)
    pdf.divider()

    # Summary section
    pdf.section_title("Summary")
    summary_data = [
        ("Total Tickets", "58"),
        ("Completed", "42"),
        ("In Progress", "10"),
        ("Blocked", "6"),
    ]

    pdf.summary_card(summary_data)
    pdf.ln(5)
    pdf.divider()

    # Table section
    pdf.section_title("Tickets")

    headers = ["Key", "Summary", "Status", "Assignee"]
    col_widths = [20, 80, 30, 30]

    table_data = [
        ("PROJ-101", "Fix login flow", "Done", "Alice"),
        ("PROJ-102", "Add metrics dashboard", "In Progress", "Bob"),
        ("PROJ-103", "Payment gateway issue", "Blocked", "Eve"),
    ]

    pdf.formatted_table(headers, table_data, col_widths)

    pdf.tag("Last updated 1 hour ago")

    pdf.output("./output/notion_report.pdf")


if __name__ == "__main__":
    generate_notion_pdf()
