from io import BytesIO
from typing import Optional

from matplotlib import pyplot as plt

NOTION_CHART_COLORS = [
    (155 / 255, 207 / 255, 87 / 255),  # green
    (246 / 255, 199 / 255, 68 / 255),  # yellow
    (108 / 255, 155 / 255, 245 / 255),  # blue
    (221 / 255, 148 / 255, 255 / 255),  # purple
    (255 / 255, 170 / 255, 153 / 255),  # coral
    (181 / 255, 181 / 255, 181 / 255),  # gray
]


def build_pie_chart_bytes(values: list[float], size: float = 35) -> Optional[BytesIO]:
    """
    Return a PNG image as bytes for a pie chart.
    :param values: The values to plot
    :param size: The size of the chart in mm
    :return: the bytes of the chart or None if there are no values
    """

    size_inch = size / 25.4

    if sum(values) == 0:
        return None

    fig, ax = plt.subplots(figsize=(size_inch, size_inch))
    colors = NOTION_CHART_COLORS[: len(values)]
    ax.pie(values, colors=colors)

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=200, bbox_inches="tight", transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf
