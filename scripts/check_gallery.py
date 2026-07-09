#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from render_gallery import TEMPLATES


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated gallery files.")
    parser.add_argument("gallery", type=Path)
    parser.add_argument("--formats", default="png,svg")
    args = parser.parse_args()

    formats = [item.strip() for item in args.formats.split(",") if item.strip()]
    errors: list[str] = []
    for template in TEMPLATES:
        for fmt in formats:
            path = args.gallery / f"{template['id']}.{fmt}"
            if not path.is_file():
                errors.append(f"missing {path}")
            elif path.stat().st_size < 1024:
                errors.append(f"too small {path}")
    for extra in ["index.md", "provenance.md"]:
        if not (args.gallery / extra).is_file():
            errors.append(f"missing {args.gallery / extra}")
    manifest_path = args.gallery / "manifest.json"
    if not manifest_path.is_file():
        errors.append(f"missing {manifest_path}")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{manifest_path}: invalid JSON: {exc.msg}")
        else:
            if manifest.get("schemaVersion") != 1:
                errors.append(f"{manifest_path}: unsupported schemaVersion")
            if manifest.get("templateCount") != len(TEMPLATES):
                errors.append(f"{manifest_path}: templateCount drift")
            expected_ids = [template["id"] for template in TEMPLATES]
            templates = manifest.get("templates")
            actual_ids = [item.get("id") for item in templates] if isinstance(templates, list) else []
            if actual_ids != expected_ids:
                errors.append(f"{manifest_path}: template ids drift")

    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"Gallery check passed for {len(TEMPLATES)} templates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
