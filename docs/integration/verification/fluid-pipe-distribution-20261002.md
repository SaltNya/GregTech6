# 流体管道：炼药锅、多目标压力及面连接

日期：2026-10-02。工作树：`C:\Dev\GregTech6\GregTech6-main`。承接 [通道身份批次](fluid-pipe-channels-20261002.md)，旧批次的结论仅代表其当时源码。

## 来源与行为

对照只读原 GT6 `C:\Dev\gregtech6-master\gregtech6-master\src\main\java\gregapi\tileentity\connectors\MultiTileEntityPipeFluid.java` 的 `distribute`、`fill`、`breakBlock` 及 `FL.WATER` 分类；继续参考 wolfram0108 的现代炼药锅方块适配。原来源 SHA-256、作者和许可归属见前批记录及项目 NOTICE。本批没有整体替换任何来源项目，也没有变更注册 ID、存档字段或 Minecraft 版本。

- 炼药锅先于普通邻居分配；空锅和水锅分开判断，补一、二、三档分别消费 334、667、1000 mB。只允许原版 WATER 分类（包括蒸馏水、河水等），海水不因属于现代水标签而自动获得资格。源面连接和流体过滤盖板均有效；不会覆盖熔岩锅、细雪锅。
- 普通分配只选择低液位、流体身份兼容且接收面开放的邻管；机器先模拟 1 mB，拒绝时再模拟全部可提供流体，以兼容最小批量接收器。拒收机器不计入分母。
- 均分分母包括源管道、所有候选邻管和接受机器，分子只包括源管道及候选邻管液量；统一向上取整。邻管先填，机器后填，再向邻管推送源管道超过半容量的剩余压力。管道和机器列表分别随机插入，避免固定方向优先。
- 平台共用 `FluidPipeChannels.distributionLevel/pressureShare/cauldronCost`；均值先除后加，避免多个 long 储量求和溢出。内部邻管转移保留 long 储量，外部能力按平台 int 契约提供流体。
- 所有有方向的能力请求均返回懒创建的面包装器，每次操作读取当前连接和盖板。实际接受外部填充才标记对应通道的回流位，模拟不改内容或回流；内部无方向操作保留。直接邻管候选按原版在选择时标记接收位，包括因目标容量不足未实际转移的情况。
- 拆管转移检查源面连接、源过滤和接收能力；接收管道的面包装器负责其连接与过滤。原版炼药锅专用消耗不计入普通传输计数，保持该分支语义。

## 验证

- `:core:check :compileJava :neoforge:compileJava :compileBootstrapGameTestJava :neoforge:compileBootstrapGameTestJava`：成功，30 秒，17 项任务。共享四组共 6375 条断言：128 行为、6160 材料、53 热力学、34 设备规格。日志：`work/pipe-distribution-compile.log`。
- 初轮游戏回归：两版各 15 项通过，任务退出 0（3m33s）。日志：`work/pipe-distribution-gametest.log`。
- 随后删除已经没有生产调用方的旧逐对均衡 helper 及其 6 项旧策略断言，增加原均值奇数取整断言；最终共享四组为 **6370** 条（123 / 6160 / 53 / 34），不是测试丢失。测试储液桶显式清空旧方块，拆管测试改成实际 `removeBlock`，检查源实体已移除及接收液量。
- 最终 `:core:check :runGameTestServer :neoforge:runGameTestServer`：成功，3m55s。Forge 16:23:14、NeoForge 16:24:48 各 `All 15 required tests passed`，两服务器正常保存退出。日志：`work/pipe-distribution-final-tests.log`。
- 正式 `:build :neoforge:build`：成功，3m59s，28 项任务；未使用 directCore 开发选项。日志：`work/pipe-distribution-build.log`。
- `tools/integration/verify_artifacts.py`：通过。585 个当前 core class 与两版 JAR 逐字节一致；两版模组信息、许可/NOTICE、无重复项及无测试专用条目验证通过。[验包回执](fluid-pipe-distribution-artifacts-20261002.json)。

新增 10 项平台游戏场景，加上前批 5 项通道测试，共每平台 15 项。使用真实注册钢管、不锈钢桶、流体和盖板，手动调用服务器 tick；不同场景使用独立坐标。炼药锅测试还包含 9 组水位/余量固定数值。旧 Forge `PipeCoverTests` 面过滤测试补上明确打开两面的前置步骤，避免关闭连接掩盖过滤行为。

复现沿用本地经官方哈希验证的 Gradle 8.8，Java 17 / 21、`--offline --no-daemon` 和连接/读取 15 秒超时。开发测试用 `-PdirectCoreResources=true -PdirectCoreClasspath=true`，正式构建不用这些选项。测试命名空间 `gregtech_fluid_channels`，最终两平台测试目录分别位于各自模块的 `build/pipe-distribution-final-20261002`。

## 边界与后续

最终产物：

| 平台 | 项目相对路径 | 字节数 | SHA-256 |
|---|---|---:|---|
| Forge 1.20.1 | `build/libs/gregtech6-1.20.1-forge-0.0.0.jar` | 38,484,095 | `3aeb4d6ed3493f957f57ea5961ff8c7cf9901a127452b4ee43e88ce7fc647cfc` |
| NeoForge 1.21.1 | `neoforge/build/libs/gregtech6-neoforge-1.21.1-0.0.0.jar` | 36,675,702 | `0513996aa864c5f417032345d4bacbc8f4d0782cee85de963d86e36a58f5fa2c` |

本批是开发环境单次/连续两次 tick 的行为回归，不代表客户端观察、生存获得设备、完整网络性能、成品安装运行或独立进程读写存档已验收。最小批量机器的模拟兜底已实现，但本批实际机器夹具是普通储液桶，不能据此声明所有第三方处理器兼容。

仍需推进玩家桶操作的点击面过滤及容器回写、管道危险损耗与传输统计/温度时序、完整盖板组合，以及真实保存重载和双平台客户端/成品范围。目标保持进行中。

后续桶交互的具体依据：当前 `FluidPipeBlockEntity.handleUse` 的填满容器分支执行 `heldHandler.drain` 和 `this.fill` 后没有将 `heldHandler.getContainer()` 写回玩家手中；本机 Forge 47.4.20 源码包 `FluidBucketWrapper.setFluid` 是替换包装器内部 `container`，并不会自行替换玩家物品栏。下一批应采用平台的容器交互事务，验证生存空/满桶、堆叠、空间不足、创造模式、面连接及过滤，不能只添加一次 `setItemInHand` 就声称容器语义完整。
