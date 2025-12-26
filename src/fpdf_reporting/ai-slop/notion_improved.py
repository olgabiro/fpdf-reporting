# Notion-style PDF Report Template using FPDF2 (updated with rounded tags + Notion-colored status tags)
# You can replace FONT_FAMILY = "Helvetica" with "Inter" (or any other)
# once you add the font via pdf.add_font().

import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF, XPos, YPos

FONT_FAMILY = "Helvetica"  # Change this to Inter later

NOTION_COLORS = [
    (212 / 255, 228 / 255, 247 / 255),
    (255 / 255, 232 / 255, 163 / 255),
    (252 / 255, 216 / 255, 212 / 255),
    (217 / 255, 241 / 255, 208 / 255),
    (155 / 255, 207 / 255, 87 / 255),  # green
    (246 / 255, 199 / 255, 68 / 255),  # yellow
    (108 / 255, 155 / 255, 245 / 255),  # blue
    (221 / 255, 148 / 255, 255 / 255),  # purple
    (255 / 255, 170 / 255, 153 / 255),  # coral
    (181 / 255, 181 / 255, 181 / 255),  # gray
]


def make_pie_chart(
    title: str, data_pairs: list[tuple[str, float]], outfile: str
) -> None:
    """
    data_pairs = [("Committed", 12), ("Maybe", 5), ("None", 2)]
    """
    labels = [p[0] for p in data_pairs]
    sizes = [p[1] for p in data_pairs]

    fig, ax = plt.subplots(figsize=(3, 3))  # small footprint
    fig.patch.set_facecolor("white")

    pie = ax.pie(
        sizes, colors=NOTION_COLORS[: len(labels)], startangle=90, counterclock=False
    )

    # Adding data labels directly on slices
    for i, w in enumerate(pie[0]):
        ang = (w.theta2 + w.theta1) / 2
        x = np.cos(np.deg2rad(ang))
        y = np.sin(np.deg2rad(ang))
        ax.text(x * 0.6, y * 0.6, f"{sizes[i]}", ha="center", va="center", fontsize=10)

    ax.set_title(title, fontsize=12)
    ax.axis("equal")

    plt.savefig(outfile, dpi=200, bbox_inches="tight")
    plt.close(fig)


