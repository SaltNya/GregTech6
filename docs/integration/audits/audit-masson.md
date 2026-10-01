# masson / CrucibleCraft 只读审计（2026-09-30）

来源：`F:\Dev\GregtTech6New\Libs\cruciblecraft`。本审计未编辑、构建、启动或运行来源树内的工具。报告唯一写入目标为本文件。以下相对路径均以来源目录为根；冒号后的数字为核实过的行号。结论仅分为源码存在、文档声称、尚需本次执行验证。

## 1. 完整性、历史与构建条件

- 未发现来源树或已检查的 F:\、F:\Dev\、F:\Dev\GregtTech6New\、Libs\ 祖先中的 AGENTS.md；全树 `rg --files --hidden --no-ignore -g AGENTS.md` 也没有结果。
- 当前是源码快照，无 `.git`。`git rev-parse --show-toplevel`、`git status`、`git log -1` 均返回 not a git repository。因此不能从当前目录证明原始提交、分支、作者逐提交历史或工作树是否有未提交变更。保留 CREDITS 中作者与固定上游 SHA，并另取可获得的原始仓库历史再关联，不能编造来源 commit。
- 可检索文件约 61,173 个；主 Java 文件 1,119，test Java 文件 544。仅为当前文件统计，不是功能完成数。src/addons/crops 与 foods 是独立源码集/独立 jar，不应直接当主模组内容全部合并。
- Gradle wrapper 脚本、wrapper jar、11 个冻结生成资源根、8 个 gradle/scripts 引用文件均存在。11 根分别有 21,336 / 2,127 / 11 / 269 / 32 / 157 / 48 / 3 / 4 / 16,355 / 117 个文件。完整根名在 tools/generated_resource_roots.json；资源存在不证明生成器可重放或运行时正确。
- `build.gradle:4,23`：ModDevGradle 2.0.142 / Java 21。`gradle-wrapper.properties:3`：Gradle 9.2.1。`gradle.properties:12-25`：Minecraft 1.21.1、NeoForge 21.1.243、Parchment 2024.11.17。`mod_version:37` 为 0.1.0-test.20260927.1。未提供 Forge 1.20.1 分支或适配层；大量 net.neoforged 和 1.21 DataComponent API，不能按换版本参数直接回移。
- `gradle/scripts/dependencies.gradle`：Jade 15.10.0、EMI 1.1.24、KubeJS 2101.7.2-build.368 为 compileOnly；开发 localRuntime 还有 Jade/EMI/YACL 3.8.2/REMI 4.7.3。可用 `-PoptionalCompat=ccOnly` 抑制 optional runtime，但 compileOnly 仍须解析。Junit 5.11.4、DFU 8.0.16。Maven 来源是 Maven Central、NeoForge CDN、Modrinth、Latvian、JitPack；插件仓库 Gradle Plugin Portal。需要 Python 来执行 resource duplicate gate。
- `.github/workflows/build.yml` 存在：Java21、assemble、common→client import gate 与多个 Python/Java profiles。不是双版本 CI。此快照没有 build/、run*/ 或 fresh 日志，不能把 CI 文件和历史 receipt 当通过记录。
- `docs/current/code-tree.md` 明确常规构建不需要 gt6_code、gt6_dump 等参考检出；源码重提取/源行对账需要固定 revision 的外部数据。这些输入不在当前来源目录。部分 frozen historical generator 已删除，生成树仍保留。需要保持生成资源和 provenance 的关系，不能宣称全量可再生成。

## 2. 授权与归属

- `LICENSE:2,4` 作者 Lorbineitte Masson，SPDX LGPL-3.0-or-later；不是 MIT。LICENSE 提供 LGPL 声明与全文网址，并未附完整全文。整合时保存原 LICENSE/NOTICE/CREDITS，按实际采用范围保留授权信息，不自行给整个合并代码改授权。
- `NOTICE:11-15` / `CREDITS.md:16-32`：GT6 参考 commit 3703e40308c8c030763fd6297dea8b210d2a77b1；源码/来源数据 LGPL-3.0-or-later；GT6 默认资产声称为 CC0；GregTech logos 及衍生 logos 为 CC-BY-NC-4.0，项目声称未采用；砧几何源于 GT6 MultiTileEntityAnvil 32025。
- `NOTICE:21-23` / `CREDITS.md:35-40`：GTM de5d2c4a4c863b94a10bfb5d0839df2de8246628 仅管几何/命名参考，LGPL-3.0。NeoForge MDK MIT 全文在 NOTICE。net/neoforged 参考文件保留 LGPL-2.1-only 文件头，非主源码集；net/minecraft 参考文件也在源码集外，不应复制进合并发布源码集。
- tools 中有 gt6_pipe_source.json、t20_worldgen_source_policy.json、t13_denominator_manifest.json 等逐文件来源材料，应随采用代码/数据保存 relevant 部分。textures/ 有编辑/参考资产，不能仅依据根许可证就无差别发布其中所有内容；每个采用资产依 CREDITS/来源政策逐项确认。
- CREDITS.md 与 neoforge.mods.toml 使用 icodestuljh GitHub 地址，README 使用 lombinaxmasson；当前没有 remote 可判哪个是可用历史仓库，合并不得猜测远端归属。
- 玩家指南要求仅小群私测、不要公开发布，是发布准备度声明；不是替代 LICENSE 的新授权。本报告没有验证外部上游许可证原文或为未知资产作法律结论。

