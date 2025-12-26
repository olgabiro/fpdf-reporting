from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Optional


class Category(StrEnum):
    COMMITTED = "Committed"
    NICE_TO_HAVE = "Nice to have"
    MAYBE = "Maybe"


class Status(StrEnum):
    READY_FOR_DEV = "Ready for dev"
    ON_HOLD = "On Hold"
    IN_PROGRESS = "In progress"
    READY_FOR_QA = "Ready for QA"
    LOCAL_TESTING = "Local testing"
    READY_TO_MERGE = "Ready to merge"
    OTHER = "Other"


@dataclass(slots=True)
class Ticket:
    key: str
    summary: str
    status: Status
    issue_type: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    flagged: bool = False
    priority: Optional[str] = None
    story_points: Optional[int] = None
    tester_story_points: Optional[float] = None
    component: Optional[str] = None
    developer: Optional[str] = None
    assignee: Optional[str] = None
    category: Optional[Category] = None
