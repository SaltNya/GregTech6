"""Extract GT6 `aRegistry.add(...)` block recipes (pattern + keys) for chosen categories.

`Loader_MultiTileEntities` registers every multi-tile block with its crafting pattern as trailing
arguments of `aRegistry.add(...)`: `"pattern", "pattern", 'K', <ingredient>, …`. This pulls them out
per category so the port can add the missing crafting recipes (storage, chests, anvils, ...) with the
original patterns instead of guessing.

Usage:
  python tools/extract_gt6_block_recipes.py Storage Chests "Misc Tool Blocks"
  python tools/extract_gt6_block_recipes.py Anvil --contains
"""

from __future__ import annotations

import argparse
import os
import re

GT6 = r"F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java"
SOURCE = os.path.join(GT6, "gregtech", "loaders", "b", "Loader_MultiTileEntities.java")

ADD_START = re.compile(r'aRegistry\.add\(')


def statements(text: str):
    """Yield (line_number, statement) with parens balanced, so multi-line calls stay whole."""
    buf, depth, start = "", 0, 1
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("//")[0]
        if not buf and not line.strip():
            continue
        if not buf:
            start = number
        buf += line + "\n"
        depth += line.count("(") - line.count(")")
        if depth <= 0:
            if buf.strip():
                yield start, buf
            buf, depth = "", 0
    if buf.strip():
        yield start, buf


def split_args(statement: str) -> list[str]:
    inner = statement[statement.index("(") + 1 : statement.rindex(")")]
    args, current, depth, in_string = [], "", 0, False
    for index, ch in enumerate(inner):
        if ch == '"' and (index == 0 or inner[index - 1] != "\\"):
            in_string = not in_string
        if in_string:
            current += ch
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            args.append(current.strip())
            current = ""
            continue
        current += ch
    if current.strip():
        args.append(current.strip())
    return args


def add_calls(statement: str):
    """Yield each `aRegistry.add(...)` argument list in a statement (several can share a line)."""
    start = 0
    while True:
        index = statement.find("aRegistry.add(", start)
        if index < 0:
            return
        depth, position = 0, statement.index("(", index)
        for position in range(statement.index("(", index), len(statement)):
            if statement[position] == "(":
                depth += 1
            elif statement[position] == ")":
                depth -= 1
                if depth == 0:
                    break
        yield statement[statement.index("(", index) : position + 1]
        start = position + 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("categories", nargs="+")
    parser.add_argument("--contains", action="store_true", help="substring match instead of equality")
    args = parser.parse_args()

    text = open(SOURCE, encoding="utf-8", errors="replace").read()
    shown = 0
    for line, statement in statements(text):
        if not ADD_START.search(statement):
            continue
        for call in add_calls(statement):
            parts = split_args(call)
            if len(parts) < 7:
                continue
            name, category = parts[0], parts[1]
            matched = any((c in category) if args.contains else (c == category) for c in args.categories)
            if not matched:
                continue
            # patterns are the trailing string literals; keys are the 'K', <value> pairs after them
            patterns = [p.strip('"') for p in parts if re.fullmatch(r'"(?:[A-Za-z0-9 ]{1,3})"', p)]
            keys = []
            for index, part in enumerate(parts):
                if re.fullmatch(r"'.'", part) and index + 1 < len(parts):
                    keys.append(f"{part.strip(chr(39))}={parts[index + 1]}")
            print(f"L{line}: {name}  [{category}]")
            if patterns:
                print(f"    patterns: {patterns}")
            print(f"    keys: {', '.join(keys) if keys else '(none)'}")
            shown += 1
    print(f"\n{shown} rows")


if __name__ == "__main__":
    main()
