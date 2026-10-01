#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
comp = (ROOT / "src/main/java/com/gregtech/gregtech/data/generated/MaterialCompositionData.java").read_text(encoding="utf-8")
refs = set(re.findall(r'get\("([^"]+)"\)', comp))
pattern = r"^\s+(\w+(?:\s*,\s*\w+)*)\s*=\s*(?:\w+\.)?(?:create|metal|element|alloy|ore|gem|dust|gas|wood|stone|elec|cent|clay)\("
fields = set()
for rel in (
    "tools/generated/materials-source.java.txt",
    "src/main/java/com/gregtech/gregtech/data/ImportedMaterialData.java",
    "src/main/java/com/gregtech/gregtech/data/AntimatterMaterials.java",
):
    source = (ROOT / rel).read_text(encoding="utf-8")
    for match in re.finditer(pattern, source, re.M):
        for part in match.group(1).split(","):
            fields.add(part.strip())
fields |= {"Ma", "Empty", "NULL"}
missing = sorted(r for r in refs if r not in fields)
print("missing count", len(missing))
for name in missing:
    print(name)
