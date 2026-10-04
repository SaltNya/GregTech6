"""Original GT6 recipes for the currently shipped long-distance block identities.

Gregorius Techneticies' Loader_Blocks.java:160-186 and Loader_MultiTileEntities.java:906-914
(read-only source snapshot). A voltage-named wire selects one real source material of that
rating. This does not claim to restore the source's sixteen separate material variants.
The ambiguous old long_dist_pipe stays a compatibility block without an invented recipe.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "core/src/main/resources/data/gregtech"

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def item(name):
    return {"item": "gregtech:" + name}

def tag(name):
    return {"tag": "gregtech:" + name}

def recipe(name, pattern, keys):
    write(DATA / f"recipes/long_distance/{name}.json", {
        "type": "gregtech:tool_shaped", "allow_mirror": False,
        "pattern": pattern, "key": keys, "result": item(name),
    })

def run():
    for family, materials in {
        "plate/any_plastic": ["plastic", "polycarbonate", "pvc", "teflon", "bakelite"],
        "plate_curved/any_copper": ["copper", "annealed_copper"],
    }.items():
        prefix = family.split("/")[0]
        write(DATA / f"tags/items/long_distance/{family}.json", {
            "replace": False,
            "values": [{"id": f"#gregtech:{prefix}/{material}", "required": False} for material in materials],
        })
    for name, wire in {
        "long_dist_wire": item("wire_16_tin"),
        "long_dist_wire_ev": item("wire_16_tin"),
        "long_dist_wire_iv": tag("wire_16/any_copper"),
        "long_dist_wire_luv": item("wire_16_silver"),
        "long_dist_wire_zpm": item("wire_16_steel"),
        "long_dist_wire_uv": item("wire_16_graphene"),
    }.items():
        recipe(name, ["RSR", "PWP", "RSR"], {
            "R": tag("plate/rubber"), "S": tag("plate_curved/aluminium"),
            "P": tag("long_distance/plate_curved/any_copper"), "W": wire,
        })
    for name, pipe in {"long_dist_pipe_item": "item_pipe_medium_electrum", "long_dist_pipe_fluid": "pipe_medium_stainless_steel"}.items():
        recipe(name, ["SPS", "PwP", "SPS"], {
            "S": tag("long_distance/plate/any_plastic"),
            "P": item(pipe), "w": item("tool_wrench"),
        })
    for name, casing, pipe in [
        ("long_dist_endpoint_item", "platinum", "item_pipe_medium_platinum"),
        ("long_dist_endpoint_fluid", "tungsten", "pipe_medium_tungsten"),
    ]:
        recipe(name, ["ZPZ", "PMP", "ZPZ"], {
            "Z": tag("long_distance/plate/any_plastic"), "P": item(pipe),
            "M": item("casing_machine_" + casing),
        })
    # These first three registry names predate the source alignment; their real grades
    # and translated names are EV, IV, LuV. Keep the IDs for existing saves.
    for suffix, transformer in {
        "ulv": "ev_iv", "lv": "iv_luv", "mv": "luv_zpm", "zpm": "zpm_uv", "uv": "uv_xv",
    }.items():
        recipe("long_dist_transformer_" + suffix, ["WMW", "MxM", "WMW"], {
            "W": item("cable_04_annealed_copper"), "M": item("transformer_" + transformer),
            "x": item("tool_wire_cutter"),
        })
    print("Wrote 15 original-pattern long-distance recipes and 2 shared family tags.")

if __name__ == "__main__":
    run()
