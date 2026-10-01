"""Show the report entry for a set of material declarations (flags, sets, ids).

Usage:  python tools/show_material_form_entry.py Co Hf No Au Gold Ke Nq
"""

from __future__ import annotations

import json
import pathlib
import sys

REPORT = pathlib.Path("docs/gt6-form-flags.json")


def main() -> None:
    materials = json.loads(REPORT.read_text(encoding="utf-8"))["materials"]
    for name in sys.argv[1:]:
        entry = materials.get(name)
        if entry is None:
            print(f"  {name:14} (not in the report)")
            continue
        print(f"  {name:14} ids={entry['ids']} sets={entry['sets']} flags={','.join(entry['flags'])}")


if __name__ == "__main__":
    main()
