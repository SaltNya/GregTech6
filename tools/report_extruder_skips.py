"""Group the Extruder rows the transpiled set had to skip, from the newest gate log.

The extruder set is the one that keeps losing rows to missing content, and the reasons differ in
kind: a form GT6 itself never registers is not a port defect, while a form GT6 has and the port
lacks is a real gap. This tool prints both, so the next batch can be sized from evidence.

Usage:  python tools/report_extruder_skips.py [path/to/gametest.log]
"""

from __future__ import annotations

import collections
import pathlib
import re
import sys

LOG = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "build/gametest.log")


def main() -> None:
    if not LOG.exists():
        raise SystemExit(f"no log at {LOG} - run the GameTest gate first")
    text = LOG.read_text(encoding="utf-8", errors="replace")
    rows = collections.Counter()
    reasons = collections.Counter()
    total = 0
    for line in text.splitlines():
        if "chem skip (Extruder)" not in line:
            continue
        total += 1
        match = re.search(r"in=(\S+) fIn=(\S+) fOut=(\S+) out=(\S+)", line)
        if not match:
            continue
        in_token, f_in, f_out, out = match.groups()
        if out != "ok":
            parts = out.split(":")
            rows[parts[1] if len(parts) > 2 else out] += 1
            reasons["missing item form"] += 1
        elif in_token != "ok":
            rows["input " + in_token] += 1
            reasons["missing input"] += 1
        elif f_in != "ok":
            rows["fluid in " + f_in] += 1
            reasons["missing fluid input"] += 1
        elif f_out != "ok":
            rows["fluid out " + f_out] += 1
            reasons["missing fluid output"] += 1
        else:
            reasons["recipe-map rejection (collision)"] += 1
    print(f"{total} skipped extruder rows in {LOG}")
    for reason, n in reasons.most_common():
        print(f"  {n:5}  {reason}")
    print("-- by symbol --")
    for symbol, n in rows.most_common(25):
        print(f"  {n:5}  {symbol}")


if __name__ == "__main__":
    main()
