#!/usr/bin/env python3

import os
import re
import subprocess
import unicodedata
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[2]
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def git_output(*arguments: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *arguments],
        check=True,
        capture_output=True,
    )
    return result.stdout


if (REPO_ROOT / ".git").exists():
    tracked_files = {
        Path(raw_path.decode("utf-8"))
        for raw_path in git_output("ls-files", "-z").split(b"\0")
        if raw_path
    }
    markdown_paths = sorted(path for path in tracked_files if path.suffix == ".md")

    def read_repository_text(relative_path: Path) -> str:
        return git_output("show", f":{relative_path.as_posix()}").decode("utf-8")

    def target_exists(relative_path: Path) -> bool:
        return relative_path in tracked_files or any(
            candidate.is_relative_to(relative_path) for candidate in tracked_files
        )

else:
    tracked_files = set()
    markdown_paths = [
        path.relative_to(REPO_ROOT)
        for path in sorted(REPO_ROOT.glob("*.md")) + sorted((REPO_ROOT / "docs").rglob("*.md"))
    ]

    def read_repository_text(relative_path: Path) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def target_exists(relative_path: Path) -> bool:
        return (REPO_ROOT / relative_path).exists()


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
    for line in read_repository_text(path).splitlines():
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
for markdown_path in markdown_paths:
    in_fence = False
    for line_number, line in enumerate(read_repository_text(markdown_path).splitlines(), 1):
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
            resolved = markdown_path if not path_part else Path(
                (markdown_path.parent / unquote(path_part)).as_posix()
            )
            resolved = Path(os.path.normpath(resolved.as_posix()))
            checked += 1
            if resolved.is_absolute() or str(resolved).startswith("..") or not target_exists(resolved):
                errors.append(f"{markdown_path}:{line_number}: missing tracked target")
                continue
            if separator and resolved.suffix == ".md" and slugify(unquote(fragment)) not in headings(resolved):
                errors.append(f"{markdown_path}:{line_number}: missing fragment")

if errors:
    raise SystemExit("FAIL: relative Markdown links\n" + "\n".join(errors))
print(f"PASS: {checked} relative Markdown links")
