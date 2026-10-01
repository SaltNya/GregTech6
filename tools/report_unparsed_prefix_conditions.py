"""List shared prefixes whose port condition the comparison could not parse.

``compare_prefix_conditions.py`` only sees conditions written in ``MaterialPrefix`` (item forms) and in
``MaterialPrefixes``' ``block("…")`` builders. Families the port implements in their own registries
(cables, cells/capsules, armor, pipes …) therefore show as "not parsed" — this lists them so the
"0 unconsulted flags" result is not over-claimed.

Usage:  python tools/report_unparsed_prefix_conditions.py
"""

from __future__ import annotations

import json
import pathlib

REPORT = pathlib.Path("docs/prefix-condition-comparison.json")


def main() -> None:
    conditions = json.loads(REPORT.read_text(encoding="utf-8"))["conditions"]
    unparsed = [name for name, entry in sorted(conditions.items())
                if not entry["portConditionParsed"]]
    print(f"shared prefixes: {len(conditions)}; without a parsed port condition: {len(unparsed)}")
    print("  " + ", ".join(unparsed))
    with_flags = [name for name in unparsed if conditions[name]["gt6Flags"]]
    print(f"  of those, GT6 declares flags for {len(with_flags)}: "
          + ", ".join(f"{name}({','.join(conditions[name]['gt6Flags'])})" for name in with_flags))


if __name__ == "__main__":
    main()
