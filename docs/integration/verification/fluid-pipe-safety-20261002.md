# 流体管：实际温度、独立物理耐性与泄漏统计

日期：2026-10-02。工作树：`C:\Dev\GregTech6\GregTech6-main`。承接 [玩家容器批次](fluid-container-interaction-20261002.md)。

## 实现与来源

原 GT6 `gregapi/tileentity/connectors/MultiTileEntityPipeFluid.java:277-341` 在每个通道开始时读取流体温度，首个非空通道替换上一 tick 的温度，之后保留已经遇到的最高温度；仅整 tick 没有非空通道时向环境变化 1 K。气体、等离子体、酸性各自检查对应耐性，依次泄漏 8、64、16 单位并施加各自伤害；实际泄漏记入传输量，之后才分配该通道并清除其回流位。

本批两版采用上述温度与三个物理危险分支的顺序。共享 `FluidPipeSafety` 保存独立损失计划和温度规则，平台负责流体分类、注册温度及未知流体的 FluidType 回退、实体伤害和世界变更。修复旧的“任意危险不耐受就累加所有危险”的错误，以及酸性分支提前返回导致漏掉复合流体热伤害的问题。统计在 tick 开始清零，泄漏与正常输出共同累计，液量不足时只累计实际移除量。

腐蚀随机决策仍为每次酸性分支 1/100；隔离为 protected 方法供游戏测试强制两种结果。生产概率未改。销毁前排空所有通道，避免方块拆除回调把本该销毁的内容输出给邻管。

原版来源 SHA-256：`3a6850055375e7975145b03abab44c5922746a6f4053dd8d3163de989f37b110`。只读 wolfram0108 对应文件核对了同一处理顺序，SHA-256：`f368a2cea36dd76b0d22e393de21e7fcc8eec0ee021e96805b552cc23e077335`。原作者及 LGPL-3.0-or-later 归属沿用 NOTICE，没有新引入依赖或修改参考目录。

## 回归场景

共享新增 14 条固定期望：气密钢的酸气损失、仅耐酸时仍漏气、三物理危害叠加、全耐性、首通道覆盖旧温度、后续最高温度、空管升降温及 long 极值。

新增双平台 `FluidPipeSafetyTests` 七项，与既有 24 项管道/玩家容器场景一起运行：

1. 钢管装 100 mB 氯化氢后保留 84，泄漏统计 16，而非 24。
2. 木管同样流体保留 76；仅剩 10 时统计 10；空管下一 tick 清零。
3. 钢管等离子体损失 64，钛管同样流体保留 100。
4. 多通道最高温、冷流体替换旧高温、空管每 tick 降 1 K。
5. 木管 100 mB 天然气漏 8 后两管各 46，源传输统计 54。
6. 强制腐蚀销毁首通道时，其他通道一起清空且邻管没有收到拆管残液。
7. 活跃测试区域内的牛受到木管蒸汽实际温度造成的热伤害。

这些是实际注册方块和实体的开发服务端测试。只有腐蚀随机抽签被测试子类控制；没有用手写模拟容器替代管道。场景分别使用不同高度，清理旧管残液并重置自动连接。

## 验证记录

`:core:check :runGameTestServer :neoforge:runGameTestServer` 首轮通过，7m41s，30 项任务，退出 0。Forge 17:43:05、NeoForge 17:46:09 各记录 `All 31 required tests passed`，两服务器正常保存并关闭。共享合同合计 6,384 条断言：137 行为（12 组）、6,160 材料、53 热力学、34 设备规格。日志：`work/fluid-safety-tests.log`。

复现使用本地已验证的 Gradle 8.8、Java 17/21、`--offline --no-daemon`、`-PdirectCoreResources=true -PdirectCoreClasspath=true -PgameTestHeap=3g -PgameTestNamespaces=gregtech_fluid_channels`，两个模块的测试目录各为 `build/fluid-safety-tests`。正式构建不使用 directCore 参数。

正式 `:build :neoforge:build` 成功，3m05s，28 项任务，退出 0，日志 `work/fluid-safety-build.log`。`verify_artifacts.py` 验包通过：587 个当前 core class 在两包中逐字节一致，双版模组信息、许可/NOTICE、无重复项及无测试专用条目通过。[完整验包回执](fluid-pipe-safety-artifacts-20261002.json)。

| 平台 | 项目相对路径 | 字节数 | SHA-256 |
|---|---|---:|---|
| Forge 1.20.1 | `build/libs/gregtech6-1.20.1-forge-0.0.0.jar` | 38,487,377 | `f2929faac5f65951443fb80c984f436bb9ad4d13f804f41d6055f9bbef46bb34` |
| NeoForge 1.21.1 | `neoforge/build/libs/gregtech6-neoforge-1.21.1-0.0.0.jar` | 36,677,804 | `135e53f75dcd6f7bfe0b1782f0ac51ddeaf79b78e08947128fb3dad55c868bfe` |

## 未覆盖和后续

魔法流体泄漏、魔法防护注册与污染方块兼容，以及超温向邻域起火/销毁为火焰的分支尚未移植。等离子体测试本批只验证物理耐性；添加超温分支后需要同时覆盖高温后果，不能为了保留旧测试而跳过它。酸性实体伤害沿用已有公共实现，本批强制腐蚀场景验证的是移除和内容销毁；热伤害有新增活体证据，但不扩大为全部生物、护具和创造模式验收。

后续注册对照已确认：原版 `Loader_MultiTileEntities.java:1846-1885` 的管道目录包含独立魔法耐性、木/处理木 340 K、塑料 370 K、橡胶 350 K 的专用阈值。当前共享目录把全部魔法耐性写为 false，`PipeSpec.maxTemperature()` 又覆盖 record 的阈值字段而从材料重新计算；Forge 注册也重建 spec（NeoForge 直接使用共享 spec），不能仅改共享构造参数解决。目录中部分容量和酸/等离子耐性也不同（例如原版钛管基础容量 300、不耐酸/等离子，而当前为 400、两者均耐受）。本批钛管测试仅验证现有 spec 的执行，不宣称材质目录符合原版；后续应逐项修正目录、注册适配和相应测试。缺失 Thaumcraft 污染方块时，原版 `IL.block()` 经 `ST.block(null)` 返回 `CS.NB = Blocks.air`，已核实其空气回退，不应臆造第三方现代注册 ID。

传输统计本批覆盖 tick 内泄漏和分配，原版拆管输出统计仍需单独对照。炼药锅消耗沿用原版不计传输的既有规则。没有验证独立 JVM 存档重载、客户端、生存取得链路或成品安装运行；不以本批声明完整流体危险系统或整个移植完成。
