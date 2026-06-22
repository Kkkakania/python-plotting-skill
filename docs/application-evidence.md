# Application Evidence

Snapshot date: 2026-06-22.

This note is a short reviewer-facing summary. It is not a promise of Codex for
Open Source eligibility, credits, or ChatGPT Pro access.

Use this as companion evidence for the plotting-skill ecosystem. It is not the main Codex for Open Source application repository; that role belongs to
`matlab-scientific-figures` because it has the main gallery, release history,
MATLAB APIs, and broader maintainer workflow.

## Repository to cite

<https://github.com/Kkkakania/python-plotting-skill>

## Current evidence

- `skills/python-plotting-skill/SKILL.md` defines the agent workflow.
- `scripts/render_gallery.py` generates 15 deterministic Matplotlib examples.
- `docs/gallery` stores checked PNG/SVG outputs.
- `scripts/release_check.sh` runs tests, gallery rendering, privacy checks, and
  source-boundary checks.
- The repository has English and Chinese README files, provenance docs, and a
  GitHub Actions Quality workflow.
- The repository scan now includes a README template-count guard, so the public
  template count fails CI if it drifts from `scripts/render_gallery.py`.
- New issues receive a small maintainer triage checklist, so first-use reports
  and template requests can be classified without exposing private data.
- First-use feedback is tracked in
  [`python-plotting-skill#1`](https://github.com/Kkkakania/python-plotting-skill/issues/1);
  small v0.2 template requests are tracked in
  [`python-plotting-skill#2`](https://github.com/Kkkakania/python-plotting-skill/issues/2).

## Checked snapshot

| Field | Value |
|---|---|
| Checked baseline commit | `fc9b1f4` |
| Checked baseline workflow | Quality run `27925041264`, successful and annotation-free |
| Workflow URL | <https://github.com/Kkkakania/python-plotting-skill/actions/runs/27925041264> |
| Local release gate | `PYTHON=.venv/bin/python bash scripts/release_check.sh` |

Latest local release-gate result:

```text
11 passed
Gallery check passed for 15 templates.
Repository check passed.
Release check passed.
```

This snapshot is maintenance evidence for the Python skill. It is not evidence of external adoption, usage volume, or reviewer approval.

## What Codex would help with

- review new templates for chart/data mismatch;
- triage first-use reports;
- summarize gallery-render failures;
- draft release notes from merged commits;
- keep English and Chinese docs aligned without turning the Chinese README into
  a direct translation.

Do not claim broad adoption, download volume, external endorsement, or
guaranteed benefit-program results. Cite only public commits, workflow runs,
checked examples, and redacted issues.
