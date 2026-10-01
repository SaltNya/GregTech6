"""List the materials the port's generated form table marks with a flag.

Usage:  python tools/report_form_flag_materials.py STONES [--limit 20]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "src" / "main" / "java" / "com" / "gregtech" / "gregtech" / "data" / "generated" / "MaterialForms.java"
ROW = re.compile(r'"([^"|]+)\|([A-Z_,]+)"')


def main() -> int:
    flag = sys.argv[1] if len(sys.argv) > 1 else "STONES"
    limit = 20
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    rows = ROW.findall(FORMS.read_text(encoding="utf-8"))
    matches = [key for key, flags in rows if flag in flags.split(",")]
    print(f"rows: {len(rows)}, with {flag}: {len(matches)}")
    print("  " + ", ".join(matches[:limit]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
