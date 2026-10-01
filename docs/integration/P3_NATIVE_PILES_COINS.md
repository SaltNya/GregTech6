# P3 — Native material piles and coins

Use source1 complete3 single-material piles and4x4 coin pile, real slot merging/taking/top-column/removal/world placement and stockpile/coin expiry handlers. Share pile capacity/height/27 ordered offsets plus coin grid selection/repack and mint pixel depth/cell bounds in core, consumed by both platform implementations. Adopt brokestar metadata equality guard for stockpiles to retain distinct item payloads while preserving original cross-item canonical material identity. Native parses/saves full stack components under original gt.value/gt.coin.item and16 stacksize keys, synchronizes real sizes/material/custom die, and upgrades existing registered material coin items in place to source CoinItem rather than registering duplicate coins. Port original block/entity and stamped-item renderers; source core mint data reused. masson mold boundary is compared, not substituted for coin piles.

- The preceding ordinary Neo server startup predates all construction/bars/spikes/piles/coins from this turn; these batches are compile-covered only.
- Stocked pile previews/getDrops clear contents as source; drop/removal conservation and event ordering are not runtime-proven. Source load allows count above64 and onLoad then invalid STACK state; malicious/noncanonical save still an unresolved source gap.
- Source stockpile merge used only prefix/material and could lose differing tags. Adopt brokestar full-tag merge guard while retaining baseline canonical material equivalence: Forge tag equality and Neo component-patch equality. Cross-item vanilla material defaults/components remain unverified.
- Source stockpiles allow auxiliary empty blocks and column walk stops at255; these differences remain documented.
- Coin 200-tick settle/repack, custom32-row die, creative handling, full inventory rejection, collision and renderer/texture UV have not been exercised in game. Inventory aliases retain existing baked material model and stamped-die wrapper; material model resource gaps still apply.
- masson coinage mold has explicit stamped/blank automation boundary but lacks this pile feature in inspected file; no unrelated second material/coin registry imported. Full coinage mold/play chain integration remains pending.
- Native expiry extends life rather than cancellation; source expiry collision with other handlers or world protection remains unverified.
- Forge runtime/client/server of these batches/independent reload/old saves/new production jars are not proven.

Grouped compile passed20s. Native ItemExpireEvent has no cancellation: a completed stockpile transfer discards the entity and an incomplete transfer extends6000ticks; coins extend200ticks. No new fixtures or repeated startup. Full integration remains active.
