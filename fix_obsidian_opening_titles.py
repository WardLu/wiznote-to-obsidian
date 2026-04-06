#!/usr/bin/env python3
import argparse
import os
import re
from pathlib import Path


FRONTMATTER_DELIM = "---"


def split_frontmatter(text: str):
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        return "", text

    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            return "".join(lines[: i + 1]), "".join(lines[i + 1 :])

    return "", text


def extract_title(frontmatter: str) -> str | None:
    match = re.search(r"^title:\s*(.+)$", frontmatter, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip()


def is_duplicate_opening(line: str, title: str | None) -> bool:
    stripped = line.strip()
    if not stripped:
        return False

    if stripped == "无标题":
        return True

    if not title:
        return False

    if stripped == title:
        return True

    heading = re.match(r"^#{1,6}\s+(.*)$", stripped)
    if heading and heading.group(1).strip() == title:
        return True

    return False


def clean_body(body: str, title: str | None):
    lines = body.splitlines(keepends=True)
    idx = 0
    removed = []

    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    while idx < len(lines) and is_duplicate_opening(lines[idx], title):
        removed.append(lines[idx].rstrip("\n"))
        idx += 1
        while idx < len(lines) and not lines[idx].strip():
            idx += 1

    cleaned = "".join(lines[idx:]).lstrip("\n")
    return cleaned, removed


def process_file(path: Path, dry_run: bool = False):
    text = path.read_text(encoding="utf-8", errors="ignore")
    frontmatter, body = split_frontmatter(text)
    if not frontmatter:
        return False, []

    title = extract_title(frontmatter)
    cleaned_body, removed = clean_body(body, title)

    frontmatter = frontmatter.rstrip("\n")
    cleaned_body = cleaned_body.lstrip("\n")
    new_text = frontmatter + "\n\n" + cleaned_body
    if not cleaned_body:
        new_text = frontmatter + "\n"

    if new_text == text:
        return False, []

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")

    return True, removed


def main():
    parser = argparse.ArgumentParser(
        description="Remove duplicated opening titles and '无标题' placeholders after frontmatter"
    )
    parser.add_argument(
        "base",
        nargs="?",
        default=str(Path(__file__).resolve().parent / "wiznote_obsidian"),
        help="Base directory to process (default: ./wiznote_obsidian)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would be modified without writing changes",
    )
    args = parser.parse_args()

    base = Path(os.path.abspath(os.path.expanduser(args.base)))
    if not base.is_dir():
        raise SystemExit(f"Directory not found: {base}")

    changed = 0
    for path in base.rglob("*.md"):
        updated, removed = process_file(path, dry_run=args.dry_run)
        if not updated:
            continue
        action = "Would fix" if args.dry_run else "Fixed"
        print(f"{action}: {path}")
        print(f"  Removed opening lines: {', '.join(repr(x) for x in removed)}")
        changed += 1

    summary = "would be fixed" if args.dry_run else "fixed"
    print(f"\nTotal files {summary}: {changed}")


if __name__ == "__main__":
    main()
