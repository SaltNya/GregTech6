# P1：共享核心首批提取

日期：2026-09-30。来源：saltnya 文件快照；本地导入标签 `import/saltnya-snapshot`，导入提交 `41561782`。原始作者提交历史与适用授权尚未确认，保留原文与来源记录；这次提取未添加或替换第三方许可。

## 已实施的边界

八个原有类从 `src/main/java/com/gregtech/gregtech/api` 移至 `core/src/main/java/com/gregtech/gregtech/api`，保持每个文件字节、原包名、类名、参数、返回值和可见性。逐文件 SHA-256 写入 `core/provenance/saltnya-extractions.json`；移动前分别与只读来源目录核对，移动后再次核对。

- `recipe/MachineWorkCost`：BigInteger 机器工作量、并行/效率与普通/cheap overclock，拒绝无法承受的工作量。
- `machine/crucible/CrucibleMath`：坩埚和材料/流体单位转换、上下取整、显示比例。
- `energy/GTVoltageTiers`：完整电压阶梯、正负电压查档与显示名称。
- `energy/EnergyPackets`：有符号旋转包幅值、有限缓冲可容纳的完整包数。
- `material/AtomicProperties`：质子/电子/中子/额外质量与严格质量加法。
- `material/GTValues`：GT6 原始精度 `U=648648000` 与 U2/U3/U4/U9/U72。
- `definition/DefinitionCatalog`：加载前验证批次 ID 路径、唯一性与不可变顺序快照。
- `multiblock/PartBindings`：以泛型位置/角色及回调原子管理多方块所有权。

依赖闭包仅为 `java.base`。`PartBindings` 的位置/角色类型和注册/释放回调仍由平台提供；没有把 BlockPos、Direction、BlockState、ItemStack、FluidStack、NBT、Minecraft 注册器或 loader 类型引进 core。

Forge 调用方继续调用相同全限定类名，不增加第二套数学实现。单位、注册 ID、NBT 字段与机器状态机均未改动。NeoForge 应消费同一个 core 输出；core 的 Java 17 字节码可由 NeoForge 的 Java 21 运行时加载。这个步骤尚不意味着完整材料目录、合金、机器或存档已跨版本共享。

## 没有纳入本批的类及理由

- `energy/GTEnergyStore` 实现了 Forge `IEnergyStorage` adapter。
- `energy/EnergyBlockDefaults` 闭包包含 Minecraft `Direction`、`IEnergyBlock`、`GregTechTags` 与平台 sides。
- `energy/WireSpec` 和 `energy/EnergyNodeSpec` 闭包包含 `GTMaterial`；`GTMaterial` 还连到游戏物品/材质等边界。
- `recipe/RecipePowerStats` 依赖游戏 `Recipe`；`recipe/FluidFuelBatch` 依赖 `Recipe`、`FluidStack` 与游戏 IO 规划。
- `machine/crucible/CrucibleReactions` 的配方表/执行器依赖 `GTMaterialRegistry`、生成材料数据与 `CrucibleMaterialStack`；不能简单把一个无 net.minecraft import 的表面类称为纯 Java 闭包。

GTVoltageTiers 的公开数组、CrucibleMath 的原始 long 乘法和其他既有边界行为均保留。潜在溢出或可变数组问题应由独立的行为变更、记录与验收处理，不能混进字节保持的搬迁。

## 构建接线约定

`core/build.gradle` 使用 java-library 与 Java 17，main 编译不需要游戏依赖；`coreBehaviorContracts` 在 test 输出上执行固定行为样本，挂到 `core:check`。

根 Forge 与 NeoForge 各自 `implementation project(':core')`。发布 jar 各嵌入一次 core main output，并依赖 `core:classes`。根 `check` 应依赖 `core:check`；移走的八个类不能再次加入根 source set。test 输出及 standalone 编译目录不得嵌进模组。

如果使用运行时开发 classpath 而非成品 jar，两平台通过 project dependency 加载 core。模组 jar 中的 core 类数量/路径、旧根编译输出清理和双平台加载均由主线统一构建检查；本子任务没有启动 Gradle，以避免共享 checkout 的并行构建。

## 有意义的固定行为样本

`core/src/test/java/com/gregtech/gregtech/core/CoreBehaviorContracts.java` 有 64 条断言、7 组：

