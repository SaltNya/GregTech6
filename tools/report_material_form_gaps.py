"""List the material form gaps (GT6 declares a form the port does not register), largest first."""
import json
import pathlib

data = json.loads(pathlib.Path("docs/material-form-gap.json").read_text(encoding="utf-8"))
rows = []
for flag, entry in data.items():
    if not isinstance(entry, dict):
        continue
    gt6 = entry.get("gt6Materials", 0)
    port = entry.get("portMaterials", 0)
    examples = entry.get("examplesMissing") or []
    if examples:
        rows.append((gt6 - port, flag, entry.get("prefix") or "", gt6, port, examples))
rows.sort(key=lambda r: (-r[0], r[1]))
print(f"{len(rows)} flags still have missing examples")
for gap, flag, prefix, gt6, port, examples in rows[:20]:
    print(f"{flag:16} {prefix:18} gt6={gt6:4} port={port:4} gap={gap:4} "
          f"e.g. {', '.join(examples[:5])}")
