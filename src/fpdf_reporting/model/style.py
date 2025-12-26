from typing import Optional, Tuple

from fpdf_reporting.model.ticket import Category, Status


class Style:
    category_colors: dict[Optional[Category], Tuple[int, int, int]]
    status_colors: dict[Status, Tuple[int, int, int]]
    chart_colors: list[Tuple[int, int, int]]
    card_background: Tuple[int, int, int]
    header_background: Tuple[int, int, int]
    table_header_color: Tuple[int, int, int]
    table_row_colors: list[Tuple[int, int, int]]
    font_color: Tuple[int, int, int]
    section_title_color: Tuple[int, int, int]
    card_details_color: Tuple[int, int, int]
    border_color: Tuple[int, int, int] = (230, 230, 230)


class NotionStyle(Style):
    category_colors: dict[Optional[Category], Tuple[int, int, int]] = {
        Category.COMMITTED: (217, 241, 208),
        Category.NICE_TO_HAVE: (255, 232, 163),
        Category.MAYBE: (212, 228, 247),
        None: (227, 226, 224),
    }
    status_colors: dict[Status, Tuple[int, int, int]] = {
        Status.READY_FOR_DEV: (217, 241, 208),  # green
        Status.ON_HOLD: (255, 232, 163),  # yellow
        Status.IN_PROGRESS: (252, 216, 212),  # red
        Status.READY_FOR_QA: (212, 228, 247),  # blue
        Status.LOCAL_TESTING: (212, 228, 247),  # blue
        Status.READY_TO_MERGE: (227, 226, 224),  # neutral gray
        Status.OTHER: (227, 226, 224),  # neutral gray
    }
    chart_colors: list[Tuple[int, int, int]] = [
        (155, 207, 87),  # green
        (246, 199, 68),  # yellow
        (108, 155, 245),  # blue
        (221, 148, 255),  # purple
        (255, 170, 153),  # coral
        (181, 181, 181),  # gray
    ]
    card_background: Tuple[int, int, int] = (255, 238, 189)
    header_background: Tuple[int, int, int] = (247, 246, 243)
    table_header_color: Tuple[int, int, int] = (243, 242, 239)
    table_row_colors: list[Tuple[int, int, int]] = [(255, 255, 255), (250, 249, 247)]
    font_color: Tuple[int, int, int] = (55, 53, 47)
    section_title_color: Tuple[int, int, int] = (55, 53, 47)
    card_details_color: Tuple[int, int, int] = (80, 79, 75)
