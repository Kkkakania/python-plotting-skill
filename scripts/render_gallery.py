#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "docs" / "gallery"
RNG = np.random.default_rng(20260620)


def apply_style(ax: plt.Axes, title: str) -> None:
    ax.set_title(title, loc="left", fontsize=11, fontweight="bold")
    ax.grid(True, color="#d9dee7", linewidth=0.7, alpha=0.75)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#8090a0")
    ax.spines["bottom"].set_color("#8090a0")
    ax.tick_params(colors="#324052", labelsize=8)


def finish(fig: plt.Figure) -> plt.Figure:
    fig.patch.set_facecolor("white")
    fig.tight_layout(pad=1.4)
    return fig


def plot_line_trend() -> plt.Figure:
    x = np.arange(1, 25)
    y = 0.35 * x + np.sin(x / 2.7) + RNG.normal(0, 0.22, len(x))
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(x, y, color="#2455a4", linewidth=2.1)
    ax.scatter(x[-1], y[-1], color="#c23b22", zorder=3)
    ax.set_xlabel("Month")
    ax.set_ylabel("Index")
    apply_style(ax, "Line trend")
    return finish(fig)


def plot_multi_line_comparison() -> plt.Figure:
    x = np.linspace(0, 10, 80)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    colors = ["#2455a4", "#2f8f5b", "#b45f06"]
    for idx, phase in enumerate([0.0, 0.8, 1.6]):
        y = np.sin(x + phase) + idx * 0.35 + 0.06 * x
        ax.plot(x, y, label=f"method {idx + 1}", linewidth=1.8, color=colors[idx])
    ax.legend(frameon=False, fontsize=8, ncols=3)
    ax.set_xlabel("Step")
    ax.set_ylabel("Response")
    apply_style(ax, "Multi-line comparison")
    return finish(fig)


def plot_scatter_relationship() -> plt.Figure:
    x = RNG.normal(0, 1, 140)
    y = 0.65 * x + RNG.normal(0, 0.55, len(x))
    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    ax.scatter(x, y, s=28, alpha=0.74, color="#286c8e", edgecolor="white", linewidth=0.4)
    ax.set_xlabel("Predictor")
    ax.set_ylabel("Response")
    apply_style(ax, "Scatter relationship")
    return finish(fig)


def plot_regression_scatter() -> plt.Figure:
    x = np.linspace(0, 8, 120)
    y = 1.2 + 0.48 * x + RNG.normal(0, 0.55, len(x))
    coeff = np.polyfit(x, y, deg=1)
    fit = np.polyval(coeff, x)
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    ax.scatter(x, y, s=22, color="#6777a8", alpha=0.68)
    ax.plot(x, fit, color="#bb3e03", linewidth=2.0, label="linear fit")
    ax.legend(frameon=False, fontsize=8)
    ax.set_xlabel("Input")
    ax.set_ylabel("Output")
    apply_style(ax, "Regression scatter")
    return finish(fig)


def plot_confidence_band() -> plt.Figure:
    x = np.linspace(0, 12, 80)
    mean = 0.2 * x + np.sin(x / 1.9)
    band = 0.35 + 0.04 * np.sqrt(x + 1)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.fill_between(x, mean - band, mean + band, color="#9ecae1", alpha=0.55, linewidth=0)
    ax.plot(x, mean, color="#2455a4", linewidth=2.1)
    ax.set_xlabel("Time")
    ax.set_ylabel("Mean response")
    apply_style(ax, "Confidence band")
    return finish(fig)


def plot_grouped_bar() -> plt.Figure:
    labels = ["A", "B", "C", "D"]
    x = np.arange(len(labels))
    width = 0.24
    values = np.array([[5.1, 6.0, 6.8, 7.4], [4.7, 5.8, 6.1, 6.9], [5.5, 6.3, 7.0, 7.8]])
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    for idx, color in enumerate(["#2455a4", "#2f8f5b", "#b45f06"]):
        ax.bar(x + (idx - 1) * width, values[idx], width=width, label=f"group {idx + 1}", color=color)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Score")
    ax.legend(frameon=False, fontsize=8, ncols=3)
    apply_style(ax, "Grouped bar")
    return finish(fig)


