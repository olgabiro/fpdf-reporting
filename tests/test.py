import pytest
from model.style import NotionStyle
from model.ticket import Category, Status, Ticket
from rendering.pdf_generator import PDF

DARK_BACKGROUND = (38, 33, 43)


@pytest.mark.skip(reason="Manually run")
def test():
    style = NotionStyle()
    pdf = PDF(style)

    pdf.add_page()

    pdf.document_header("JIRA Summary Test")

    pdf.document_header("Other header", centered=True)

    pdf.section_title("Overview")
    pdf.summary_card(
        ["Total Tickets: 58", "Completed: 42", "In Progress: 10", "Blocked: 6"],
        width=50,
    )

    pdf.summary_card(
        ["Total Tickets: 58", "Completed: 42", "In Progress: 10", "Blocked: 6"],
        width=50,
    )

    (_, y) = pdf.summary_card(
        ["Total Tickets: 58", "Completed: 42", "In Progress: 10", "Blocked: 6"],
        width=50,
    )

    pdf.set_y(y + 10)

    pdf.styled_table(
        headers=["Key", "Summary", "Status", "Assignee"],
        rows=[
            ("PROJ-101", "Fix login flow", "Done", "Alice"),
            ("PROJ-102", "Add metrics dashboard", "In Progress", "Bob"),
            ("PROJ-103", "Payment gateway issue", "Blocked", "Eve"),
        ],
        col_widths=[20, 80, 30, 30],
    )

    pdf.detailed_tickets_table(
        tickets=[
            Ticket(
                key="PD-123",
                summary="GIS CLM Update",
                status=Status.IN_PROGRESS,
                issue_type="Improvement",
                priority="High",
                story_points=8,
                category=Category.COMMITTED,
            ),
            Ticket(
                key="PD-2134",
                summary="Postgres performance issues",
                status=Status.ON_HOLD,
                issue_type="Bug",
                priority="Low",
                story_points=13,
                flagged=True,
                category="Nice to have",
            ),
            Ticket(
                key="PD-34",
                summary="Angular upgrade",
                status=Status.READY_TO_MERGE,
                issue_type="Improvement",
                story_points=13,
                category="Maybe",
            ),
        ]
    )

    pdf.add_page()
    pdf.bar_chart([10, 5, 8, 3, 2, 7, 1])
    pdf.output("./output/test.pdf")
