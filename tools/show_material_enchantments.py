"""Print a few material enchantment rows from the generated table."""

import io
import re

text = io.open("src/main/java/com/gregtech/gregtech/loaders/c/GTEnchantmentTable.java",
               encoding="utf-8", errors="replace").read()
for name in ["Diamond", "Gold", "Plastic", "Iron", "Ruby", "Thaumium"]:
    match = re.search(r'new Material\("' + name + r'", List\.of\(([^;]*?)\)\),', text)
    if not match:
        print("%-10s -> not in table" % name)
        continue
    print("%-10s -> %s" % (name, match.group(1)[:300]))