## 3. 系统实现证据与吸收建议

材料：`material/MaterialCatalog.java:24,41,190,257,333` 有统一 bootstrap、require、alloy index、runtimeRevision。`material/def/MaterialDefinition.java:32-56` 通过 Codec 定义 id、forms、thermal、composition 等；`registry/ModComponents.java:18` 有 1.21 DataComponent，`api/unit/MaterialUnits.java` 由 TagsUpdatedEvent 建立外部物品映射。长尾组件材料与公共16独立前缀是当前文档明确策略。建议吸收元数据与身份审计方法，转换进选定统一材料模型，不保留第二套 MaterialCatalog/注册系统。

配方：`recipe/gt/RecipeMap.java:29` 有不可变 lookup snapshots、handlers 和紧凑配方族；大量生成根和 tools/recipe_bulk 数据来源编译。可以吸收源行 provenance、紧凑矩阵/分片与精确映射设计；运行时 RecipeMap 直接引用 ItemStack、ResourceLocation、FluidStack，不是纯 Java 核心。docs/current/gt6-full-coverage.md 的 565,619 已证明源行/80.0% 目标进度只是其现有生成对账声明，本次没有重算，也不能证明所有配方纯生存可获得。

机器：machine/processing 有 MachineKindCatalog、MachineKindSpec、MachineExecutionPlan、MachineTransaction、ProcessingMachineSpecFactory、ProcessingMachineAutoIo 等。`ProcessingRuntime.java:8` 将 pause/reset/progress 抽为状态机；内容已有多种基本/大型机器和可用性目录。可吸收事务/输出容量/欠功率停顿语义与目录，不复制整个注册矩阵。docs/current/gt6-full-coverage.md:13-30 的机器种类、138 capability 与 126 runtime_ready 数字仍要按具体运行内容验证。

能源：`api/energy/EnergyType.java` 分 HU/KU/RU/EU/LU/TU/QU/CU/MU/AIR，保留 signed strength × packet count 语义；`energy/EnergyPackets.java` 纯 Java 溢出安全。目录有 cable/converter/rotation/steam/transformer/cooler/battery/nuclear/fusion 等。建议优先吸收包算术、每 tick budget 与 KU/RU区别，统一映射原基线能源类型。不能因为 enum 存在就证明全部 GT6 能源已实现。

物流：`logistics/fluidnet/FluidLogisticsNetwork.java:31`、`itemnet/ItemLogisticsNetwork.java:31`、`genericnet/GenericLogisticsNetwork.java:37` 有独立运行时类，且 pipe、cover、hopper、core、displaycpu、machinecover 目录有实现和测试。吸收比例守恒传输、simulate/commit、有限网络工作预算、盖板行为身份规范；不要注册并存三套管网底层。单块/大坩埚的流体 capability 边界直接依赖 NeoForge，需写两平台适配。

世界生成：StoneLayerRockFeature、LargeVeinFeature/LargeVeinLayout、SmallOreFeature、SubsurfaceFluidDepositConfiguration、FluidSpringFeature、BedrockOreVeinFeature、树/作物与 GtDungeonStructure 实现存在。`StoneLayerRockFeature.java:43` 有实际 place；`GtDungeonStructure.java:64` 有 layout，而文档仍可能把对应 capability 记 prep/未签收。应按源码+当前实例判断，不能把计划目录当无实现，也不能把 Feature 类当验证完成。吸收固定上游参数、石层/矿宿主/泉矿 mutex 和测试布局，统一世界生成注册与配置。

