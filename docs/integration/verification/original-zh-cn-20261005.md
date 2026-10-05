# Issues 15 and 17: original Chinese patch

The user supplied `C:/Dev/GregTech_zh_cn.lang`. All 125676 original keys are retained verbatim. The importer binds 6520 modern aliases using original registration numbers, material names, source declarations and unambiguous names. Material items, material blocks and arrows read exact `oredict.<prefix><material>` names when present, preserving source names rather than composing new Chinese phrases. Stone blocks and slabs have individual keys (544 exact original bindings, 320 additional port names using English fallback).

Native registered creative pages are bound to their original prefix or MultiTileEntity/MultiItem page keys. Seven remaining unmapped prefix titles belong to the original hidden hot-ingot/scrap/plant pages and are not registered visible pages. Other missing or ambiguous port-only strings remain English; no new Chinese text is written. The importer records these gaps.

Both clients were switched to actual `zh_cn` and checked 864 stone inventory names, language key availability and six component-cover atlas sprites. The final Forge naming boundary passed enumeration of every patched registered material-form item and block (see final runtime receipt). Neither external translation packs nor an external addon installation were tested.

Hash, bindings, ambiguous keys, fallback keys, author/license evidence and source declarations: [source record](original-zh-cn-source-20261005.json).
