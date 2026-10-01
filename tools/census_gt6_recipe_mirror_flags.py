"""Census GT6's crafting-table rows by their CR flag expression (which of them allow mirroring?).

The port's 1.20.1 recipes mirror by default, GT6's ``CR.DEF`` does not: ``gregapi/util/CR.java:161``
defines ``DEF = BUF|NO_REM`` and ``MIR`` is a separate flag that every ``*_MIR`` constant adds. This
tool answers "which rows actually set MIR", so the port can copy the answer instead of guessing.

Usage:  python tools/census_gt6_recipe_mirror_flags.py
"""

from __future__ import annotations

import collections
import json
import os
import pathlib
import re

GT6 = pathlib.Path(r"F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java")
OUT = pathlib.Path("docs/gt6-crafting-mirror-flags.json")

FLAG_CONST = re.compile(r"long\s+(\w+)\s*=\s*([^;]+);")
SHAPED = re.compile(r"CR\.shaped\s*\((.*)", re.S)
PART = re.compile(r"CR\.(\w+)")


def statements(path: pathlib.Path):
    text = path.read_text(encoding="utf-8", errors="replace")
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


def flag_table() -> dict[str, set[str]]:
    """CR constant -> the bit names it is made of (resolved through the ``B[n]`` building blocks)."""
    text = (GT6 / "gregapi/util/CR.java").read_text(encoding="utf-8", errors="replace")
    raw = {name: value.strip() for name, value in FLAG_CONST.findall(text)}
    bits: dict[str, set[str]] = {}
    for _ in range(6):
        changed = False
        for name, value in raw.items():
            resolved: set[str] = set()
            for token in re.split(r"[|&()\s]+", value):
                token = token.strip()
                if not token:
                    continue
                if token.startswith("B[") or token.startswith("B ["):
                    resolved.add("BIT" + token)
                elif token in bits:
                    # keep the constant's own name: ``DEF_MIR`` -> {DEF…, MIR, …} is what the
                    # caller asks about, and the bit it stands for collapses to ``BITB[0]``
                    resolved |= bits[token] | {token}
                else:
                    resolved.add(token)
            if bits.get(name) != resolved:
                bits[name] = resolved
                changed = True
        if not changed:
            break
    return bits


def split_top_level(argument_text: str) -> list[str]:
    """Split an argument list on commas that sit outside any nested call/array/string."""
    parts, depth, current, in_string = [], 0, "", False
    index = 0
    while index < len(argument_text):
        char = argument_text[index]
        if in_string:
            if char == "\\":
                current += argument_text[index : index + 2]
                index += 2
                continue
            if char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        if char == "," and depth == 0 and not in_string:
            parts.append(current.strip())
            current = ""
        else:
            current += char
        index += 1
    if current.strip():
        parts.append(current.strip())
    return parts


def main() -> None:
    bits = flag_table()
    mirror_aware = {name for name, members in bits.items() if any("MIR" in m for m in members)}
    rows = collections.Counter()
    with_mirror: list[dict] = []
    pattern_mirror: dict[str, bool] = {}
    total = 0
    skipped = 0
    for path in GT6.rglob("*.java"):
        for stmt in statements(path):
            match = SHAPED.search(stmt)
            if not match:
                continue
            args = split_top_level(match.group(1).rstrip().rstrip(";").rstrip(")"))
            if len(args) < 3:
                skipped += 1
                continue
            result, flags = args[0], args[1]
            if not flags.startswith("CR.") and not re.fullmatch(r"[A-Z_]+", flags):
                skipped += 1                      # the low-level overload (enchantment arrays)
                continue
            total += 1
            rows[flags] += 1
            members: set[str] = set()
            for name in re.findall(r"\b(\w+)\b", flags):
                members |= bits.get(name, set())
            allows_mirror = any("MIR" in m for m in members)
            # Pattern rows are the leading string literals right after the flag expression; the
            # first non-literal argument is a key char ('d', 'w', …) and everything behind it is
            # ingredient data. GT6 pads each row to three characters while the port keeps the
            # original widths, so the signature trims trailing spaces on both sides (leading ones
            # stay: they carry the position).
            patterns = []
            for arg in args[2:]:
                if not re.fullmatch(r'"(?:[^"\\]|\\.)*"', arg.strip()):
                    break
                patterns.append(arg.strip()[1:-1])
            signature = "\n".join(row.rstrip() for row in patterns if row.strip()) if patterns else ""
            if signature:
                pattern_mirror[signature] = pattern_mirror.get(signature, False) or allows_mirror
            if allows_mirror:
                with_mirror.append({
                    "file": str(path.relative_to(GT6)).replace("\\", "/"),
                    "result": result,
                    "flags": flags,
                })
    mirror_patterns = sorted(p for p, allowed in pattern_mirror.items() if allowed)
    report = {
        "shapedRows": total,
        "skippedRows": skipped,
        "byFlag": dict(rows.most_common()),
        "mirrorAllowedRows": len(with_mirror),
        "mirrorRows": with_mirror,
        "mirrorConstants": sorted(mirror_aware),
        "patternMirror": {p: pattern_mirror[p] for p in sorted(pattern_mirror)},
        "mirrorPatterns": mirror_patterns,
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{total} CR.shaped rows ({skipped} low-level overloads skipped); "
          f"{len(with_mirror)} of them set MIR")
    for flag, count in rows.most_common(12):
        print(f"  {count:5}  {flag}")
    print(f"distinct patterns: {len(pattern_mirror)}, of which mirror-allowing: {len(mirror_patterns)}")
    print("mirror-allowing constants:", sorted(mirror_aware)[:12])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
