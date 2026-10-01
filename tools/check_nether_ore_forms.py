"""Check GT6 form flags for the materials GT6's nether worldgen needs an ore block for."""

import io
import json

FLAGS = "docs/gt6-form-flags.json"
NAMES = ["AncientDebris", "Glowstone", "Gloomstone", "Efrine", "Firestone", "VoidQuartz",
         "NetherQuartz", "Coltan", "Eudialyte", "Diamond", "Coal", "Redstone"]

data = json.load(io.open(FLAGS, encoding="utf-8"))
materials = data["materials"]
print("materials entries:", len(materials))
sample_key = next(iter(materials))
print("sample:", sample_key, "->", str(materials[sample_key])[:200])

for name in NAMES:
    entry = materials.get(name)
    if entry is None:
        print("%-16s (not present)" % name)
        continue
    text = str(entry)
    print("%-16s ORES=%-5s %s" % (name, "ORES" in text, text[:150]))
