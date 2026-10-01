"""Extract GT6's per-block stack sizes from `Loader_MultiTileEntities.java`.

`aRegistry.add(name, category, id, creativeTab, class, toolQuality, stackSize, block, nbt, pattern…)`
carries the max stack size GT6 gives the item: 16 for machines, tool blocks and anvils, `64/size` for
wires, 64/32/16 for the larger item pipes, and so on. The port registered most of these blocks with
vanilla's default 64, which is what this table is for.

Usage: python tools/extract_gt6_stack_sizes.py [--json docs/gt6-stack-sizes.json]
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
GT6 = r"F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java"
SOURCE = os.path.join(GT6, "gregtech", "loaders", "b", "Loader_MultiTileEntities.java")

ADD = re.compile(r'aRegistry\.add\(\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*([\w.\[\]+* /()-]+?)\s*,\s*([\w.\[\]+* /()-]+?)\s*,'
                 r'\s*([\w.]+\.class)\s*,\s*([^,]+?)\s*,\s*([^,]+?)\s*,')
HELPER = re.compile(r'(\w+)\.(addItemPipes|addFluidPipes|addElectricWires)\(([^;]*)\)')


def statements(text: str) -> list[str]:
    out, buf, depth = [], "", 0
    for raw in text.splitlines():
        line = raw.split("//")[0]
        if not buf and not line.strip():
            continue
        buf += line + "\n"
        depth += line.count("(") - line.count(")")
        if depth <= 0:
            if buf.strip():
                out.append(buf)
            buf, depth = "", 0
    if buf.strip():
        out.append(buf)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default=None)
    parser.add_argument("--category", default=None, help="only show one category")
    args = parser.parse_args()

    text = open(SOURCE, encoding="utf-8", errors="replace").read()
    per_category: dict[str, Counter] = {}
    rows: list[dict] = []
    for stmt in statements(text):
        match = ADD.search(stmt)
        if match:
            name, category = match.group(1), match.group(2)
            stack = match.group(7).strip()
            if re.fullmatch(r"\d+", stack):
                per_category.setdefault(category, Counter())[int(stack)] += 1
                rows.append({"kind": "block", "name": name, "category": category, "stack": int(stack)})
        for helper in HELPER.finditer(stmt):
            if helper.group(2) != "addElectricWires":
                continue
            # addElectricWires registers 1x..16x wire (64/size) and cables (64,32,16,8,4)
            for size in range(1, 17):
                per_category.setdefault("Electric Wires", Counter())[max(1, 64 // size)] += 1
            for stack in (64, 32, 16, 8, 4):
                per_category.setdefault("Electric Wires", Counter())[stack] += 1

    print("stack sizes per GT6 category")
    for category in sorted(per_category):
        if args.category and category != args.category:
            continue
        counts = per_category[category]
        summary = ", ".join(f"{size}x{count}" for size, count in sorted(counts.items(), reverse=True))
        print(f"  {category:28} {summary}")
    if args.json:
        path = os.path.join(ROOT, args.json)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump({"categories": {k: dict(v) for k, v in sorted(per_category.items())},
                       "rows": rows}, handle, indent=2)
        print("wrote " + path)


if __name__ == "__main__":
    main()
