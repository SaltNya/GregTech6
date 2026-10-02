# 流体管材目录与旧容量迁移

日期：2026-10-02。工作树：`C:\Dev\GregTech6\GregTech6-main`。承接 [温度和物理危害批次](fluid-pipe-safety-20261002.md)。

## 对照及实现

逐项读取原版 `Loader_MultiTileEntities.java:1846-1885` 的 40 个 `addFluidPipes` 调用，按已存在的材料身份映射至当前 40 种管材，保留当前注册名、顺序及七种尺寸。来源固定值存入共享合同测试，而非在测试时从生产目录复制期望值。`MT.TungstenAlloy` / `MT.DeshAlloy` / `MT.IronWood` 的身份同时以原版 `MT.java` 的 HSLA-Tungsten-Alloy / Workers Alloy / Ironwood 声明核实。

28 种管材的容量、耐性或显式耐温有变化，见 [逐项差异](fluid-pipe-catalog-changes-20261002.json)。基础容量：青铜 120→150、钛 400→300、钨 600→350。多种管材旧目录误把魔法耐性写成等离子耐性；现在气体、酸、等离子、魔法四位分别按原版赋值。木和处理木 340 K、塑料 370 K、橡胶 350 K；其他材料采用原版 `(long)(meltingPoint * 1.25)`，不再四舍五入。

`PipeSpec` 移除覆盖 record 字段的 `maxTemperature()` 重算，新增显式阈值工厂重载。Forge 注册新增接收完整 spec 的入口，当前目录直接传入，避免重建时丢掉魔法耐性和专用阈值；旧签名保留给已有调用者，NeoForge 原来已经直接注册共享 spec。两版管道内部各通道也接收 `magicProof`。魔法流体的实际泄漏/中毒分支尚未在此批实现，不以配置通过声称危害行为完成。

## 旧存档容量

原平台 `FluidTankGT.readFromNBT` 会恢复每罐保存的 `Capacity`，导致新注册参数被旧容量覆盖。本批只在管道的加载与同步入口复制通道 NBT，将基础容量设为当前 spec 后交给既有反序列化；输入 NBT 不变，罐内 Amount 和流体附加数据沿用原有读取。没有调用会截断液量的 `setCapacity`。

既有共享 long 储液语义使有效容量至少等于现存液量，因此缩容旧管完整保留超额内容，无法再填，正常排出后恢复到新基础容量。举例：钛中型旧容量 2400、存量 2200，新基础容量 1800；加载仍为 2200，排出 400 后有效容量变为 1800，随后只能补至 1800。青铜中型旧 720、新 900，加载旧液量后可补至 900。再次保存写入新基础容量。

这是本项目现有现代保存格式的迁移选择，不宣称直接读取 GT6 1.7.10 世界或跨模组迁移。

## 回归

共享新增 1,430 条合同检查：280 个唯一注册 ID、40×7 个固定容量/通道数/四耐性组合、28 个显式耐温组合及自定义阈值工厂保留。原 137 条行为合同合为 1,567 条，加材料 6,160、热力学 53、设备规格 34，共 7,814 条断言通过。

双平台新增 `FluidPipeCatalogTests` 三项：真实注册表中全部 280 个方块的 spec 和实体容量/通道数；钛管超额旧液量加载、排出、回填、再次保存及更新包；青铜扩容不被旧标签覆盖。NBT 场景使用真实方块实体但直接序列化/反序列化，不是独立 JVM 世界保存重载。上批等离子防护场景改用原版确有防护的下界合金管，继续保留钢管泄漏 64 的断言；不再把旧目录中错误的钛耐性当作期望。

`:core:check :runGameTestServer :neoforge:runGameTestServer` 首轮通过（7m53s、30 项任务、退出 0），日志 `work/fluid-catalog-tests.log`。Forge 18:02:38、NeoForge 18:05:42 各 `All 34 required tests passed`，包括新增 3 项和之前 31 项回归，两服务器正常保存退出。

复现使用本地已校验的 Gradle 8.8、Java 17/21、`--offline --no-daemon`，开发参数为 `-PdirectCoreResources=true -PdirectCoreClasspath=true -PgameTestHeap=3g -PgameTestNamespaces=gregtech_fluid_channels`。两模块测试目录各为 `build/fluid-catalog-tests`。正式构建不使用 directCore 开发参数。

正式 `:build :neoforge:build` 通过，6m31s，28 项任务，退出 0；日志 `work/fluid-catalog-build.log`。双包的 587 个当前共享 core class 逐字节匹配，元数据、许可/NOTICE、无重复项及无测试专用条目验包通过。[完整回执](fluid-pipe-catalog-artifacts-20261002.json)。

| 平台 | 项目相对路径 | 字节数 | SHA-256 |
|---|---|---:|---|
| Forge 1.20.1 | `build/libs/gregtech6-1.20.1-forge-0.0.0.jar` | 38,487,678 | `5e691e5ab0f7932ba696dc890029398ed6a837d9bfda70aac76fbf3e5b250816` |
| NeoForge 1.21.1 | `neoforge/build/libs/gregtech6-neoforge-1.21.1-0.0.0.jar` | 36,678,186 | `3137df47729819d829c9917f21b157d50041eb4f53889bf2f426d1025704bd4c` |

## 来源及边界

- 原 GT6 `Loader_MultiTileEntities.java` SHA-256：`96f579dd5c0a26a759ddee34c312dadbc5d52123e2b85e82da6a40f68b494393`。
- 原 GT6 `MultiTileEntityPipeFluid.java` SHA-256：`3a6850055375e7975145b03abab44c5922746a6f4053dd8d3163de989f37b110`；`addFluidPipes:83-98` 提供默认耐温与尺寸倍率。
- wolfram0108 的 `Loader_MultiTileEntities.java` SHA-256：`4d87cacde8defa33df30359d345046daa8e901ab0419dca2766d2140d8af1562`，去掉排版空白后，全部 40 条管道注册的完整参数列表与原版一致。

沿用原作者及 LGPL-3.0-or-later、NOTICE，不修改参考目录，不新增运行时依赖。当前仅完成容量、四耐性、通道数和耐温目录参数；原版接触伤害开关、可燃性、阻挡/外观及硬度等剩余参数不能因本批通过而视为对齐。魔法危害、超温起火、完整材质温度来源、客户端、生存取得、独立世界重载、成品安装仍需后续证据。
