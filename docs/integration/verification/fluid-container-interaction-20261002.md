# 玩家流体容器：点击面与物品回写

日期：2026-10-02。工作树：`C:\Dev\GregTech6\GregTech6-main`。承接 [流体分配批次](fluid-pipe-distribution-20261002.md)。

## 缺陷与实现

Forge 的管道和储液桶旧逻辑直接排空手持物品的流体能力，然后填充自身，没有把能力返回的容器替换回玩家手中。本机 Forge 47.4.20 源码包的 `FluidBucketWrapper.setFluid` 替换的是包装器内部的 `container`；这不等于替换玩家物品栏中的 ItemStack。因此不能仅凭管内新增 1000 mB 就判断倒桶成功。

本批新增 Forge `platform/forge/transport/FluidContainerInteraction`，采用与本工程 NeoForge 适配器一致的容器事务：先检查一个物品的内容，有流体时调用 `tryEmptyContainerAndStow`，空容器调用 `tryFillContainerAndStow`；由平台处理可接受液量、单个容器、堆叠结果入包或掉落、创造模式与声音；成功后替换所用手的物品。Forge 管道和储液桶均使用此适配器，NeoForge 储液桶保持既有事务实现。

双版管道的方块交互传递 `hit.getDirection()`；容器通过对应面的能力操作，接受连接限制、过滤与通道回流标记。无方向内部访问不再作为玩家桶操作的入口。玩家第一次用有流体的容器点击空过滤盖板仍先设定过滤条件，不转移流体；已设定后才尝试容器事务。

## 对照依据

- 原 GT6 `gregapi/tileentity/base/TileEntityBase06Covers.java:106-135,346-366`：盖板点击先处理，流体填入/排出通过目标面的拦截。
- 原 GT6 `gregapi/tileentity/connectors/MultiTileEntityPipeFluid.java:464-472,510-511`：通道选择与接收/输出连接限制。
- 原 GT6 `gregapi/tileentity/tank/TileEntityBase08FluidContainer.java:142-157`：容器入罐优先、消耗单件并给回结果；不是只更改流体能力。
- 本工程已有 NeoForge `platform/neoforge/transport/FluidContainerInteraction.java`：现代平台事务适配参考。本批并未新增第三方运行时。
- 平台行为直接核对本机 Forge 47.4.20 `FluidUtil` 与 `FluidBucketWrapper` 源码包。创造模式采用现代平台语义：原手持物保留，目标中的流体仍按交互增减；不声称这一点与 1.7.10 原实现逐指令一致。

作者和许可归属沿用项目 NOTICE、LGPL-3.0-or-later 及第三方资源分项声明。

## 验证进度

首次编译中生产代码通过，NeoForge bootstrap 测试因 1.21.1 没有 `makeMockSurvivalPlayer` 而失败。改用各平台 `FakePlayerFactory`，显式设为生存模式，并为每项测试使用独立玩家与坐标。

首次 Forge 运行共 24 项，只有“物品栏满时掉落”失败：夹具填满了主物品栏，却空着副手，平台的合并玩家物品能力仍可接收结果。已根据同版本 `Player` 能力实现补上占满副手的前置条件；这是测试设置修正，不能将初轮记为全通过。初轮日志：`work/fluid-container-tests.log`。

该首轮在世界保存阶段还发生 `OutOfMemoryError: Java heap space`（默认测试堆 1536m）。确认错误后终止本次失败任务，进程清理完成；没有停止其他 Java 进程。NeoForge 测试启动增加与 Forge 相同的 `gameTestHeap` 参数支持，默认仍为 1536m；本批复核明确使用 `-PgameTestHeap=3g`，不改变普通客户端或服务器设置。

3g 复核消除了此次保存阶段 OOM，但“满物品栏掉落”仍有一次失败。读取其 `world/entities/r.220.220.mca`，确认存在 `minecraft:item`，坐标 `[113102.0,180.5,113000.5]`，物品 `minecraft:water_bucket`、`Count:1`、`Age:0`。该实体已产生并保存，远坐标区块却不在即时可见实体查询范围内。最终将该场景放在 GameTest 活跃区域，并在下一 tick 检查唯一掉落实物；保留物品栏与流体的即时数量检查。第二轮日志：`work/fluid-container-final-tests.log`。这次实体文件检查只证明指定结果实体，不能当作普遍存档兼容验收。

