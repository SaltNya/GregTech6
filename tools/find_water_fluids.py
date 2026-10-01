"""Find the port's water-family fluid ids (GT6 FL.Ocean / FL.River / FL.Swamp and friends)."""

import glob
import io
import re

PATTERNS = ("river", "sea", "swamp", "ocean", "water")

hits = set()
for path in glob.glob("src/main/java/com/gregtech/gregtech/**/*.java", recursive=True):
    text = io.open(path, encoding="utf-8", errors="replace").read()
    for match in re.finditer(r'fluid\(\s*"([A-Za-z0-9_]+)"', text):
        name = match.group(1)
        if any(key in name.lower() for key in PATTERNS):
            hits.add((path.replace("\\", "/").split("/")[-1], name))
for entry in sorted(hits):
    print("%-34s %s" % entry)
