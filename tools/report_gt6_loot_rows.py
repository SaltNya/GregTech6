"""Summarise docs/gt6-loot-rows.json: rows per table, skip reasons, and the vanilla-table rows.

Usage:  python tools/report_gt6_loot_rows.py
"""

from __future__ import annotations

import collections
import json
import pathlib

REPORT = pathlib.Path("docs/gt6-loot-rows.json")


def main() -> None:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    print(f"rows {data['rows']}, skipped {data['skipped']}")
    print("--- rows per table ---")
    for table, count in sorted(data["perTable"].items()):
        print(f"  {table:28} {count:4}")

    print("--- skip reasons (recorded sample) ---")
    for reason, count in collections.Counter(r["reason"] for r in data["skippedRows"]).most_common():
        print(f"  {count:4}  {reason}")

    print("--- rows added to the vanilla chest tables ---")
    for row in data["vanillaRows"]:
        table = row["table"].replace("van.", "")
        print(f"  {table:24} w{row['weight']:<5} {row['min']}-{row['max']:<3} {row['spec']}")


if __name__ == "__main__":
    main()
