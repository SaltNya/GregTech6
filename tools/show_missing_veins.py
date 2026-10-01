"""Print GT6's large-ore parameters for the veins the port is missing."""

import json

WANT = ["lignite", "coal", "bauxite", "iodinesalt", "rocksalt",
        "cassiterite", "molybdenum", "platinum"]

data = json.load(open("docs/gt6-large-ores.json", encoding="utf-8"))
for reg in data["registrations"]:
    if reg["name"] not in WANT:
        continue
    print("%-12s minY=%-4s maxY=%-4s weight=%-4s count=%-3s size=%-3s indicator=%s dims=%s"
          % (reg["name"], reg["minY"], reg["maxY"], reg["weight"], reg["count"], reg["size"],
             reg["indicator"], reg["dims"]))
    print("             materials: %s" % ", ".join(reg["materials"]))
