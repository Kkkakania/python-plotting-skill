from __future__ import annotations

import importlib.util
import os
import pathlib
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
        "skills/python-plotting-skill/SKILL.md",
        ".github/workflows/quality.yml",
        ".github/ISSUE_TEMPLATE/first-use-feedback.yml",
        ".github/ISSUE_TEMPLATE/template-request.yml",
    ]
    for file_name in required:
        path = ROOT / file_name
        assert path.is_file(), file_name
        assert path.stat().st_size > 100, file_name

    assert "[简体中文](README.zh-CN.md)" in read("README.md")
    assert "[English](README.md)" in read("README.zh-CN.md")
    assert "broad adoption" in read("README.md")
    assert "不要声称" in read("README.zh-CN.md")
    assert "Python version" in read(".github/ISSUE_TEMPLATE/first-use-feedback.yml")
    assert "synthetic data" in read(".github/ISSUE_TEMPLATE/template-request.yml")


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
    }
    assert len(ids) >= 12
    assert required.issubset(ids)
    assert len(ids) == len(set(ids))
    for template in templates:
        assert template["title"]
        assert template["task"]
        assert template["risk"]


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


def test_release_check_and_scans_pass():
    result = subprocess.run(
        ["bash", "scripts/release_check.sh"],
        cwd=ROOT,
        env={**os.environ, "PYTHON": sys.executable},
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
