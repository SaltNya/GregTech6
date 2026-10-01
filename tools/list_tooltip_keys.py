"""List shared tooltip keys available in the port's language file (for the bookshelf tooltip)."""

import io
import re

text = io.open("src/main/resources/assets/gregtech/lang/en_us.json", encoding="utf-8",
               errors="replace").read()
keys = re.findall(r'"(tooltip\.gregtech\.[a-zA-Z0-9_.]+)":\s*"([^"]*)"', text)
for key, value in keys:
    if any(word in key.lower() for word in ("click", "gui", "magnif", "pincer", "interact")):
        print("%-58s %s" % (key, value[:70]))
print("--- total tooltip keys:", len(keys))
