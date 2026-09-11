#!/usr/bin/env python3

import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[2]
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def slugify(heading: str) -> str:
    normalized = unicodedata.normalize("NFKD", heading.strip().lower())
    without_markup = re.sub(r"[`*_~]", "", normalized)
    without_punctuation = "".join(
        character
        for character in without_markup
        if character.isalnum() or character in {" ", "-", "_"}
    )
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", without_punctuation)).strip("-")


def headings(path: Path) -> set[str]:
    result: set[str] = set()
    duplicates: dict[str, int] = {}
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        base = slugify(match.group(1))
        duplicate_index = duplicates.get(base, 0)
        duplicates[base] = duplicate_index + 1
        result.add(base if duplicate_index == 0 else f"{base}-{duplicate_index}")
    return result


errors: list[str] = []
checked = 0
for markdown_path in sorted(REPO_ROOT.glob("*.md")) + sorted((REPO_ROOT / "docs").rglob("*.md")):
    in_fence = False
    for line_number, line in enumerate(markdown_path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for raw_target in LINK_PATTERN.findall(line):
            target = raw_target.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part, separator, fragment = target.partition("#")
            resolved = markdown_path if not path_part else (markdown_path.parent / unquote(path_part)).resolve()
            checked += 1
            if not resolved.exists():
                errors.append(f"{markdown_path.relative_to(REPO_ROOT)}:{line_number}: missing target")
                continue
            if separator and resolved.is_file() and slugify(unquote(fragment)) not in headings(resolved):
                errors.append(f"{markdown_path.relative_to(REPO_ROOT)}:{line_number}: missing fragment")

if errors:
    raise SystemExit("FAIL: relative Markdown links\n" + "\n".join(errors))
print(f"PASS: {checked} relative Markdown links")
