#!/usr/bin/env python3
"""
附件引用检查与清理工具

用途：
1. 列出 attachments/ 中符合正则的候选附件，以及它们被哪些笔记引用。
2. 生成 review 用的 Markdown 清单（推荐：按尺寸和文件名模式筛风景图）。
3. 列出 Markdown 中已经失效的本地图片引用。
4. 按需删除“单独占一行”的失效图片引用（默认 dry-run）。
"""

from __future__ import annotations

import argparse
import shutil
import re
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}
DEFAULT_PATTERN = r"(1920x1080|_ZH-CN|_ROW|RE\w+_1920x1080)"


@dataclass
class Reference:
    note_path: Path
    line_no: int
    raw: str
    target: str
    kind: str
    resolved_path: Path
    exists: bool

    @property
    def is_image(self) -> bool:
        target = self.target.lower()
        if target.startswith("data:image/"):
            return True
        return Path(target).suffix.lower() in IMAGE_EXTENSIONS

    @property
    def is_local(self) -> bool:
        return not self.target.startswith(
            ("http://", "https://", "mailto:", "data:", "wiz://", "#", "//")
        )


class AttachmentRefCleaner:
    def __init__(self, vault_dir: Path):
        self.vault_dir = vault_dir
        self.attachments_dir = vault_dir / "attachments"

    def backup_note(self, note_path: Path) -> None:
        backup_path = Path(str(note_path) + ".refcleanbak")
        if backup_path.exists():
            return
        shutil.copy2(note_path, backup_path)

    def markdown_files(self) -> Iterable[Path]:
        return sorted(self.vault_dir.rglob("*.md"))

    def scan_references(self) -> list[Reference]:
        refs: list[Reference] = []
        wiki_pattern = re.compile(r"(!)?\[\[([^\]|#]+)(?:#[^\]]+)?(?:\|[^\]]+)?\]\]")
        md_pattern = re.compile(r"(!)?\[[^\]]*\]\(([^)]+)\)")

        for note_path in self.markdown_files():
            text = note_path.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(text.splitlines(), 1):
                for match in wiki_pattern.finditer(line):
                    target = match.group(2).strip().strip("<>")
                    resolved = (self.vault_dir / target).resolve()
                    refs.append(
                        Reference(
                            note_path=note_path,
                            line_no=line_no,
                            raw=match.group(0),
                            target=target,
                            kind="wiki_embed" if match.group(1) else "wiki_link",
                            resolved_path=resolved,
                            exists=resolved.exists(),
                        )
                    )

                for match in md_pattern.finditer(line):
                    target = match.group(2).strip().strip("<>")
                    if target.startswith("/"):
                        resolved = (self.vault_dir / target.lstrip("/")).resolve()
                    else:
                        resolved = (note_path.parent / target).resolve()
                    refs.append(
                        Reference(
                            note_path=note_path,
                            line_no=line_no,
                            raw=match.group(0),
                            target=target,
                            kind="md_image" if match.group(1) else "md_link",
                            resolved_path=resolved,
                            exists=resolved.exists(),
                        )
                    )

        return refs

    def candidate_attachments(self, pattern: str) -> list[Path]:
        if not self.attachments_dir.exists():
            return []
        compiled = re.compile(pattern, re.IGNORECASE)
        return sorted(
            [path for path in self.attachments_dir.iterdir() if path.is_file() and compiled.search(path.name)],
            key=lambda p: p.name.lower(),
        )

    def image_dimensions(self, image_path: Path) -> tuple[int | None, int | None]:
        suffix = image_path.suffix.lower()
        try:
            if suffix == ".png":
                with image_path.open("rb") as f:
                    header = f.read(24)
                if header[:8] != b"\x89PNG\r\n\x1a\n":
                    return None, None
                width, height = struct.unpack(">II", header[16:24])
                return width, height

            if suffix in {".jpg", ".jpeg"}:
                with image_path.open("rb") as f:
                    if f.read(2) != b"\xff\xd8":
                        return None, None
                    while True:
                        marker_prefix = f.read(1)
                        if not marker_prefix:
                            return None, None
                        if marker_prefix != b"\xff":
                            continue
                        marker = f.read(1)
                        while marker == b"\xff":
                            marker = f.read(1)
                        if marker in {b"\xc0", b"\xc1", b"\xc2", b"\xc3", b"\xc5", b"\xc6", b"\xc7", b"\xc9", b"\xca", b"\xcb", b"\xcd", b"\xce", b"\xcf"}:
                            length = struct.unpack(">H", f.read(2))[0]
                            _precision = f.read(1)
                            height, width = struct.unpack(">HH", f.read(4))
                            return width, height
                        if marker in {b"\xd8", b"\xd9"}:
                            continue
                        length_bytes = f.read(2)
                        if len(length_bytes) != 2:
                            return None, None
                        length = struct.unpack(">H", length_bytes)[0]
                        f.seek(length - 2, 1)

            if suffix == ".gif":
                with image_path.open("rb") as f:
                    header = f.read(10)
                if header[:6] not in {b"GIF87a", b"GIF89a"}:
                    return None, None
                width, height = struct.unpack("<HH", header[6:10])
                return width, height

            if suffix == ".bmp":
                with image_path.open("rb") as f:
                    header = f.read(26)
                if header[:2] != b"BM":
                    return None, None
                width, height = struct.unpack("<II", header[18:26])
                return width, height
        except Exception:
            return None, None

        return None, None

    def format_size(self, size: int) -> str:
        units = ["B", "KB", "MB", "GB"]
        value = float(size)
        unit = units[0]
        for unit in units:
            if value < 1024 or unit == units[-1]:
                break
            value /= 1024
        if unit == "B":
            return f"{int(value)} {unit}"
        return f"{value:.1f} {unit}"

    def scenic_reasons(
        self,
        attachment: Path,
        width: int | None,
        height: int | None,
        filename_pattern: re.Pattern[str],
        target_width: int,
        target_height: int,
    ) -> list[str]:
        reasons: list[str] = []
        if width == target_width and height == target_height:
            reasons.append(f"size={target_width}x{target_height}")
        if filename_pattern.search(attachment.name):
            reasons.append("name-pattern")
        return reasons

    def refs_for_attachment(self, attachment: Path, refs: list[Reference]) -> list[Reference]:
        return [
            ref for ref in refs
            if ref.is_local and attachment.name == Path(ref.target).name
        ]

    def report_pattern(self, pattern: str) -> int:
        if not self.attachments_dir.exists():
            print(f"附件目录不存在: {self.attachments_dir}")
            return 1

        refs = self.scan_references()
        matched_files = self.candidate_attachments(pattern)

        print(f"Vault: {self.vault_dir}")
        print(f"附件目录: {self.attachments_dir}")
        print(f"匹配到 {len(matched_files)} 个附件\n")

        for attachment in matched_files:
            matched_refs = self.refs_for_attachment(attachment, refs)
            print(f"- {attachment.name}")
            if matched_refs:
                for ref in matched_refs:
                    rel = ref.note_path.relative_to(self.vault_dir)
                    print(f"  引用: {rel}:{ref.line_no}")
            else:
                print("  引用: 无")
            print()

        return 0

    def write_scenic_checklist(
        self,
        output_path: Path,
        target_width: int,
        target_height: int,
        filename_pattern: str,
    ) -> int:
        refs = self.scan_references()
        compiled = re.compile(filename_pattern, re.IGNORECASE)
        candidates: list[tuple[Path, int | None, int | None, str, list[Reference], list[str]]] = []

        if not self.attachments_dir.exists():
            print(f"附件目录不存在: {self.attachments_dir}")
            return 1

        for attachment in sorted(self.attachments_dir.iterdir(), key=lambda p: p.name.lower()):
            if not attachment.is_file() or attachment.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            width, height = self.image_dimensions(attachment)
            reasons = self.scenic_reasons(
                attachment=attachment,
                width=width,
                height=height,
                filename_pattern=compiled,
                target_width=target_width,
                target_height=target_height,
            )
            if not reasons:
                continue
            matched_refs = self.refs_for_attachment(attachment, refs)
            candidates.append(
                (attachment, width, height, self.format_size(attachment.stat().st_size), matched_refs, reasons)
            )

        lines = [
            "# 风景图候选清单",
            "",
            f"- Vault: `{self.vault_dir}`",
            f"- 附件目录: `{self.attachments_dir}`",
            f"- 高优先级尺寸: `{target_width}x{target_height}`",
            f"- 文件名模式: `{filename_pattern}`",
            f"- 候选数量: `{len(candidates)}`",
            "",
            "说明：",
            "- `high`：命中 1920x1080，或同时命中尺寸和文件名模式。",
            "- `review`：未命中尺寸，但命中文件名模式。",
            "- 勾选表示你打算删除这个附件文件。",
            "",
        ]

        for attachment, width, height, size_str, matched_refs, reasons in candidates:
            level = "high" if f"size={target_width}x{target_height}" in reasons else "review"
            dimensions = f"{width}x{height}" if width and height else "unknown"
            reason_str = ", ".join(reasons)
            lines.append(f"- [ ] `{attachment.name}`")
            lines.append(f"  level: `{level}`")
            lines.append(f"  size: `{size_str}`")
            lines.append(f"  dimensions: `{dimensions}`")
            lines.append(f"  reasons: `{reason_str}`")
            if matched_refs:
                for ref in matched_refs:
                    rel = ref.note_path.relative_to(self.vault_dir)
                    lines.append(f"  引用: `{rel}:{ref.line_no}`")
            else:
                lines.append("  引用: `无`")
            lines.append("")

        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"已生成风景图清单: {output_path}")
        return 0

    def missing_image_refs(self) -> list[Reference]:
        return [
            ref
            for ref in self.scan_references()
            if ref.is_local and ref.is_image and not ref.exists
        ]

    def report_missing(self) -> int:
        missing = self.missing_image_refs()
        print(f"发现 {len(missing)} 个失效的本地图片引用\n")

        for ref in missing:
            rel = ref.note_path.relative_to(self.vault_dir)
            print(f"- {rel}:{ref.line_no}")
            print(f"  类型: {ref.kind}")
            print(f"  目标: {ref.target}")
            print(f"  片段: {ref.raw}")
            print()

        return 0

    def remove_missing_lines(self, apply: bool) -> int:
        missing_by_file: dict[Path, set[int]] = {}
        removable: list[Reference] = []

        for ref in self.missing_image_refs():
            line = ref.note_path.read_text(encoding="utf-8", errors="ignore").splitlines()[ref.line_no - 1]
            if line.strip() == ref.raw.strip():
                missing_by_file.setdefault(ref.note_path, set()).add(ref.line_no)
                removable.append(ref)

        print(f"可删除的失效图片行: {len(removable)}")
        print(f"模式: {'实际写入' if apply else 'dry-run'}\n")

        for ref in removable:
            rel = ref.note_path.relative_to(self.vault_dir)
            print(f"- {rel}:{ref.line_no} -> {ref.target}")

        if not apply or not removable:
            return 0

        for note_path, line_numbers in missing_by_file.items():
            lines = note_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            kept_lines = [
                line for idx, line in enumerate(lines, 1)
                if idx not in line_numbers
            ]
            note_path.write_text("\n".join(kept_lines) + "\n", encoding="utf-8")

        return 0

    def repair_local_image_refs(self, backup_dir: Path, apply: bool, remove_unrecoverable: bool) -> int:
        self.attachments_dir.mkdir(parents=True, exist_ok=True)
        image_line_pattern = re.compile(r'(!\[[^\]]*\]\()(.+)(\))')
        updated_notes: dict[Path, list[str]] = {}
        repaired = 0
        removed = 0
        unrecoverable: list[tuple[Path, int, str]] = []

        for note_path in self.markdown_files():
            lines = note_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            note_changed = False

            for idx, line in enumerate(lines):
                if "![" not in line or "data:image/" in line or "wiz://" in line:
                    continue

                match = image_line_pattern.search(line)
                if not match:
                    continue

                prefix, target, suffix = match.groups()
                stripped = target.strip()
                if stripped.startswith(("http://", "https://", "attachments/")):
                    continue
                if stripped.startswith("<") and stripped.endswith(">"):
                    stripped = stripped[1:-1].strip()

                basename = None
                if "_files/" in stripped:
                    basename = Path(stripped.split("_files/", 1)[1]).name
                elif "/" not in stripped:
                    basename = Path(stripped).name
                else:
                    continue

                backup_source = backup_dir / basename
                if backup_source.exists():
                    dest = self.attachments_dir / basename
                    replacement = f"{prefix}attachments/{basename}{suffix}"
                    if line == replacement:
                        continue
                    if apply:
                        if not dest.exists():
                            shutil.copy2(backup_source, dest)
                    lines[idx] = replacement
                    repaired += 1
                    note_changed = True
                    continue

                unrecoverable.append((note_path, idx + 1, basename))
                if remove_unrecoverable and line.strip() == line.strip():
                    lines[idx] = ""
                    removed += 1
                    note_changed = True

            if note_changed:
                updated_notes[note_path] = lines

        print(f"Recoverable image refs rewritten: {repaired}")
        print(f"Unrecoverable image refs removed: {removed}")
        print(f"Unrecoverable image refs remaining: {len(unrecoverable) - removed}")

        if unrecoverable:
            print("\nUnrecoverable refs:")
            for note_path, line_no, basename in unrecoverable[:50]:
                rel = note_path.relative_to(self.vault_dir)
                print(f"- {rel}:{line_no} -> {basename}")
            if len(unrecoverable) > 50:
                print(f"... and {len(unrecoverable) - 50} more")

        if not apply:
            return 0

        for note_path, lines in updated_notes.items():
            self.backup_note(note_path)
            text = "\n".join(lines).replace("\n\n\n", "\n\n")
            note_path.write_text(text.rstrip() + "\n", encoding="utf-8")

        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="检查并清理 Obsidian 附件引用")
    parser.add_argument(
        "--vault-dir",
        default="wiznote_obsidian",
        help="Obsidian vault 目录，默认: wiznote_obsidian",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    pattern_parser = subparsers.add_parser(
        "report-pattern",
        help="按附件文件名正则列出候选附件和引用位置",
    )
    pattern_parser.add_argument(
        "--pattern",
        default=DEFAULT_PATTERN,
        help="Python 正则",
    )

    checklist_parser = subparsers.add_parser(
        "write-checklist",
        help="生成 review 用的候选清单（默认按 1920x1080 + 文件名模式）",
    )
    checklist_parser.add_argument(
        "--output",
        default="fix_attachment_review_checklist.md",
        help="输出 Markdown 路径",
    )
    checklist_parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="目标宽度，默认 1920",
    )
    checklist_parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="目标高度，默认 1080",
    )
    checklist_parser.add_argument(
        "--pattern",
        default=DEFAULT_PATTERN,
        help="用于辅助判断风景图的文件名正则",
    )

    subparsers.add_parser(
        "report-missing",
        help="列出所有失效的本地图片引用",
    )

    remove_parser = subparsers.add_parser(
        "remove-missing-lines",
        help="删除单独占一行的失效图片引用",
    )
    remove_parser.add_argument(
        "--apply",
        action="store_true",
        help="实际写入；默认只预览",
    )

    repair_parser = subparsers.add_parser(
        "repair-local-image-refs",
        help="从备份 attachments 恢复本地图片引用，并可删除无法恢复的失效图片行",
    )
    repair_parser.add_argument(
        "--backup-dir",
        default=str(Path.home() / "Desktop" / "attachments"),
        help="用于恢复图片文件的备份 attachments 目录",
    )
    repair_parser.add_argument(
        "--remove-unrecoverable",
        action="store_true",
        help="删除无法从备份恢复的失效图片引用行",
    )
    repair_parser.add_argument(
        "--apply",
        action="store_true",
        help="实际写入；默认只预览",
    )

    args = parser.parse_args()
    cleaner = AttachmentRefCleaner(Path(args.vault_dir))

    if args.command == "report-pattern":
        return cleaner.report_pattern(args.pattern)
    if args.command == "write-checklist":
        return cleaner.write_scenic_checklist(
            output_path=Path(args.output),
            target_width=args.width,
            target_height=args.height,
            filename_pattern=args.pattern,
        )
    if args.command == "report-missing":
        return cleaner.report_missing()
    if args.command == "remove-missing-lines":
        return cleaner.remove_missing_lines(apply=args.apply)
    if args.command == "repair-local-image-refs":
        return cleaner.repair_local_image_refs(
            backup_dir=Path(args.backup_dir),
            apply=args.apply,
            remove_unrecoverable=args.remove_unrecoverable,
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
