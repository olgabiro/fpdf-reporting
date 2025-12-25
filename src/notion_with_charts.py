# Notion-style PDF Report Template using FPDF2 (updated with rounded tags + Notion-colored status tags)
# You can replace FONT_FAMILY = "Helvetica" with "Inter" (or any other)
# once you add the font via pdf.add_font().

from io import BytesIO
from typing import Callable, Optional

import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF, XPos, YPos

FONT_FAMILY = "Helvetica"  # Change this to Inter later


class NotionPDF(FPDF):
    TAG_COLORS = {
        "Done": (217, 241, 208),  # green
        "In Progress": (255, 232, 163),  # yellow
        "Blocked": (252, 216, 212),  # red
        "Review": (212, 228, 247),  # blue
        "Default": (227, 226, 224),  # neutral gray
    }

    add_multiple_pie_charts: Callable
    add_pie_chart: Callable
    build_pie_chart_bytes: Callable

    # Utility: draw a subtle Notion divider
    def divider(self, y_offset: float=4) -> None:
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
        self.rect(x, y, text_w, text_h, style="F", round_corners=True, corner_radius=1.5)

        # Print text
        self.set_xy(x + 3, y + 1)
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
        card_height = (len(items) * 8) + 8
        self.multi_cell(0, card_height, "", fill=True)

        # print content inside card
        self.set_xy(15, start_y + 5)
        for label, value in items:
            self.set_text_color(80, 79, 75)
            self.cell(50, 6, label)
            self.set_text_color(55, 53, 47)
            self.cell(30, 6, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(3)

    # Notion-style table
    def formatted_table(self,
                        headers: list[str],
                        rows: list[tuple[str, str, str, str]],
                        col_widths: list[int]) -> None:
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

    def detailed_tickets_table(self, tickets: list[dict[str, str]]) -> None:
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
            key = t.get("key", "?")
            summary = t.get("summary", "")
            status = t.get("status", "Default")
            issue_type = t.get("issue_type", "Other")
            priority = t.get("priority", "Medium")
            story_points = str(t.get("story_points", "-"))
            flagged = t.get("flagged", False)
            component = t.get("component", "-")
            category = t.get("category", None)

            # Row box dimensions
            box_x = 10
            box_y = self.get_y()
            w = self.w - 20
            h = 18

            # Category-colored left stripe
            cat_colors = {
                "committed": (217, 241, 208),  # green
                "nice to have": (255, 232, 163),  # yellow
                "maybe": (212, 228, 247),  # blue
                None: (227, 226, 224),  # neutral gray
            }
            stripe_color = cat_colors.get(category, (227, 226, 224))

            self.set_fill_color(*stripe_color)
            self.rect(box_x, box_y, 3, h, style="F")

            # Flagged tickets get a red left border highlight
            if flagged:
                self.set_fill_color(252, 216, 212)
                self.rect(box_x, box_y, 3, h, style="F")

            # Outer row box (subtle)
            self.set_draw_color(230, 230, 230)
            self.rect(box_x, box_y, w, h)

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
            dot_y = self.get_y() + 2
            self.set_fill_color(*dot_color)
            self.ellipse(dot_x, dot_y, 3, 3, style="F")
            self.set_x(dot_x + 6)
            self.cell(10, 5, priority)

            self.ln(7)
            self.set_x(box_x + 6)

            # Summary + Story Points + Component
            self.set_font(FONT_FAMILY, "", 9)
            self.multi_cell(
                w - 12, 4, f"{summary} SP: {story_points}   Component: {component}"
            )

            self.ln(4)


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
    pdf.formatted_table(headers, transformed_rows, col_widths)

    pdf.output("notion_report.pdf")


# -------------------------
# Charting subsystem (matplotlib, in-memory PNGs)
# -------------------------


# Notion-like palette for charts (normalized for matplotlib)
NOTION_CHART_COLORS = [
    (155 / 255, 207 / 255, 87 / 255),  # green
    (246 / 255, 199 / 255, 68 / 255),  # yellow
    (108 / 255, 155 / 255, 245 / 255),  # blue
    (221 / 255, 148 / 255, 255 / 255),  # purple
    (255 / 255, 170 / 255, 153 / 255),  # coral
    (181 / 255, 181 / 255, 181 / 255),  # gray
]


def build_pie_chart_bytes(title: str,
                          data_pairs: list[tuple[str, float]],
                          size_inch: float = 2.4) -> BytesIO:  # smaller charts
    """Return a PNG image as bytes for a pie chart (non‑donut, full pie).(title, data_pairs, size_inch=3):

    data_pairs: list of (label, value)
    size_inch: figure size in inches (square)
    """
    labels = [p[0] for p in data_pairs]
    sizes = [float(p[1]) for p in data_pairs]

    # Clean small or zero slices
    total = sum(sizes)
    if total == 0:
        # create an empty placeholder chart
        fig, ax = plt.subplots(figsize=(size_inch, size_inch))
        ax.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=12)
        ax.axis("off")
    else:
        fig, ax = plt.subplots(figsize=(size_inch, size_inch))
        fig.patch.set_facecolor("white")

        colors = NOTION_CHART_COLORS[: len(labels)]

        wedges, _ = ax.pie(
            sizes,
            colors=colors,
            startangle=90,
            counterclock=False,  # full pie (no donut)
        )

        # Put numeric labels inside slices when large enough, otherwise external
        for i, w in enumerate(wedges):
            ang = (w.theta2 + w.theta1) / 2.0
            x = np.cos(np.deg2rad(ang))
            y = np.sin(np.deg2rad(ang))
            pct = sizes[i]
            # place label nearer to center
            ax.text(x * 0.6, y * 0.6, f"{pct}", ha="center", va="center", fontsize=9)

        # Title
        # ax.set_title(title, fontsize=12, pad=6)
        # ax.axis("equal")

    buf = BytesIO()
    plt.savefig(
        buf, format="png", dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor()
    )
    plt.close(fig)
    buf.seek(0)
    return buf


