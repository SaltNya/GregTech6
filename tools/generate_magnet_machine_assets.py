#!/usr/bin/env python3
"""Build only the 10 GT6 powered magnet models from original GT6 textures."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GT6 = ROOT.parent / "gregtech6-master" / "gregtech6-master" / "src" / "main" / "resources" / "assets" / "gregtech" / "textures" / "blocks" / "machines"
ASSETS = ROOT / "src" / "main" / "resources" / "assets" / "gregtech"
TEXTURES = ASSETS / "textures" / "block" / "machines"
TIERS = ("lv", "mv", "hv", "ev", "iv")
ELECTRIC_CASINGS = ("steelgalvanized", "aluminium", "stainlesssteel", "chromium", "titanium")
FLUX_RODS = ("lead", "invar", "electrum", "enderium_base", "enderium")
WIRE_SIZES = (1, 2, 4, 8, 16)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def layer(folder, overlay):
    subdir = "colored" if overlay is None else overlay
    names = {"north": "front", "south": "back", "west": "side", "east": "side", "up": "side", "down": "side"}
    textures = {side: f"gregtech:block/machines/magnets/{folder}/{subdir}/{name}" for side, name in names.items()}
    faces = {side: {"texture": "#" + side, **({"tintindex": 0} if overlay is None else {})}
             for side in names}
    return {"parent": "minecraft:block/block", "textures": textures,
            "elements": [{"from": [0, 0, 0], "to": [16, 16, 16], "faces": faces}],
            "render_type": "minecraft:cutout"}


def model(folder, active):
    return {"parent": "minecraft:block/block", "loader": "forge:composite",
            "children": {"colored": layer(folder, None),
                         "overlay": layer(folder, "overlay_active" if active else "overlay")}}


def blockstate(name):
    rotations = {"north": {}, "east": {"y": 90}, "south": {"y": 180},
                 "west": {"y": 270}, "up": {"x": 270}, "down": {"x": 90}}
    variants = {}
    for facing, rotation in rotations.items():
        for active in (False, True):
            variants[f"facing={facing},active={str(active).lower()}"] = {
                "model": f"gregtech:block/machine/energy/{name}{'_active' if active else ''}", **rotation}
    return {"variants": variants}


def main():
    for folder in ("magnet_electric", "magnet_flux"):
        for subdir in ("colored", "overlay", "overlay_active"):
            for name in ("front", "back", "side"):
                source = GT6 / "magnets" / folder / subdir / f"{name}.png"
                if not source.is_file():
                    raise FileNotFoundError(source)
                dest = TEXTURES / "magnets" / folder / subdir / source.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    shutil.copy2(source, dest)
    for tier in TIERS:
        for name, folder in ((f"electromagnet_{tier}", "magnet_electric"),
                             (f"flux_magnet_{tier}", "magnet_flux")):
            for active in (False, True):
                model_name = name + ("_active" if active else "")
                write_json(ASSETS / "models" / "block" / "machine" / "energy" / f"{model_name}.json",
                           model(folder, active))
            write_json(ASSETS / "blockstates" / f"{name}.json", blockstate(name))
            write_json(ASSETS / "models" / "item" / f"{name}.json",
                       {"parent": f"gregtech:block/machine/energy/{name}"})
    for index, tier in enumerate(TIERS):
        wire = "copper" if index < 2 else "annealed_copper"
        write_json(ROOT / "src" / "main" / "resources" / "data" / "gregtech" / "recipes"
                   / "magnets" / f"electromagnet_{tier}.json", {
                       "type": "gregtech:tool_shaped",
                       "pattern": ["CxC", "CMC", "CwC"],
                       "key": {
                           "C": {"item": f"gregtech:wire_{WIRE_SIZES[index]:02d}_{wire}"},
                           "M": {"item": f"gregtech:casing_machine_{ELECTRIC_CASINGS[index]}"},
                           "x": {"item": "gregtech:tool_wire_cutter"},
                           "w": {"item": "gregtech:tool_wrench"}},
                       "result": {"item": f"gregtech:electromagnet_{tier}"},
                       "allow_mirror": False,
                       "_comment": f"GT6 Loader_MultiTileEntities: {865 + index}"})
        write_json(ROOT / "src" / "main" / "resources" / "data" / "gregtech" / "recipes"
                   / "magnets" / f"flux_magnet_{tier}.json", {
                       "type": "minecraft:crafting_shaped",
                       "pattern": ["SSS", "SMS", "SSS"],
                       "key": {"S": {"tag": f"forge:long_rods/{FLUX_RODS[index]}"},
                               "M": {"item": f"gregtech:electromagnet_{tier}"}},
                       "result": {"item": f"gregtech:flux_magnet_{tier}"},
                       "_comment": f"GT6 Loader_MultiTileEntities: {872 + index}"})


if __name__ == "__main__":
    main()
