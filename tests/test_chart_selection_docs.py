from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_chart_selection_mentions_private_data_boundary():
    text = (ROOT / "docs" / "chart-selection.md").read_text(encoding="utf-8").lower()

    assert "private data" in text
    assert "synthetic sample" in text
