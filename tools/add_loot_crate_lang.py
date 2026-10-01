"""Add the loot crate tooltip key (GT6 LH.TOOL_TO_OPEN_CROWBAR) to both language files."""

import os

LANG = os.path.join("src", "main", "resources", "assets", "gregtech", "lang")
ANCHOR = '"block.gregtech.loot_crate":'
NEW = {
    "en_us.json": "Open with a Crowbar: one random vanilla loot roll and the Crate itself",
    "zh_cn.json": "用撬棍撬开：随机一次原版战利品 + 箱子本体",
}

for name, value in NEW.items():
    path = os.path.join(LANG, name)
    with open(path, encoding="utf-8") as handle:
        lines = handle.readlines()
    if any('"block.gregtech.loot_crate.tooltip"' in line for line in lines):
        print("%s: tooltip key already present" % name)
        continue
    for index, line in enumerate(lines):
        if ANCHOR in line:
            indent = line[:len(line) - len(line.lstrip())]
            lines[index + 1:index + 1] = ['%s"block.gregtech.loot_crate.tooltip": "%s",\n' % (indent, value)]
            print("%s: inserted the tooltip key after line %d" % (name, index + 1))
            break
    else:
        raise SystemExit("%s: anchor %s not found" % (name, ANCHOR))
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.writelines(lines)
