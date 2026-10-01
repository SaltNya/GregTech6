# 书架修复核对（2026-09-23）

原版依据是 `gregapi/tileentity/inventories/MultiTileEntityBookShelf.java`、`gregapi/load/LoaderBookList.java`、`gregapi/data/CS.java` 中的 `PlankData`，以及 `gregtech/loaders/b/Loader_MultiTileEntities.java`。目标是还原书架，而不是按空心模型主观缩小碰撞。

## 已核实并处理

- **几何**：原版六段木框（上下板、左右柱、十字隔板），两面各 14 本，共 28 槽。现有 `bookshelf.json` 的六个长方体和 `BookShelfGeometry.bookBounds` 对应原版渲染 pass 1–34；原有四朝向交互 GameTest 遍历全部 112 个可见书位。原版 `TileEntityBase01Root.getCollisionBoundingBoxFromPool()` 返回整格，书架只覆盖 *选中/射线盒* 为朝向轴的 2/16–14/16，故保留当前整格物理碰撞及内缩选中框。所谓“看得到洞就可走进去”不符合原版碰撞。
- **默认框架纹理**：原版 `CS.PlankData.PLANKS[0]` 和 `PLANK_ICONS` 默认值是 `Blocks.planks:0`，即橡木板。端口原来误用通用 `planks_wood` 图，现将默认模型及可重生成资源脚本统一改为 `minecraft:block/oak_planks`。
- **摆放与工具**：仍是四个水平朝向；通过项目统一 `ToolInteractionTarget`/`ToolInteractions` 支持原版普通扳手调面，书籍库存不因转向丢失。木质书架的 Forge 着火/蔓延值改为原版 `NBT_FLAMMABILITY=150`；注册硬度与抗爆由并行注册修复统一到原版 2.0/2.0。
- **特殊物品**：补齐 GT6 `BOOK_REGISTER` 内的石按钮、拉杆、红石火把、鹅卵石；石按钮和红石火把沿用原版编号 2 的书籍纹理，鹅卵石按原版用鹅卵石贴图。按钮点击保持 120 tick 的 15 级弱红石信号；拉杆/红石火把点击切换持续 15 级信号。潜行点击或镊子可取走，放大镜读取名称；自动化不可提取这些机关物品。
- **地牢书籍显示**：接回原版每 300 tick 检查一次附近 32 格玩家的延迟战利品生成。先前仅在点击/破坏时生成，故靠近地牢时书架长期看起来是空架。
- **光照（2026-09-27 复核）**：原版木质书架由 `Loader_MultiTileEntities` 的 `aWooden` 多方块容器注册，`aOpaque=F`，其方块光遮挡为 0；移植版曾把 `getLightBlock` 固定为 15，使架内书籍可能显黑。现在改为 0，`BookShelfGeometryTests` 对四个朝向都检查此值。书架物理碰撞仍按原版保留整格，选中框仍沿朝向轴缩进 2/16。14 张书籍纹理已逐一校验与原版字节相同；书架资源 Python 单测 3/3 通过，GameTest 待本批统一执行。
- **书架家族（2026-09-27）**：新增 `bookshelf_variants.json` 作为原版编号、材料、名称、外框纹理、硬度、抗爆、着火值的单一清单，注册 15 种有真实板材纹理的木书架及 GT6 `metalset` 表的全部 60 种金属书架。原 `gregtech:bookshelf` 保持橡木默认名称与物品 ID；其余 74 种各有独立方块、物品、四朝向方块状态与背包模型。金属外框按材料颜色着色，木材使用对应板材纹理；金属要求扳手挖掘，木材要求斧，所有变体共用原版 28 格双面藏书、附魔强度、整格物理碰撞和不遮光行为。生成器 `tools/generate_bookshelf_family.py` 可从已入库的清单重建资源；只有使用 `--refresh-manifest` 重抓 GT6 原表时才需要原项目目录。`BookShelfFamilyTests` 检查所有 75 种的注册、材质、强度、工具、库存和几何，并实际给蓝云杉及钢书架存书。
- **生存合成（2026-09-27 续补）**：GT6 `Loader_MultiTileEntities.java:143,181-183` 给金属书架注册 `PTP/sdh/PTP`（同材料螺丝、板 + 锯、螺丝刀、锤），给有有效 `PlankData.PLANKS[i]` 的木书架注册 `PPP/sfr/PPP`（对应板材 + 锯、锉、软锤）；`MultiTileEntityRegistry.java:208` 确认这些行是实际 `CR.shaped(..., CR.DEF_REV_NCC, ...)` 配方，没有 `CR.MIR`。现由 `tools/generate_bookshelf_family.py` 根据同一变体清单生成 75 条 `recipes/bookshelves/*.json`，保留原图案、不镜像，并用 `gregtech:tool_shaped` 返还磨损后的工具。金属板和螺丝用按材料区分的 `forge:plates/<material>`、`forge:screws/<material>`，可接受通用同材质物品；15 种木板则严格使用对应物种，不会混成任意木板。`BookShelfCraftingTests` 在游戏内检查 75 个结果、每种材料形态及实际 3×3 合成与工具返还。

## 证据与未验收事项

- 首轮新世界 `build/bookshelf-repair-gametest.log`：`All 113 required tests passed :)`，`EXIT:0`。该轮已经覆盖按钮/拉杆/镊子及原有书架几何、资源同步；它发生在默认橡木纹理、着火值、靠近生成和扳手 GameTest 加入之前。
- 上一批书架代码通过 `python tools/javac_selfcheck.py` 的定向编译；新增两个 GameTest 分别验证附近玩家唤醒书架、扳手转向与库存/选框。当时的全新世界 `build/repair-batch23b.log` **119 项全部通过**；首次测试曾因模拟玩家缺 Netty channel 在准备阶段失败，改用可被真实空间查询找到的普通 mock 玩家后通过。本批新增家族注册之后的统一门禁见下一项。
- 变体静态资源测试 `python -m unittest tools.tests.test_bookshelf_assets tools.tests.test_bookshelf_family -v` 为 **5/5**；涉及书架的 7 个 Java 文件经 `tools/javac_selfcheck.py` 定向编译通过。新增的家族 GameTest 与全量 Gradle 编译已在 `build/gametest_batch43_water_green.log` 的 953/953 门禁通过；这仍不能替代客户端模型与颜色的目视验收。
- 本轮配方静态验证：`python tools/generate_bookshelf_family.py --check` 校验 **75/75** 份生成 JSON；`python -m unittest tools.tests.test_bookshelf_family tools.tests.test_bookshelf_assets -v` **7/7**，其中直接校验原版两套图案和全部输出、材质标签、工具；`python tools/javac_selfcheck.py src/main/java/com/gregtech/gregtech/gametest/BookShelfCraftingTests.java` 通过。新增 GameTest 尚待主任务统一 Gradle 门禁，不能把上述静态检查当作运行时合成已经验证。
- GT6 分配了 300 个木材编号，但这些编号包括未装载第三方模组时无有效板材的空位；目前仅为有可用贴图的 15 种建立精确变体和对应配方。移植项目现有松木与乌木板材模型指向缺失 PNG，故未把它们强行作为可用木书架；补齐来源纹理后可在生成器的 `WOODS` 中追加。其他第三方板材、地牢库房按 `tShelf` 选木种、额外书籍映射与魔法材料附魔加成仍未还原。材质着色、模型朝向、挖掘掉落与客户端交互仍需 runClient 检查。
