"""Print GT6's hand-written early tool rows (Loader_Tools:255-290) from the extractor."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("ex", ROOT / "tools" / "extract_gt6_tool_recipes.py")
module = importlib.util.module_from_spec(spec)
sys.modules["ex"] = module
spec.loader.exec_module(module)

data = module.extract()
for row in data["early"]:
    print(f"{row['tool']:16} material={row['material']:22} handle={row['handle']:24} "
          f"rows={row['rows']} {row['flag']}")
