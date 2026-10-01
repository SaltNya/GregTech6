# P2 material item visual source integration

This change connects Neo material items to the same material icon selection and assets as Forge. Per the user's latest direction, this batch has not been compiled, tested, or started in either platform. Source integration is complete for this scope; visual/runtime acceptance remains pending.

## Shared selection and resources

`core/api/material/MaterialIconDefinitions` extracts the original `client/MaterialIcons` material selection in this exact order: explicit texture set, WOOD, STONE, GEM → RUBY, ORE → STONE, DUST → FINE, METAL → METALLIC, otherwise DULL. Both platform `client/MaterialIcons` classes only create Minecraft resource identifiers around the shared string paths/JSON. The original 41 `MaterialTextureSet.MODELED` entries and prefix texture filenames remain the single definitions; the core class imports no Minecraft or loader types.

The original `models/item/material/**` family and its local parent/texture closure move from `src/main/resources/assets/gregtech/` into `core/src/main/resources/assets/gregtech/`, keeping their paths relative to `assets/gregtech` and all bytes. The move includes 4,346 material models, the `item/coin_minted` parent, and 8,612 PNG textures: 8,610 under `item/material_icons` and `block/iconsets/coin` plus `coin_side`. Total: 12,959 files, 3,148,869 bytes. No other core resource tree is replaced.

The dependency read found no missing local parent/texture paths. The only external parents are vanilla `minecraft:item/generated` and `minecraft:block/block`. `coin_minted` is an ordinary vanilla elements model, so its static appearance needs no custom geometry loader. Coin data-driven minting/placement and the original Forge `CoinItemBakedModel` specialization remain a separate Neo platform gap.

`core/provenance/material-visual-resource-extraction.json` records the original saltnya import revision `415617825945a9f54b11fdc359ff9b3cf694c8cd`, shared source/destination path prefixes, and each moved file's source Git blob, byte length and SHA-256. It also records the original icon/model/tint source classes and inspected Neo API archive identities. Original author information and authorization status are retained; this move grants no new license.

The existing build embeds core output in both distribution jars. Removing the former Forge locations provides one resource source and avoids introducing duplicate entries. Packaging for this new batch is unverified.

## Neo client boundary

The new `neoforge/client/MaterialClientModels` uses `@EventBusSubscriber(... value = Dist.CLIENT, bus = MOD)` and never enters common setup. It registers all shared model identifiers, aliases each real `GTItems` holder to the selected baked model, and registers material color on tint layer 0 with white overlays. Model resolution uses the original primary set and then the original `MODELED` fallback order; a baked missing-model sentinel is rejected. It neither adds a second material catalog nor a second item definition stream.

The signatures were read from the locally resolved official 1.21.1/NeoForge 21.1.243 sources:

- `ModelEvent.java:48–63`: modifiable `Map<ModelResourceLocation, BakedModel>`.
- `ModelEvent.java:139–155`: `RegisterAdditional.register(ModelResourceLocation)` requires the `standalone` variant.
- `ModelResourceLocation.java:23–31`: separate `inventory(ResourceLocation)` and `standalone(ResourceLocation)` keys.
- Patched `ModelBakery.java:120–124`: additional models are loaded using their underlying ID and registered with the supplied standalone key; `:63` provides `MISSING_MODEL_VARIANT`.
- Patched `ModelManager.java:225–228`: baking-result modification precedes dispatch to the final model map.
- `RegisterColorHandlersEvent.java:113`: item registration accepts `ItemColor, ItemLike...`.

The event only reads the supplied baking map, without accessing the client singleton during resource loading. Inventory aliases use real holder registry IDs; model registration and lookup consistently use the Neo standalone keys. Source/API reads support these implementation choices, not a claim that the resource reload or item rendering has succeeded.

## Remaining scope

Actual baked model availability, the copper/tin/bronze and ash item appearance, palette/overlay correctness, resource reload, and dedicated-server class loading remain unverified for this commit. The Neo coin specialization, full material tooltip/translation resource closure, creative catalog UI, machine/block rendering and held tool models are still pending outside this item-model scope. Prior startup and bronze-chain evidence predates this visual change and must not be reported as its acceptance.