随后复用该测试世界，新增 9 项容器测试（含掉落）全部通过，但原 15 项管道夹具中有 7 项失败：旧夹具逐块移除管道会触发残液转移，新管的 `onPlace` 又会自动连接旧邻管，导致新场景带入上次液量。已在两版夹具的布置阶段排空旧管，并在放置后重置到默认断开状态；各场景随后自行建立需要的连接。没有修改生产的拆管或自动连接规则，也没有修改期望流量。该中间运行日志：`work/fluid-container-verified-tests.log`；不计为全通过。

新增 `FluidPipeContainerTests` 9 项服务器方块使用场景：副手往返、关闭点击面、盖板配置和双向过滤、不足一桶的空间/液量、堆叠空桶、物品栏满时结果掉落、创造模式、储液桶回写、倒桶后的单 tick 防回流。与上批 15 项管道测试共同运行。

最终验收运行 `work/fluid-container-acceptance.log`：Forge 在 17:12:49、NeoForge 在 17:15:52 均记录 `All 24 required tests passed`，两服务器正常保存退出。整个 `:core:check :runGameTestServer :neoforge:runGameTestServer` 成功，7m09s，30 项任务。共享四组 6370 条断言通过（123 行为 / 6160 材料 / 53 热力学 / 34 设备规格）。

复现参数：经官方哈希验证的本地 Gradle 8.8，Java 17 / 21，`--offline --no-daemon`，开发运行加 `-PdirectCoreResources=true -PdirectCoreClasspath=true -PgameTestHeap=3g -PgameTestNamespaces=gregtech_fluid_channels`。两版测试目录分别为各模块的 `build/fluid-container-final-20261002`；本次 Forge 复用已有测试世界，场景显式重置，NeoForge 为首次该目录运行。正式构建不用 directCore 开发选项。

正式 `:build :neoforge:build` 成功（6m11s，28 项任务），日志 `work/fluid-container-build.log`。`verify_artifacts.py` 验证通过：585 个当前共享 core class 与两包逐字节一致，双版模组信息、许可/NOTICE、无重复项及无测试专用条目均通过。[完整验包回执](fluid-container-artifacts-20261002.json)。

| 平台 | 项目相对路径 | 字节数 | SHA-256 |
|---|---|---:|---|
| Forge 1.20.1 | `build/libs/gregtech6-1.20.1-forge-0.0.0.jar` | 38,485,243 | `2bd5da9d80696f6f49c457c0eaa548aff92ff6bebb6624f294bd55083077f347` |
| NeoForge 1.21.1 | `neoforge/build/libs/gregtech6-neoforge-1.21.1-0.0.0.jar` | 36,675,692 | `34abf1f7cb9f32a6ff8f618f0a8bb5ef8ceb475b45a277652b7514227cb77832` |

## 验收边界

这些是开发环境内模拟服务端玩家直接调用方块使用入口的测试，有真实物品能力、物品栏和方块实体；不是客户端输入/网络预测、从生存采集开始的取得流程、独立 JVM 存档重载或成品安装运行证据。便携容器自身的 `onItemUseFirst`、旧版容器迁移和所有第三方容器的交互仍需单独对照，本批不据桶场景扩大结论。

下一批温度/危险规则的已读源码依据：原管道 `onServerTickPre` 在各通道处理时采用实际流体温度并保留已遇通道的最高温度；仅当全部通道为空时向环境温度变化 1 K。当前双版管道只做每 tick 最多 5 K 的环境趋近，没有从在管流体更新温度。危险泄漏目前先以“任一不防护”为门，再累加流体的所有危险类别，未逐项考虑本管已有防护；泄漏量也未记入当 tick 传输统计。魔法流体和超温分支另需对照。后续不能用只测普通水的场景宣称温度与危险系统完成。

后续实体受伤/状态效果夹具应放在 GameTest 的活跃区域，并按 tick 验证实体；仅 `getChunkAt` 读入远坐标方块，不足以证明该处实体已进入可查询、可 tick 的状态。
