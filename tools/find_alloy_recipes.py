"""Find alloying recipes in the port's generated chem tables (which materials are alloyed from what)."""

import glob
import io
import re

PATTERNS = ["Bronze", "Brass", "Steel", "Invar", "Electrum", "Cupronickel", "Solder"]

for path in sorted(glob.glob("src/main/java/com/gregtech/gregtech/loaders/**/*Gen.java", recursive=True)):
    text = io.open(path, encoding="utf-8", errors="replace").read()
    if 'CrucibleAlloying' not in text and 'Alloy' not in text:
        continue
    print("==", path.replace("\\", "/"))
    for line in text.splitlines():
        if "CrucibleAlloying" in line and any(p in line for p in PATTERNS):
            print("   ", line.strip()[:200])
