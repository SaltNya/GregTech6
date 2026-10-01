"""Undo the extra DidYouKnow declaration: the port already has GT6's map (`gt.recipe.other`,
"Did you know...?", alias Other), so only the row table needed wiring."""

import io
import os

PATH = os.path.join("src", "main", "java", "com", "gregtech", "gregtech", "data", "MachineRecipeMaps.java")
lines = io.open(PATH, encoding="utf-8").read().split("\n")
before = len(lines)
lines = [line for line in lines
         if "GT6's hint pages (RM.DidYouKnow)" not in line
         and "tab. GT6 shares the internal key" not in line
         and "port does not have, so the page gets its own key." not in line
         and '"gt.recipe.didyouknow"' not in line]
removed = before - len(lines)
io.open(PATH, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("removed %d lines of the duplicate declaration" % removed)