def plot_heatmap_matrix() -> plt.Figure:
    base = np.outer(np.linspace(-1, 1, 9), np.linspace(1, -1, 9))
    matrix = base + RNG.normal(0, 0.12, base.shape)
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    image = ax.imshow(matrix, cmap="viridis", aspect="equal")
    ax.set_xticks(range(0, 9, 2))
    ax.set_yticks(range(0, 9, 2))
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_title("Heatmap matrix", loc="left", fontsize=11, fontweight="bold")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    return finish(fig)


def plot_density_scatter() -> plt.Figure:
    x = np.concatenate([RNG.normal(-0.7, 0.45, 220), RNG.normal(0.9, 0.35, 170)])
    y = 0.55 * x + RNG.normal(0, 0.35, len(x))
    counts, x_edges, y_edges = np.histogram2d(x, y, bins=34)
    xi = np.clip(np.searchsorted(x_edges, x, side="right") - 1, 0, counts.shape[0] - 1)
    yi = np.clip(np.searchsorted(y_edges, y, side="right") - 1, 0, counts.shape[1] - 1)
    density = counts[xi, yi]
    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    sc = ax.scatter(x, y, c=density, s=24, cmap="magma", alpha=0.75, edgecolor="none")
    fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04, label="local count")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    apply_style(ax, "Density scatter")
    return finish(fig)


def plot_box_jitter() -> plt.Figure:
    groups = [RNG.normal(5.0, 0.8, 45), RNG.normal(5.8, 0.65, 45), RNG.normal(6.3, 0.9, 45)]
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    ax.boxplot(groups, widths=0.45, patch_artist=True, boxprops={"facecolor": "#dce9f6"})
    for idx, values in enumerate(groups, start=1):
        jitter = RNG.normal(0, 0.045, len(values))
        ax.scatter(np.full(len(values), idx) + jitter, values, s=18, alpha=0.65, color="#2455a4")
    ax.set_xticks([1, 2, 3], ["baseline", "mid", "final"])
    ax.set_ylabel("Value")
    apply_style(ax, "Box plot with jitter")
    return finish(fig)


def plot_violin_plot() -> plt.Figure:
    groups = [RNG.gamma(4.2, 0.8, 90), RNG.gamma(5.0, 0.7, 90), RNG.gamma(4.7, 0.9, 90)]
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    parts = ax.violinplot(groups, showmeans=False, showmedians=True)
    for body in parts["bodies"]:
        body.set_facecolor("#84a9c0")
        body.set_edgecolor("#445c6d")
        body.set_alpha(0.75)
    parts["cmedians"].set_color("#9b2226")
    ax.set_xticks([1, 2, 3], ["A", "B", "C"])
    ax.set_ylabel("Distribution")
    apply_style(ax, "Violin plot")
    return finish(fig)


def plot_small_multiples() -> plt.Figure:
    x = np.linspace(0, 8, 60)
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.4), sharex=True, sharey=True)
    for idx, ax in enumerate(axes.ravel()):
        y = np.sin(x * (0.65 + idx * 0.08)) + idx * 0.12 + RNG.normal(0, 0.08, len(x))
        ax.plot(x, y, color="#2455a4", linewidth=1.5)
        apply_style(ax, f"panel {idx + 1}")
    fig.suptitle("Small multiples", x=0.04, ha="left", fontsize=11, fontweight="bold")
    return finish(fig)


def plot_correlation_matrix() -> plt.Figure:
    base = RNG.normal(0, 1, (160, 5))
    data = np.column_stack(
        [
            base[:, 0],
            0.65 * base[:, 0] + RNG.normal(0, 0.55, 160),
            base[:, 2],
            -0.45 * base[:, 2] + RNG.normal(0, 0.7, 160),
            0.3 * base[:, 0] + 0.25 * base[:, 2] + RNG.normal(0, 0.8, 160),
        ]
    )
    corr = np.corrcoef(data, rowvar=False)
    fig, ax = plt.subplots(figsize=(4.8, 4.3))
    image = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    labels = ["x1", "x2", "x3", "x4", "x5"]
    ax.set_xticks(range(5), labels)
    ax.set_yticks(range(5), labels)
    for i in range(5):
        for j in range(5):
            ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", fontsize=8, color="#222")
    ax.set_title("Correlation matrix", loc="left", fontsize=11, fontweight="bold")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    return finish(fig)


