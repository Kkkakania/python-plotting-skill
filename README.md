# Python Plotting Skill

[English](README.md) | [简体中文](README.zh-CN.md)

[![Quality](https://github.com/Kkkakania/python-plotting-skill/actions/workflows/quality.yml/badge.svg)](https://github.com/Kkkakania/python-plotting-skill/actions/workflows/quality.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

`python-plotting-skill` is a small Codex skill for choosing and generating
Python scientific figures from clean, reproducible scripts.

It is the Python sibling of the MATLAB plotting and scientific diagram skills:

- [`matlab-plotting-skill`](https://github.com/Kkkakania/matlab-plotting-skill)
  covers MATLAB data-to-figure workflows.
- [`scientific-diagram-skill`](https://github.com/Kkkakania/scientific-diagram-skill)
  covers Mermaid and draw.io research diagrams.
- [`matlab-scientific-figures`](https://github.com/Kkkakania/matlab-scientific-figures)
  remains the MATLAB gallery and API evidence surface.

This repository starts deliberately small. The current main branch contains 20 Matplotlib templates,
synthetic data, a gallery renderer, provenance notes, and a quality gate. It
does not claim broad adoption, downloads, or external endorsement.

## Quick start

```bash
python -m pip install -e ".[test]"
python scripts/render_gallery.py --out docs/gallery --formats png,svg
bash scripts/release_check.sh
```

The renderer writes deterministic PNG and SVG outputs. It does not read private
data by default.

## Gallery preview

These examples are generated from synthetic data with a fixed seed. They are
meant to show chart structure, not real research results.

<table>
  <tr>
    <td><img src="docs/gallery/line_trend.png" width="220" alt="Line trend"><br>Line trend</td>
    <td><img src="docs/gallery/confidence_band.png" width="220" alt="Confidence band"><br>Confidence band</td>
  </tr>
  <tr>
    <td><img src="docs/gallery/heatmap_matrix.png" width="220" alt="Heatmap matrix"><br>Heatmap matrix</td>
    <td><img src="docs/gallery/small_multiples.png" width="220" alt="Small multiples"><br>Small multiples</td>
  </tr>
</table>

## Template set

| Template | Good for |
|---|---|
| `line_trend` | single time trend |
| `multi_line_comparison` | comparing several series |
| `scatter_relationship` | relationship between two numeric variables |
| `regression_scatter` | relationship plus a simple fitted trend |
| `confidence_band` | mean with uncertainty band |
| `grouped_bar` | category-by-group comparison |
| `heatmap_matrix` | matrix or grid values |
| `density_scatter` | dense x-y points |
| `box_jitter` | distribution plus observations |
| `violin_plot` | distribution shape by group |
| `small_multiples` | repeated panels on one scale |
| `category_small_multiples` | same categories compared across panels |
| `correlation_matrix` | compact correlation overview |
| `lollipop_ranking` | sorted item ranking without heavy bars |
| `paired_before_after` | paired change between two conditions |
| `spectral_density` | frequency content of a sampled signal |
| `residual_convergence` | iterative solver or simulation residual decay |
| `main_inset` | main trend with a magnified local region |
| `shared_colorbar_panels` | several heatmaps on one color scale |
| `gantt_timeline` | simple task timeline |

## Skill install

Copy or symlink `skills/python-plotting-skill` into your Codex skills directory.
Then ask for tasks like:

```text
Use Python to choose a clean figure for this table.
Generate a Matplotlib confidence-band plot from this data shape.
Create a small-multiples figure and explain when it might mislead.
```

The skill tells Codex to inspect the data shape first, choose a chart, generate
a runnable script, export clean figures, and mention limitations.

## Current limits

- v0.1 uses Matplotlib and NumPy only.
- Plotly and interactive exports are left for later.
- The gallery uses synthetic data, not real lab, school, company, or personal
  data.
- The checks catch common privacy and provenance mistakes; they are not a legal
  review and do not prove that outside material is safe to publish.

## Docs

- [Chart selection](docs/chart-selection.md)
- [Agent workflow](docs/agent-workflow.md)
- [Provenance policy](docs/provenance-policy.md)
- [Application evidence](docs/application-evidence.md)
- [v0.2 template candidates](docs/v0.2-template-candidates.md)

## Feedback

- [First-use feedback](https://github.com/Kkkakania/python-plotting-skill/issues/new?template=first-use-feedback.yml)
- [Template requests](https://github.com/Kkkakania/python-plotting-skill/issues/new?template=template-request.yml)

## License

MIT. Use the templates freely, but keep provenance clear when adapting them.
