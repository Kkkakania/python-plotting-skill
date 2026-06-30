---
name: python-plotting-skill
description: Use when Codex needs to choose, generate, review, or export Python scientific figures with Matplotlib from described data, tables, arrays, CSV-like structures, or synthetic examples; use for chart selection, runnable plotting scripts, PNG/SVG export, and figure limitation notes.
---

# Python Plotting Skill

Use this skill for Python scientific figures when the user wants a static,
reproducible plot rather than an interactive dashboard.

## Workflow

1. Identify the communication task: trend, comparison, relationship,
   distribution, matrix, uncertainty, or repeated panels.
2. Inspect the data shape. If the data is private, ask for a small synthetic
   sample with the same columns and rough ranges.
3. Choose a template from `scripts/render_gallery.py`.
4. Generate a runnable Matplotlib script with fixed seeds for examples.
5. Export PNG and SVG unless the user asks otherwise.
6. Explain what the chart can show and what it cannot prove.
7. Before public use, run `bash scripts/release_check.sh` in the repository or
   an equivalent privacy/provenance check.

## Template map

- `line_trend`: one ordered series.
- `multi_line_comparison`: several series on the same x axis.
- `scatter_relationship`: two numeric variables.
- `regression_scatter`: x-y relation with a simple fitted line.
- `confidence_band`: mean and uncertainty band.
- `grouped_bar`: grouped categorical comparison.
- `heatmap_matrix`: matrix or grid values.
- `density_scatter`: dense scatter with point density coloring.
- `box_jitter`: distribution plus observations.
- `violin_plot`: distribution shape by group.
- `small_multiples`: repeated panels.
- `category_small_multiples`: repeated category panels.
- `correlation_matrix`: pairwise correlations.
- `lollipop_ranking`: sorted item rankings.
- `paired_before_after`: paired changes between two conditions.
- `spectral_density`: frequency content for sampled signals.

## Boundaries

Do not copy private data, paper figures, local paths, unclear snippets, or
third-party gallery assets into generated examples. Use synthetic data when the
goal is to demonstrate a visual pattern.

For diagrams, use `scientific-diagram-skill`. For MATLAB render workflows, use
`matlab-plotting-skill`.
