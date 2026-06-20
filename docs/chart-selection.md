# Chart Selection

Start with the communication task, not the prettiest chart.

| Task | First template |
|---|---|
| Show one trend over time | `line_trend` |
| Compare several series on one axis | `multi_line_comparison` |
| Show x-y relationship | `scatter_relationship` |
| Show x-y relationship with a simple trend | `regression_scatter` |
| Show uncertainty around a mean | `confidence_band` |
| Compare groups across categories | `grouped_bar` |
| Show a matrix of values | `heatmap_matrix` |
| Show many overlapping points | `density_scatter` |
| Compare distributions with observations | `box_jitter` |
| Compare distribution shapes | `violin_plot` |
| Repeat the same chart for several groups | `small_multiples` |
| Summarize pairwise correlations | `correlation_matrix` |

The template is a starting point. Before presenting a figure, check whether the
data supports the claim the figure appears to make. A fitted trend line does not
prove causality, and a correlation matrix does not explain mechanism.
