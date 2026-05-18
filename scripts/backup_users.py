#!/usr/bin/env python3
"""Create a daily backup of data/user.json and keep the last 14 days.

Run this script from cron or a scheduler once per day.
"""

from pathlib import Path
import datetime
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
USER_FILE = DATA_DIR / "user.json"
BACKUP_DIR = DATA_DIR / "backups"
KEEP_DAYS = 14


def main():
    if not USER_FILE.exists():
        print(f"User file not found: {USER_FILE}", file=sys.stderr)
        return 2

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.datetime.utcnow()
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    dest = BACKUP_DIR / f"users-{stamp}.json"

    # Copy file contents (validate JSON but still write even if invalid)
    content = USER_FILE.read_text(encoding="utf-8")
    try:
        json.loads(content)
    except Exception as exc:
        print(f"Warning: {USER_FILE} is not valid JSON: {exc}", file=sys.stderr)

    dest.write_text(content, encoding="utf-8")
    print(f"Wrote backup: {dest}")

    # Prune old backups
    cutoff = now - datetime.timedelta(days=KEEP_DAYS)
    for p in sorted(BACKUP_DIR.glob("users-*.json")):
        try:
            mtime = datetime.datetime.utcfromtimestamp(p.stat().st_mtime)
            if mtime < cutoff:
                p.unlink()
                print(f"Removed old backup: {p}")
        except Exception as exc:
            print(f"Failed to consider {p}: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
