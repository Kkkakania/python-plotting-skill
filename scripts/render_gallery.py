#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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


def plot_category_small_multiples() -> plt.Figure:
    labels = ["A", "B", "C", "D"]
    panels = ["site 1", "site 2", "site 3", "site 4"]
    values = np.array(
        [
            [4.8, 6.2, 5.4, 7.1],
            [5.5, 5.9, 6.8, 6.4],
            [6.1, 4.9, 5.8, 7.3],
            [4.6, 5.2, 6.3, 6.9],
        ]
    )
    colors = ["#2455a4", "#2f8f5b", "#b45f06", "#6f4e7c"]

    fig, axes = plt.subplots(2, 2, figsize=(6.8, 4.6), sharey=True)
    x = np.arange(len(labels))
    for ax, panel, row in zip(axes.ravel(), panels, values, strict=True):
        ax.bar(x, row, color=colors, width=0.68)
        ax.set_xticks(x, labels)
        ax.set_ylim(0, 8)
        apply_style(ax, panel)
    axes[0, 0].set_ylabel("Score")
    axes[1, 0].set_ylabel("Score")
    fig.suptitle("Category small multiples", x=0.04, ha="left", fontsize=11, fontweight="bold")
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


def plot_lollipop_ranking() -> plt.Figure:
    labels = np.array(["alpha", "beta", "gamma", "delta", "epsilon", "zeta"])
    values = np.array([73, 61, 88, 54, 79, 67], dtype=float)
    order = np.argsort(values)
    labels = labels[order]
    values = values[order]
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(6.0, 3.9))
    ax.hlines(y, 0, values, color="#b7c4d4", linewidth=2.2)
    ax.scatter(values, y, s=70, color="#2455a4", edgecolor="white", linewidth=0.8, zorder=3)
    for yi, value in zip(y, values, strict=True):
        ax.text(value + 1.4, yi, f"{value:.0f}", va="center", fontsize=8, color="#324052")
    ax.set_yticks(y, labels)
    ax.set_xlim(0, max(values) + 12)
    ax.set_xlabel("Score")
    apply_style(ax, "Lollipop ranking")
    return finish(fig)


def plot_paired_before_after() -> plt.Figure:
    before = np.array([62, 58, 71, 66, 54, 73, 69, 61, 57, 76, 64, 68], dtype=float)
    after = before + np.array([5, 7, 3, 8, 6, 4, 9, 5, 7, 2, 6, 8], dtype=float)

    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    for old, new in zip(before, after, strict=True):
        color = "#2f8f5b" if new >= old else "#bb3e03"
        ax.plot([0, 1], [old, new], color="#9fb1c5", linewidth=1.3, zorder=1)
        ax.scatter([0, 1], [old, new], s=38, color=color, edgecolor="white", linewidth=0.7, zorder=2)
    ax.set_xticks([0, 1], ["before", "after"])
    ax.set_xlim(-0.18, 1.18)
    ax.set_ylabel("Score")
    apply_style(ax, "Paired before/after")
    return finish(fig)


def plot_spectral_density() -> plt.Figure:
    sample_rate = 200.0
    duration = 4.0
    time = np.arange(0, duration, 1 / sample_rate)
    signal = (
        0.9 * np.sin(2 * math.pi * 18 * time)
        + 0.45 * np.sin(2 * math.pi * 42 * time)
        + RNG.normal(0, 0.18, len(time))
    )
    window = np.hanning(len(signal))
    spectrum = np.fft.rfft((signal - signal.mean()) * window)
    frequency = np.fft.rfftfreq(len(signal), d=1 / sample_rate)
    power = (np.abs(spectrum) ** 2) / (sample_rate * np.sum(window**2))
    power_db = 10 * np.log10(np.maximum(power, 1e-10))

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(frequency, power_db, color="#2455a4", linewidth=1.7)
    ax.fill_between(frequency, power_db.min() - 3, power_db, color="#9ecae1", alpha=0.35, linewidth=0)
    ax.set_xlim(0, 80)
    ax.set_ylim(power_db.min() - 3, power_db.max() + 3)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power density (dB)")
    apply_style(ax, "Spectral density")
    return finish(fig)


