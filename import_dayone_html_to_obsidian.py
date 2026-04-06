#!/usr/bin/env python3
"""Import Day One HTML export entries into an Obsidian journal folder."""

from __future__ import annotations

import argparse
import re
import shutil
import signal
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote

from bs4 import BeautifulSoup
from markdownify import markdownify as md


DEFAULT_HTML = (
    "/Users/haoyuebai/Dev/wiznote-to-obsidian/dayoneExort/Export - 思维日记/"
    "%E6%80%9D%E7%BB%B4%E6%97%A5%E8%AE%B0.html"
)
DEFAULT_VAULT = (
    "/Users/haoyuebai/Library/Mobile Documents/iCloud~md~obsidian/Documents/"
    "wiznote_obsidian"
)
PRESETS = {
    "journal": {
        "html": (
            "/Users/haoyuebai/Dev/wiznote-to-obsidian/dayoneExort/Export - 思维日记/"
            "%E6%80%9D%E7%BB%B4%E6%97%A5%E8%AE%B0.html"
        ),
        "target_dir": "My Journals",
        "target_mode": "monthly",
        "filename_style": "date",
        "filename_prefix": "",
    },
    "pingpong": {
        "html": (
            "/Users/haoyuebai/Dev/wiznote-to-obsidian/dayoneExort/Export - 乒乒乓乓/"
            "%E4%B9%92%E4%B9%92%E4%B9%93%E4%B9%93.html"
        ),
        "target_dir": "乒乒乓乓",
        "target_mode": "flat",
        "filename_style": "date-prefix-city",
        "filename_prefix": "乒乓",
    },
    "tongji_course": {
        "html": (
            "/Users/haoyuebai/Dev/wiznote-to-obsidian/dayoneExort/Export - 听课笔记/"
            "%E5%90%AC%E8%AF%BE%E7%AC%94%E8%AE%B0.html"
        ),
        "target_dir": "课程笔记/同济",
        "target_mode": "flat",
        "filename_style": "h1",
        "filename_prefix": "",
    },
}
DATE_RE = re.compile(
    r"^(?P<prefix>.+?,\s+\d{1,2}\s+\w{3}\s+\d{4},\s+\d{1,2}:\d{2}\s+[AP]M)\s+GMT(?P<offset>[+-]\d{1,2})(?::?(?P<minutes>\d{2}))?$"
)
TZ_ABBREVIATIONS = {
    "UTC": "+0000",
    "GMT": "+0000",
    "PST": "-0800",
    "PDT": "-0700",
    "MST": "-0700",
    "MDT": "-0600",
    "CST": "-0600",
    "CDT": "-0500",
    "EST": "-0500",
    "EDT": "-0400",
    "JST": "+0900",
    "CST-CHINA": "+0800",
}
IMAGE_MD_RE = re.compile(r"!\[[^\]]*]\((photos/[^)\n]+)\)")
MULTIBLANK_RE = re.compile(r"\n{3,}")
WEATHER_ONLY_RE = re.compile(r"^-?\d+\s*°C\b", re.IGNORECASE)
INVALID_FILENAME_CHARS = re.compile(r'[\\/:\*\?"<>|]+')


@dataclass
class AttachmentPlan:
    source_rel: str
    source_path: Path
    dest_rel: str
    dest_path: Path


@dataclass
class EntryPlan:
    dt: datetime
    location: str | None
    title_hint: str | None
    filename: str
    month_dir: Path
    note_path: Path
    attachments: list[AttachmentPlan]
    content_md: str
    note_text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Import Day One HTML export entries into Obsidian using a preset type. "
            "Defaults to dry-run; use --write to actually create files."
        )
    )
    parser.add_argument(
        "note_type",
        choices=sorted(PRESETS.keys()),
        help="Preset import type, for example 'journal' or 'pingpong'.",
    )
    parser.add_argument(
        "--vault-root",
        default=DEFAULT_VAULT,
        help="Obsidian vault root that contains the target folders and 'attachments'.",
    )
    parser.add_argument(
        "--attachments-dir",
        default="attachments",
        help="Attachments directory name inside the vault root.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Actually create notes and copy attachments. Without this flag the script only previews.",
    )
    parser.add_argument(
        "--preview-limit",
        type=int,
        default=5,
        help="Number of notes to show detailed preview for during dry run.",
    )
    return parser.parse_args()


