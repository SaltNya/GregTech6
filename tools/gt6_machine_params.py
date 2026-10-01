#!/usr/bin/env python3
"""Print GT6 machine registration parameters (energy, input, min/max, parallel, material).

Usage: python tools/gt6_machine_params.py "Coke Oven" "Implosion Compressor" ...
"""
import re
import sys
from pathlib import Path

SOURCE = Path(
    r"F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java"
    r"\gregtech\loaders\b\Loader_MultiTileEntities.java"
)


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    # Split on registration boundaries so multi-line registrations stay together.
    starts = [m.start() for m in re.finditer(r"aRegistry\.add\(", text)]
    starts.append(len(text))
    blocks = [text[starts[i]:starts[i + 1]] for i in range(len(starts) - 1)]

    wanted = sys.argv[1:]
    for name in wanted:
        hits = 0
        for block in blocks:
            head = block[:200]
            if f'"{name}' not in head:
                continue
            display = re.match(r'aRegistry\.add\(\s*"([^"]*)"', block)
            if not display:
                continue
            shown = display.group(1).strip().rstrip("(").strip()
            if shown != name:
                continue
            mat = None
            for candidate in re.finditer(r"aMat\s*=\s*([^;]+);", text[: text.find(block)]):
                mat = candidate
            energy = re.search(r"NBT_ENERGY_ACCEPTED\s*,\s*TD\.Energy\.(\w+)", block)
            nbt_input = re.search(r"NBT_INPUT\s*,\s*(-?\d+)", block)
            nbt_min = re.search(r"NBT_INPUT_MIN\s*,\s*(-?\d+)", block)
            nbt_max = re.search(r"NBT_INPUT_MAX\s*,\s*(-?\d+)", block)
            parallel = re.search(r"NBT_PARALLEL\s*,\s*(\d+)", block)
            parallel_duration = "NBT_PARALLEL_DURATION" in block
            hardness = re.search(r"NBT_HARDNESS\s*,\s*([\d.]+)F", block)
            tex = re.search(r'NBT_TEXTURE\s*,\s*"([^"]+)"', block)
            hits += 1
            print(
                "%-26s mat=%-18s energy=%-4s input=%-6s min=%-5s max=%-7s parallel=%-5s parDur=%-5s hardness=%-6s tex=%s"
                % (
                    name,
                    mat.group(1).strip() if mat else "?",
                    energy.group(1) if energy else "-",
                    nbt_input.group(1) if nbt_input else "-",
                    nbt_min.group(1) if nbt_min else "-",
                    nbt_max.group(1) if nbt_max else "-",
                    parallel.group(1) if parallel else "-",
                    parallel_duration,
                    hardness.group(1) if hardness else "-",
                    tex.group(1) if tex else "-",
                )
            )
        if hits == 0:
            print("%-26s NOT FOUND" % name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
