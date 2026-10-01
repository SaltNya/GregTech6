"""Which GT6 files register rows into a given recipe map, and how many?

Companion to ``census_gt6_recipe_sites.py``: that tool shows *where* recipe rows live outside the
transpiled packages, this one answers "who feeds map X" so a family can be traced to its source.

Usage:  python tools/census_gt6_recipe_map_sources.py Extruder Laminator Drying
"""

from __future__ import annotations

import collections
import pathlib
import re
import sys

GT6 = pathlib.Path(r"F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java")
RM_ADD = re.compile(r"\bRM\.(\w+)\.(?:addRecipe\d?|addFakeRecipe|add)\(")


def main() -> None:
    wanted = set(sys.argv[1:]) or {"Extruder"}
    sources: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    for path in GT6.rglob("*.java"):
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(GT6).as_posix()
        for name in RM_ADD.findall(text):
            if name in wanted:
                sources[name][rel] += 1
    for name in sorted(sources):
        print(f"=== {name}: {sum(sources[name].values())} rows")
        for rel, count in sources[name].most_common(6):
            print(f"  {count:5}  {rel}")


if __name__ == "__main__":
    main()
