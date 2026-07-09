from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_renderer():
    path = ROOT / "scripts" / "render_gallery.py"
    spec = importlib.util.spec_from_file_location("render_gallery", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_gallery_manifest_marks_private_data_absent(tmp_path):
    renderer = load_renderer()

    renderer.render(tmp_path, ["png"])

    generated = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    committed = json.loads((ROOT / "docs" / "gallery" / "manifest.json").read_text(encoding="utf-8"))
    assert generated["privateData"] is False
    assert committed["privateData"] is False
