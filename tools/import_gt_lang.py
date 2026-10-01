#!/usr/bin/env python3
"""Merge GregTech.lang (GT6 legacy) into 1.20.1 JSON lang files."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANG_SRC = ROOT.parent / "GregTech.lang"
JAVA_SOURCES = (
    ROOT / "tools/generated/materials-source.java.txt",
    ROOT / "src/main/java/com/gregtech/gregtech/data/ImportedMaterialData.java",
    ROOT / "src/main/java/com/gregtech/gregtech/data/AntimatterMaterials.java",
)
ZH_OUT = ROOT / "src/main/resources/assets/gregtech/lang/zh_cn.json"
EN_OUT = ROOT / "src/main/resources/assets/gregtech/lang/en_us.json"

GT_LANG_RE = re.compile(r'^\s*S:([^=]+)=(.*)$')
MATERIAL_LINE_RE = re.compile(
    r"(\w+(?:\s*,\s*\w+)*)\s*=\s*(?:\w+\.)?(?:create|metal|element|alloy|ore|gem|dust|gas|wood|stone|elec|cent|clay)\(\s*[^,]+,\s*\"((?:\\.|[^\"\\])*)\""
)
LOCAL_NAME_RE = re.compile(r'\.setLocalName\("((?:\\.|[^"\\])*)"\)')

GT_LANG_TOOLTIPS = {
    "gt.lang.contained.materials": "tooltip.gregtech.contained_materials",
    "gt.lang.has.shapeless": "tooltip.gregtech.shapeless_recipes",
}

EXTRA_ZH = {
    "tooltip.gregtech.f3h_hint": "启用 F3+H 模式以查看所含材料信息。",
    "tooltip.gregtech.material_from_gt": "材料来自格雷科技",
    "tooltip.gregtech.vanilla_material": "原版材料",
}
EXTRA_EN = {
    "tooltip.gregtech.f3h_hint": "Enable F3+H Mode for Info about contained Materials.",
    "tooltip.gregtech.material_from_gt": "Material from GregTech",
    "tooltip.gregtech.vanilla_material": "Vanilla Material",
    "tooltip.gregtech.contained_materials": "Contained Materials:",
    "tooltip.gregtech.shapeless_recipes": "Has Shapeless Recipes with Amounts: ",
}


def sanitize(name: str) -> str:
    return name.replace(" ", "").replace("-", "").replace("'", "")


def load_gt_lang() -> dict[str, str]:
    entries: dict[str, str] = {}
    if not LANG_SRC.is_file():
        print(f"Warning: lang source missing: {LANG_SRC}")
        return entries
    for line in LANG_SRC.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = GT_LANG_RE.match(line)
        if match:
            entries[match.group(1).strip()] = match.group(2)
    return entries


def load_json(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_material_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if MATERIAL_LINE_RE.search(lines[i]):
            block = lines[i]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("."):
                block += lines[i]
                i += 1
            blocks.append(block)
        else:
            i += 1
    return blocks


def parse_material_entries() -> list[tuple[str, str, str, str | None]]:
    """(field, factory_name, registry_key, setLocalName)."""
    entries: list[tuple[str, str, str, str | None]] = []
    for java_file in JAVA_SOURCES:
        if not java_file.is_file():
            continue
        for block in parse_material_blocks(java_file.read_text(encoding="utf-8")):
            match = MATERIAL_LINE_RE.search(block)
            if not match:
                continue
            field = match.group(1).split(",")[0].strip()
            factory_name = match.group(2)
            registry = sanitize(factory_name)
            local_match = LOCAL_NAME_RE.search(block)
            local_name = local_match.group(1) if local_match else None
            entries.append((field, factory_name, registry, local_name))
    return entries


def english_display(factory_name: str, registry: str, local_name: str | None) -> str:
    if local_name and " " in local_name:
        return local_name
    return factory_name


def gt_lang_lookup(gt_lang: dict[str, str], field: str, factory_name: str) -> str | None:
    for candidate in (factory_name, field, sanitize(factory_name)):
        value = gt_lang.get(f"gt.material.{candidate}")
        if value:
            return value
    return None


def merge_materials(gt_lang: dict[str, str], zh: dict[str, str], en: dict[str, str]) -> tuple[int, int]:
    entries = parse_material_entries()
    # Canonical keys belong to the material whose registry name they are. GT6 field names are
    # sometimes the *local* name of a different material (MT's field `Gold` is the BiomesOPlenty wood
    # "Goldwood"), and writing that field as an alias key would overwrite the metal gold's own entry.
    canonical = {registry.lower() for _, _, registry, _ in entries}
    zh_count = 0
    en_count = 0
    skipped = 0
    for field, factory_name, registry, local_name in entries:
        json_key = f"material.gregtech.{registry.lower()}"
        gt_value = gt_lang_lookup(gt_lang, field, factory_name)
        if gt_value:
            zh[json_key] = gt_value
            zh_count += 1
        en[json_key] = english_display(factory_name, registry, local_name)
        en_count += 1
        if field != registry:
            alias_key = f"material.gregtech.{field.lower()}"
            if field.lower() in canonical and field.lower() != registry.lower():
                skipped += 1
                continue
            if gt_value:
                zh[alias_key] = gt_value
            en[alias_key] = en[json_key]
    if skipped:
        print(f"Skipped {skipped} field-name aliases that would shadow another material's key")
    return zh_count, en_count


def main() -> None:
    gt_lang = load_gt_lang()
    zh = load_json(ZH_OUT)
    en = load_json(EN_OUT)

    zh_count, en_count = merge_materials(gt_lang, zh, en)

    for gt_key, json_key in GT_LANG_TOOLTIPS.items():
        if gt_key in gt_lang:
            zh[json_key] = gt_lang[gt_key]

    zh.update(EXTRA_ZH)
    en.update(EXTRA_EN)

    write_json(ZH_OUT, zh)
    write_json(EN_OUT, en)
    print(f"Merged {zh_count} material entries into zh_cn.json")
    print(f"Wrote {en_count} material entries into en_us.json")


if __name__ == "__main__":
    main()

    from sync_standard_chinese import sync
    sync()
