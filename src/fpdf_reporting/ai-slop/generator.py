from fpdf import FPDF, XPos, YPos


def get_data() -> list[tuple[str, str, str, str]]:
    return [
        ("PROJ-101", "Fix login flow", "Done", "Alice"),
        ("PROJ-102", "Add metrics dashboard", "In Progress", "Bob"),
        ("PROJ-103", "Payment gateway issue", "Blocked", "Eve"),
    ]


def get_summary_data() -> list[tuple[str, str]]:
    return [
        ("Total Tickets", "58"),
        ("Completed", "42"),
        ("In Progress", "10"),
        ("Blocked", "6"),
    ]


STRIPE_DARK = (10, 37, 64)
STRIPE_LIGHT_BG = (246, 249, 252)
STRIPE_GRAY_TEXT = (66, 84, 102)
STRIPE_HEADER_BG = (230, 236, 244)
STRIPE_ACCENT = (99, 91, 255)
STRIPE_ROW_ALT = (242, 245, 252)


def generate_minimalist() -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)

    pdf.set_fill_color(45, 62, 80)  # dark blue-gray
    pdf.set_text_color(255, 255, 255)
    pdf.cell(
        0,
        20,
        "Sprint 42 - JIRA Report",
        align="C",
        fill=True,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(45, 62, 80)
    pdf.cell(0, 10, "Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 10)
    for label, value in get_summary_data():
        pdf.set_text_color(80, 80, 80)
        pdf.cell(50, 8, label)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(30, 8, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(243, 246, 250)  # light-gray header background
    pdf.set_text_color(45, 62, 80)

    col_widths = [20, 80, 30, 30]
    headers = ["Key", "Summary", "Status", "Assignee"]

    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 10, h, border="B", fill=True)
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 9)
    fill_colors = [(255, 255, 255), (247, 249, 252)]
    row_index = 0

    for row in get_data():
        pdf.set_fill_color(*fill_colors[row_index % 2])
        for i, cell in enumerate(row):
            pdf.cell(col_widths[i], 8, cell, border="B", fill=True)
        pdf.ln(8)
        row_index += 1

    pdf.output("./output/report.pdf")


def generate_stripe_style() -> None:
    pdf = FPDF()
    pdf.add_page()

    # --- Stripe header bar ---
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_fill_color(10, 37, 64)  # deep navy
    pdf.set_text_color(255, 255, 255)
    pdf.cell(
        0,
        20,
        "Sprint 42 - JIRA Report",
        align="C",
        fill=True,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    pdf.ln(8)

    # --- Section title ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(10, 37, 64)
    pdf.cell(0, 10, "Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- Summary rows ---
    pdf.set_font("Helvetica", "", 10)
    for label, value in get_summary_data():
        pdf.set_text_color(66, 84, 102)  # Stripe gray text
        pdf.cell(50, 8, label)
        pdf.set_text_color(99, 91, 255)  # accent color
        pdf.cell(30, 8, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)

    # --- Table Header ---
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(230, 236, 244)  # soft bluish-gray
    pdf.set_text_color(10, 37, 64)

    col_widths = [20, 80, 30, 30]
    headers = ["Key", "Summary", "Status", "Assignee"]

    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 10, h, border="B", fill=True)
    pdf.ln(10)

    # --- Table Rows ---
    pdf.set_font("Helvetica", "", 9)
    row_colors = [
        (255, 255, 255),  # white
        (242, 245, 252),  # subtle stripe tint
    ]
    row_index = 0

    for row in get_data():
        pdf.set_fill_color(*row_colors[row_index % 2])
        for i, cell in enumerate(row):
            pdf.cell(col_widths[i], 8, cell, border="B", fill=True)
        pdf.ln(8)
        row_index += 1

    pdf.output("./output/report_stripe.pdf")


def generate_notion_style() -> None:
    pdf = FPDF()
    pdf.add_page()

    # --- Notion-style header block ---
    pdf.set_fill_color(247, 246, 243)  # warm light gray
    pdf.set_text_color(55, 53, 47)  # Notion dark gray
    pdf.set_font("Helvetica", "B", 20)
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

    # --- Section heading ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(55, 53, 47)
    pdf.cell(0, 10, "Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # --- Summary content ---
    pdf.set_font("Helvetica", "", 10)
    for label, value in get_summary_data():
        pdf.set_text_color(80, 79, 75)  # soft gray text
        pdf.cell(50, 8, label)
        pdf.set_text_color(55, 53, 47)
        pdf.cell(30, 8, value, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)

    # --- Table header (Notion-style block) ---
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(55, 53, 47)
    pdf.set_fill_color(243, 242, 239)  # slightly darker warm gray than header block

    col_widths = [20, 80, 30, 30]
    headers = ["Key", "Summary", "Status", "Assignee"]

    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 10, h, border="B", fill=True)
    pdf.ln(10)

    # --- Table rows ---
    pdf.set_font("Helvetica", "", 9)

    # Notion-like alternating row colors (just barely noticeable)
    row_colors = [
        (255, 255, 255),  # pure white
        (250, 249, 247),  # faint warm beige tint
    ]

    row_index = 0
    for row in get_data():
        pdf.set_fill_color(*row_colors[row_index % 2])
        pdf.set_text_color(55, 53, 47)

        for i, cell in enumerate(row):
            pdf.cell(col_widths[i], 8, cell, border="B", fill=True)

        pdf.ln(8)
        row_index += 1

    pdf.output("./output/report_notion.pdf")


if __name__ == "__main__":
    generate_minimalist()
    generate_stripe_style()
    generate_notion_style()
