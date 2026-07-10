#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
    "docs/gallery",
}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".toml", ".txt", ".sh"}

LOCAL_ROOT_PATTERNS = [
    re.compile("/" + "users" + "/", re.IGNORECASE),
    re.compile("/" + "home" + "/", re.IGNORECASE),
    re.compile("/" + "mnt" + "/", re.IGNORECASE),
    re.compile(r"[a-z]:" + r"\\+" + "users" + r"\\+", re.IGNORECASE),
    re.compile(r"%userprofile%[\\/]", re.IGNORECASE),
    re.compile("/" + "work" + "spaces" + "/", re.IGNORECASE),
    re.compile("/" + "vol" + "umes" + "/", re.IGNORECASE),
]
SENSITIVE_WORDS = [
    "身份" + "证",
    "银行" + "卡",
    "手机" + "号",
    "家庭" + "住址",
    "微信" + "号",
]


def should_skip(path: Path) -> bool:
    rel_path = path.relative_to(ROOT)
    rel = rel_path.as_posix()
    if any(part == "__pycache__" or part.endswith(".egg-info") for part in rel_path.parts):
        return True
    return any(rel == part or rel.startswith(part + "/") for part in SKIP_DIRS)


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        if path.name == "LICENSE":
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def has_local_root_marker(text: str) -> bool:
    return any(pattern.search(text) for pattern in LOCAL_ROOT_PATTERNS)


def check_readme_template_count_claims(
    readme_text: str,
    readme_zh_text: str,
    template_count: int,
    errors: list[str],
) -> None:
    english_counts = re.findall(r"contains (\d+) Matplotlib templates", readme_text)
    chinese_counts = re.findall(r"(\d+) 个 Matplotlib 模板", readme_zh_text)
    expected = str(template_count)

    if not english_counts or expected not in english_counts:
        errors.append("README.md: stale template count claim")
    if not chinese_counts or expected not in chinese_counts:
        errors.append("README.zh-CN.md: stale template count claim")


def load_template_count() -> int:
    import importlib.util

    renderer_path = ROOT / "scripts" / "render_gallery.py"
    spec = importlib.util.spec_from_file_location("render_gallery", renderer_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load render_gallery.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return len(module.TEMPLATES)


def main() -> int:
    email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    errors: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        if email.search(text):
            errors.append(f"{rel}: email-like private marker")
        if has_local_root_marker(text):
            errors.append(f"{rel}: local absolute path marker")
        for word in SENSITIVE_WORDS:
            if word in text:
                errors.append(f"{rel}: sensitive personal-data marker")
        placeholder = "TO" + "DO"
        if placeholder in text:
            errors.append(f"{rel}: placeholder marker")
    check_readme_template_count_claims(
        (ROOT / "README.md").read_text(encoding="utf-8"),
        (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
        load_template_count(),
        errors,
    )
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Repository check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
