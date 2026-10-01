"""Enumerate the non-ASCII characters of a file, with counts and code points.

Usage:  python tools/report_non_ascii_chars.py <file> [...]
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    for name in sys.argv[1:]:
        path = Path(name)
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        counts = Counter(c for c in text if ord(c) > 127)
        print(f"{path}: bom={raw.startswith(b'\\xef\\xbb\\xbf')}, distinct non-ascii={len(counts)}")
        for char, count in counts.most_common(20):
            print(f"    U+{ord(char):04X} x{count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
