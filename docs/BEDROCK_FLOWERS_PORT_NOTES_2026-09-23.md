# GT6 bedrock indicator flowers

Source: `gregtech/blocks/plants/BlockFlowersA.java` and `BlockFlowersB.java` in the original GT6 tree. The port has one block item per metadata value: 9 A flowers and 8 B flowers. The registry names remain stable, while English and Chinese display names now follow GT6 and the supplied `GregTech.lang` file.

Only A0/A1 contain 1 U Wheat, B0/B1 contain 1 U Acacia wood, and B6 contains 1 U Palm wood. The remaining 12 flowers indicate an ore but do **not** contain that ore. Original mortar/shredder, squeezer/juicer, hand-crafting, B7 smelting and `RM.biomass(8)` routes use the port's existing material forms, dye fluids, cactus juice and vanilla green dye (`IL.Dye_Cactus = Items.dye:2` in GT6).

GT6's optional IC2 extractor registrations remain absent: this port does not depend on IC2 or expose its extractor recipe map. GT6's ore-dictionary `flower` registration has no direct Forge item-tag equivalent added in this slice. No substitute outputs were invented for either omission.

After the unified build, validate that the generated Acacia/Palm stick and dust forms resolve and test B-family desert placement on natural sand. `BedrockFlowerRepairTests` covers all 17 metadata/material mappings, original harvest drops, representative machine routes and hand/smelting recipes.
