from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_renderer():
    path = ROOT / "scripts" / "render_gallery.py"
    spec = importlib.util.spec_from_file_location("render_gallery", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_formats_deduplicates_preserving_order():
    renderer = load_renderer()

    assert renderer.parse_formats("png,png,svg") == ["png", "svg"]


def test_render_gallery_rejects_empty_format_list(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "render_gallery.py"),
            "--out",
            str(tmp_path / "gallery"),
            "--formats",
            ",",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    assert "--formats must include at least one" in result.stderr


def test_render_gallery_rejects_empty_output_dir():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "render_gallery.py"),
            "--out",
            "",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    assert "--out must not be empty" in result.stderr


def test_list_json_exposes_machine_readable_catalog_without_rendering(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "render_gallery.py"),
            "--list",
            "--json",
            "--out",
            str(tmp_path / "unused"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    payload = json.loads(result.stdout)
    assert result.returncode == 0
    assert payload["schemaVersion"] == 1
    assert payload["templateCount"] == len(payload["templates"])
    assert payload["templates"][0] == {
        "id": "line_trend",
        "title": "Line trend",
        "task": "Show one trend over time.",
        "risk": "Can hide seasonal or subgroup patterns.",
    }
    assert not (tmp_path / "unused").exists()


def test_json_requires_list_mode():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "render_gallery.py"), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    assert "--json requires --list" in result.stderr
