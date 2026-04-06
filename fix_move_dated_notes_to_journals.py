#!/usr/bin/env python3
"""Move date-prefixed notes from My Notes into My Journals by frontmatter date."""

from __future__ import annotations

import argparse
import re
import signal
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DATE_PREFIX_RE = re.compile(r"^\d{1,2}\.\d{1,2}(?:\D.*)?\.md$")
FRONTMATTER_DATE_RE = re.compile(r"(?m)^date:\s*(\d{4}-\d{2}-\d{2})\s*$")


@dataclass
class MovePlan:
    source: Path
    target: Path
    created_dir: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Move notes whose filenames start with M.D into My Journals/"
            "YYYY-MM according to each note's frontmatter date."
        )
    )
    parser.add_argument(
        "--vault-root",
        default="wiznote_obsidian",
        help="Vault root directory that contains 'My Notes' and 'My Journals'.",
    )
    parser.add_argument(
        "--source-dir",
        default="My Notes",
        help="Source directory name inside the vault root.",
    )
    parser.add_argument(
        "--target-dir",
        default="My Journals",
        help="Target directory name inside the vault root.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned moves without changing files.",
    )
    return parser.parse_args()


def read_note_date(note_path: Path) -> datetime:
    text = note_path.read_text(encoding="utf-8", errors="ignore")
    match = FRONTMATTER_DATE_RE.search(text)
    if not match:
        raise ValueError(f"missing valid 'date' frontmatter: {note_path}")
    return datetime.strptime(match.group(1), "%Y-%m-%d")


def resolve_month_dir(journals_dir: Path, note_date: datetime) -> tuple[Path, bool]:
    padded = journals_dir / note_date.strftime("%Y-%m")
    if padded.exists():
        return padded, False

    unpadded = journals_dir / f"{note_date.year}-{note_date.month}"
    if unpadded.exists():
        return unpadded, False

    return padded, True


def unique_target_path(target_dir: Path, filename: str) -> Path:
    candidate = target_dir / filename
    if not candidate.exists():
        return candidate

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    index = 2
    while True:
        candidate = target_dir / f"{stem} ({index}){suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def build_move_plan(source_dir: Path, journals_dir: Path) -> list[MovePlan]:
    plans: list[MovePlan] = []
    for note_path in sorted(source_dir.iterdir(), key=lambda path: path.name):
        if not note_path.is_file() or not DATE_PREFIX_RE.match(note_path.name):
            continue

        note_date = read_note_date(note_path)
        month_dir, created_dir = resolve_month_dir(journals_dir, note_date)
        target = unique_target_path(month_dir, note_path.name)
        plans.append(MovePlan(source=note_path, target=target, created_dir=created_dir))
    return plans


def execute_moves(plans: list[MovePlan], dry_run: bool) -> None:
    created_dirs: set[Path] = set()
    moved = 0

    for plan in plans:
        if plan.created_dir and plan.target.parent not in created_dirs:
            action = "CREATE" if dry_run else "create"
            print(f"{action} {plan.target.parent}")
            if not dry_run:
                plan.target.parent.mkdir(parents=True, exist_ok=True)
            created_dirs.add(plan.target.parent)

        action = "MOVE" if dry_run else "move"
        print(f"{action} {plan.source} -> {plan.target}")
        if not dry_run:
            shutil.move(str(plan.source), str(plan.target))
        moved += 1

    summary = "would move" if dry_run else "moved"
    print(f"\nSummary: {summary} {moved} notes.")
    if created_dirs:
        dir_summary = "would create" if dry_run else "created"
        print(f"Summary: {dir_summary} {len(created_dirs)} month folders.")


def main() -> int:
    args = parse_args()
    vault_root = Path(args.vault_root).expanduser().resolve()
    source_dir = vault_root / args.source_dir
    journals_dir = vault_root / args.target_dir

    if not source_dir.is_dir():
        raise SystemExit(f"source directory not found: {source_dir}")
    if not journals_dir.is_dir():
        raise SystemExit(f"target directory not found: {journals_dir}")

    plans = build_move_plan(source_dir, journals_dir)
    if not plans:
        print("No date-prefixed notes found to move.")
        return 0

    execute_moves(plans, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    raise SystemExit(main())