# Attach staticmethod to class
NotionPDF.build_pie_chart_bytes = build_pie_chart_bytes


def add_pie_chart(self: NotionPDF,
                  title: str,
                  data_pairs: list[tuple[str, int]],
                  max_width_mm: float = 70,
                  size_inch: float = 2.4,
                  caption: Optional[str] = None,
                  legend: bool = True) -> None:
    """Generate a pie chart in-memory and insert it into the PDF.

    - max_width_mm: how wide the chart should be on the page (mm)
    - size_inch: matplotlib figure size in inches (controls resolution)
    - caption: optional text shown below the chart
    """
    img_buf = self.build_pie_chart_bytes(title, data_pairs, size_inch=size_inch)

    # X/Y position calculations
    x = self.get_x()
    y = self.get_y()

    try:
        # fpdf2 supports file-like objects for image; try to use BytesIO directly
        self.image(img_buf, x=x, y=y, w=max_width_mm)
    except Exception:
        # Fallback: write to a temporary file and use that (rare environments)
        import tempfile

        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.write(img_buf.getbuffer())
        tmp.flush()
        tmp.close()
        self.image(tmp.name, x=x, y=y, w=max_width_mm)

    # move cursor to the right of the image
    self.set_y(y)
    self.set_x(x + max_width_mm + 0)  # caller can add spacing

    # Legend on the right side
    legend_x = x + max_width_mm + 4
    legend_y = y + 8

    if legend:
        self.set_font(FONT_FAMILY, "", 9)
        legend_colors = NOTION_CHART_COLORS
        for idx, (label, val) in enumerate(data_pairs):
            r, g, b = [int(c * 255) for c in legend_colors[idx]]

            self.set_xy(legend_x, legend_y)
            self.set_fill_color(r, g, b)
            self.ellipse(self.get_x(), self.get_y() + 1, 3, 3, style="F")

            self.set_x(self.get_x() + 5)
            self.set_text_color(60, 60, 60)
            self.cell(40, 4, f"{label} ({val})", new_x="LMARGIN", new_y="NEXT")
            legend_y += 5

    # Caption under chart (optional)
    if caption:
        self.set_xy(x, y + max_width_mm - 2)
        self.set_font(FONT_FAMILY, "", 9)
        self.set_text_color(90, 90, 90)
        self.cell(max_width_mm, 5, caption, align="C")

    # Move cursor below
    # self.set_y(y + max_width_mm + 8)
    # self.set_x(self.l_margin) # reset X to original and move down by image height
    # img_h_mm = max_width_mm  # approximate for square charts
    # self.set_xy(x, y + img_h_mm + 2)
    # if caption:
    #     self.set_font(FONT_FAMILY, "", 9)
    #     self.set_text_color(90, 90, 90)
    #     self.cell(max_width_mm, 5, caption, align="C")
    #     self.ln(5)

    # Legend below chart
    # if legend:
    #     self.set_font(FONT_FAMILY, "", 9)
    #     legend_colors = NOTION_CHART_COLORS
    #     for idx, (label, val) in enumerate(data_pairs):
    #         if idx == len(data_pairs):
    #             break
    #         r, g, b = [int(c*255) for c in legend_colors[idx]]
    #         self.set_x(x)
    #         # color circle
    #         self.set_fill_color(r, g, b)
    #         self.ellipse(self.get_x(), self.get_y()+1, 3, 3, style="F")
    #         self.set_x(self.get_x() + 5)
    #         self.set_text_color(60, 60, 60)
    #         self.cell(0, 5, f"{label} ({val})", new_x="LMARGIN", new_y="NEXT")

    # move cursor below legend
    self.ln(4)
    self.set_x(self.l_margin)  # reset X to original and move down by image height
    # approximate height from width using square aspect
    img_h_mm = max_width_mm  # approximate for square charts
    self.set_xy(x, y + img_h_mm + 2)
    # if caption:
    #     self.set_font(FONT_FAMILY, "", 9)
    #     self.set_text_color(90, 90, 90)
    #     self.cell(max_width_mm, 6, caption, align="C")