渲染/界面：`client/ClientSetup.java:93-114` CLIENT 限定事件注册；client/render 有坩埚内腔、材料液面、大型机器、pipe cover、储藏/显示渲染，content/menu 与 client/screen 有机器/仓储/焦炉界面，compat/emi 和 jade 有投影与观察。适合吸收几何/液面/tooltip/观察数据。所有 MC/NeoForge client 类型留平台，runtime-neutral 核心不得导入它们。大量屏幕/资产存在，未做客户端视觉 QA。

版本适配：主类 `CrucibleCraft.java:48-82` 通过 NeoForge IEventBus 注册；`ClientSetup.java:92` 的 @Mod(dist=CLIENT) 是客户端 bootstrap；`network/MaterialConfigurationHandshake.java:26,31,43` 配置握手 NETWORK_VERSION=1。主材料启动事件与动态材料注册高度耦合 NeoForge FMLConstructModEvent/ModLoader，不能直接做 Forge 层复用。

## 4. 优先可抽取的坩埚/熔炼核心

可直接经归属记录采用并改包的纯 Java 文件：

1. `heat/CrucibleThermalModel.java:19`。step 参数是温度float、storedEnergy long、cooldown ticks、incomingEnergy long、thermalMass kg、ambient ℃；1 HU 对100kg提升1 K，度数整数转换/余能保留、100 tick热缓冲和10 tick被动漂移；`mixTemperature:97` 按 GT6 整数质量算法混温；`shouldBoil` 删除沸腾材料；display interpolation 不能改权威状态；`addSignedEnergy` 饱和处理正负能量。
2. `fluid/MoltenTransferMath.java:15,28`。144 mB/锭，fill 按 composition quantum 向下取整，drain 要组成 key 完全一致且比例相同，gcd 最小整数比例。没有 Minecraft/loader 依赖。其 int quantum/总量应在新核心加明确上界或 long 校验，避免导入更大单位时溢出。
3. `material/GT6ImportUnits.java:11-13`。GT6一锭648,648,000 U；CC一锭144，1 CC单位4,504,500 U。GT6→CC非整除抛异常；CC→GT6 multiplyExact。温度 Kelvin↔℃偏移273.15。可保留作显式旧系统边界转换，不能把144单位定成整合全局精度；GT6细小材料形态可能不能表示为整 CC unit，须统一高精度核心或拒绝并保留余量。
4. `energy/EnergyPackets.java:8`。abs(packet size)饱和、size×amount溢出饱和、whole packets按可容纳能量计算。`machine/component/ThermalComponent.java:7,103` 只依赖该类与 ThermalModel，可作为纯状态容器，但客户端display字段更适合独立presentation projection。

可切割逻辑，不能原封不动整体复制到 core：

- `recipe/AlloyIndex.java:159,251,343`。第一层 composition + extras，不递归展平；允许余料且至多一种固态组分，产物必须熔融；批次整数比、转换取最小have/cost、最大output优先。构造/熔点查询耦合 MaterialDefinition/MaterialCatalog/MaterialPrefixes，抽取 AlloyRecipe/Conversion 纯 DTO 并传统一材料性质查询/ingotUnits，不引入CC底层。
- `machine/component/CompositionTank.java:20,111`。String→int物质量，反应次序为合金后 boil/burn/acid/explosive/phase change；unknown material 会阻止反应并保留内容。缓存耦合 MaterialCatalog.runtimeRevision；要传统一 catalog revision/provider。`phaseChange` 使用源处理目标和整数单位，有截断语义，需要明确是否保留此上游行为。
- `machine/component/CrucibleProcessCore.java:41-44,479-539`。单坩埚16锭，大坩埚432锭；虽然注释 block-independent，import Direction、CompoundTag、Tag、FluidStack、IFluidHandler、ModFluids、hosts等，它不是MC独立核心。采用顺序应是热模型→整数质量→合金→DTO状态，保留世界雨水/酸损坏/爆炸/能力/ItemStack在平台。
- `recipe/SteelmakingProcess.java` / SteelmakingTickDecisions：高碳3:1铁/碳、每20ticks/10 carbon units、范围1-2 units/锭；此定义与当前CC精度/MaterialPrefixes绑定，须核实与基线GT6直接air-alloy反应取舍，再考虑采用。

持久化边界：`CrucibleProcessCore.save:479` 写 composition子Compound(String→int)、casing_material_id、temperature/old_temperature、cached_energy_per_tick、stored_energy、cooldown_ticks、stored_air、steel_batch_iron_units、steel_reaction_ticks、air_ku_remainder；`restore:506` 保留未知正数材质键、非有限温度回ambient、夹紧cooldown/air余数。没有schema version。clientTag只有组成/casing/temp/steel部分数据。建议核心用带schemaVersion的 Snapshot DTO，Forge NBT与NeoForge NBT/component各自 codec，显式映射旧ID并保留unknown/quarantine，防止静默丢失。

