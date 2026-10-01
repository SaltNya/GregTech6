"""Search GT6's Java sources for crafting recipes by *statement* (multi-line calls included).

Line-based greps miss calls that are formatted across several lines, which is exactly how GT6 writes
many of its `CR.shaped(...)`/`CR.shapeless(...)` recipes. This tool joins each statement by paren
balance and then matches a regex against the whole statement.

Usage:
  python tools/search_gt6_statements.py "wireGt0?1\\.mat" "CR\\.shaped"
  python tools/search_gt6_statements.py --any "wirecutter" --any "CR\\."
"""

from __future__ import annotations

import argparse
import os
import re

GT6 = r"F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java"


def statements(path: str):
    text = open(path, encoding="utf-8", errors="replace").read()
    buf, depth = "", 0
    for raw in text.splitlines():
        line = raw.split("//")[0]
        if not buf and not line.strip():
            continue
        buf += line + "\n"
        depth += line.count("(") - line.count(")")
        if depth <= 0:
            if buf.strip():
                yield buf
            buf, depth = "", 0
    if buf.strip():
        yield buf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("patterns", nargs="+", help="all patterns must match the statement")
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()
    compiled = [re.compile(p) for p in args.patterns]

    hits = 0
    for base, _, files in os.walk(GT6):
        for name in files:
            if not name.endswith(".java"):
                continue
            path = os.path.join(base, name)
            for statement in statements(path):
                if not all(c.search(statement) for c in compiled):
                    continue
                flat = " ".join(statement.split())
                print(f"{name}: {flat[:400]}")
                hits += 1
                if hits >= args.limit:
                    print(f"... (stopped at {args.limit} hits)")
                    return
    print(f"{hits} matching statements")


if __name__ == "__main__":
    main()