def parse_dayone_datetime(raw: str) -> datetime:
    text = " ".join(raw.split())
    match = DATE_RE.match(text)
    if match:
        prefix = match.group("prefix")
        offset_hours = int(match.group("offset"))
        offset_minutes = match.group("minutes") or "00"
        tz = f"{offset_hours:+03d}{offset_minutes}"
        normalized = f"{prefix} GMT{tz}"
        return datetime.strptime(normalized, "%A, %d %b %Y, %I:%M %p GMT%z")

    parts = text.rsplit(" ", 1)
    if len(parts) == 2:
        prefix, tz_name = parts
        tz_value = TZ_ABBREVIATIONS.get(tz_name.upper())
        if tz_value:
            normalized = f"{prefix} GMT{tz_value}"
            return datetime.strptime(normalized, "%A, %d %b %Y, %I:%M %p GMT%z")

    raise ValueError(f"unrecognized Day One datetime: {raw!r}")


def journal_name_from_html(html_path: Path) -> str:
    stem = unquote(html_path.stem)
    return stem if stem else html_path.parent.name.removeprefix("Export - ").strip()


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def normalize_location(location: str | None) -> str | None:
    if not location:
        return None

    text = re.sub(r"\s+", " ", location).strip()
    if not text:
        return None
    if WEATHER_ONLY_RE.match(text):
        return None
    return text


def sanitize_filename_part(text: str | None) -> str | None:
    if not text:
        return None
    value = re.sub(r"\s+", " ", text).strip()
    if not value:
        return None
    value = INVALID_FILENAME_CHARS.sub("-", value)
    value = value.rstrip(". ").strip()
    return value or None


def extract_city_from_location(location: str | None) -> str | None:
    location = normalize_location(location)
    if not location:
        return None

    parts = [part.strip() for part in location.split(",") if part.strip()]
    if not parts:
        return None

    municipalities = {"北京市", "上海市", "天津市", "重庆市"}
    if len(parts) >= 2 and parts[-1] == "中国" and parts[-2] in municipalities:
        city = parts[-2]
    elif len(parts) >= 3 and parts[-1] == "中国":
        city = parts[-3]
    elif len(parts) >= 2:
        city = parts[-2]
    else:
        city = parts[-1]

    city = re.sub(r'[\\/:\*\?"<>|]+', "-", city).strip()
    if not city:
        return None
    if WEATHER_ONLY_RE.match(city):
        return None
    return city


def make_filename(
    dt: datetime,
    sequence: int,
    filename_style: str,
    filename_prefix: str,
    location: str | None,
    title_hint: str | None,
) -> str:
    if filename_style == "h1":
        stem = sanitize_filename_part(title_hint) or dt.strftime("%Y-%m-%d")
        candidate = f"{stem}.md"
    elif filename_style == "date-prefix-city" and filename_prefix:
        city = extract_city_from_location(location)
        if city:
            candidate = f"{dt:%Y-%m-%d}-{filename_prefix}-{city}.md"
        else:
            candidate = f"{dt:%Y-%m-%d}-{filename_prefix}.md"
    elif filename_style == "date-prefix" and filename_prefix:
        candidate = f"{dt:%Y-%m-%d}-{filename_prefix}.md"
    else:
        candidate = f"{dt:%Y-%m-%d}.md"
    if sequence == 1:
        return candidate
    stem = Path(candidate).stem
    return f"{stem}_{sequence}.md"


def file_has_dayone_tag(note_path: Path) -> bool:
    if not note_path.exists() or not note_path.is_file():
        return False

    try:
        text = note_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False

    if not text.startswith("---\n"):
        return False

    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return False

    frontmatter = parts[0]
    return re.search(r"(?mi)^tags:\s*(?:\[[^\]]*\bDayOne\b[^\]]*\]|.*\bDayOne\b.*)$", frontmatter) is not None


def resolve_note_path(
    target_dir: Path,
    dt: datetime,
    sequence: int,
    filename_style: str,
    filename_prefix: str,
    location: str | None,
    title_hint: str | None,
) -> tuple[str, Path]:
    current = sequence
    while True:
        filename = make_filename(dt, current, filename_style, filename_prefix, location, title_hint)
        note_path = target_dir / filename
        if not note_path.exists() or file_has_dayone_tag(note_path):
            return filename, note_path
        current += 1


def build_attachment_plan(
    journal: str,
    uuid: str,
    source_rel: str,
    export_dir: Path,
    attachments_dir: Path,
) -> AttachmentPlan:
    source_path = export_dir / source_rel
    ext = source_path.suffix.lower()
    safe_journal = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff_-]+", "-", journal).strip("-") or "dayone"
    dest_name = f"dayone-{safe_journal}-{uuid[:12]}-{Path(source_rel).stem}{ext}"
    dest_path = attachments_dir / dest_name
    dest_rel = dest_path.relative_to(attachments_dir.parent).as_posix()
    return AttachmentPlan(
        source_rel=source_rel,
        source_path=source_path,
        dest_rel=dest_rel,
        dest_path=dest_path,
    )


