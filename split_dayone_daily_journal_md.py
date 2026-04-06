#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List

SOURCE_MD = Path(
    "/Users/haoyuebai/Library/Mobile Documents/iCloud~md~obsidian/Documents/wiznote_obsidian/My Journals/DayOne/日常日记.md"
)
TARGET_ROOT = Path(
    "/Users/haoyuebai/Library/Mobile Documents/iCloud~md~obsidian/Documents/wiznote_obsidian/My Journals"
)

DATE_HEADING_RE = re.compile(
    r"^# (?P<weekday>[A-Za-z]+), (?P<day>\d{1,2}) (?P<month>[A-Z][a-z]{2}) (?P<year>\d{4}), "
    r"(?P<hour>\d{1,2}):(?P<minute>\d{2}) (?P<ampm>AM|PM) GMT(?P<offset>[+-]\d{1,2})$"
)
WEATHER_RE = re.compile(
    r"^\d{1,2}(?:\.\d+)?°C\s+[A-Za-z]"
)
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
IMAGE_LINE_RE = re.compile(r"^!\[.*?\]\(.*?\)\s*$")
OBSIDIAN_IMAGE_RE = re.compile(r"^!\[\[.*?\]\]\s*$")
INVALID_FILENAME_CHARS_RE = re.compile(r'[\\/:*?"<>|]')


@dataclass
class Entry:
    dt: datetime
    location: str | None
    body: str


@dataclass
class PlanItem:
    entry: Entry
    path: Path
    overwrite: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split the combined Day One daily journal markdown into Obsidian journal notes."
    )
    parser.add_argument("--write", action="store_true", help="Write notes to disk. Dry run by default.")
    parser.add_argument(
        "--preview-limit",
        type=int,
        default=5,
        help="How many planned notes to preview in dry run output.",
    )
    return parser.parse_args()


def strip_frontmatter(text: str) -> str:
    text = text.replace("\r\n", "\n")
    match = FRONTMATTER_RE.match(text)
    if match:
        text = text[match.end():]
    lines = text.split("\n")
    filtered: List[str] = []
    for line in lines:
        if line.strip() == "%E6%97%A5%E5%B8%B8%E6%97%A5%E8%AE%B0":
            continue
        filtered.append(line)
    return "\n".join(filtered).strip() + "\n"


def parse_dayone_heading(line: str) -> datetime | None:
    match = DATE_HEADING_RE.match(line.strip())
    if not match:
        return None
    data = match.groupdict()
    naive = datetime.strptime(
        f"{data['day']} {data['month']} {data['year']} {data['hour']}:{data['minute']} {data['ampm']}",
        "%d %b %Y %I:%M %p",
    )
    offset_hours = int(data["offset"])
    tz = timezone(timedelta(hours=offset_hours))
    return naive.replace(tzinfo=tz)


def looks_like_location(line: str) -> bool:
    stripped = line.strip().rstrip("  ")
    if not stripped:
        return False
    if WEATHER_RE.match(stripped):
        return False
    if "°C" in stripped:
        return False
    if stripped.startswith("# "):
        return False
    if stripped.startswith("!"):
        return False
    # Day One export locations here are comma-delimited place strings.
    return "," in stripped


def normalize_location(line: str | None) -> str | None:
    if not line:
        return None
    stripped = line.strip().rstrip("  ")
    return stripped or None


def sanitize_filename(name: str) -> str:
    cleaned = INVALID_FILENAME_CHARS_RE.sub("-", name).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip(". ")
    return cleaned or "untitled"


def transform_body(lines: List[str]) -> str:
    out: List[str] = []
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            if out and out[-1] != "":
                out.append("")
            continue
        if IMAGE_LINE_RE.match(stripped) or OBSIDIAN_IMAGE_RE.match(stripped):
            continue
        if WEATHER_RE.match(stripped):
            continue
        if stripped.startswith("# "):
            text = stripped[2:].strip()
            if text:
                out.append(f"**{text}**")
            continue
        out.append(stripped)
    while out and out[-1] == "":
        out.pop()
    return "\n\n".join(chunk for chunk in collapse_paragraphs(out) if chunk)


def collapse_paragraphs(lines: List[str]) -> List[str]:
    paragraphs: List[str] = []
    buf: List[str] = []
    for line in lines:
        if line == "":
            if buf:
                paragraphs.append("\n".join(buf))
                buf = []
            continue
        buf.append(line)
    if buf:
        paragraphs.append("\n".join(buf))
    return paragraphs


