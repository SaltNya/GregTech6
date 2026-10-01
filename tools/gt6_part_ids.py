#!/usr/bin/env python3
"""List GT6 multiblock part ids (walls, coils, parts, controllers) with their names.

Usage: python tools/gt6_part_ids.py [--used] 
  --used : only ids referenced by the extracted multiblock crafting recipes
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

SOURCE = Path(
    r"F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java"
    r"\gregtech\loaders\b\Loader_MultiTileEntities.java"
)
MULTIBLOCK_JSON = Path(__file__).with_name("gt6_multiblock_recipes.json")


def part_name(text: str) -> str:
    """Best-effort part name from the registration arguments."""
    m = re.search(r'UT\.NBT\.make\(', text)
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--used", action="store_true")
    ap.add_argument("--range", default="18000-18120,17200-17220")
    args = ap.parse_args()

    wanted: set[int] = set()
    for part in args.range.split(","):
        lo, _, hi = part.partition("-")
        wanted.update(range(int(lo), int(hi) + 1))

    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    entries: dict[int, str] = {}
    for m in re.finditer(r'aRegistry\.add\(\s*"([^"]*)"', text):
        tail = text[m.start():m.start() + 400]
        idm = re.search(r'"Multiblock Machines"\s*,\s*(\d+)\s*,', tail)
        if idm:
            entries[int(idm.group(1))] = m.group(1).strip()

    used: Counter[int] = Counter()
    if args.used:
        data = json.loads(MULTIBLOCK_JSON.read_text(encoding="utf-8"))
        for e in data["entries"]:
            for value in e["keys"].values():
                idm = re.fullmatch(r"aRegistry\.getItem\((\d+)\)", value.strip())
                if idm:
                    used[int(idm.group(1))] += 1
        print("== part ids referenced by multiblock crafting recipes ==")
        for pid in sorted(used):
            print("  %-6d %-44s x%d" % (pid, entries.get(pid, "<not found>"), used[pid]))
        return 0

    print("== GT6 Multiblock Machines tab registrations ==")
    for pid in sorted(entries):
        if pid in wanted or not wanted:
            print("  %-6d %s" % (pid, entries[pid]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
