#!/usr/bin/env python3
"""List every distinct ingredient expression used by GT6 basic-machine crafting recipes."""
import collections
import json
import re
from pathlib import Path

p = Path(__file__).with_name("gt6_basic_machine_recipes.json")
data = json.loads(p.read_text(encoding="utf-8"))


def norm(expr: str) -> str:
    e = expr.strip()
    e = re.sub(r"\s+\.", ".", e)
    e = re.sub(r"\.\s*dat", ".dat", e)
    e = re.sub(r"\(\s*", "(", e)
    e = re.sub(r"\s*\)", ")", e)
    e = re.sub(r"\s+", " ", e)
    return e


uses = collections.Counter()
machines = collections.defaultdict(set)
for e in data["entries"]:
    for sym, expr in e["keys"].items():
        uses[norm(expr)] += 1
        machines[norm(expr)].add(e["machine"])

for expr, n in sorted(uses.items(), key=lambda kv: (-kv[1], kv[0])):
    who = sorted(machines[expr])
    who_s = ",".join(who[:4]) + ("..." if len(who) > 4 else "")
    print("%-52s %3d  %s" % (expr, n, who_s))
print("distinct:", len(uses))
