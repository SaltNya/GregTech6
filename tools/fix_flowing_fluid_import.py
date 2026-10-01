"""FlowingFluid lives in net.minecraft.world.level.material, not in the Forge fluids package."""

import io
import os

PATH = os.path.join("src", "main", "java", "com", "gregtech", "gregtech", "loaders", "a", "Loader_Fluids.java")
text = io.open(PATH, encoding="utf-8").read()
text = text.replace("import net.minecraftforge.fluids.FlowingFluid;\n", "")
text = text.replace("import net.minecraft.world.level.block.LiquidBlock;",
                    "import net.minecraft.world.level.material.FlowingFluid;\n"
                    "import net.minecraft.world.level.block.LiquidBlock;", 1)
io.open(PATH, "w", encoding="utf-8", newline="\n").write(text)
print("FlowingFluid import fixed")