def clean_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = IMAGE_MD_RE.sub(lambda m: m.group(0), text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = MULTIBLANK_RE.sub("\n\n", text)
    return text.strip()


def replace_markdown_images(text: str, attachments: Iterable[AttachmentPlan]) -> str:
    mapping = {item.source_rel: item.dest_rel for item in attachments}

    def repl(match: re.Match[str]) -> str:
        source_rel = match.group(1)
        dest_rel = mapping.get(source_rel)
        if not dest_rel:
            return match.group(0)
        return f"![[{dest_rel}]]"

    return IMAGE_MD_RE.sub(repl, text)


def entry_already_imported(month_dir: Path, uuid: str) -> Path | None:
    needle = f'dayone_uuid: "{uuid}"'
    if not month_dir.exists():
        return None
    for note_path in month_dir.glob("*.md"):
        try:
            text = note_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if needle in text:
            return note_path
    return None


def build_note_text(
    *,
    dt: datetime,
    location: str | None,
    attachments: list[AttachmentPlan],
    body: str,
) -> str:
    lines = [
        "---",
        f"date: {dt:%Y-%m-%d}",
        "tags: [DayOne]",
    ]
    if location:
        lines.append(f"location: {yaml_quote(location)}")

    lines.append("---")
    lines.append("")
    if body:
        lines.append(body)
    return "\n".join(lines).rstrip() + "\n"


def build_entry_plan(
    *,
    segment_html: str,
    journal: str,
    html_path: Path,
    attachments_root: Path,
    sequence: int,
) -> EntryPlan:
    segment_soup = BeautifulSoup(segment_html, "html.parser")
    entry = segment_soup.find("div", class_="entry")
    if entry is None:
        raise ValueError("segment missing .entry block")

    uuid = entry.get("entryuuid") or entry.get("entryUUID")
    if not uuid:
        raise ValueError("entry missing UUID")

    date_el = entry.find("h1", class_="date")
    if date_el is None:
        raise ValueError(f"entry {uuid} missing date")
    dt = parse_dayone_datetime(date_el.get_text(" ", strip=True))

    month_dir = Path()

    entry_copy = BeautifulSoup(segment_html, "html.parser")
    entry_node = entry_copy.find("div", class_="entry")
    if entry_node is None:
        raise ValueError(f"entry {uuid} could not be reparsed")

    location_div = entry_node.find("div", class_="location")
    location = None
    if location_div is not None:
        pieces = list(location_div.stripped_strings)
        if pieces:
            location = normalize_location(pieces[0])

    title_hint = None
    for heading in entry_copy.find_all("h1"):
        if "date" in (heading.get("class") or []):
            continue
        title_hint = sanitize_filename_part(heading.get_text(" ", strip=True))
        if title_hint:
            break

    attachments: list[AttachmentPlan] = []
    for img in entry_copy.find_all("img"):
        src = (img.get("src") or "").strip()
        if src.startswith("photos/"):
            attachments.append(
                build_attachment_plan(
                    journal=journal,
                    uuid=uuid,
                    source_rel=src,
                    export_dir=html_path.parent,
                    attachments_dir=attachments_root,
                )
            )

    for selector in ("div.header", "div.location", "img.weather-icon"):
        found = entry_node.select_one(selector)
        if found is not None:
            found.decompose()

    for anchor in entry_node.find_all("a", href=True):
        if anchor.get("href", "").startswith("dayone2://"):
            anchor.decompose()

    if not entry_node.get_text(strip=True) and not entry_node.find(["img", "p", "ul", "ol", "blockquote"]):
        entry_node.decompose()

    # Day One export often uses heading tags for the opening sentence. Keep them as
    # emphasized body text instead of markdown headings.
    for heading in entry_copy.find_all(re.compile(r"^h[1-6]$")):
        heading.name = "strong"

    content_html = entry_copy.decode_contents().strip()
    content_md = md(content_html, heading_style="ATX", bullets="-")
    content_md = replace_markdown_images(content_md, attachments)
    content_md = clean_markdown(content_md)

    filename = make_filename(dt, sequence, "date", "", location, title_hint)
    note_path = Path(filename)
    note_text = build_note_text(
        dt=dt,
        location=location,
        attachments=attachments,
        body=content_md,
    )

    return EntryPlan(
        dt=dt,
        location=location,
        title_hint=title_hint,
        filename=filename,
        month_dir=month_dir,
        note_path=note_path,
        attachments=attachments,
        content_md=content_md,
        note_text=note_text,
    )


def load_existing_names(journals_root: Path) -> dict[Path, set[str]]:
    mapping: dict[Path, set[str]] = {}
    if not journals_root.exists():
        return mapping
    for month_dir in journals_root.iterdir():
        if month_dir.is_dir():
            mapping[month_dir] = {path.name for path in month_dir.glob("*.md")}
    return mapping


def build_plans(
    html_path: Path,
    target_root: Path,
    attachments_root: Path,
    target_mode: str,
    filename_style: str,
    filename_prefix: str,
) -> list[EntryPlan]:
    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
    journal = journal_name_from_html(html_path)

    starts = [match.start() for match in re.finditer(r"<div class='entry'", html_text)]
    plans: list[EntryPlan] = []
    sequence_by_day: dict[str, int] = {}
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(html_text)
        segment_html = html_text[start:end]
        segment_soup = BeautifulSoup(segment_html, "html.parser")
        entry = segment_soup.find("div", class_="entry")
        if entry is None:
            continue
        date_el = entry.find("h1", class_="date")
        if date_el is None:
            continue
        dt = parse_dayone_datetime(date_el.get_text(" ", strip=True))
        day_key = dt.strftime("%Y-%m-%d")
        sequence_by_day[day_key] = sequence_by_day.get(day_key, 0) + 1
        plan = build_entry_plan(
            segment_html=segment_html,
            journal=journal,
            html_path=html_path,
            attachments_root=attachments_root,
            sequence=sequence_by_day[day_key],
        )
        plan.month_dir = target_root / f"{plan.dt:%Y-%m}" if target_mode == "monthly" else target_root
        plan.filename, plan.note_path = resolve_note_path(
            plan.month_dir,
            plan.dt,
            sequence_by_day[day_key],
            filename_style,
            filename_prefix,
            plan.location,
            plan.title_hint,
        )
        plans.append(plan)
    return plans


def print_preview(plans: list[EntryPlan], preview_limit: int) -> None:
    print(f"Planned entries: {len(plans)}")
    print(f"Detailed preview: first {min(preview_limit, len(plans))} entries\n")
    for index, plan in enumerate(plans[:preview_limit], start=1):
        print(f"[{index}] {plan.dt:%Y-%m-%d %H:%M}  {plan.note_path}")
        if plan.location:
            print(f"    location: {plan.location}")
        if plan.attachments:
            print("    attachments:")
            for attachment in plan.attachments[:5]:
                print(f"      - {attachment.source_rel} -> {attachment.dest_rel}")
            if len(plan.attachments) > 5:
                print(f"      - ... {len(plan.attachments) - 5} more")
        print("    frontmatter+body preview:")
        preview_text = "\n".join(plan.note_text.splitlines()[:20])
        print(indent_block(preview_text, "      "))
        print("")

    month_counts: dict[str, int] = {}
    attachment_count = 0
    for plan in plans:
        month_counts[plan.month_dir.name] = month_counts.get(plan.month_dir.name, 0) + 1
        attachment_count += len(plan.attachments)

    print("Month distribution:")
    for month, count in sorted(month_counts.items()):
        print(f"  {month}: {count}")
    print(f"\nTotal attachment copies: {attachment_count}")


def indent_block(text: str, prefix: str) -> str:
    return "\n".join(f"{prefix}{line}" for line in text.splitlines())


def execute_write(plans: list[EntryPlan], attachments_root: Path) -> None:
    copied_attachments = 0
    written_notes = 0

    attachments_root.mkdir(parents=True, exist_ok=True)

    for plan in plans:
        plan.month_dir.mkdir(parents=True, exist_ok=True)

        for attachment in plan.attachments:
            if not attachment.source_path.exists():
                raise FileNotFoundError(f"missing attachment: {attachment.source_path}")
            if not attachment.dest_path.exists():
                shutil.copy2(attachment.source_path, attachment.dest_path)
                copied_attachments += 1

        plan.note_path.write_text(plan.note_text, encoding="utf-8")
        written_notes += 1
        print(f"WROTE {plan.note_path}")

    print(f"\nCompleted: wrote {written_notes} notes and copied {copied_attachments} attachments.")


def main() -> int:
    args = parse_args()
    preset = PRESETS[args.note_type]
    html_path = Path(preset["html"]).expanduser().resolve()
    vault_root = Path(args.vault_root).expanduser().resolve()
    target_root = vault_root / preset["target_dir"]
    attachments_root = vault_root / args.attachments_dir

    if not html_path.is_file():
        raise SystemExit(f"html not found: {html_path}")
    if not vault_root.is_dir():
        raise SystemExit(f"vault root not found: {vault_root}")
    if not target_root.exists() and not args.write:
        print(f"target directory will be created on write: {target_root}")

    plans = build_plans(
        html_path,
        target_root,
        attachments_root,
        preset["target_mode"],
        preset["filename_style"],
        preset["filename_prefix"],
    )
    if not plans:
        print("No Day One entries found.")
        return 0

    if not args.write:
        print_preview(plans, args.preview_limit)
        print("\nDry run only. Re-run with --write to create notes and attachments.")
        return 0

    execute_write(plans, attachments_root)
    return 0


if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    raise SystemExit(main())
