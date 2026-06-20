#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
PYTHON_BIN="${PYTHON:-python3}"

echo "== Python tests =="
if [[ -n "${PYTEST_CURRENT_TEST:-}" ]]; then
  echo "Skipping nested pytest because release_check.sh is already running under pytest."
else
  "$PYTHON_BIN" -m pytest
fi

echo "== Render gallery =="
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
"$PYTHON_BIN" scripts/render_gallery.py --out "$tmp_dir/gallery" --formats png,svg
"$PYTHON_BIN" scripts/check_gallery.py "$tmp_dir/gallery" --formats png,svg

echo "== Repository scan =="
"$PYTHON_BIN" scripts/check_repository.py

echo "Release check passed."