def plot_residual_convergence() -> plt.Figure:
    iteration = np.arange(1, 61)
    baseline = 1.2 * np.exp(-iteration / 13.0) + 2.8e-3
    accelerated = 1.0 * np.exp(-iteration / 8.0) + 7.5e-4
    damped = 0.85 * np.exp(-iteration / 5.5) + 1.6e-4

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.semilogy(iteration, baseline, color="#2455a4", linewidth=1.9, label="baseline")
    ax.semilogy(iteration, accelerated, color="#2f8f5b", linewidth=1.9, label="accelerated")
    ax.semilogy(iteration, damped, color="#b45f06", linewidth=1.9, label="damped")
    ax.axhline(1e-3, color="#8b1e3f", linewidth=1.0, linestyle="--", label="target")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Relative residual")
    ax.legend(frameon=False, fontsize=8, ncols=4)
    apply_style(ax, "Residual convergence")
    return finish(fig)


def plot_main_inset() -> plt.Figure:
    x = np.linspace(0, 10, 240)
    baseline = 0.18 * x + np.sin(1.25 * x)
    local_event = 0.8 * np.exp(-0.5 * ((x - 5.1) / 0.28) ** 2)
    y = baseline + local_event

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(x, y, color="#2455a4", linewidth=1.9)
    ax.set_xlabel("Distance")
    ax.set_ylabel("Response")
    apply_style(ax, "Main plot with inset")

    inset = ax.inset_axes([0.56, 0.14, 0.36, 0.36])
    inset.plot(x, y, color="#2455a4", linewidth=1.4)
    inset.set_xlim(4.5, 5.7)
    inset.set_ylim(0.85, 2.35)
    inset.set_xticks([4.5, 5.1, 5.7])
    inset.set_yticks([1.0, 1.6, 2.2])
    inset.tick_params(colors="#324052", labelsize=7)
    inset.grid(True, color="#d9dee7", linewidth=0.6, alpha=0.75)
    inset.set_title("local detail", fontsize=8)
    ax.indicate_inset_zoom(inset, edgecolor="#8b1e3f", linewidth=0.8)
    return finish(fig)


def plot_shared_colorbar_panels() -> plt.Figure:
    x = np.linspace(-2.2, 2.2, 36)
    y = np.linspace(-2.2, 2.2, 30)
    xx, yy = np.meshgrid(x, y)
    fields = [
        np.sin(xx) + np.cos(yy),
        np.sin(xx + 0.55) + np.cos(yy - 0.35),
        0.7 * np.sin(1.4 * xx) + np.cos(0.8 * yy),
        np.sin(xx - yy / 2) + 0.35 * np.cos(xx + yy),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(6.2, 4.6), sharex=True, sharey=True)
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(left=0.08, right=0.84, bottom=0.1, top=0.86, wspace=0.16, hspace=0.32)
    vmin = min(float(field.min()) for field in fields)
    vmax = max(float(field.max()) for field in fields)
    image = None
    for idx, (ax, field) in enumerate(zip(axes.ravel(), fields, strict=True), start=1):
        image = ax.imshow(field, cmap="viridis", vmin=vmin, vmax=vmax, origin="lower", aspect="auto")
        ax.set_title(f"case {idx}", loc="left", fontsize=9, fontweight="bold")
        ax.tick_params(colors="#324052", labelsize=7)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
    assert image is not None
    fig.colorbar(image, ax=axes.ravel().tolist(), fraction=0.046, pad=0.04, label="shared scale")
    fig.suptitle("Shared colorbar panels", x=0.04, ha="left", fontsize=11, fontweight="bold")
    return fig