# bind to class
NotionPDF.add_pie_chart = add_pie_chart


def add_multiple_pie_charts(self: NotionPDF,
                            charts: list[tuple[str, list[tuple[str, int]]]],
                            per_row: int = 2,
                            chart_width: float = 50,
                            h_spacing: float = 45,
                            v_spacing: float = 16,
                            size_inch: float = 3
                            ) -> None:
    """Add several pie charts.

    charts: list of (title, data_pairs)
    per_row: how many charts per row
    chart_width: width per chart in mm
    h_spacing, v_spacing: spacing in mm
    """

    x_start = self.get_x()
    y = self.get_y()

    for idx, (title, pairs) in enumerate(charts):
        col = idx % per_row
        if col == 0 and idx != 0:
            # new row
            y = y + chart_width + v_spacing
            x = x_start
            # check for page overflow
            if y + chart_width + v_spacing > self.h - self.b_margin:
                self.add_page()
                y = self.get_y()
        else:
            x = x_start + col * (chart_width + h_spacing)

        self.set_xy(x, y)
        caption = title
        self.add_pie_chart(
            title, pairs, max_width_mm=chart_width, size_inch=size_inch, caption=caption
        )

    # move cursor below the charts
    final_row_count = (len(charts) + per_row - 1) // per_row
    self.set_y(y + final_row_count * (chart_width + v_spacing))
    self.set_x(self.l_margin)


# bind to class
NotionPDF.add_multiple_pie_charts = add_multiple_pie_charts

# -------------------------
# EXAMPLE USAGE (charts)
# -------------------------
if __name__ == "__main__":
    generate_notion_pdf()

    # small demo for charts
    pdf = NotionPDF()
    pdf.add_page()

    charts = [
        (
            "Story Points by Category",
            [("Committed", 12), ("Nice to have", 5), ("Maybe", 2)],
        ),
        (
            "Story Points by Component",
            [("Platform", 20), ("Strategic", 6), ("Infra", 3)],
        ),
        ("Story Points by Priority", [("High", 10), ("Medium", 12), ("Low", 7)]),
    ]

    pdf.add_multiple_pie_charts(charts, per_row=2, chart_width=50, h_spacing=55)
    pdf.output("notion_report_with_charts.pdf")
