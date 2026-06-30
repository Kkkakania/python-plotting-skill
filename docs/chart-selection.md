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
| Compare the same categories across panels | `category_small_multiples` |
| Summarize pairwise correlations | `correlation_matrix` |
| Rank ordered items without heavy bars | `lollipop_ranking` |
| Show paired change between two conditions | `paired_before_after` |
| Show frequency content for a sampled signal | `spectral_density` |
| Show iterative residual decay | `residual_convergence` |
| Magnify one local region inside a main trend | `main_inset` |

The template is a starting point. Before presenting a figure, check whether the
data supports the claim the figure appears to make. A fitted trend line does not
prove causality, a correlation matrix does not explain mechanism, and a ranking
needs sample-size or uncertainty context when adjacent values are close. A
before/after chart only makes sense when each line connects the same unit.
Category small multiples are easier to compare when every panel keeps the same
category order and y-axis scale. Spectral density plots need the sampling rate,
frequency units, and any windowing choices stated beside the figure. Residual
convergence plots should state the stopping rule and whether the residual is
absolute, relative, normalized, or scaled. Inset plots should explain why the
local region matters, otherwise the zoom can overstate a small feature.
