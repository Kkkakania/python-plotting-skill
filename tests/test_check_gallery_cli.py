from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_check_gallery_rejects_unsupported_formats(tmp_path):
    result = subprocess.run(
        [sys.executable, "scripts/check_gallery.py", str(tmp_path), "--formats", "png,jpg"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Unsupported format(s): jpg" in result.stderr


def test_check_gallery_rejects_path_like_format(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "check_gallery.py"),
            str(tmp_path),
            "--formats",
            "../png",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 2
    assert "Unsupported format(s): ../png" in result.stderr


def test_check_gallery_rejects_non_object_manifest(tmp_path):
    (tmp_path / "manifest.json").write_text(json.dumps([]), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_gallery.py"), str(tmp_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "manifest root must be an object" in result.stdout
    assert "Traceback" not in result.stderr
