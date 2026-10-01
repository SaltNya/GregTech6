#!/usr/bin/env python3
"""Generate lang entries for all GTTechnological items (item.gregtech.<id>)."""

import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
JAVA = os.path.join(ROOT, "src", "main", "java", "com", "gregtech", "gregtech",
                    "registry", "GTTechnological.java")
LANG_EN = os.path.join(ROOT, "src", "main", "resources", "assets", "gregtech", "lang", "en_us.json")
LANG_ZH = os.path.join(ROOT, "src", "main", "resources", "assets", "gregtech", "lang", "zh_cn.json")

VOLTS = {"ulv", "lv", "mv", "hv", "ev", "iv", "luv", "zpm", "uv", "puv1", "xv"}

ZH = {
    "compact": "紧凑型", "electric": "电力", "motor": "马达", "pump": "泵",
    "conveyor": "传送带", "piston": "活塞", "robot": "机械", "arm": "臂",
    "force": "力场", "field": "力场", "emitter": "发射器", "signal": "信号",
    "sensor": "传感器", "cover": "覆盖板", "blank": "空白", "crafting": "合成",
    "table": "台", "machine": "机器", "status": "状态", "display": "显示",
    "automatic": "自动", "switch": "开关", "energy": "能量", "redstone": "红石",
    "auto": "自动", "selector": "选择器", "manual": "手动", "reboot": "重启",
    "1m": "(1分钟)", "5m": "(5分钟)", "10m": "(10分钟)", "20m": "(20分钟)", "30m": "(30分钟)",
    "activity": "活动", "detector": "侦测器", "possible": "(可行)", "running": "(运行)",
    "processing": "(处理中)", "success": "(成功)", "progress": "进度", "drain": "排液口",
    "air": "空气", "vent": "通风口", "item": "物品", "fluid": "流体", "filter": "过滤器",
    "controller": "控制器", "shutter": "闸门", "button": "按钮", "panel": "面板",
    "warning": "警告", "conductor": "导体", "accept": "(接收)", "emit": "(发射)",
    "retriever": "回收", "pressure": "压力", "value": "阀", "logistics": "物流",
    "cpu": "CPU", "logic": "逻辑", "control": "控制", "storage": "存储",
    "conversion": "转换", "filtered": "过滤", "export": "输出", "import": "输入",
    "bus": "总线", "generic": "通用", "dump": "倾倒", "laser": "激光",
    "emptygas": "空气", "helium": "氦", "neon": "氖", "argon": "氩", "krypton": "氪",
    "xenon": "氙", "heliumneon": "氦氖", "carbonmonoxide": "一氧化碳", "carbondioxide": "二氧化碳",
    "usb1": "USB1", "usb2": "USB2", "usb3": "USB3", "usb4": "USB4",
    "stick": "存储棒", "cable": "线缆", "hdd": "硬盘", "crystal": "晶体",
    "circuit": "电路", "diamond": "钻石", "emerald": "绿宝石", "ruby": "红宝石",
    "sapphire": "蓝宝石", "processor": "处理器", "socket": "插槽", "plate": "基板",
    "copper": "铜", "gold": "金", "platinum": "铂", "magic": "魔法", "enderium": "末影",
    "signalum": "信素", "hsla": "HSLA", "wire": "导线", "wiring": "布线",
    "board": "电路板", "basic": "基础", "good": "良好", "advanced": "高级",
    "elite": "精英", "master": "大师", "ultimate": "终极", "part": "部件",
    "enderpearl": "末影珍珠", "endereye": "末影之眼", "power": "能量", "module": "模块",
    "lead": "铅", "acid": "酸", "cell": "电池", "empty": "(空)", "filled": "(满)",
    "alkaline": "碱性", "nickel": "镍", "cadmium": "镉", "lithium": "锂",
    "cobalt": "钴", "manganese": "锰", "slicer": "切片机", "shape": "模板",
    "flat": "(平整)", "grid": "(网格)", "eights": "(八等分)", "hollow": "(空心)",
    "split": "(对半)", "quaters": "(四等分)", "press": "冲压", "bullet": "子弹",
    "casing": "弹壳", "small": "小型", "medium": "中型", "large": "大型",
    "extruder": "挤压", "low": "低温", "heat": "", "longrod": "长杆", "bolt": "螺栓",
    "ring": "环", "ingot": "锭", "tinypipe": "微型管", "smallpipe": "小型管",
    "mediumpipe": "中型管", "largepipe": "大型管", "hugepipe": "巨型管", "block": "块",
    "swordblade": "剑刃", "pickaxehead": "镐头", "shovelhead": "锹头", "axehead": "斧头",
    "hoehead": "锄头", "hammerhead": "锤头", "filehead": "锉刀头", "sawblade": "锯片",
    "gear": "齿轮", "bottle": "瓶", "curvedplate": "弯板", "smallgear": "小齿轮",
    "rod": "杆", "capsulecellcontainer": "胶囊容器", "foil": "箔", "tinyplate": "小板",
    "finewire": "细线", "foodmold": "食物模具", "bun": "圆面包", "bread": "面包",
    "baguette": "法棍", "cylinder": "圆柱", "toast": "吐司",
}


def parse_overrides(text):
    overrides = {}
    for m in re.finditer(r'put\("([^"]+)",\s*"([^"]+)"\)', text):
        overrides[m.group(1)] = m.group(2)
    return overrides


def parse_ids(text):
    array = text.split("String[] IDS = {")[1].split("};")[0]
    return re.findall(r'"([a-z0-9_]+)"', array)


def en_name(item_id, overrides):
    if item_id in overrides:
        return overrides[item_id]
    parts = [p for p in item_id.split("_") if p]
    words = []
    for i, p in enumerate(parts):
        if p in VOLTS and i == len(parts) - 1:
            words.append("(" + p.upper() + ")")
        else:
            words.append(p.capitalize())
    return " ".join(words)


def zh_name(item_id):
    parts = [p for p in item_id.split("_") if p]
    out = []
    for i, p in enumerate(parts):
        if p in VOLTS and i == len(parts) - 1:
            out.append("(" + p.upper() + ")")
        else:
            out.append(ZH.get(p, p.upper() if len(p) <= 4 else p.capitalize()))
    return "".join(out)


def main():
    text = open(JAVA, encoding="utf-8").read()
    overrides = parse_overrides(text)
    ids = parse_ids(text)
    for path, namer in ((LANG_EN, lambda i: en_name(i, overrides)), (LANG_ZH, zh_name)):
        with open(path, encoding="utf-8-sig") as f:
            lang = json.load(f)
        for item_id in ids:
            lang["item.gregtech." + item_id] = namer(item_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(lang, f, indent=2, ensure_ascii=False, sort_keys=True)
            f.write("\n")
    print(f"tech lang entries: {len(ids)} per language")


if __name__ == "__main__":
    main()

    from sync_standard_chinese import sync
    sync()
