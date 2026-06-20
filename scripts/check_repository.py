#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "docs/gallery"}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".toml", ".txt", ".sh"}

LOCAL_ROOTS = [
    "/" + "Users" + "/",
    "/" + "ho" + "me" + "/",
    "C:" + "\\\\" + "Users" + "\\\\",
]
SENSITIVE_WORDS = [
    "身份" + "证",
    "银行" + "卡",
    "手机" + "号",
    "家庭" + "住址",
    "微信" + "号",
]


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(rel == part or rel.startswith(part + "/") for part in SKIP_DIRS)


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        if path.name == "LICENSE":
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main() -> int:
    email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    errors: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        if email.search(text):
            errors.append(f"{rel}: email-like private marker")
        for root in LOCAL_ROOTS:
            if root in text:
                errors.append(f"{rel}: local absolute path marker")
        for word in SENSITIVE_WORDS:
            if word in text:
                errors.append(f"{rel}: sensitive personal-data marker")
        placeholder = "TO" + "DO"
        if placeholder in text:
            errors.append(f"{rel}: placeholder marker")
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Repository check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