- 机器耗能数值采用原 `BlueprintRegressionTests.java:276-283`：32EU ×192ticks 普通超频输出 minimumPower=128/totalWork=12288；4并行、50%效率、cheap 模式为32/49152；TU 并行保持256工作量；巨大工作量必须拒绝。
- 电压/危害边界采用原 `HazardDamageTests.java:208-222` 的 8/9/32/512/8192V、tierMin(40/520)、maxVoltageOf(40)=128 和 signed -32 样本。
- 材料转换采用原 U 与 `GregTechConstants.L=144`：144L/16L/432L 分别为648648000/72072000/1945944000材料单位；比例取整66/67与容量封顶100。
- 旋转幅值采用原 `AxialGeneratorTests.java:75-77` 和 `AxleRepairTests.java:125,132` 的负 RU 和 Long.MIN_VALUE 拒绝场景；有限100能量缓冲只能接受三个32单位完整包。
- 原子质量：原默认98、ZERO、Magic 负额外质量许可、负粒子数与质量溢出拒绝。
- 定义目录：原 `DefinitionCatalogTest.java:9-27` 的唯一 ID、保持顺序、源列表变动隔离与只读快照。
- 多方块所有权：有效结构声明 wall/vent；一个 foreign part 不能导致部分新声明；失效时释放之前所有部件且无残留。

预期值为固定数值/外部可观察结果，测试没有重写待测算法。core 合约不验证 Minecraft tick、实际合金或世界磁盘存储；原有 GameTests 保留，后续需要继续运行。

已执行：

```powershell
./core/verify-core.ps1 -JdkHome 'C:/Program Files/Java/jdk-17.0.4'
```

结果：Java 17 `javac --release 17` 编译成功，64 条断言全过；8 个文件 SHA-256 与 manifest 完全一致，原 source 位置无重复。`javap -verbose` 确认 major version 61；`jdeps --multi-release 17 -summary core/build/standalone-contracts` 仅输出 `java.base`。

这是 core 的当前验证；双平台构建、模组 jar 类重复检查、客户端/专服/真实玩法/世界重载仍由验证账本分别记录，不能以本报告覆盖。

## 铜锡青铜首条链的必要代码边界

与 `PLAN.md` 的首条短链一致：真实采集原料 → 原料处理 → 固体燃烧箱供热 → 坩埚合金 → 模具浇铸青铜 → 制作并使用青铜工具。蒸汽机器/管道属于后续拓展，不能据本批 core 宣布整条链完成。

1. **采集/身份/物质量**：`worldgen/GTFeatures`、`GTOreVeinFeature`/`GTSurfaceDepositFeature`、`block/OreBlock`，`api/material/GTMaterialRegistry`/`GTMaterial`、`content/material/generated/{ElementMaterials,CompoundMaterials,OreMaterials}`、`data/generated/MaterialCompositionData`、`data/MaterialPrefix` 与 `registry/GTItems`。`GTValues` 已共享，但材料目录和 ItemStack 映射尚留 Forge。
2. **原料处理/合金配方**：`loaders/c/Loader_Recipes_Alloys` 与 `GTAlloyTable`；后者第25-26行包含 3 Copper（或 AnnealedCopper）+1 Tin→4 Bronze。`api/machine/crucible/CrucibleItemInput`、`CrucibleMaterialStack`、`CrucibleReactions`（含 AnnealedCopper/Tin 明示配方及材料 composition fallback），`content/recipe/CrucibleSmeltingRecipes`/`StoneAndToolSurvivalRecipes`/`SurvivalUtilityRecipes` 与工具处理类。不能只验证书籍中的铜锡配方行就声称坩埚实际产物正确。
3. **热量与实际 ticking 机器**：`api/machine/MachineRegistry`、`registry/GTBlockEntities`；`blockentity/machine/SolidBurningBoxBlockEntity`、`SmeltingCrucibleBlockEntity` 及对应 `block/machine` 类，`api/machine/{CrucibleSpec,MachineSpec,FurnaceFuelHelper}` 中坩埚/燃烧箱规格、燃料与材质定义、HU packet 与 `api/energy/IEnergyBlock` 平台接口。
4. **浇铸/工具**：`blockentity/machine/CrucibleFaucetBlockEntity`/`MoldBlockEntity`、`api/machine/{ITileEntityMold,ITileEntityCrucible}` 与 `api/machine/crucible` 的材料规则，`registry/GTToolItems`/`GTItems`、`item/GTToolItem` 与 `api/tool` 的生存配方和耐久；逐项核实需要的工具、模具获得路径。
5. **客户端/存储边界**：`client/SmeltingCrucibleRenderer`、`SmelteryHullRenderer`、`CrucibleClientModels`，block interaction 和 BE update packet/NBT；验证客户端可观察熔体/模具变化。先保留原 NBT 键与 registry ID，再用真实关服/重启世界验证持久化；不能替代成 saveWithoutMetadata/load 的对象回写。

这些是下一阶段依赖边界清单，并非它们已迁移或生存流程已验证的声明。
