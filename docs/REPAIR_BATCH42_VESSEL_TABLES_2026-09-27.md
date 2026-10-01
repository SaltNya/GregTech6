# 第四十二批：原版手工器皿与桌式变体（2026-09-27）

本批按 `gregtech6-master/src/main/java/gregtech/loaders/b/Loader_MultiTileEntities.java:2172-2177` 与对应 `MultiTileEntityBathingPot*`、`MultiTileEntityMixingBowlTable` 类核对。GTM 未用于复制代码。

- 32705 `mixing_bowl_table`：陶瓷混合碗桌，继承 Mixer 手工处理、六物品输入、8,000 mB 输入/输出罐、雨水收集与存档；桌式碰撞和渲染把盆抬高 8 px。
- 32707 `bathing_pot_table`：不锈钢浸洗盆桌，继承 Bath 配方与 8,000 mB 罐，桌式几何同上。
- 32720 `bathing_pot_table_wood`、32721 `bathing_pot_wood`：木制浸洗盆桌和独立木盆，Bath 配方、4,000 mB 罐、木材耐温、简单液体/酸/气体/魔法液限制及 100 可燃度。

四项原本均无移植版方块注册。本批复用既有 `ProcessingToolBlockEntity` 的物品、流体、手工加工、雨水、NBT 与掉落逻辑；新增原版两层纹理、桌底/桌侧纹理、方块及物品模型、中英名称和原版形状合成。桌式模型与碰撞由 `tools/rebuild_container_tool_models.py` 同源生成；方块实体动态液面与物品向上移动 8 px。木盆合成保留锯、锤、胶、木板和铅长杆的原版格局，三张桌由对应盆与砖台阶合成（GT6 的 `Blocks.stone_slab` metadata 4）。

定向 `PortRegressionTests.originalVesselTablesShareRecipesButKeepMaterialLimits` 覆盖四项的有效方块实体、配方表、容量、木材可燃与热液拒绝、水容量、NBT 及桌式外形，并用既有 Mixer 配方验证陶瓷桌真实加工。静态检查：16 个新增 JSON 解析通过、44 处模型贴图引用均存在，模型生成脚本 `py_compile` 与改动文件 `git diff --check` 通过。编译与 GameTest 交由总批次统一门禁，本文在门禁完成前不记通过。

## 当前占位判读边界

`docs/PLACEHOLDER_CENSUS_2026-09-23.md` 中的 53 个“纯端口主控”是修复前快照；当前 `GT6MultiblockIds` 记 117 项，其中 45 个被动结构件、72 个控制器、0 个标注占位、0 个缺失数值 ID。`MultiblockDefinitions.part()` 里的普通 `Block` 属被动结构件。`GTToolBlocks.simple()` 虽保留普通 `Block` 兜底，但当前所有显式调用 ID 都命中特化实现，不能把兜底分支当作一个实际注册的占位方块。此前列为占位的 `logistics_core`、`advanced_button`、`railroad`、`scaffold`、`coin_mold`、`concrete`、`sandwich_block` 与 `greg_lantern` 在后续批次已接行为，不应重复列为纯壳。

这不是 12,000 余个注册方块的逐块运行清单。已确认尚未等价的范围包括专用物流罐的网络存储节点、原版主控的部分端口权限与内部机制、跨模组兼容及客户端外观；它们与“注册物只有普通方块/纯端口”是不同缺口。约 300 种木质书架变体仍缺注册，另由书架批处理。本批没有修改板锭、硬币、书架或地牢文件。
