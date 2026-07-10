from __future__ import annotations

import importlib.util
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
