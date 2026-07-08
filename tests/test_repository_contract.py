from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_renderer():
    path = ROOT / "scripts" / "render_gallery.py"
    spec = importlib.util.spec_from_file_location("render_gallery", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_repository_checker():
    path = ROOT / "scripts" / "check_repository.py"
    spec = importlib.util.spec_from_file_location("check_repository", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_core_repository_files_exist_and_are_bilingual():
    required = [
        "README.md",
        "README.zh-CN.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "docs/chart-selection.md",
        "docs/agent-workflow.md",
        "docs/provenance-policy.md",
        "docs/application-evidence.md",
        "docs/v0.2-template-candidates.md",
        "skills/python-plotting-skill/SKILL.md",
        ".github/workflows/quality.yml",
        ".github/workflows/issue-triage.yml",
        ".github/ISSUE_TEMPLATE/first-use-feedback.yml",
        ".github/ISSUE_TEMPLATE/template-request.yml",
    ]
    for file_name in required:
        path = ROOT / file_name
        assert path.is_file(), file_name
        assert path.stat().st_size > 100, file_name

    assert "[简体中文](README.zh-CN.md)" in read("README.md")
    assert "[English](README.md)" in read("README.zh-CN.md")
    assert "actions/workflows/quality.yml/badge.svg" in read("README.md")
    assert "actions/workflows/quality.yml/badge.svg" in read("README.zh-CN.md")
    assert "docs/gallery/line_trend.png" in read("README.md")
    assert "docs/gallery/line_trend.png" in read("README.zh-CN.md")
    assert "docs/v0.2-template-candidates.md" in read("README.md")
    assert "issues/new?template=first-use-feedback.yml" in read("README.md")
    assert "issues/new?template=first-use-feedback.yml" in read("README.zh-CN.md")
    assert "python-plotting-skill/issues/1" not in read("README.md")
    assert "python-plotting-skill/issues/1" not in read("README.zh-CN.md")
    assert "issues/new?template=template-request.yml" in read("README.md")
    assert "issues/new?template=template-request.yml" in read("README.zh-CN.md")
    assert "python-plotting-skill/issues/2" not in read("README.md")
    assert "python-plotting-skill/issues/2" not in read("README.zh-CN.md")
    assert "github.com/Kkkakania/scientific-diagram-skill" in read("README.md")
    assert "github.com/Kkkakania/scientific-diagram-skill" in read("README.zh-CN.md")
    assert "matlab-plotting-skill/tree/main/skills/scientific-diagram-skill" not in read("README.md")
    assert "matlab-plotting-skill/tree/main/skills/scientific-diagram-skill" not in read("README.zh-CN.md")
    assert "broad adoption" in read("README.md")
    assert "不要声称" in read("README.zh-CN.md")
    assert "contains 20 Matplotlib templates" in read("README.md")
    assert "19 Matplotlib templates" not in read("README.md")
    assert "20 个 Matplotlib 模板" in read("README.zh-CN.md")
    assert "19 个 Matplotlib 模板" not in read("README.zh-CN.md")
    assert "Python version" in read(".github/ISSUE_TEMPLATE/first-use-feedback.yml")
    assert "synthetic data" in read(".github/ISSUE_TEMPLATE/template-request.yml")
    triage = read(".github/workflows/issue-triage.yml")
    assert "python-plotting-skill-triage" in triage
    assert "synthetic CSV" in triage
    assert "Matplotlib" in triage
    assert "not a claim about adoption" in triage
    quality = read(".github/workflows/quality.yml")
    assert "actions/checkout@v5" in quality
    assert "actions/setup-python@v6" in quality
    assert "actions/checkout@v4" not in quality
    assert "actions/setup-python@v5" not in quality


def test_application_evidence_is_current_and_bounded():
    text = read("docs/application-evidence.md")
    assert "Snapshot date: 2026-06-22." in text
    assert "Use this as companion evidence" in text
    assert "not the main Codex for Open Source application repository" in text
    assert "Quality workflow" in text
    assert "Checked baseline commit | `fc9b1f4`" in text
    assert "Quality run `27925041264`, successful and annotation-free" in text
    assert "https://github.com/Kkkakania/python-plotting-skill/actions/runs/27925041264" in text
    assert "PYTHON=.venv/bin/python bash scripts/release_check.sh" in text
    assert "11 passed" in text
    assert "Gallery check passed for 15 templates." in text
    assert "Repository check passed." in text
    assert "first-use" in text
    assert "Do not claim broad adoption" in text
    assert "not evidence of external adoption" in text
    assert "guaranteed" in text
    assert "README template-count guard" in text
    assert "221bf12" not in text
    assert "27906611032" not in text
    assert "4f0622f" not in text
    assert "27924202891" not in text
    assert "Latest checked commit" not in text
    assert "61e3352" not in text
    assert "27924928257" not in text


def test_repository_scan_skips_generated_python_artifacts():
    checker = load_repository_checker()
    assert checker.should_skip(ROOT / ".pytest_cache" / "README.md")
    assert checker.should_skip(ROOT / "scripts" / "__pycache__" / "render_gallery.pyc")
    assert checker.should_skip(ROOT / "python_plotting_skill.egg-info" / "PKG-INFO")


def test_repository_scan_detects_common_local_path_variants():
    checker = load_repository_checker()
    samples = [
        "/" + "Users" + "/example/private.csv",
        "/" + "home" + "/example/private.csv",
        "/" + "mnt" + "/c/" + "Users" + "/example/private.csv",
        "C:" + "\\" + "Users" + "\\" + "example" + "\\" + "private.csv",
        "%USER" + "PROFILE%" + "\\" + "example" + "\\" + "private.csv",
        "/" + "work" + "spaces" + "/private-repo/private.csv",
        "/" + "Vol" + "umes" + "/External/private.csv",
    ]

    for sample in samples:
        assert checker.has_local_root_marker(sample), sample


def test_generated_python_artifacts_are_not_tracked():
    output = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    blocked = (".venv/", ".pytest_cache/", "__pycache__/", ".pyc", ".egg-info/")
    tracked = [path for path in output.splitlines() if any(part in path for part in blocked)]

    assert tracked == []


def test_repository_scan_validates_readme_template_count_claims():
    checker = load_repository_checker()
    renderer = load_renderer()
    count = len(renderer.TEMPLATES)

    errors: list[str] = []
    checker.check_readme_template_count_claims(
        read("README.md"),
        read("README.zh-CN.md"),
        count,
        errors,
    )
    assert errors == []

    stale_errors: list[str] = []
    checker.check_readme_template_count_claims(
        "This repository contains 14 Matplotlib templates.",
        "当前 main 分支保持小而清楚：14 个 Matplotlib 模板。",
        count,
        stale_errors,
    )
    assert "README.md: stale template count claim" in stale_errors
    assert "README.zh-CN.md: stale template count claim" in stale_errors


def test_skill_frontmatter_and_workflow_are_specific():
    text = read("skills/python-plotting-skill/SKILL.md")
    assert "name: python-plotting-skill" in text
    assert "description:" in text
    assert "Matplotlib" in text
    assert "synthetic data" in text
    assert "scripts/render_gallery.py" in text
    assert ("TO" + "DO") not in text


def test_template_catalog_has_v0_1_scope():
    renderer = load_renderer()
    templates = renderer.TEMPLATES
    ids = [template["id"] for template in templates]
    required = {
        "line_trend",
        "multi_line_comparison",
        "scatter_relationship",
        "regression_scatter",
        "confidence_band",
        "grouped_bar",
        "heatmap_matrix",
        "density_scatter",
        "box_jitter",
        "violin_plot",
        "small_multiples",
        "correlation_matrix",
        "lollipop_ranking",
        "paired_before_after",
        "category_small_multiples",
        "spectral_density",
        "residual_convergence",
        "main_inset",
        "shared_colorbar_panels",
        "gantt_timeline",
    }
    assert len(ids) >= 20
    assert required.issubset(ids)
    assert len(ids) == len(set(ids))
    for template in templates:
        assert template["title"]
        assert template["task"]
        assert template["risk"]


def test_committed_gallery_manifest_matches_renderer_catalog():
    renderer = load_renderer()
    ids = {template["id"] for template in renderer.TEMPLATES}
    manifest = json.loads(read("docs/gallery/manifest.json"))

    assert manifest["schemaVersion"] == 1
    assert manifest["generatedBy"] == "scripts/render_gallery.py"
    assert manifest["templateCount"] == len(ids)
    assert {template["id"] for template in manifest["templates"]} == ids


def test_skill_template_map_matches_renderer_catalog():
    renderer = load_renderer()
    expected = {template["id"] for template in renderer.TEMPLATES}
    skill_text = read("skills/python-plotting-skill/SKILL.md")
    mapped = set(re.findall(r"^- `([^`]+)`:", skill_text, flags=re.MULTILINE))

    assert mapped == expected


def test_gallery_renderer_generates_png_and_svg(tmp_path):
    command = [
        sys.executable,
        str(ROOT / "scripts" / "render_gallery.py"),
        "--out",
        str(tmp_path),
        "--formats",
        "png,svg",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr

    renderer = load_renderer()
    ids = [template["id"] for template in renderer.TEMPLATES]
    for template_id in ids:
        assert (tmp_path / f"{template_id}.png").stat().st_size > 1024
        assert (tmp_path / f"{template_id}.svg").stat().st_size > 1024
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["schemaVersion"] == 1
    assert manifest["templateCount"] == len(ids)
    assert {item["id"] for item in manifest["templates"]} == set(ids)


def test_lollipop_ranking_is_documented():
    assert "`lollipop_ranking`" in read("README.md")
    assert "`lollipop_ranking`" in read("README.zh-CN.md")
    assert "`lollipop_ranking`" in read("docs/chart-selection.md")


def test_paired_before_after_is_documented():
    assert "`paired_before_after`" in read("README.md")
    assert "`paired_before_after`" in read("README.zh-CN.md")
    assert "`paired_before_after`" in read("docs/chart-selection.md")


def test_category_small_multiples_is_documented():
    assert "`category_small_multiples`" in read("README.md")
    assert "`category_small_multiples`" in read("README.zh-CN.md")
    assert "`category_small_multiples`" in read("docs/chart-selection.md")


def test_spectral_density_is_documented():
    assert "`spectral_density`" in read("README.md")
    assert "`spectral_density`" in read("README.zh-CN.md")
    assert "`spectral_density`" in read("docs/chart-selection.md")


def test_residual_convergence_is_documented():
    assert "`residual_convergence`" in read("README.md")
    assert "`residual_convergence`" in read("README.zh-CN.md")
    assert "`residual_convergence`" in read("docs/chart-selection.md")


def test_main_inset_is_documented():
    assert "`main_inset`" in read("README.md")
    assert "`main_inset`" in read("README.zh-CN.md")
    assert "`main_inset`" in read("docs/chart-selection.md")


def test_shared_colorbar_panels_is_documented():
    assert "`shared_colorbar_panels`" in read("README.md")
    assert "`shared_colorbar_panels`" in read("README.zh-CN.md")
    assert "`shared_colorbar_panels`" in read("docs/chart-selection.md")


def test_gantt_timeline_is_documented():
    assert "`gantt_timeline`" in read("README.md")
    assert "`gantt_timeline`" in read("README.zh-CN.md")
    assert "`gantt_timeline`" in read("docs/chart-selection.md")


def test_v02_template_candidates_are_bounded():
    text = read("docs/v0.2-template-candidates.md")
    assert "python-plotting-skill#2" in text
    assert "bounded v0.2 shortlist is complete" in text
    assert "new template-request issue" in text
    assert "`spectral_density`" in text
    assert "`residual_convergence`" in text
    assert "`main_inset`" in text
    assert "Full Origin-style parity" in text
    assert "private data" in text


def test_release_check_and_scans_pass():
    result = subprocess.run(
        ["bash", "scripts/release_check.sh"],
        cwd=ROOT,
        env={**os.environ, "PYTHON": sys.executable},
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
