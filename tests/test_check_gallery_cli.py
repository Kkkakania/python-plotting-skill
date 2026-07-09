from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_renderer():
    path = ROOT / "scripts" / "render_gallery.py"
    spec = importlib.util.spec_from_file_location("render_gallery", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_check_gallery_rejects_empty_format_list(tmp_path):
    gallery = tmp_path / "gallery"
    gallery.mkdir()
    renderer = load_renderer()
    (gallery / "index.md").write_text("# Gallery\n", encoding="utf-8")
    (gallery / "provenance.md").write_text("Clean-room synthetic gallery.\n", encoding="utf-8")
    (gallery / "manifest.json").write_text(
        json.dumps({"schemaVersion": 1, "templateCount": len(renderer.TEMPLATES)}),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_gallery.py"), str(gallery), "--formats", ","],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    assert "--formats must include at least one" in result.stderr
