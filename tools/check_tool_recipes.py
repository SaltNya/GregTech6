"""Compare GT6's tool crafting rows with the port's pattern table.

GT6 side (``tools/extract_gt6_tool_recipes.py``): every ``new OreProcessing_Tool(...)`` row of
``Loader_Tools.java`` with its 8th argument (the shaped recipe of the tool) and 9th (the shaped recipe
of its head), plus the ``AdvancedCraftingTool`` registrations that are shapeless (head + handle).

Port side (``docs/tool-assembly-coverage.json``, written by ``ToolAssemblyTests``): the pattern table
of ``GTToolRecipes`` as it is registered at runtime.

Usage:  python tools/check_tool_recipes.py [--json docs/gt6-tool-recipe-parity.json]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT_REPORT = ROOT / "docs" / "tool-assembly-coverage.json"

# GT6 tool id -> port tool id.
TOOLS = {
    "WRENCH": "wrench", "MONKEY_WRENCH": "monkey_wrench",
    "BENDING_CYLINDER": "bending_cylinder", "BENDING_CYLINDER_SMALL": "small_bending_cylinder",
    "CROWBAR": "crowbar", "PLUNGER": "plunger", "PINCERS": "pincers", "SCOOP": "scoop",
    "KNIFE": "knife", "BUTCHERYKNIFE": "butchery_knife", "WIRECUTTER": "wire_cutter",
    "BRANCHCUTTER": "branch_cutter", "SCISSORS": "scissors", "CLUB": "club",
    "HAND_DRILL": "hand_drill", "UNIVERSALSPADE": "universal_spade",
    "PICKAXE": "pickaxe", "SHOVEL": "shovel", "SPADE": "spade", "AXE": "axe",
    "DOUBLE_AXE": "double_axe", "HOE": "hoe", "SWORD": "sword",
    "HARDHAMMER": "hammer", "SOFTHAMMER": "soft_hammer", "FILE": "file", "SAW": "saw",
    "CHISEL": "chisel", "SCREWDRIVER": "screwdriver", "SENSE": "sense", "PLOW": "plow",
    "CONSTRUCTION_PICK": "construction_pick", "BUILDERWAND": "builder_wand",
}
# Rows GT6 writes by hand rather than through OreProcessing_Tool (Loader_Tools:225-290).
HAND_WRITTEN = {"rolling_pin": [["  S", " I ", "S f"]], "flint_and_tinder": [["T ", " F"]]}


def load_extractor():
    spec = importlib.util.spec_from_file_location("extract", ROOT / "tools" / "extract_gt6_tool_recipes.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["extract"] = module
    spec.loader.exec_module(module)
    return module.extract()


def is_early(pattern: dict) -> bool:
    """Whether a dumped port pattern is one of GT6's hand-written early rows."""
    gate = pattern.get("gate") or {}
    return bool(gate.get("toolMaterial") or gate.get("onlyMaterial") or gate.get("onlyStone")
                or gate.get("items"))


