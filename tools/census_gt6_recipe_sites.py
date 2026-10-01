"""Census of GT6 recipe-registration sites *outside* the transpiled loader packages.

The port's transpilers read ``gregtech/loaders/**`` (``Loader_Recipes_*``, ``Loader_Loot``,
``Loader_Books``, registration patterns in ``Loader_MultiTileEntities``) and, since §26, part of
``GT6_Main``. Everything else that registers recipes is invisible to them — this counts those sites so
the remaining ones can be ported deliberately instead of being discovered one by one.

Usage:  python tools/census_gt6_recipe_sites.py [--limit N]
"""

from __future__ import annotations

import collections
import pathlib
import re
import sys

GT6 = pathlib.Path(r"F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java")
# Packages the transpilers already read (or that hold no portable rows): other mods' compat, worldgen
# (loot is handled), the multi-item/item behaviour classes, and the recipe-map definitions themselves.
TRANSPILED = ("gregtech/loaders/", "gregtech/worldgen/", "gregtech/compat/")
SKIP_FILES = re.compile(r"^(Compat_|Loader_|MD\.|MultiItem|RecipeMap)")
PATTERNS = {
    "RM.add": re.compile(r"\bRM\.(\w+)\.(?:addRecipe\d?|addFakeRecipe|add)\("),
    "CR.shaped": re.compile(r"\bCR\.shaped\("),
    "CR.shapeless": re.compile(r"\bCR\.shapeless\("),
    "registry-pattern": re.compile(r"\baRegistry\.add\("),
    "ChestGenHooks": re.compile(r"ChestGenHooks\.addItem\("),
}


def main() -> None:
    limit = 25
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    per_file: collections.Counter[str] = collections.Counter()
    per_kind: collections.Counter[str] = collections.Counter()
    maps: collections.Counter[str] = collections.Counter()
    for path in GT6.rglob("*.java"):
        rel = path.relative_to(GT6).as_posix()
        if rel.startswith(TRANSPILED) or SKIP_FILES.match(path.name):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        total = 0
        for kind, pattern in PATTERNS.items():
            hits = pattern.findall(text)
            if not hits:
                continue
            count = len(hits)
            total += count
            per_kind[kind] += count
            if kind == "RM.add":
                for name in hits:
                    maps[name] += 1
        if total:
            per_file[rel] = total

    print(f"files with recipe registrations outside the transpiled packages: {len(per_file)}")
    print(f"rows by kind: {dict(per_kind)}")
    print("--- top files ---")
    for rel, count in per_file.most_common(limit):
        print(f"  {count:5}  {rel}")
    print("--- recipe maps touched ---")
    for name, count in maps.most_common(15):
        print(f"  {count:5}  {name}")


if __name__ == "__main__":
    main()