class NotionPDF(FPDF):
    TAG_COLORS = {
        "Done": (217, 241, 208),  # green
        "In Progress": (255, 232, 163),  # yellow
        "Blocked": (252, 216, 212),  # red
        "Review": (212, 228, 247),  # blue
        "Default": (227, 226, 224),  # neutral gray
    }

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

        # Notion-like rounded tag using rounded rectangles

    def tag(self, text: str, status: str = "Default") -> None:
        bg = self.TAG_COLORS.get(status, self.TAG_COLORS["Default"])
        self.set_font(FONT_FAMILY, "", 9)
        self.set_text_color(55, 53, 47)

        text_w = self.get_string_width(text) + 6
        text_h = 6
        x, y = self.get_x(), self.get_y()

        # Draw rounded rectangle
        self.set_fill_color(*bg)
        self.rect(
            x, y, text_w, text_h, style="F", round_corners=True, corner_radius=1.5
        )

        # Print text
        self.set_xy(x + 2, y + 1)
        self.cell(text_w, text_h - 2, text, border=0)
        self.set_xy(x + text_w, y)  # end cell

    def summary_card(self, items: list[tuple[str, str]]) -> None:
        self.set_fill_color(247, 246, 243)
        self.set_xy(10, self.get_y())

        # approximate a card block
        self.set_font(FONT_FAMILY, "", 10)
        self.set_text_color(80, 79, 75)
        start_y = self.get_y()

        # compute card height
        card_height = (len(items) * 8) + 3
        card_width = 80
        self.multi_cell(card_width, card_height, "", fill=True)

        # print content inside card
        self.set_xy(15, start_y + 5)
        for label, value in items:
            self.set_text_color(50, 79, 75)
            self.cell(40, 6, label)
            self.set_text_color(55, 53, 47)
            self.cell(10, 6, value)
            self.set_text_color(55, 53, 47)
            self.cell(10, 6, value)
            self.set_text_color(55, 53, 47)
            self.cell(10, 6, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_x(15)

        self.ln(6)

    # Notion-style table
    def notion_table(
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

    # ------------------------------------------------------------------
    # Detailed Tickets Table (Notion-style rich row visualization)
    # ------------------------------------------------------------------

    def detailed_tickets_table(
        self, tickets: list[dict[str, str | bool | int]]
    ) -> None:
        """
        Render a detailed list of tickets with:
        - Key
        - Summary
        - Status (rounded tag)
        - Issue Type (tag)
        - Priority (color dot)
        - Story Points
        - Flagged (red left border)
        - Component (text)
        - Category (colored left stripe)
        """
        self.set_font(FONT_FAMILY, "", 10)

        for t in tickets:
            key: str = str(t.get("key", "PD-132"))
            summary: str = str(t.get("summary", "Example Summary"))
            status: str = str(t.get("status", "In Progress"))
            issue_type: str = str(t.get("issue_type", "Bug"))
            priority: str = str(t.get("priority", "Medium"))
            story_points: str = str(t.get("story_points", "-"))
            flagged: bool = bool(t.get("flagged", False))
            component: str = str(t.get("component", "Strategical"))
            category: str | None = str(t.get("category", "committed"))

            # Row box dimensions
            box_x = 10
            box_y = self.get_y()
            w = self.w - 20
            h = 22

            # Category-colored left stripe
            cat_colors = {
                "committed": (217, 241, 208),  # green
                "nice to have": (255, 232, 163),  # yellow
                "maybe": (212, 228, 247),  # blue
                None: (227, 226, 224),  # neutral gray
            }
            stripe_color = cat_colors.get(category, (227, 226, 224))

            self.set_fill_color(*stripe_color)
            self.rect(
                box_x, box_y, 3, h, style="F", round_corners=True, corner_radius=5
            )

            # Flagged tickets get a red left border highlight
            if flagged:
                self.set_draw_color(252, 216, 212)
            else:
                # Outer row box (subtle)
                self.set_draw_color(230, 230, 230)
            self.rect(box_x, box_y, w, h, round_corners=True, corner_radius=1.5)

            # Text positioning
            self.set_xy(box_x + 6, box_y + 2)

            # TOP: KEY + TAGS
            self.set_font(FONT_FAMILY, "B", 10)
            self.set_text_color(55, 53, 47)
            self.cell(25, 5, key)

            # Status tag
            self.tag(status, status)
            self.ln(6)
            self.set_x(box_x + 6)

            # Issue type tag
            self.tag(issue_type, "Default")

            # Priority indicator
            pri_colors = {
                "High": (252, 216, 212),  # red
                "Medium": (255, 232, 163),  # yellow
                "Low": (217, 241, 208),  # green
            }
            dot_color = pri_colors.get(priority, (227, 226, 224))
            dot_x = self.get_x() + 2
            dot_y = self.get_y() + 1.5
            self.set_fill_color(*dot_color)
            self.ellipse(dot_x, dot_y, 3, 3, style="F")
            self.set_xy(dot_x + 3, dot_y - 1)
            self.cell(10, 5, priority)

            self.ln(7)
            self.set_x(box_x + 6)

            # Summary + Story Points + Component
            self.set_font(FONT_FAMILY, "", 9)
            self.multi_cell(
                w - 12, 4, f"{summary} SP: {story_points}   Component: {component}"
            )

            self.ln(5)


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

    # Example: use tags in table
    # Convert statuses to tags
    transformed_rows = []
    for key, summary, status, assignee in table_data:
        transformed_rows.append((key, summary, status, assignee))
    pdf.notion_table(headers, transformed_rows, col_widths)

    pdf.ln(6)
    pdf.section_title("Detailed Tickets")
    pdf.detailed_tickets_table(
        [
            {},
            {
                "key": "PROJ-104",
                "summary": "longer summary here",
                "status": "Review",
                "issue_type": "Feature",
                "priority": "High",
                "story_points": 2,
                "category": "nice to have",
                "flagged": True,
            },
        ]
    )

    pdf.section_title("Story Points Distribution")

    make_pie_chart(
        "Categories",
        [("Committed", 12), ("Maybe", 5), ("None", 2)],
        "category_chart.png",
    )
    make_pie_chart(
        "Priorities", [("High", 10), ("Medium", 20), ("Low", 30)], "priority_chart.png"
    )
    chart_width = 40  # mm
    pdf.image("category_chart.png", x=pdf.get_x(), y=pdf.get_y(), w=chart_width)
    pdf.set_x(pdf.get_x() + chart_width + 10)
    pdf.image("priority_chart.png", x=pdf.get_x(), y=pdf.get_y(), w=chart_width)
    pdf.ln(40)  # move to next row

    # pdf.ln(2)
    pdf.set_font(FONT_FAMILY, "", 10)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(chart_width, 6, "Story Points by Category", align="C")

    pdf.output("./output/notion_improved_report.pdf")


if __name__ == "__main__":
    generate_notion_pdf()
