"""Check GT6 form flags (docs/gt6-form-flags.json) for the given material names.

Usage: python tools/check_form_flags.py Lignite Coal Palladium ...
"""

import io
import json
import sys

data = json.load(io.open("docs/gt6-form-flags.json", encoding="utf-8"))
materials = data["materials"]

names = sys.argv[1:]
if not names:
    print(__doc__)
    raise SystemExit(0)
for name in names:
    entry = materials.get(name)
    if entry is None:
        print("%-16s (not present in the form table)" % name)
        continue
    flags = entry.get("flags", [])
    print("%-16s ORES=%-5s flags=%s" % (name, "ORES" in flags, ",".join(flags)))
