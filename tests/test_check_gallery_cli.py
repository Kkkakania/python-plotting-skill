from __future__ import annotations

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

    assert result.returncode != 0
    assert "Unsupported format(s): jpg" in result.stderr
