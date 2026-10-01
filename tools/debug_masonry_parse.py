"""Debug helper: print what tools/check_masonry_rows.py parses out of GT6's BlockStones."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("masonry", ROOT / "tools" / "check_masonry_rows.py")
module = importlib.util.module_from_spec(spec)
sys.modules["masonry"] = module
spec.loader.exec_module(module)

parsed = module.parse_gt6()
print("machines:", dict(parsed["machines"]))
print("smeltGroups:", parsed["smeltGroups"], "preamble:", parsed["smeltPreamble"],
      "generify:", parsed["generify"], "cleanmoss:", parsed["cleanmoss"], "sawing:", parsed["sawing"])
print("crafting rows:", len(parsed["crafting"]), "preamble:", parsed["craftingPreamble"])
for row in parsed["crafting"]:
    print(f"  {row['group']:9} {row['kind']:9} mirror={int(row.get('mirror', False))}"
          f" tools={row.get('tools')} patterns={row.get('patterns')}")
