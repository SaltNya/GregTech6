"""Report the port's multiblock part table (ids and names)."""

import io
import re

PATH = "src/main/java/com/gregtech/gregtech/content/multiblock/LargeMachineParts.java"
text = io.open(PATH, encoding="utf-8", errors="replace").read()
parts = re.findall(r'new Part\((\d+),\s*"([a-z0-9_]+)"', text)
print("parts now:", len(parts))
for pid, name in parts:
    if int(pid) >= 17000:
        print("   %-6s %s" % (pid, name))
