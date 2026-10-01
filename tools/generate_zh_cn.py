#!/usr/bin/env python3
"""Regenerate zh_cn.json from en_us.json + GregTech.lang."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_PATH = ROOT / "src/main/resources/assets/gregtech/lang/en_us.json"
ZH_PATH = ROOT / "src/main/resources/assets/gregtech/lang/zh_cn.json"
GT_LANG = Path(__file__).resolve().parents[2] / "GregTech.lang"

STATIC_EN_ZH = {
    "%s Block of Dust": "%s粉块",
    "%s Block of Gems": "%s宝石块",
    "%s Block of Ingots": "%s锭块",
    "%s Block of Plates": "%s板块",
    "%s Block of Gem Plates": "%s宝石板块",
    "%s Block of Ore": "%s矿石块",
    "%s Block of Cast Metal": "%s铸造金属块",
    "%s Machine Casing": "%s机械外壳",
    "%s Dense Machine Casing": "%s致密机械外壳",
    "%s Robust Machine Casing": "%s加强机械外壳",
    "%s Reinforced Machine Casing": "%s高强度机械外壳",
    "%s Crate of Dust": "%s粉板条箱",
    "%s Crate of Gems": "%s宝石板条箱",
    "%s Crate of Ingots": "%s锭板条箱",
    "%s Crate of Plates": "%s板板条箱",
    "%s Crate of Gem Plates": "%s宝石板板条箱",
    "%s Crate of Ore": "%s粗矿板条箱",
    "%s Slab": "%s半砖",
    "%s Plastic Tube": "%s塑料管",
    "%s Wooden Arrow": "%s木箭",
    "%s Billet": "%s短锭",
    "Molten %s": "熔融%s",
    "Crucibles / Molds": "坩埚/模具",
    "Fluid Types": "流体",
    "%1$s was boiled alive": "%1$s被活活烫死",
    "GregTech Smelting Crucible": "GregTech 熔炼坩埚",
    "GregTech Energy Buffer": "GregTech 能量缓存",
    "Top": "顶面",
    "No GUI. Click to interact!": "没有界面，右键以放入/取出物品!",
    "No GUI. Click to interact! (%1$s)": "没有界面，右键以放入/取出物品! (%1$s)",
    "This Mold produces %1$s": "这个模具生产 %1$s",
    "Use a Chisel in order to select the Shape of the Mold": "使用一个凿子选择模具的形状",
    "Blocks of Cast Metal": "铸造金属块",
    "Use Monkey Wrench to toggle automatic Inputs": "使用活动扳手调整自动输入",
    "Use Pincers to extract Items": "用取物钳取出发烫的内容物",
    "Use Soft Hammer to Reset": "使用软锤来重置",
}


def parse_gt_lang(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*S:([^=]+)=(.*)", line)
        if m:
            entries[m.group(1)] = m.group(2)
    return entries


def build_material_maps(gt: dict[str, str], en: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    by_id: dict[str, str] = {}
    from_gt: set[str] = set()
    for key, zh in gt.items():
        if key.startswith("gt.material."):
            mat_id = key[12:].lower()
            by_id[mat_id] = zh
            from_gt.add(mat_id)

    en_to_zh: dict[str, str] = {}
    for key, en_name in en.items():
        if key.startswith("material.gregtech."):
            mat_id = key[18:].lower()
            zh = by_id.get(mat_id, en_name)
            by_id.setdefault(mat_id, zh)
            if mat_id in from_gt:
                en_to_zh[en_name.lower()] = by_id[mat_id]
                en_to_zh[en_name.replace(" ", "").lower()] = by_id[mat_id]
            elif en_name.lower() not in en_to_zh:
                en_to_zh[en_name.lower()] = zh
                en_to_zh[en_name.replace(" ", "").lower()] = zh
    return by_id, en_to_zh


def build_fluid_map(gt: dict[str, str]) -> dict[str, str]:
    fluids: dict[str, str] = {}
    for key, zh in gt.items():
        if key.startswith("fluid."):
            fluids[f"fluid_type.gregtech.{key[6:]}"] = zh
    return fluids


def translate_material_phrase(text: str, en_to_zh: dict[str, str]) -> str:
    if text.lower() in en_to_zh:
        return en_to_zh[text.lower()]
    compact = text.replace(" ", "").lower()
    if compact in en_to_zh:
        return en_to_zh[compact]
    return text


def translate_value(key: str, en_val: str, gt: dict[str, str], mat_by_id: dict[str, str],
                    en_to_zh: dict[str, str], fluids: dict[str, str]) -> str:
    if en_val in STATIC_EN_ZH:
        return STATIC_EN_ZH[en_val]

    if key.startswith("material.gregtech."):
        return mat_by_id.get(key[18:].lower(), en_val)

    if key.startswith("fluid_type.gregtech."):
        if key in fluids:
            return fluids[key]
        if key == "fluid_type.gregtech.molten_material":
            return "熔融%s"
        if key.startswith("fluid_type.gregtech.molten."):
            mat_id = key[len("fluid_type.gregtech.molten.") :]
            zh_mat = mat_by_id.get(mat_id.lower())
            if zh_mat:
                return f"熔融{zh_mat}"
        return en_val

    m = re.fullmatch(r"Smelting Crucible \((.+)\)", en_val)
    if m:
        return f"熔炼坩埚 ({translate_material_phrase(m.group(1), en_to_zh)})"

    m = re.fullmatch(r"Mold Basin \((.+)\)", en_val)
    if m:
        return f"浇铸盆 ({translate_material_phrase(m.group(1), en_to_zh)})"

    m = re.fullmatch(r"Crucible Crossing \((.+)\)", en_val)
    if m:
        return f"坩埚浇铸道 ({translate_material_phrase(m.group(1), en_to_zh)})"

    m = re.fullmatch(r"Crucible Faucet \((.+)\)", en_val)
    if m:
        return f"坩埚浇铸口 ({translate_material_phrase(m.group(1), en_to_zh)})"

    m = re.fullmatch(r"Dense Burning Box \(Solid, (.+)\)", en_val)
    if m:
        return f"致密燃烧室 (固体, {translate_material_phrase(m.group(1), en_to_zh)})"

    m = re.fullmatch(r"Burning Box \(Solid, (.+)\)", en_val)
    if m:
        return f"燃烧室 (固体, {translate_material_phrase(m.group(1), en_to_zh)})"

    if en_val == "Brick Burning Box (Solid)":
        return "砖燃烧室 (固体)"

    m = re.fullmatch(r"Mold \((.+)\)", en_val)
    if m:
        return f"模具 ({translate_material_phrase(m.group(1), en_to_zh)})"

    if en_val.startswith("Molten "):
        mat = en_val[7:]
        zh_mat = translate_material_phrase(mat, en_to_zh)
        return f"熔融{zh_mat}"

    if "%s" in en_val and en_val in STATIC_EN_ZH:
        return STATIC_EN_ZH[en_val]

    # gt.* keys in en_us (if any)
    if key.startswith("item.gregtech.tool."):
        m = re.fullmatch(r"(.+) (.+)", en_val)
        if m:
            head, tool = m.groups()
            tool_map = {
                "Pickaxe": "镐",
                "Shovel": "铲",
                "Axe": "斧",
                "Sword": "剑",
                "Hoe": "锄",
                "Hammer": "锤",
                "Wrench": "扳手",
                "File": "锉",
                "Saw": "锯",
                "Screwdriver": "螺丝刀",
                "Wire Cutter": "剪线钳",
                "Knife": "刀",
                "Mortar": "研钵",
                "Rolling Pin": "擀面杖",
                "Spade": "铲",
                "Universal Spade": "通用铲",
                "Gem-tipped Pickaxe": "宝石尖镐",
            }
            if tool in tool_map:
                return f"{translate_material_phrase(head, en_to_zh)}{tool_map[tool]}"

    # oredict-style fallback from GregTech.lang
    ore_key = "oredict." + key.split(".", 2)[-1]
    if ore_key in gt:
        return gt[ore_key]

    return en_val


def main() -> None:
    gt = parse_gt_lang(GT_LANG)
    en = json.loads(EN_PATH.read_text(encoding="utf-8-sig"))
    mat_by_id, en_to_zh = build_material_maps(gt, en)
    fluids = build_fluid_map(gt)

    zh: dict[str, str] = {}
    for key, en_val in en.items():
        zh[key] = translate_value(key, en_val, gt, mat_by_id, en_to_zh, fluids)

    ZH_PATH.write_text(json.dumps(dict(sorted(zh.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(zh)} entries to {ZH_PATH}")


if __name__ == "__main__":
    main()
