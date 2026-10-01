#!/usr/bin/env python3
"""Count how many recipes GT6 registers into each RecipeMap (RM.*) in the original source.

Used to size the remaining work for the port's empty recipe maps.
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

ORIGINAL = Path(r"F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java")

# RM.<Map>.<method>(  — plus the ore-dict/loader helper forms used for bulk registration.
CALL = re.compile(r"\bRM\.(\w+)\s*\.\s*(\w+)\s*\(")
DEFAULT_MAPS = {"Furnace", "Roaster", "Distiller", "Shredder", "Crusher", "Sifter"}


def main() -> int:
    want = set(sys.argv[1:])
    counts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    files: dict[str, set[str]] = collections.defaultdict(set)
    for path in ORIGINAL.rglob("*.java"):
        # 1.7.10 cross-mod compat recipes do not apply to the 1.20.1 port.
        if "Compat_" in path.name or "/compat/" in path.as_posix():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in CALL.finditer(text):
            machine, method = m.group(1), m.group(2)
            counts[machine][method] += 1
            files[machine].add(path.name)
    rows = sorted(counts.items(), key=lambda kv: -sum(kv[1].values()))
    for machine, methods in rows:
        if want and machine not in want:
            continue
        adds = sum(n for method, n in methods.items() if method.startswith("add"))
        total = sum(methods.values())
        where = ",".join(sorted(files[machine])[:3])
        print("%-24s add=%-5d total=%-5d  %s" % (machine, adds, total, where))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
