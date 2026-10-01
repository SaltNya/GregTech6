"""Rename GTNetherDepositFeature's private LAVA_LEVEL to the public NETHER_WATER_LEVEL."""

import io

PATH = "src/main/java/com/gregtech/gregtech/worldgen/GTNetherDepositFeature.java"
OLD = "    /** Nether lava sea level. */\n    private static final int LAVA_LEVEL = 31;"
NEW = ("    /** GT6's nether water level ({@code WD.waterLevel} in a no-sky dimension) - the lava sea. */\n"
       "    public static final int NETHER_WATER_LEVEL = 31;")

text = io.open(PATH, encoding="utf-8").read()
if "NETHER_WATER_LEVEL" in text:
    print("already renamed")
else:
    assert text.count(OLD) == 1, "anchors: %d" % text.count(OLD)
    text = text.replace(OLD, NEW)
    count = text.count("LAVA_LEVEL")
    text = text.replace("LAVA_LEVEL", "NETHER_WATER_LEVEL")
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(text)
    print("renamed %d usages" % count)
