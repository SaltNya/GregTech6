#!/usr/bin/env python3
"""Print GT6 basic-machine crafting recipes grouped by machine (readable debug view)."""
import json
import sys
import collections
from pathlib import Path

p = Path(__file__).with_name("gt6_basic_machine_recipes.json")
data = json.loads(p.read_text(encoding="utf-8"))
by = collections.OrderedDict()
for e in data["entries"]:
    by.setdefault(e["machine"], []).append(e)

wanted = sys.argv[1:] or list(by)
for name in wanted:
    if name not in by:
        print("--- %s: NOT PRESENT" % name)
        continue
    print("--- %s ---" % name)
    for e in by[name]:
        print("   tier=%-24s id=%-6s %s" % (e["tier"], e["registryId"], e["pattern"]))
        print("      keys=%s" % e["keys"])
