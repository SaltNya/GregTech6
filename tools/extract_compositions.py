#!/usr/bin/env python3
"""Generate MaterialCompositionData.java from GT6 MT.java composition chains."""

from __future__ import annotations

import re
from pathlib import Path

SRC = Path(r"f:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java\gregapi\data\MT.java")
OUT = Path(
    r"f:\Dev\GregTech\GregTech6\src\main\java\com\gregtech\gregtech\data\generated\MaterialCompositionData.java"
)

ASSIGN_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\w+)\s*\(")
INT_RE = re.compile(r"^-?\d+$")


def extract_balanced_args(text: str, open_index: int) -> str | None:
    depth = 0
    in_string = False
    escape = False
    for i in range(open_index, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : i]
    return None


def split_args(arg_str: str) -> list[str]:
    args: list[str] = []
    current: list[str] = []
    depth = 0
    in_string = False
    escape = False
    for ch in arg_str:
        if in_string:
            current.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            current.append(ch)
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
            continue
        current.append(ch)
    tail = "".join(current).strip()
    if tail:
        args.append(tail)
    return args


def find_calls(line: str, method: str) -> list[str]:
    results: list[str] = []
    needle = f".{method}("
    start = 0
    while True:
        idx = line.find(needle, start)
        if idx < 0:
            break
        open_idx = idx + len(needle) - 1
        args = extract_balanced_args(line, open_idx)
        if args is not None:
            results.append(args)
        start = idx + len(needle)
    return results


def parse_components(arg_str: str) -> tuple[int, list[tuple[str, str]]] | None:
    tokens = split_args(arg_str)
    if len(tokens) < 3:
        return None
    divider = 0
    start = 0
    if INT_RE.fullmatch(tokens[0]):
        divider = int(tokens[0])
        start = 1
    pairs: list[tuple[str, str]] = []
    i = start
    while i + 1 < len(tokens):
        mat = tokens[i].strip()
        amt = tokens[i + 1].strip()
        if re.match(r"[A-Za-z_][A-Za-z0-9_]*$", mat):
            pairs.append((mat, amt))
            i += 2
        else:
            i += 1
    if not pairs:
        return None
    if divider == 0:
        total = sum(parse_amount_units(amt) for _, amt in pairs)
        divider = max(1, total)
    return divider, pairs


def parse_amount_units(token: str) -> int:
    token = token.strip().replace(" ", "")
    m = re.fullmatch(r"(\d+)\*U", token)
    if m:
        return int(m.group(1))
    if token == "U":
        return 1
    m = re.fullmatch(r"U(\d+)", token)
    if m:
        return 1
    if INT_RE.fullmatch(token):
        return int(token)
    return 1


def amount_expr(token: str) -> str:
    token = token.strip().replace(" ", "")
    if token == "U":
        return "GTValues.U"
    m = re.fullmatch(r"(\d+)\*U", token)
    if m:
        return f"GTValues.U * {m.group(1)}"
    m = re.fullmatch(r"U(\d+)", token)
    if m:
        return f"GTValues.U{m.group(1)}"
    m = re.fullmatch(r"(\d+)\*U(\d+)", token)
    if m:
        return f"GTValues.U{m.group(2)} * {m.group(1)}"
    if INT_RE.fullmatch(token):
        return f"GTValues.U * {token}"
    return "GTValues.U"


def java_field(field: str) -> str:
    if field and field[0].isdigit():
        return f"M_{field}"
    return field


def main() -> None:
    lines = SRC.read_text(encoding="utf-8", errors="ignore").splitlines()
    entries: list[str] = []
    seen: set[str] = set()

    for line in lines:
        match = ASSIGN_RE.match(line)
        if not match:
            continue
        field = java_field(match.group(1))
        if field in seen:
            continue
        components: list[tuple[int, list[tuple[str, str]]]] = []
        for method in ("setMcfg", "setAloy", "uumMcfg", "uumAloy", "mcfg"):
            for args in find_calls(line, method):
                parsed = parse_components(args)
                if parsed:
                    components.append(parsed)
        if not components:
            continue
        seen.add(field)
        divider, pairs = components[-1]
        parts = ",\n                ".join(
            f"MaterialComponent.of(GTMaterialRegistry.get(\"{mat}\"), {amount_expr(amt)})"
            for mat, amt in pairs
        )
        entries.append(
            f"        bind(\"{field}\", {divider},\n"
            f"                {parts});"
        )

    body = "\n".join(entries)
    java = f"""package com.gregtech.gregtech.data.generated;

import com.gregtech.gregtech.api.material.GTMaterial;
import com.gregtech.gregtech.api.material.GTMaterialRegistry;
import com.gregtech.gregtech.api.material.GTValues;
import com.gregtech.gregtech.api.material.MaterialComponent;
import com.gregtech.gregtech.api.material.MaterialChemistry;

/** Auto-generated from GT6 MT.java composition chains. */
public final class MaterialCompositionData {{
    private MaterialCompositionData() {{}}

    public static void apply() {{
{body}
        MaterialChemistry.rebuildAll();
    }}

    private static void bind(String materialName, long divider, MaterialComponent... components) {{
        GTMaterial material = GTMaterialRegistry.get(materialName);
        if (!material.isValid()) {{
            return;
        }}
        java.util.ArrayList<MaterialComponent> valid = new java.util.ArrayList<>();
        for (MaterialComponent component : components) {{
            if (component != null && component.material().isValid()) {{
                valid.add(component);
            }}
        }}
        if (valid.isEmpty()) {{
            return;
        }}
        material.setComposition(divider, valid.toArray(MaterialComponent[]::new));
    }}
}}
"""
    OUT.write_text(java, encoding="utf-8")
    print(f"Wrote {len(entries)} composition bindings to {OUT}")


if __name__ == "__main__":
    main()
