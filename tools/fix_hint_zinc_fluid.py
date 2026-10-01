"""The galvanized steel hint's molten zinc: the port resolves it through the material fluid spec."""

import io
import os

PATH = os.path.join("src", "main", "java", "com", "gregtech", "gregtech", "content", "recipe", "GTMainRecipes.java")
text = io.open(PATH, encoding="utf-8").read()
assert text.count('"f:Zn:144", "f:Zn:144", "Loader_Recipes_Hints:50"') == 1
text = text.replace('"f:Zn:144", "f:Zn:144", "Loader_Recipes_Hints:50"',
                    '"m:Zn:144", "m:Zn:144", "Loader_Recipes_Hints:50"')
io.open(PATH, "w", encoding="utf-8", newline="\n").write(text)
print("molten zinc now uses the material fluid spec")
