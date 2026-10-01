"""Drop the retired port-only cover items' language keys (one key per line, line-based so the rest of
the file is untouched)."""
import pathlib

KEYS = (
    "item.gregtech.cover_conveyor",
    "item.gregtech.cover_pump",
    "item.gregtech.cover_redstone_repeater",
    "item.gregtech.cover_redstone_torch",
    "item.gregtech.cover_robot_arm",
    "item.gregtech.cover_tag_selector",
)

for name in ("en_us.json", "zh_cn.json"):
    path = pathlib.Path("src/main/resources/assets/gregtech/lang") / name
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = [line for line in lines if not any(f'"{key}"' in line for key in KEYS)]
    removed = len(lines) - len(kept)
    if removed:
        path.write_text("".join(kept), encoding="utf-8")
    print(f"{name}: removed {removed} lines, {len(kept)} remain")
