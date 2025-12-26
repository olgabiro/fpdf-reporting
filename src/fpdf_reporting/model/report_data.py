from fpdf_reporting.model.ticket import Category, Ticket


class ReportData:
    not_delivered: list[Ticket]
    story_points_by_category: dict[Category, int] = {}
    story_points_by_status: dict[str, int] = {}
    story_points_by_component: dict[str, int] = {}
    story_points_by_priority: dict[str, int] = {}
    story_points_by_issue_type: dict[str, int] = {}

    def __init__(self, not_delivered: list[Ticket]) -> None:
        self.not_delivered = not_delivered