def plot_gantt_timeline() -> plt.Figure:
    tasks = ["scope", "data prep", "analysis", "figures", "review"]
    starts = [dt.date(2026, 1, 5), dt.date(2026, 1, 12), dt.date(2026, 1, 19), dt.date(2026, 1, 29), dt.date(2026, 2, 5)]
    durations = np.array([8, 9, 13, 8, 6])
    colors = ["#2455a4", "#2f8f5b", "#b45f06", "#6f4e7c", "#8b1e3f"]
    y = np.arange(len(tasks))

    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    ax.barh(y, durations, left=mdates.date2num(starts), color=colors, height=0.56)
    ax.set_yticks(y, tasks)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax.set_xlabel("Date")
    ax.set_ylabel("Task")
    apply_style(ax, "Gantt timeline")
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
    {"id": "category_small_multiples", "title": "Category small multiples", "task": "Compare the same categories across several panels.", "risk": "Panel comparisons need the same category order and y-axis scale.", "plot": plot_category_small_multiples},
    {"id": "correlation_matrix", "title": "Correlation matrix", "task": "Summarize pairwise correlations.", "risk": "Correlation signs need domain interpretation.", "plot": plot_correlation_matrix},
    {"id": "lollipop_ranking", "title": "Lollipop ranking", "task": "Rank ordered items without heavy bars.", "risk": "Rankings need uncertainty or sample-size context when values are close.", "plot": plot_lollipop_ranking},
    {"id": "paired_before_after", "title": "Paired before/after", "task": "Show paired change between two conditions.", "risk": "The paired design must be real; do not connect unrelated groups.", "plot": plot_paired_before_after},
    {"id": "spectral_density", "title": "Spectral density", "task": "Show frequency content in a sampled signal.", "risk": "Sampling rate, windowing, and units must be stated.", "plot": plot_spectral_density},
    {"id": "residual_convergence", "title": "Residual convergence", "task": "Show iterative residual decay.", "risk": "Log scales can hide plateaus or stopping-rule problems.", "plot": plot_residual_convergence},
    {"id": "main_inset", "title": "Main plot with inset", "task": "Show a main trend with a magnified local region.", "risk": "Insets can overemphasize small local features.", "plot": plot_main_inset},
    {"id": "shared_colorbar_panels", "title": "Shared colorbar panels", "task": "Compare several heatmaps on one color scale.", "risk": "A shared scale can hide subtle within-panel variation.", "plot": plot_shared_colorbar_panels},
    {"id": "gantt_timeline", "title": "Gantt timeline", "task": "Show tasks on a simple calendar timeline.", "risk": "Timelines can imply false precision when dates are tentative.", "plot": plot_gantt_timeline},
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
    write_manifest(out_dir, formats)


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


def write_manifest(out_dir: Path, formats: list[str]) -> None:
    payload = {
        "schemaVersion": 1,
        "generatedBy": "scripts/render_gallery.py",
        "templateCount": len(TEMPLATES),
        "privateData": False,
        "formats": formats,
        "templates": [
            {
                "id": str(template["id"]),
                "title": str(template["title"]),
                "task": str(template["task"]),
                "risk": str(template["risk"]),
                "outputs": [f"{template['id']}.{fmt}" for fmt in formats],
            }
            for template in TEMPLATES
        ],
    }
    (out_dir / "manifest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_formats(raw: str) -> list[str]:
    allowed = {"png", "svg", "pdf"}
    formats = list(dict.fromkeys(item.strip().lower() for item in raw.split(",") if item.strip()))
    if not formats:
        raise ValueError("--formats must include at least one format")
    bad = sorted(set(formats) - allowed)
    if bad:
        raise ValueError(f"Unsupported format(s): {', '.join(bad)}")
    return formats


def parse_output_dir(raw: str) -> Path:
    if not raw.strip():
        raise ValueError("--out must not be empty")
    return Path(raw)


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

    try:
        out_dir = parse_output_dir(args.out)
        formats = parse_formats(args.formats)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    render(out_dir, formats)
    print(f"Rendered {len(TEMPLATES)} templates to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
