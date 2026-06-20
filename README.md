# Python Plotting Skill

[English](README.md) | [简体中文](README.zh-CN.md)

`python-plotting-skill` is a small Codex skill for choosing and generating
Python scientific figures from clean, reproducible scripts.

It is the Python sibling of the MATLAB plotting and scientific diagram skills:

- [`matlab-plotting-skill`](https://github.com/Kkkakania/matlab-plotting-skill)
  covers MATLAB data-to-figure workflows.
- [`scientific-diagram-skill`](https://github.com/Kkkakania/matlab-plotting-skill/tree/main/skills/scientific-diagram-skill)
  covers Mermaid and draw.io research diagrams.
- [`matlab-scientific-figures`](https://github.com/Kkkakania/matlab-scientific-figures)
  remains the MATLAB gallery and API evidence surface.

This repository starts deliberately small. v0.1 contains 12 Matplotlib templates,
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
| `correlation_matrix` | compact correlation overview |

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

## License

MIT. Use the templates freely, but keep provenance clear when adapting them.
