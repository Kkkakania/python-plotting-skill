#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from render_gallery import TEMPLATES, parse_formats


def expected_manifest_templates(formats: list[str]) -> list[dict[str, object]]:
    return [
        {
            "id": str(template["id"]),
            "title": str(template["title"]),
            "task": str(template["task"]),
            "risk": str(template["risk"]),
            "outputs": [f"{template['id']}.{fmt}" for fmt in formats],
        }
        for template in TEMPLATES
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated gallery files.")
    parser.add_argument("gallery", type=Path)
    parser.add_argument("--formats", default="png,svg")
    args = parser.parse_args()

    try:
        formats = parse_formats(args.formats)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

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
            if manifest.get("generatedBy") != "scripts/render_gallery.py":
                errors.append(f"{manifest_path}: unexpected generator")
            if manifest.get("templateCount") != len(TEMPLATES):
                errors.append(f"{manifest_path}: templateCount drift")
            if manifest.get("formats") != formats:
                errors.append(f"{manifest_path}: format list drift")
            if manifest.get("templates") != expected_manifest_templates(formats):
                errors.append(f"{manifest_path}: manifest template catalog drift")

    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"Gallery check passed for {len(TEMPLATES)} templates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
