# Gallery

Generated from synthetic data by `scripts/render_gallery.py`.

| Template | Task | Risk | Preview |
|---|---|---|---|
| `line_trend` | Show one trend over time. | Can hide seasonal or subgroup patterns. | ![Line trend](line_trend.png) |
| `multi_line_comparison` | Compare several series on one axis. | Too many lines become unreadable. | ![Multi-line comparison](multi_line_comparison.png) |
| `scatter_relationship` | Show relation between two numeric variables. | Correlation does not prove causality. | ![Scatter relationship](scatter_relationship.png) |
| `regression_scatter` | Show x-y relation with a fitted trend. | A straight fit can hide nonlinear structure. | ![Regression scatter](regression_scatter.png) |
| `confidence_band` | Show mean and uncertainty. | Band meaning must be defined. | ![Confidence band](confidence_band.png) |
| `grouped_bar` | Compare categories across groups. | Bars hide within-group variation. | ![Grouped bar](grouped_bar.png) |
| `heatmap_matrix` | Show matrix or grid values. | Color scale choices can exaggerate small changes. | ![Heatmap matrix](heatmap_matrix.png) |
| `density_scatter` | Show dense x-y points. | Binning can create artificial clusters. | ![Density scatter](density_scatter.png) |
| `box_jitter` | Compare distributions and observations. | Small samples need visible points. | ![Box plot with jitter](box_jitter.png) |
| `violin_plot` | Compare distribution shapes. | Kernel smoothing can imply unsupported detail. | ![Violin plot](violin_plot.png) |
| `small_multiples` | Repeat comparable panels. | Panels need shared scales to compare fairly. | ![Small multiples](small_multiples.png) |
| `correlation_matrix` | Summarize pairwise correlations. | Correlation signs need domain interpretation. | ![Correlation matrix](correlation_matrix.png) |
| `lollipop_ranking` | Rank ordered items without heavy bars. | Rankings need uncertainty or sample-size context when values are close. | ![Lollipop ranking](lollipop_ranking.png) |
| `paired_before_after` | Show paired change between two conditions. | The paired design must be real; do not connect unrelated groups. | ![Paired before/after](paired_before_after.png) |
