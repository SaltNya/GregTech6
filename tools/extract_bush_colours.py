"""Extract GT6's berry bush colour table (BushesGT.put calls in MultiItemFood) so the port's bush
block can tint its stage textures with GT6's own colours."""

import os
import re

GT6 = os.path.join("..", "gregtech6-master", "gregtech6-master", "build", "sources", "java",
                   "gregtech", "items", "MultiItemFood.java")

pattern = re.compile(
    r"BushesGT\.put\(IL\.(Food_\w+)\.get\(1\),\s*(0x[0-9a-fA-F]+),\s*(0x[0-9a-fA-F]+),\s*(0x[0-9a-fA-F]+),\s*(0x[0-9a-fA-F]+)\)")

rows = []
with open(GT6, encoding="utf-8", errors="replace") as handle:
    for line in handle:
        match = pattern.search(line)
        if match:
            rows.append(match.groups())

# The port's berry item ids (GTMultiItemsGen food entries) keyed by the GT6 field name.
PORT_IDS = {
    "Food_Blueberry": "blueberry",
    "Food_Gooseberry": "gooseberry",
    "Food_Candleberry": "candleberry",
    "Food_Cranberry": "cranberry",
    "Food_Currants_Black": "black_currants",
    "Food_Currants_White": "white_currants",
    "Food_Currants_Red": "red_currants",
    "Food_Blackberry": "blackberry",
    "Food_Raspberry": "raspberry",
    "Food_Strawberry": "strawberry",
    "Food_Elderberry": "elderberry",
    "Food_Hellderberry": "hellderberry",
    "Food_Snowberry": "snowberry",
}

print("GT6 BushesGT.put rows: %d" % len(rows))
print("// name, bush, bloom, immature, berry")
for name, bush, bloom, immature, berry in rows:
    port = PORT_IDS.get(name)
    print('        entry("%s", %s, %s, %s, %s),%s' % (
        port or name, bush, bloom, immature, berry,
        "" if port else "   // not a port item id yet"))
