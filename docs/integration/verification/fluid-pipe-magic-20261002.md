# 流体管魔法泄漏、中毒与损毁

日期：2026-10-02。工作树：`C:\Dev\GregTech6\GregTech6-main`。承接 [管材参数批次](fluid-pipe-catalog-20261002.md)。

## 原版依据和实现

原 GT6 `MultiTileEntityPipeFluid.onServerTickPre:284-295` 在物理危害前独立检查魔法流体：不耐魔法时，气体泄漏 16、非气体泄漏 4；实际损失计入传输量，播放泄漏声，在半径 3 的包围盒内施加 1200 tick、放大等级 1 的中毒，然后以 1/100 概率清空所有通道并替换管道。若未销毁，再运行已有气体、等离子和酸性分支。即使本次泄漏耗尽罐内液体，进入通道时识别的魔法危害仍执行。

共享 `FluidPipeSafety.magicLoss` 保留这一独立规则，双平台在真实管道 tick 中使用。`FluidHazards.isMagic` 通过静态流体 MAGIC 标志或对应材料 MAGICAL 属性识别，流动形式沿用现有注册名解析；空流体与未知流体不被推定为魔法。后者对应原版 `FL.java:1119` 在创建材料流体时加入 MAGIC 集合。

范围效果直接交给 `LivingEntity.addEffect`，不套用热伤害或酸伤害的护具判断；由现代实体自身的状态效果规则决定能否接受中毒。独立 protected 销毁抽签方法默认仍为 1/100，游戏夹具只覆盖抽签结果，不替换世界操作。销毁前清空全部通道，避免拆管回调把内容输出给邻管。

## Thaumcraft 兼容范围

原版根据气/液选择 Thaumcraft flux gas/goo，未安装时 `IL.block()` → `ST.block(null)` → `CS.NB = Blocks.air`。当前工程尚无对应污染方块集成，本批实现其缺失时的空气回退；没有猜测现代第三方注册 ID 或生成替代污染方块。已装第三方污染模组时的替换、goo 等级和持久化仍须实际集成后验收。

## 验证场景

共享新增 7 条固定期望：魔法液体 4、魔法气体 16、魔法耐性分别保护两者、普通气/液无魔法损失、无防护魔法气体合计 16+8。四组共享检查合计 7,821 条断言（行为 1,574、材料 6,160、热力学 53、设备规格 34）。

两版新增 `FluidPipeMagicTests` 五项，与先前 34 项共同运行：

1. Holywater、XP、XP_Molten、Mob、Sap_Rainbow 的实际注册静止/流动形式为魔法；水、岩浆、空值不为魔法。
2. 钢管 100 mB 圣水变为 96，统计为 4；半径三内牛获得 1200 tick 中毒 II，范围外牛不受影响。
3. Desh 管保留全部圣水、不施加中毒，强制销毁抽签也不能越过魔法防护。
4. 仅剩 3 mB 时实际统计 3，仍施加中毒，下一空 tick 统计清零。
5. 首通道圣水触发损毁时，其他通道一起清空，连通邻管不收到任何残液。

游戏场景使用活跃测试区域、真实注册管道和牛，稀有随机结果由测试子类固定。此批注册世界场景采用魔法液体；魔法气体 16 与物理气体叠加的数值路径由共享合同覆盖，未宣称已验证注册魔法气体实体伤害。材料 MAGICAL 属性本身的来源完备性仍属于材料审计，不能以本批静态流体检查覆盖全部材料派生流体。

`:core:check :runGameTestServer :neoforge:runGameTestServer` 首轮成功，7m35s，30 项任务，退出 0；日志 `work/fluid-magic-tests.log`。Forge 18:24:06、NeoForge 18:27:09 各 `All 39 required tests passed`，五项新增与前批 34 项全部通过，两服务器正常保存退出。

运行采用本地已校验 Gradle 8.8、Java 17/21、`--offline --no-daemon`，开发参数 `-PdirectCoreResources=true -PdirectCoreClasspath=true -PgameTestHeap=3g -PgameTestNamespaces=gregtech_fluid_channels`，两模块测试目录分别为 `build/fluid-magic-tests`。正式构建不使用 directCore 参数。

正式 `:build :neoforge:build` 成功，6m43s，28 项任务，退出 0；日志 `work/fluid-magic-build.log`。两包中 587 个当前共享 class 逐字节匹配，元数据、许可/NOTICE、无重复和测试专用条目验包通过。[完整验包回执](fluid-pipe-magic-artifacts-20261002.json)。

| 平台 | 项目相对路径 | 字节数 | SHA-256 |
|---|---|---:|---|
| Forge 1.20.1 | `build/libs/gregtech6-1.20.1-forge-0.0.0.jar` | 38,488,940 | `9e5f6f64c0404637fe518a0a5ac3479a6d02cf2b05b334cf1575d072478b3580` |
| NeoForge 1.21.1 | `neoforge/build/libs/gregtech6-neoforge-1.21.1-0.0.0.jar` | 36,678,726 | `a7ce061ca7b5bead9f843fa5fe3574f302a740be8b078f987eee353d3cae1a38` |

## 来源和剩余范围

对照只读原 GT6 `MultiTileEntityPipeFluid.java`（SHA-256 `3a6850055375e7975145b03abab44c5922746a6f4053dd8d3163de989f37b110`）与 wolfram0108 对应文件（`f368a2cea36dd76b0d22e393de21e7fcc8eec0ee021e96805b552cc23e077335`），并沿用前批已核实的 `IL.block`/`ST.block`/`CS.NB` 回退依据。原作者、LGPL-3.0-or-later 及资源声明保持，未新增外部依赖或修改参考目录。

后续仍需超温起火、接触伤害/可燃性等管材行为、其他储液设备的魔法规则、第三方污染集成。上述测试不是客户端操作、生存取得、独立 JVM 世界重载或成品安装运行证据。

下一批已读依据：原版 `WD.burn/fire:702-727` 对六邻域调用火焰处理，跳过岩浆/火，只处理地毯或无碰撞块，并保护非易燃 `IItemGT` 方块和 Thaumcraft 节点；不是任意邻块都替换成火。当前 `ItemBehaviors.lightVanillaFire` 只处理空目标，其工具权限与点火语义不能直接替代管道过热。后续需要核对现代碰撞/方块保护映射并覆盖这些差别。