def matches_family(pattern: dict, family: str) -> bool:
    """Whether a dumped port pattern belongs to one of GT6's early-row families."""
    gate = pattern.get("gate", {})
    if family == "stone":
        return bool(gate.get("onlyStone"))
    if family in ("flint", "bone"):
        return (gate.get("toolMaterial") or "") == ("Flint" if family == "flint" else "Bone")
    return (gate.get("onlyMaterial") or "").lower() == family


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="")
    args = parser.parse_args()

    gt6 = load_extractor()
    report = json.loads(PORT_REPORT.read_text(encoding="utf-8"))
    port_shaped = report.get("shaped", {})
    port_heads = report.get("heads", {})

    problems: list[str] = []
    checked = 0
    for gt6_name, port_id in sorted(TOOLS.items()):
        entry = gt6["tools"].get(gt6_name, {})
        want_tool = [row for row in entry.get("toolRecipes", [])]
        want_head = [row for row in entry.get("headRecipes", [])]
        # GT6's OreProcessing_Tool rows are the non-early ones; the hand-written early rows (flint,
        # obsidian, stone, petrified wood, bone) are compared separately below.
        port_patterns = port_shaped.get(port_id, [])
        have_tool = [pattern["rows"] for pattern in port_patterns if not is_early(pattern)]
        have_head = [pattern["rows"] for pattern in port_heads.get(port_id, [])]
        mirror = [pattern["mirror"] for pattern in port_patterns if not is_early(pattern)]
        if want_tool != have_tool:
            problems.append(f"{port_id}: shaped rows GT6 {want_tool} != port {have_tool}")
        if want_head != have_head:
            problems.append(f"{port_id}: head rows GT6 {want_head} != port {have_head}")
        if want_tool and any(mirror):
            problems.append(f"{port_id}: GT6's OreProcessing_Tool rows never mirror, port mirrors {mirror}")
        checked += 1
    for port_id, rows in HAND_WRITTEN.items():
        have = [pattern["rows"] for pattern in port_shaped.get(port_id, [])]
        if rows != have:
            problems.append(f"{port_id}: hand-written rows GT6 {rows} != port {have}")
        checked += 1
    if "flint_and_tinder" in port_shaped and not port_shaped["flint_and_tinder"][0]["mirror"]:
        problems.append("flint_and_tinder: GT6's row is CR.DEF_MIR")

    # Loader_Tools:255-290 — the early tools, keyed by the family the row is written for.
    families: dict[tuple[str, str], list[str]] = {}
    for row in gt6["early"]:
        family = None
        if row["material"] == "MT.Flint":
            family = "flint"
        elif row["material"] == "MT.Bone":
            family = "bone"
        elif "Obsidian" in row["loop"] or "Obsidian" in row["item"]:
            family = "obsidian"
        elif "PetrifiedWood" in row["loop"] or "PetrifiedWood" in row["item"]:
            family = "petrifiedwood"
        elif "Stone" in row["loop"]:
            family = "stone"
        if family is None or row["tool"] not in TOOLS:
            continue
        # GT6 uses 'S' for the handle in these rows, the port's pattern table uses 'H'.
        rows = [r.replace("S", "H") for r in row["rows"]]
        families.setdefault((TOOLS[row["tool"]], family), rows)
    early_checked = 0
    for (port_id, family), rows in sorted(families.items()):
        have = [pattern["rows"] for pattern in port_shaped.get(port_id, [])
                if matches_family(pattern, family)]
        if [rows] != have:
            problems.append(f"{port_id} ({family}): GT6 {rows} != port {have}")
        early_checked += 1
    if early_checked != 21:
        problems.append(f"early rows compared: {early_checked}, expected 21")

    # The head + handle tools: GT6 registers them shapeless (AdvancedCraftingTool), the port must too.
    # (A tool can have both: the pickaxe comes from a head + handle *and* from three rocks.)
    gt6_advanced = {row["tool"] for row in gt6["advanced"]}
    port_assemblies = set(report.get("assemblies", []))
    for name in sorted(gt6_advanced):
        port_id = TOOLS.get(name)
        if port_id is None:
            continue
        if port_id not in port_assemblies:
            problems.append(f"{port_id}: GT6 registers a shapeless head + handle row, the port has none")

    payload = {
        "toolsChecked": checked,
        "gt6Advanced": sorted(gt6_advanced),
        "gt6EarlyRows": len(gt6["early"]),
        "portShapedTools": sorted(port_shaped),
        "portHeadTools": sorted(port_heads),
        "problems": problems,
    }
    print(f"tools compared        : {checked}")
    print(f"port shaped rows      : {len(port_shaped)} tools")
    print(f"port head rows        : {len(port_heads)} tools,"
          f" {sum(len(v) for v in port_heads.values())} patterns")
    print(f"GT6 advanced (shapeless) tools: {len(gt6_advanced)}; GT6 early hand-written rows:"
          f" {len(gt6['early'])}")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for problem in problems:
            print("  - " + problem)
    else:
        print("\nOK: the port's tool patterns match GT6's rows.")
    if args.json:
        out = (ROOT / args.json).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        print(f"wrote {out}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
