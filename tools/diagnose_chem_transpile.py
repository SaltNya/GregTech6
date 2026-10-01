#!/usr/bin/env python3
"""Report why tools/transpile_gt6_chem.py skips individual GT6 recipes.

Usage: python tools/diagnose_chem_transpile.py [set]

Groups the untranslated `RM.<Map>.addRecipe*` calls by map and by the reason the
transpiler bailed out, with one example line each. Used to decide which parser gaps are
worth closing (they fill whole RecipeMaps at once).
"""

import collections
import re
import sys
from pathlib import Path

SET = sys.argv[1] if len(sys.argv) > 1 else "chem"
sys.argv = [sys.argv[0], SET]

sys.path.insert(0, str(Path(__file__).resolve().parent))
import transpile_gt6_chem as T  # noqa: E402


def reason(map_name, body):
    """Mirror parse_call but say which check failed."""
    args = T.split_args(body)
    if not args:
        return "no args"
    if args[0] not in ("T", "F"):
        return "first arg not T/F: %s" % args[0][:40]
    idx = 1
    nums = []
    while idx < len(args) and re.fullmatch(r"[0-9*+\-/ ]+", args[idx]):
        try:
            nums.append(int(eval(args[idx])))
        except Exception:
            return "unparsable number: %s" % args[idx][:40]
        idx += 1
    if len(nums) != 2:
        return "expected 2 numbers (EU, duration), got %d" % len(nums)
    if idx < len(args) and args[idx].startswith("new long[]"):
        idx += 1
    seen_fluid = False
    fluids = 0
    for arg in args[idx:]:
        if T.is_fluid_expr(arg):
            fl = T.parse_fluid(arg)
            if fl is None:
                return "fluid expr: %s" % arg[:50]
            fluids += 1
            seen_fluid = True
        else:
            it = T.parse_item(arg)
            if it is None:
                return "item expr: %s" % arg[:50]
    if fluids > 2:
        return "more than 2 fluid groups (%d)" % fluids
    return None


def main() -> int:
    text = T.unroll_loops(T.strip_comments(open(T.SRC, encoding="utf-8").read()))
    by_reason = collections.Counter()
    by_map = collections.Counter()
    examples = {}
    total = ok = 0
    for m in re.finditer(r"RM\.(\w+)\s*\.addRecipe[012X]\s*\(", text):
        total += 1
        map_name = m.group(1)
        if map_name not in T.PORT_MAPS:
            by_reason["map not in port: " + map_name] += 1
            continue
        try:
            body = T.balanced(text, m.end() - 1)
        except ValueError:
            by_reason["unbalanced parentheses"] += 1
            continue
        parsed = T.parse_call(map_name, body)
        if parsed:
            ok += 1
            continue
        why = reason(map_name, body) or "unknown (parse_call rejected the result)"
        key = (map_name, why.split(":")[0])
        by_map[map_name] += 1
        by_reason[why.split(":")[0]] += 1
        examples.setdefault(key, " ".join(body.split())[:150])

    print("translated %d / %d" % (ok, total))
    print("\n== skipped per map (top 25) ==")
    for map_name, n in by_map.most_common(25):
        print("  %-24s %d" % (map_name, n))
    print("\n== skip reasons ==")
    for why, n in by_reason.most_common():
        print("  %-34s %d" % (why, n))
    print("\n== examples ==")
    for (map_name, why), example in sorted(examples.items()):
        print("  [%s] %s -> %s" % (map_name, why, example))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
