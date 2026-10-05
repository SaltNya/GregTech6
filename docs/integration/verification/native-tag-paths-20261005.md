# Issue 16: native tag resource paths

NeoForge 1.21 uses `tags/item` and `tags/block`, while Forge 1.20.1 uses the plural directories. The Neo runtime material tag pack now normalizes all legacy callers before emitting both child tags and their parent references, including clay balls, glass panes and moldforms. Existing `forge:` identities remain compatible with the native `c:` aliases.

Each actual fresh-world recipe registry was inspected: 278653 nonempty declared GT ingredient positions per platform, with zero ingredients resolving to no items. Forge retained its correct plural paths. This proves loaded GT crafting tags in these installations; it does not prove every external addon recipe.
