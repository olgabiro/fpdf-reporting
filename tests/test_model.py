import pytest

from fpdf_reporting.model.report_data import ReportData
from fpdf_reporting.model.ticket import Status, Ticket


@pytest.fixture
def ticket():
    return Ticket(
        key="PD-1234",
        summary="Test ticket",
        status=Status.IN_PROGRESS,
        issue_type="Bug",
    )


@pytest.fixture
def report_data(ticket: Ticket):
    return ReportData([ticket])


def test_ticket_creation(ticket):
    assert ticket.key == "PD-1234"
    assert ticket.summary == "Test ticket"
    assert ticket.status == Status.IN_PROGRESS


def test_report_data_creation(report_data: ReportData):
    assert len(report_data.not_delivered) == 1
    assert report_data.story_points_by_status == {}
    assert report_data.story_points_by_category == {}
    assert report_data.story_points_by_component == {}
    assert report_data.story_points_by_priority == {}
    assert report_data.story_points_by_issue_type == {}