def parse_entries(text: str) -> List[Entry]:
    lines = text.split("\n")
    indices: List[int] = []
    dts: List[datetime] = []
    for idx, line in enumerate(lines):
        dt = parse_dayone_heading(line)
        if dt is not None:
            indices.append(idx)
            dts.append(dt)
    entries: List[Entry] = []
    for i, start in enumerate(indices):
        end = indices[i + 1] if i + 1 < len(indices) else len(lines)
        chunk = lines[start + 1 : end]
        while chunk and not chunk[0].strip():
            chunk.pop(0)
        location = None
        if chunk and looks_like_location(chunk[0]):
            location = normalize_location(chunk.pop(0))
        while chunk and not chunk[0].strip():
            chunk.pop(0)
        if chunk and WEATHER_RE.match(chunk[0].strip()):
            chunk.pop(0)
        body = transform_body(chunk)
        if not body:
            continue
        entries.append(Entry(dt=dts[i], location=location, body=body))
    return entries


def has_dayone_tag(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    frontmatter_match = FRONTMATTER_RE.match(text)
    if not frontmatter_match:
        return False
    frontmatter = frontmatter_match.group(0)
    return "DayOne" in frontmatter


def render_note(entry: Entry) -> str:
    frontmatter = ["---", f"date: {entry.dt.date().isoformat()}", "tags: [DayOne]"]
    if entry.location:
        escaped = entry.location.replace('"', '\\"')
        frontmatter.append(f'location: "{escaped}"')
    frontmatter.append("---")
    return "\n".join(frontmatter) + "\n\n" + entry.body.strip() + "\n"


def plan_paths(entries: List[Entry]) -> List[PlanItem]:
    counters: dict[str, int] = {}
    plans: List[PlanItem] = []
    for entry in entries:
        date_str = entry.dt.date().isoformat()
        month_dir = TARGET_ROOT / entry.dt.strftime("%Y-%m")
        counters[date_str] = counters.get(date_str, 0) + 1
        suffix = "" if counters[date_str] == 1 else f"_{counters[date_str]}"
        candidate = month_dir / f"{date_str}{suffix}.md"
        overwrite = False
        if candidate.exists() and has_dayone_tag(candidate):
            overwrite = True
        elif candidate.exists():
            n = counters[date_str]
            while True:
                n += 1
                alt = month_dir / f"{date_str}_{n}.md"
                if not alt.exists() or has_dayone_tag(alt):
                    candidate = alt
                    overwrite = alt.exists()
                    counters[date_str] = n
                    break
        plans.append(PlanItem(entry=entry, path=candidate, overwrite=overwrite))
    return plans


def preview(plans: List[PlanItem], limit: int) -> None:
    print(f"Source markdown: {SOURCE_MD}")
    print(f"Target root: {TARGET_ROOT}")
    print(f"Entries parsed: {len(plans)}")
    print("Images/attachments: all removed from output")
    print()
    for idx, item in enumerate(plans[:limit], start=1):
        print(f"[{idx}] {item.entry.dt.isoformat()}  {item.path}")
        if item.entry.location:
            print(f"    location: {item.entry.location}")
        print(f"    mode: {'overwrite' if item.overwrite else 'create'}")
        print("    frontmatter+body preview:")
        note = render_note(item.entry).splitlines()
        for line in note[:14]:
            print(f"      {line}")
        if len(note) > 14:
            print("      ...")
        print()


def write_notes(plans: List[PlanItem]) -> None:
    written = 0
    overwritten = 0
    for item in plans:
        item.path.parent.mkdir(parents=True, exist_ok=True)
        item.path.write_text(render_note(item.entry), encoding="utf-8")
        written += 1
        if item.overwrite:
            overwritten += 1
    print(f"Wrote {written} notes ({overwritten} overwritten, {written - overwritten} created).")


def main() -> int:
    args = parse_args()
    if not SOURCE_MD.exists():
        print(f"Source file not found: {SOURCE_MD}", file=sys.stderr)
        return 1
    raw = SOURCE_MD.read_text(encoding="utf-8")
    text = strip_frontmatter(raw)
    entries = parse_entries(text)
    plans = plan_paths(entries)
    if not args.write:
        preview(plans, args.preview_limit)
        return 0
    write_notes(plans)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
