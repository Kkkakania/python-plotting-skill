#!/usr/bin/env python3
from __future__ import annotations

import argparse
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

    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"Gallery check passed for {len(TEMPLATES)} templates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