TEMPLATES: list[dict[str, str | Callable[[], plt.Figure]]] = [
    {"id": "line_trend", "title": "Line trend", "task": "Show one trend over time.", "risk": "Can hide seasonal or subgroup patterns.", "plot": plot_line_trend},
    {"id": "multi_line_comparison", "title": "Multi-line comparison", "task": "Compare several series on one axis.", "risk": "Too many lines become unreadable.", "plot": plot_multi_line_comparison},
    {"id": "scatter_relationship", "title": "Scatter relationship", "task": "Show relation between two numeric variables.", "risk": "Correlation does not prove causality.", "plot": plot_scatter_relationship},
    {"id": "regression_scatter", "title": "Regression scatter", "task": "Show x-y relation with a fitted trend.", "risk": "A straight fit can hide nonlinear structure.", "plot": plot_regression_scatter},
    {"id": "confidence_band", "title": "Confidence band", "task": "Show mean and uncertainty.", "risk": "Band meaning must be defined.", "plot": plot_confidence_band},
    {"id": "grouped_bar", "title": "Grouped bar", "task": "Compare categories across groups.", "risk": "Bars hide within-group variation.", "plot": plot_grouped_bar},
    {"id": "heatmap_matrix", "title": "Heatmap matrix", "task": "Show matrix or grid values.", "risk": "Color scale choices can exaggerate small changes.", "plot": plot_heatmap_matrix},
    {"id": "density_scatter", "title": "Density scatter", "task": "Show dense x-y points.", "risk": "Binning can create artificial clusters.", "plot": plot_density_scatter},
    {"id": "box_jitter", "title": "Box plot with jitter", "task": "Compare distributions and observations.", "risk": "Small samples need visible points.", "plot": plot_box_jitter},
    {"id": "violin_plot", "title": "Violin plot", "task": "Compare distribution shapes.", "risk": "Kernel smoothing can imply unsupported detail.", "plot": plot_violin_plot},
    {"id": "small_multiples", "title": "Small multiples", "task": "Repeat comparable panels.", "risk": "Panels need shared scales to compare fairly.", "plot": plot_small_multiples},
    {"id": "correlation_matrix", "title": "Correlation matrix", "task": "Summarize pairwise correlations.", "risk": "Correlation signs need domain interpretation.", "plot": plot_correlation_matrix},
]


def render(out_dir: Path, formats: list[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for template in TEMPLATES:
        fig = template["plot"]()
        assert isinstance(fig, plt.Figure)
        for fmt in formats:
            target = out_dir / f"{template['id']}.{fmt}"
            fig.savefig(target, dpi=160, metadata={"Creator": "python-plotting-skill clean-room renderer"})
        plt.close(fig)
    write_index(out_dir, formats)


def write_index(out_dir: Path, formats: list[str]) -> None:
    lines = [
        "# Gallery",
        "",
        "Generated from synthetic data by `scripts/render_gallery.py`.",
        "",
        "| Template | Task | Risk | Preview |",
        "|---|---|---|---|",
    ]
    preview_ext = "png" if "png" in formats else formats[0]
    for template in TEMPLATES:
        lines.append(
            f"| `{template['id']}` | {template['task']} | {template['risk']} | ![{template['title']}]({template['id']}.{preview_ext}) |"
        )
    (out_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    provenance = [
        "# Gallery Provenance",
        "",
        "- Data: deterministic synthetic arrays generated inside `scripts/render_gallery.py`.",
        "- Seed: 20260620.",
        "- Private data: none.",
        "- External images: none.",
    ]
    (out_dir / "provenance.md").write_text("\n".join(provenance) + "\n", encoding="utf-8")


def parse_formats(raw: str) -> list[str]:
    allowed = {"png", "svg", "pdf"}
    formats = [item.strip().lower() for item in raw.split(",") if item.strip()]
    bad = sorted(set(formats) - allowed)
    if bad:
        raise SystemExit(f"Unsupported format(s): {', '.join(bad)}")
    return formats or ["png", "svg"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Render clean-room Python plotting gallery examples.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output directory.")
    parser.add_argument("--formats", default="png,svg", help="Comma-separated formats: png,svg,pdf.")
    parser.add_argument("--list", action="store_true", help="List template ids and exit.")
    args = parser.parse_args()

    if args.list:
        for template in TEMPLATES:
            print(f"{template['id']}: {template['task']}")
        return 0

    render(Path(args.out), parse_formats(args.formats))
    print(f"Rendered {len(TEMPLATES)} templates to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