## 5. 验证与最小玩法流程

测试源码存在但本次未执行：CrucibleThermalModelTest（余能/混温/环境底限）、MoltenTransferMathTest（144mB和3:1守恒/模拟）、AlloyIndexTest（Black Bronze一层Electrum、Red Alloy不展开、extras、common divider、余铜）、CompositionTankTest、CrucibleProcessCoreTest（HU/KU、容量、合金、浇模、雨水、冷料混温）、ThermalComponentTest、SteelmakingTickDecisionsTest。这些应迁为真行为测试；不得仅建立与当前实现一模一样的fixture。

GameTest源码含 `CrucibleCraftGameTests.java:466` crudeOilFuelEngineDynamoPowersElectrolyzer、`:1424` steamEnginePowersSifterThroughKu，及 CrucibleMoldInteraction/BehaviorCorrection、MteCrucibleFoundryRuntime 测试。适合采用实际生产recipe reload→供能→下游加工的结构，不等于生存获得链已通。

`docs/current/verification.md:61-73` 明确：裸 runGameTestServer 只有namespace占位成功测试；必须 `-PgameTestGrid=<id>`，8领域grid覆盖default/machines/energy/logistics/multiblock/worldgen/content/measurement。历史receipt不是PASS；GameTest服务器不写关服区块存档，需真实dedicated世界保存/退出/重启测试。客户端smoke只证明第一tick不崩溃，不能作玩家流程验证。

建议首个整合验收：开新世界→获取铜/锡与燃料→统一材料物质量输入→热源升温→3:1青铜合金→同一物质量浇锭/冷却→用于一个基础加工机→保存正常退出→重新打开世界核对剩余组成/能量/温度/机器进度→专服同流程，再加客户端UI/液面检查。保留项目1完整玩法基线，先抽纯运算按两版本相同数据运行；不要为做到双版本先只注册几种CC材料导致基线功能悄然消失。

兼容范围必须单独声明：`docs/current/player-guide.md:9` 明确没有DataFixer，旧beta/rc存档可能丢物品/对不上方块；`:108` 不支持旧档升级；`:28` 之后五节点玩家路径也明确不保证零创造全链。当前缺旧ID表/历史存档夹具，本次无法确认兼容。

## 6. NeoForge 最小启动配置参考

保持自己的单一modId：Java21 + NeoForge21.1.243 + ModDevGradle2.0.142（不必复制其全部verification/release脚本）；neoforge { version; runs { client/client(); server/server() + --nogui; gameTestServer/type }; mods { <name> { sourceSet main } } }；模板 META-INF/neoforge.mods.toml 用javafml、MC[1.21.1]、required neoforge版本范围。`gradle/scripts/runs.gradle` 展示开发run，来源本身将test绑入client/server/GameTest，production jar仍main，合并初期不要把544tests当生产源码。

`CrucibleCraft.java:48-82` 模式：@Mod(modId)，构造注入IEventBus/ModContainer；把每类 DeferredRegister.register(modBus) 与 lifecycle listener注册上去。共同核心不能依赖IEventBus，材料数据转换后由平台做一遍注册。客户端独立 CLIENT limited @Mod/EventBusSubscriber，BlockEntityRenderer/MenuScreens/Color/Geometry事件仅客户端。具体可启动最小配置必须经本次build/client/server执行验收；本报告只是源码参考。

## 7. 阻塞/待核实项

- 没有当前原始Git历史；需要可获得的原仓库clone/bundle关联作者与snapshot。可先做只读快照来源登记并开展纯逻辑整合，不阻止所有工作。
- 外部来源dump/完整GT6/纹理固定revision缺失，不能鲜执行完整source replay。现有生成物可读，但可再生成性/资产逐项授权仍待确认。
- 没有本次fresh构建/运行结果。来源明确16GiB建议，recipe reload进度存在性能债务（known-issues提到allocation待测、旧20.7s日志不得当PASS）。应在隔离的整合目录/快照副本进行验证。
- 1.20.1平台不存在；NBT与1.21组件/网络Codec/Recipe目录差异需要专门适配。
- 本项目全量coverage和survival是分开的；126accepted runtime_ready不等于范围完成，公开测试制品仍不能依据这些数字宣称功能已完成。
