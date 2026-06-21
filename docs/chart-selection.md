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
| Rank ordered items without heavy bars | `lollipop_ranking` |
| Show paired change between two conditions | `paired_before_after` |

The template is a starting point. Before presenting a figure, check whether the
data supports the claim the figure appears to make. A fitted trend line does not
prove causality, a correlation matrix does not explain mechanism, and a ranking
needs sample-size or uncertainty context when adjacent values are close. A
before/after chart only makes sense when each line connects the same unit.
