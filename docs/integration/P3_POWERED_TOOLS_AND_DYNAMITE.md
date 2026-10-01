# P3 — Powered tools, mining charges and assembly

Source: preserved saltnya baseline, original authors/history/license unchanged. Exact source and baseline SHA-256 plus 31 copied asset references are in `core/provenance/powered-tools-dynamite-source-integration.json`. Source directories remain read-only.

## Adopted behavior and shared core

- Four real LV electric tool IDs: drill, chainsaw, wrench and screwdriver. `ElectricToolCatalog` owns original capacities/use costs, assembly rows and material eligibility for both platforms; `ElectricToolWearRules` owns material maximum, random wear bounds, saturating damage and scrap counts. Platform NBT/component storage remains thin.
- Neo uses the already registered LV–IV batteries through aliases, without duplicate battery factories. Powered tools use actual IItemEnergy packets and existing energy-node charging. EU charge and material wear remain separate; one final partial charge can pay a click, while the next click is disabled. Wrench/monkey-wrench dispatch, machine-first sneak switching, screwdriver dispatch, chainsaw target/leaf/ice rules and woodworking placement are preserved.
- Three original mining charges: dynamite (resistance 10, fortune 5), boomstick (10, 3), strong dynamite (40, 5). Actual directional/sunk states, 100-tick ignition, 20-tick remote/redstone ignition, defusing callback, fixed 3×3×3 resistance-filtered explosion, fortune loot and no item-entity damage. Original `Fuse` key is kept in native block entity storage.
- Original MultiItem `remote_activator` ID now has actual binding/activation behavior. Neo had not previously registered this family; its original metadata is used by the MultiItem registry. Up to 64 coordinates per dimension, a 128-block range on each axis, no forced loading of bound chunks, and the original keep-bound return contract. Legacy keys survive inside CUSTOM_DATA; every binding/activation write commits the updated component.
- Powered drill retains reverse inventory placement, native protection/rollback hooks, temporary sunk state via BLOCK_STATE component, actual EU/wear consumption and first available hotbar remote binding.
- Original material/battery assembly rows are generated into the mandatory native datapack, with exact tools and forms, no mirror, and actual battery-derived capacity/unpowered output. Dedicated serializer transmits stable tool/material/battery identities and reconstructs original ingredients/components, avoiding legacy ItemStack NBT. Native common forms accept `c:` tags. Manual tools in the recipe return with original wear. ImplosionRecipes is enabled now that actual dynamite exists.
- Original tool and explosive models/textures are retained, with PNGs in shared core and native color boundaries.

## Boundary choices and known gaps

Neo 1.21.1 removed the item's start-break hook. A native BreakEvent subscriber runs at LOWEST, respects earlier cancellations, calls the original protected chainsaw conversion and cancels vanilla processing only when conversion handled the block. Neo IShearable removed the explicit fortune argument; custom overrides receive the native enchanted stack/components. Runtime leaf/ice conversion still requires a checkpoint.

Unported ItemPipe/Bars concrete classes and GTGrass/Diggable substrate classes are not fabricated or registered here. Existing tag, natural-stone/ore, RockOre and fluid-pipe gates are retained; those class-specific branches return when their full native families are ported. The actual charge entity implements the defusing protocol; the spray extinguisher item is pending. The remote's original feedback/coordinate compatibility limitations are preserved. Full advanced button/lever behavior is pending.

## Verification

After three source waves, core/NeoForge/Forge Java compilation passed in 27 seconds. Five initial Neo API errors were corrected. Receipt: `verification/p3-powered-tools-compile.json`.

A single opt-in Neo ordinary-server checkpoint is running for actual recipe loading, charge simulation/injection/click consumption/partial depletion, independent material wear, native stack save/parse, assembly network round trip and real world fuse ignition/tick/defusing/remote binding. Fixture is excluded from production jars. Runtime status must be recorded from game markers, not Gradle exit alone.

No graphical client, complete survival, full blast/drill/chain-saw actions, independent world process restart, old-save compatibility or new production jar claim follows from compilation or this limited checkpoint.

First runtime attempt loaded 4,536 powered assembly rows (6,166 total vanilla recipes), then failed at the missing remote factory. The assumption that remote belonged to GTTechnological was corrected against original GTMultiItemsGen/GTMultiItems; its actual factory is now registered in the native MultiItem subset. Failed run/crash log are retained; retry is running. Gradle reported success after the crash, so this attempt is explicitly FAIL.

Retry PASSED in 1m32s: all nine reported powered checkpoint groups, 4,536 powered assembly rows/6,166 loaded vanilla recipes, 200 ticks and normal world save/stop. Actual observed game markers and failed/successful log hashes are recorded in `verification/p3-neoforge-powered-tools-checkpoint.json`. Client/chain-saw break events/full drill and explosion actions/remote air-use/full material matrix and independent process world reload remain unverified. The initial remote factory crash is retained as a failed result, even though Gradle reported success.
