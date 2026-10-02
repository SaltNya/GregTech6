# 管道超温、邻域点火与木管可燃性

日期：2026-10-02。工作树：`C:\Dev\GregTech6\GregTech6-main`。承接 [魔法危害批次](fluid-pipe-magic-20261002.md)。

## 原版规则与实现

原 GT6 `MultiTileEntityPipeFluid:320-331` 在每个通道的流体危害处理之后、分配之前检查 `temperature > maxTemperature`，空通道也检查。过热时对六邻域执行 `setOnFire()`，每通道独立 1/100 抽签；抽中则清空所有通道，再把中心换成普通火焰并立即返回。仅整 tick 未遇非空通道时才在循环结束后降/升温 1 K。等于阈值安全，等离子耐性不绕过耐温限制。

两版管道已插入这一顺序，独立 protected 抽签方法保持生产概率并允许测试固定结果。新增平台 `PipeIgnition` 适配原版 `WD.burn/fire:702-727`：

- 跳过岩浆、已有火；普通火焰状态使用 `Blocks.FIRE`，不因灵魂土改成灵魂火。
- 只处理地毯或当前碰撞形状为空的目标；可燃的实心木板也不能直接被此函数替换。
- 原版 GT `BlockBase/IBlockBase`、`BlockBaseFluid`、多实体方块等族的 `IItemGT` 非易燃保护，在当前工程以 `gregtech` 注册命名空间归属映射；可燃 GT 目标仍允许点燃。现代接口没有 UNKNOWN 方向，检查六面任一可燃性。
- 增加 `gregtech:pipe_fire_protected` 方块标签，供兼容层明确保护节点等外部方块。这不是自动识别 Thaumcraft INode 或所有第三方旧接口的实现；第三方范围保留待验。

共享 `FluidPipeSafety.canIgnite` 保留排除、形状和非易燃 GT 保护规则。没有套用玩家打火器的编辑权限或“只点空位”逻辑。

## 木管火焰参数

原版管材注册只有木、处理木开启可燃标志，传入 NBT 值 150。`TileEntityBase07Paintable:107-108` 对可燃性和火焰蔓延速度都返回此值。共享 PipeSpec 新增参数，两版方块分别覆盖这两个现代火焰接口；40×7 个规格的两种木管均为 150，其余为 0。保留原有构造和工厂签名的重载，其旧调用默认 0；当前注册完整传递共享 spec。

原版泡沫覆盖还能屏蔽可燃性，目前管道没有对应泡沫状态；本批不声明泡沫交互或全部材质行为完成。接触伤害开关、阻挡/外观、硬度等仍须继续对照。

## 回归范围

共享新增 286 条断言：280 个管材规格的原版可燃性值、6 个点燃规则边界。行为合同共 1,860，另材料 6,160、热力学 53、设备规格 34，共 8,107 条已通过。

新 `FluidPipeOverheatTests` 八项，在不同绝对高度的活跃测试区使用真实管道和世界方块，覆盖：六面空气点火；地毯/实心可燃块/岩浆/已有火/GT 流体保护；外部保护标签；烧毁前清空且不向邻管转移；阈值与空管先烧毁后冷却；四通道空管逐通道抽签后只冷却一次；耐等离子管仍超温烧毁；首通道冷流体覆盖旧热量与首空通道先检查旧热量的区别。

旧物理危险夹具固定“超温不烧毁”抽签，使原有泄漏和热伤害检查可重复，但仍执行邻域点火。新的过热场景独立强制销毁，不再用旧测试的存活假设掩盖新增分支。已有目录场景检查全部注册方块的可燃性和火焰蔓延速度。

保护标签的火把条目只在两版 bootstrapGameTest 资源中，用于验证外部保护路径；正式成品必须确认不包含该测试标签。它不改变生产版火把可燃规则。

首轮 Forge 47 项中 46 项通过，`neighborShapeLavaFireAndGtFluidProtection` 在布置断言失败：圣水没有注册世界方块，不能用来验证 GT 非碰撞世界方块保护。查阅 `Loader_Fluids` 的 WORLD_FLUID_PATHS 后，将两版目标改为已注册的沼泽水世界方块，保留命名空间、空碰撞和保护结果断言；生产规则未因该失败调整。首轮日志 `work/fluid-overheat-tests.log`，5m12s、退出 1，服务器正常保存关闭，NeoForge 未执行。该轮不计全部通过。

修正后 `:core:check :runGameTestServer :neoforge:runGameTestServer` 成功（6m59s、30 项任务、退出 0）。Forge 18:57:45、NeoForge 19:00:41 各 `All 47 required tests passed`，两服务器正常保存退出；日志 `work/fluid-overheat-acceptance.log`。Forge 复用首轮测试世界，场景清理后全部通过；不是独立世界重载验收。

复现采用本地已校验 Gradle 8.8、Java 17/21、`--offline --no-daemon`，开发参数 `-PdirectCoreResources=true -PdirectCoreClasspath=true -PgameTestHeap=3g -PgameTestNamespaces=gregtech_fluid_channels`。两模块测试目录各为 `build/fluid-overheat-tests`。正式构建不带 directCore 参数。

正式构建与成品检查运行中，最终验包待写入。

## 来源与验收边界

- 原 GT6 `MultiTileEntityPipeFluid.java` SHA-256：`3a6850055375e7975145b03abab44c5922746a6f4053dd8d3163de989f37b110`。
- 原 GT6 `WD.java` SHA-256：`c8335988b7bd9dbf44df6790d867ac6cfe2e6414793abb0cdd14c32cd342f095`。
- 原 GT6 `TileEntityBase07Paintable.java` SHA-256：`5d1319131c91d93690e5f6ece787210de15756283103a4ec6b94738bb07c5b28`。
- 原版及 wolfram `TileEntityBase01Root.setToFire` 均使用普通火焰；原版 `TileEntityBase10ConnectorRendered:205-206` 的泡沫保护记录为后续缺口。

沿用作者署名、LGPL-3.0-or-later 和 NOTICE，参考目录只读，无新运行时依赖。开发服务器的确定性瞬时检查不等于长时间火灾蔓延模拟、客户端、生存取得、独立世界重载或成品安装运行。命名空间保护是当前块族的现代映射，不据此宣称第三方旧接口或 Thaumcraft 节点已兼容。
