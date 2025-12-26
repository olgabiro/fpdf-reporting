import pytest
from model.style import NotionStyle
from rendering.graphs import build_pie_chart_bytes
from rendering.pdf_generator import PDF


@pytest.fixture
def pdf() -> PDF:
    pdf = PDF(NotionStyle())
    pdf.add_page()
    return pdf


@pytest.fixture
def data() -> dict[str, float]:
    return {
        "one": 12,
        "two": 15,
        "zero": 0,
        "three": 30,
        "four": 55,
        "five": 100,
    }


@pytest.mark.skip(reason="Run manually")
def test_basic_components(pdf: PDF):
    pdf.document_header("TEST - Basic Header")
    pdf.section_title("TEST - Basic Section")
    pdf.summary_card(["Basic Card", "Line No 2", "Line No 3"])
    pdf.output("./output/basic-components.pdf")


@pytest.mark.skip(reason="Run manually")
def test_graphs(pdf: PDF, data: dict[str, float]):
    pdf.document_header("TEST - Graphs", centered=True)
    graph_size = 40

    # building a simple graph
    values = list(data.values())
    chart_bytes = build_pie_chart_bytes(values, size=graph_size)
    pdf.image(chart_bytes, pdf.get_x(), pdf.get_y(), w=graph_size)

    pdf.output("./output/graphs.pdf")


def test_graph_with_no_data_returns_none():
    assert build_pie_chart_bytes([0, 0, 0]) is None
