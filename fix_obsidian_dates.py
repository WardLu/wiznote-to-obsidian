#!/usr/bin/env python3
import argparse
import os
import re
from datetime import datetime
from pathlib import Path

def timestamp_to_date(ts):
    try:
        ts = int(ts)
        # Check if it's milliseconds or seconds
        if ts > 1e12:
            ts = ts / 1000
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    except:
        return None

def process_file(filepath, dry_run=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find date: timestamp pattern
    new_content = content
    for match in re.finditer(r'^date:\s*(\d+)$', content, re.MULTILINE):
        ts = match.group(1)
        date_str = timestamp_to_date(ts)
        if date_str:
            new_content = new_content.replace(f'date: {ts}', f'date: {date_str}')
    
    if new_content != content:
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        return True
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert Obsidian frontmatter date timestamps to YYYY-MM-DD"
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
    for root, dirs, files in os.walk(base):
        # Process md files
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                if process_file(filepath, dry_run=args.dry_run):
                    action = "Would fix" if args.dry_run else "Fixed"
                    print(f"{action}: {filepath}")
                    count += 1
        
        # Delete empty _files folders
        if args.dry_run:
            continue

        for d in list(dirs):
            if d.endswith('_files'):
                dirpath = os.path.join(root, d)
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)
                    print(f"Deleted empty folder: {dirpath}")
    
    summary = "would be fixed" if args.dry_run else "fixed"
    print(f"\nTotal files {summary}: {count}")

if __name__ == "__main__":
    main()
