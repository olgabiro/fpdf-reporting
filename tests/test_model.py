import pytest

from model.ticket import Status, Ticket


@pytest.fixture
def ticket():
    return Ticket(
        key="PD-1234",
        summary="Test ticket",
        status=Status.IN_PROGRESS,
        issue_type="Bug",
    )


def test_ticket_creation(ticket):
    assert ticket.key == "PD-1234"
    assert ticket.summary == "Test ticket"
    assert ticket.status == Status.IN_PROGRESS
