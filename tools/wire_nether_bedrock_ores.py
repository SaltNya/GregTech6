"""Add the Nether biome modifier for GT6's bedrock ores (the feature now switches tables by dimension)."""

import io
import json
import os

DATA = os.path.join("src", "main", "resources", "data", "gregtech", "forge", "biome_modifier")
PATH = os.path.join(DATA, "gt_nether_bedrock_ores.json")

payload = {
    "type": "forge:add_features",
    "biomes": "#minecraft:is_nether",
    "features": ["gregtech:gt_bedrock_ores"],
    "step": "underground_ores",
}

os.makedirs(DATA, exist_ok=True)
if os.path.exists(PATH):
    print("already written: %s" % PATH.replace("\\", "/"))
else:
    with open(PATH, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    print("wrote %s" % PATH.replace("\\", "/"))
