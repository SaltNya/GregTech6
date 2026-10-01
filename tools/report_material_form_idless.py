"""List GT6 material declarations that have form flags but no captured id.

Declarations that call a *zero-argument* factory (``Au = gold()``, ``MT.java:636`` -> ``gold()``
returns ``noblemetal(790, …)``) carry their id inside the factory body, so the id lookup cannot see
them; this lists them so the id resolver can be checked against the real declarations.

Usage:  python tools/report_material_form_idless.py
"""

from __future__ import annotations

import json
import pathlib

REPORT = pathlib.Path("docs/gt6-form-flags.json")


def main() -> None:
    materials = json.loads(REPORT.read_text(encoding="utf-8"))["materials"]
    idless = {name: data for name, data in materials.items() if not data.get("ids")}
    with_flags = {name: data for name, data in idless.items() if data["flags"]}
    print(f"materials in the report: {len(materials)}")
    print(f"without a captured id: {len(idless)} (of which {len(with_flags)} have flags)")
    for name, data in sorted(with_flags.items()):
        print(f"  {name:28} {','.join(sorted(data['flags'])[:8])}")
    print("--- idless and flag-less (ignored) ---")
    print("  " + ", ".join(sorted(name for name in idless if not idless[name]["flags"]))[:800])


if __name__ == "__main__":
    main()
