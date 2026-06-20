# Contributing

Keep contributions small and reviewable.

- Use synthetic data for examples.
- Do not add private datasets, local paths, copied paper figures, or unclear
  third-party snippets.
- Add or update tests when changing the template catalog, gallery renderer, or
  documentation contract.
- Run `bash scripts/release_check.sh` before opening a PR.

New templates should explain:

- the chart task;
- the expected data shape;
- a common way the chart can mislead;
- the exported file names.
