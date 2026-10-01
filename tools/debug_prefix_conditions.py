"""Debug helper for tools/compare_prefix_conditions.py: show what it parses for a few prefixes."""

from __future__ import annotations

import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location(
    "cmp", pathlib.Path("tools/compare_prefix_conditions.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

helpers = mod.port_helpers()
print(f"helpers parsed: {len(helpers)}: {sorted(helpers)}")
for name in ("HAS_PROJECTILE", "GT6_PROJECTILES", "HAS_DUST", "GT6_PLATES"):
    print(f"  {name:18} {helpers.get(name, '(absent)')[:80]}")

flags = mod.generator_flags()
port = mod.port_prefixes(flags)
for name in ("bulletGtLarge", "dust", "minecartWheels", "toolHeadArrow", "gem", "plateDense"):
    entry = port.get(name)
    print(f"  {name:16} flags={entry['flags'] if entry else '(no entry)'} props={entry['properties'] if entry else ''}")
