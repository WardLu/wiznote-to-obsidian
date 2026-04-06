#!/usr/bin/env python3
import argparse
import os
import re
from pathlib import Path

TAG_MAP = {
    "c63131d9-270e-4f90-92c2-e022e20f0560": "星标",
    "1d9bdff0-3ba9-4964-b818-4e926ec1da63": "星标2",
}


def normalize_tags(raw_tags: str) -> str | None:
    value = raw_tags.strip()
    if value == "None":
        return None

    parts = [part for part in value.split("*") if part]
    if not parts:
        return None

    names = []
    for part in parts:
        mapped = TAG_MAP.get(part)
        if not mapped:
            # Unknown tags are left untouched so data is not lost.
            mapped = part
        if mapped not in names:
            names.append(mapped)

    if len(names) == 1:
        return names[0]

    return "[" + ", ".join(names) + "]"


def process_file(filepath: str, dry_run: bool = False) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"^tags:\s*(.+)$", content, re.MULTILINE)
    if not match:
        return False

    original = match.group(1).strip()
    normalized = normalize_tags(original)
    if normalized is None:
        new_content = re.sub(
            r"^tags:\s*None\s*(?:\r?\n)?",
            "",
            content,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        new_content = re.sub(
            r"^tags:\s*.+$",
            f"tags: {normalized}",
            content,
            count=1,
            flags=re.MULTILINE,
        )

    if new_content == content:
        return False

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert WizNote tag UUIDs in Obsidian frontmatter back to readable names"
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

    base = os.path.abspath(os.path.expanduser(args.base))
    if not os.path.isdir(base):
        raise SystemExit(f"Directory not found: {base}")

    count = 0
    for path in Path(base).rglob("*.md"):
        if process_file(str(path), dry_run=args.dry_run):
            action = "Would fix" if args.dry_run else "Fixed"
            print(f"{action}: {path}")
            count += 1

    summary = "would be fixed" if args.dry_run else "fixed"
    print(f"\nTotal files {summary}: {count}")


if __name__ == "__main__":
    main()
