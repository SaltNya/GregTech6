# P3 — Item pipes and hopper families

The preserved saltnya snapshot supplies the complete registration/interaction baseline. Original author/history/license records remain unchanged. Exact original hashes, working-baseline hashes and adopted assets are tracked in `core/provenance/item-logistics-source-integration.json`. Source directories are read-only.

## Three source waves

- Shared `ItemPipeCatalog` supplies 21 original material families, six sizes and 126 stable block/item IDs. Both registration adapters use the same table and existing `ItemPipeSpec` rules. Native entities preserve the original buffer, routing, ingress tracking, side controls, item filter/retriever and panel covers, drops, wrench actions and connection shapes. Neo block capabilities return real sided views and explicitly invalidate cached views after cover/connection changes.
- Shared `HopperCatalog` supplies 60 normal and 60 FIFO queue variants, with original slot counts/material/hardness/resistance. Shared `HopperControlRules` supplies original byte mode cycling and slot limits. Full native entities retain timed output/input, exact/divisible normal modes, FIFO cascading, rail/minecart capability handling, world item collection, adjacent-inventory notifications, redstone gating, menus and legacy GT keys. Normal and queue blocks now implement the real screwdriver target contract. Existing native menu types/screens are reused.
- Original item-pipe dynamic models, cover renderer and hopper six-facing models/material colors are connected. Source PNGs, including all original composite color and overlay layers, are shared in core. Composite model loader namespaces are changed to `neoforge:composite`; original child geometry stays intact. `PipeWeldingRules` owns the original five rows and exact easy/hard work costs for both versions; native `PipeRecipes` builds real Welder/Boxinator/Unboxinator recipes over the same material identities. Original five wooden-pipe crafting rows are adapted to 1.21 result IDs and singular recipe paths.

## Native storage and API decisions

Grouped compilation initially found five API errors: native item equality uses components, and native minecart item capabilities have a Void context, so the old directional argument is removed. These are boundary changes, not a second inventory implementation.

Minecraft 1.21.1 `ItemStack.CODEC` restricts count to 1..99. Original large pipe buffers permit up to 2048. Native pipe storage therefore saves a component-bearing one-count template for counts above 99, with an explicit `gt.pipe_count` inside the existing `gt.items/Items` entry; ordinary counts keep the native format. Load and update tags restore the count within the original pipe capacity. Forge format remains unchanged. This preserves local native buffer counts; it does not prove migration of legacy Forge stacks or cross-version worlds.

## Comparison and pending choices

Read code, not prior project completion declarations:

- brokestar `mdk/src/main/java/gregtech6/tileentity/connectors/GTItemPipeBlockEntity.java` implements stable priority-queue minimum-step relaxation, minimum distance memoization, capacity gates and sorted transfer order.
- masson `logistics/pipe/item/ItemPipeNetworkTraversal.java` uses a loaded-only weighted frontier, a 32768-visited cap, stable endpoint ordering and logistics storage priority; `ItemPipeTransferPlan.java` reserves per-pipe budgets and revalidates topology before delivery. It depends on its own topology/storage/diagnostics interfaces and cannot be copied unchanged into a second runtime.
- masson `logistics/hopper/HopperTransferCore.java` has explicit mode/slot limits and separate simulated transfers. Its count/stack-limit arithmetic agrees with the baseline rules now shared; its handler-backed transfer core still requires adapter and divergent-handler comparison.

The baseline's first-exit BFS does not establish minimum weighted distance. Replacement with a shared weighted traversal is pending; this checkpoint preserves baseline behavior and does not claim it is the best implementation. Also pending: source direct-push actual remainder handling and disabled-input behavior of externally exposed pipe views. These are recorded candidates, not silently treated as solved.

## Validation and gaps

Initial grouped compile failed (21 seconds); corrected core/Neo/Forge Java compile passed (26 seconds). First fixture compile failed due to a vanilla/GT hopper wildcard-name conflict (3m23s); the corrected fixture ran and failed at second FIFO insertion (4m25s). This reproduced a baseline bug: inventory/block wake flags were cleared during cooldown even when processing had not run. Both platform hopper types now retain flags until a processing pass; real extraction also schedules inventory work. The unchanged FIFO cases are being rerun in a fresh world, without forcing an empty cooldown or manually waking extraction. The route fixture explicitly forces only its isolated pipe chunk to tick. A scoped Neo checkpoint is pending for actual registration, Welder rows, capability invalidation/filter components, oversized buffer save/load/update tag, exact normal emission, FIFO component order and an actual two-pipe transfer with no backflow. See the final receipts for authoritative outcomes.

No full matrix, client world interaction, complete survival acquisition, independent JVM reload, old-save compatibility or new production jar verification is claimed. The scoped fixture's in-memory save/load is not an independently restarted world.

No normal/queue hopper crafting recipe was found in the baseline runtime loaders, crafting catalogs or recipe resources inspected; survival acquisition remains a gap. Restrictive item pipes are intentionally skipped by baseline PipeRecipes; the original COATED.NOT material gate has no port equivalent. Wooden beams/species are not yet fully native, so the larger wooden-pipe recipes do not establish survival reachability. Logistics core, multiblocks, long-distance pipes and remaining world generation continue in later batches.


Final corrected checkpoint PASS (1m38s), fresh isolated world `neoforge/build/p3-item-logistics-startup-20261001-r3`: all listed native cases, 343 actual pipe processing rows, FIFO insertion across initial cooldown and advancement after extraction without manual wake, an actual 80-tick two-pipe route, then 200-tick ordinary server lifecycle and normal world save/stop. Both modified platform hopper classes compiled. Authoritative receipts: `verification/p3-item-logistics-compile.json` and `verification/p3-neoforge-item-logistics-checkpoint.json`. The two failed attempts and crash world are preserved; their Gradle exit status is not used as functional success.


Follow-up 2026-10-01: The weighted route and confirmed-transfer candidates are now integrated in both platforms and checked in a scoped native world. See P3_SHARED_ITEM_ROUTING.md and its receipts for adopted scope and remaining limits. Earlier baseline/failed-attempt evidence remains historical.
