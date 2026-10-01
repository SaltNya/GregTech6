# brokestar233 来源审计（只读，2026-09-30）

来源根：`F:\Dev\GregtTech6New\Libs\gregtech6-main`。以下路径均相对此根。审计只读取文件；没有改来源、下载缺件、执行 Gradle、启动游戏或服务器。运行验证状态一律 **未知/未执行**。文档记载的通过、完成度、CI/发布，均归为来源声明，不能作为本次验收证据。

## 总体判断

这是有真实实现与大规模测试基础的双版本移植来源。优势是材料数据、配方扩展、机器/能源/物流、世界生成覆盖广，并且已建立 Stonecutter 双节点与实际平台条件分支。适合逐项吸收平台适配、测试/RCON、纯 Java 能源/坩埚内核、配方和世界生成实现；不能仅凭 README 的“完整移植”断言替代项目1。

当前快照 **不具备完整构建输入**：没有 `.git`，`third-party/modularui/` 是空目录。缺件必须先恢复并固定出处/提交，再在整合目录的副本验证。源树无构建/游戏日志、JUnit XML 或发布 jar；唯一发现的 jar 是 Gradle wrapper。

## 指令及完整性

- 完整阅读根 `AGENTS.md`，用 `rg --files --hidden -g AGENTS.md` 检查后未发现嵌套 AGENTS。根宪法要求 state/recall/project_status，但当前工具目录没有这些工具；采用 `docs/PROJECT_STATE.md`、`docs/TODO.md` 镜像。来源规则仅作为本来源审计背景，没有搬用其 Git 身份、授权或旧会话裁定至新项目。
- 根目录没有 `.git`；`git status --short`、`git remote -v`、`git log -1`、`git submodule status` 均报 `fatal: not a git repository`。不能从此归档恢复原始 Git 历史、实际 HEAD、submodule gitlink 或提交签名。`docs/PROJECT_STATE.md:14` 声明 main=1b2e1a4cc，但这是待外部恢复核对的文本。
- `.gitmodules:6-8` 声明 `third-party/modularui`，URL `https://github.com/Meow404club/modularui.git`。目录存在但 `rg --files --hidden third-party/modularui` 返回 **0** 文件。没有 fork 的源码、LICENSE、FORK.md、THIRD_PARTY.md、DIVERGE.md，亦没有 gitlink commit。`.gitmodules:4` 的 30fef611 是旧注释，不能当最新固定版本。
- `settings.gradle.kts:31,49-59` 强制 include/create 双腿 ModularUI 项目。`mdk/build.forge.gradle.kts:156,162,166` 同时 jarJar、modCompileOnly、modRuntimeOnly 依赖其 Forge 节点。GUI 类直接引用 `brachy.modularui`（例如 `gui/machines/GTBasicMachineMUI.java:3-14`），所以不能靠移除空子项目而声称恢复构建。
- 静态文件统计（`rg --files`，不是内容/完成度指标）：root `src/main/java` 31 文件、`src/test` 18 文件；`mdk/src/main/java` 695 文件、`mdk/src/test/java` 490 文件；generated resources 208875 文件、main resources 9749 文件；RCON chains 252 文件。显式/generated 资源树在，缺的主要构建部件是 ModularUI fork。

## 许可证、作者、资源出处

- 根 `LICENSE` 是 LGPL v3 附加许可文本；`NOTICE.md:7-10,27` 与 `README.md:119` 声明代码 LGPL-3.0-or-later。具体来源头有证据：`src/main/java/gregapi/data/MT.java:7-10` 与 `mdk/src/main/java/gregtech6/recipes/Recipe.java:2,6-9` 保留 LGPL v3 or later，后者保留 GregTech-6 Team 版权；`MT.java:43` 保留 Gregorius Techneticies 作者。`mdk/gradle.properties:13,15` 记代码许可及 GregoriusT/brokestar233。
- `NOTICE.md:14-18` 声明 ModularUI 是 brachy84/ModularUI-Modern 的自维护 fork，仓库 Meow404club/modularui，许可 LGPL-3.0，发布采用 jarJar。由于 fork 源码/许可正文未在归档中，不能把它升级为 LGPL-or-later，也不能确认所有内嵌组件（例如 EvalEx/mixinextras）的实际版本/许可清单。需从完整原仓与 fork 恢复对应记录。
- 不能统一标注全部资产 CC0。`README.md:120` 与 `NOTICE.md:9` 泛称 CC0，但 `mdk/src/main/resources/assets/README.md:9937-9942`、`:10643-10646` 对 amazawa UI 专门声明 `tfc-amazawa-light-gui v1.0.5g`、Apache-2.0、作者天沢香，并有逐文件 SHA256 和来源链接。73 张面板及裁切部件要保留该分项授权/署名，不能随代码迁移重新标为 CC0。
- `docs/licenses/amazawa-gui-authorization.png` 存在，已用 view_image 目验。截图明确对高版本 GT6 借用 GT UI 作许可并要求“标注一下就行”，另有 Modrinth 链接说明。保留截图及专门出处；它不证明其中所有第三方原资产来源，截图还说明参考了基岩 OreUI 和新版 AE，不能仅据样式描述推定所有像素来自作者原创。
- 文件清单没有 GregTech `LICENSE.assets`、Apache-2.0 全文、GNU GPL 全文，只有根 LGPL 文本与 `.zcode/skills/*/LICENSE`。这是发布资料缺口，需在不改变授权的前提下补齐真正适用的文本/NOTICE；当前审计不作授权重新判定。上游 assets README 有大量 CC0 说明/摘要、SHA manifest，可作为溯源线索而非许可原件的替代。
- `NOTICE.md:20-23` 明列 JEI/Jade/KubeJS 未捆绑；EMI 已存在 compile-only 依赖（Forge build:179），主 NOTICE 没有同步这项存在性清单。分项台账需修订。
- 在整合仓保留完整原始快照、作者头、分项清单和原仓 bundle/ref；仅凭解压树不能承诺“已保留原始历史”。

## 构建条件与平台边界

- `gradle/wrapper/gradle-wrapper.properties:3` 固定 Gradle 8.14；`settings.gradle.kts:16-18` 固定 Stonecutter 0.7；`mdk/stonecutter.gradle.kts:20-21` 固定 ModDevGradle/legacyforge 2.0.144。
- `settings.gradle.kts:38-42` 明确 1.20.1-forge 与 1.21.1-neoforge，活动共享源是 Forge；root `build.gradle:10-13` 是 Java 17 java-library，仅 mavenCentral+JUnit 依赖（:20-27）。root 数据/数学与接口可不依赖 Minecraft 编译。
- `mdk/versions/1.20.1-forge/gradle.properties:7-8` 为 MC 1.20.1、Forge 47.4.10；`mdk/build.forge.gradle.kts:72-75` 为 JDK17。Neo 节点属性 :5-8 为 MC1.21.1、NeoForge21.1.249、FML2；Neo build 使用 JDK21。`README.md:94` 明确需本机两套 JDK且无自动下载。版本钉值是源码现状，没有在本审计联网验证“最新”。
- 模块形态是 root纯Java + `mdk/src` 两节点共用，**不是两份独立模组内核**。但大量机器/配方逻辑仍在 Minecraft 依赖的 mdk，不能说所有核心已经纯Java抽离。
- `mdk/stonecutter.gradle.kts:25,59-61` 活动节点+条件常量，后续文本/regex替换转换平台 API；语义差异也有真实双腿片段：`tileentity/TileEntityBase01Root.java:437-446` 的 Forge LazyOptional getCapability，`:462` 起 Neo capability 形态；`registry/GT6CapabilityWiring.java:107-125` 注册 Neo ItemHandler/FluidHandler/FE 等；`TileEntityBase03TicksAndSync.java:300-307` 分支保存同步面及 :389 起 registries provider；`registry/GT6DataComponents.java` 为 Neo item组件面。
- `mdk/build.neoforge.gradle.kts:303-330` 共享 generated resources 并转换 tag 路径（1.21复数/单数变更）；`:403` 尝试把JUnit FML配置链接到 `/dev/null`，失败则回退原子文件。跨Windows/Linux验证应覆盖这类平台假设，不能仅在旧WSL环境沿用结果。
- 旧注释已陈旧：root `gradle.properties:29,32`、`mdk/stonecutter.gradle.kts:9-11` 仍描述 Neo“红但编译可达”；项目状态后来声称双腿发布。说明源注释不能当最终状态。

## 系统实现证据与候选价值

### 材料

- `gregapi/data/MT.java`、`OP.java`、MaterialRegistry/MaterialGraph 为完整数据型核心；`registry/GTMaterialItems.java:91-97` 实际按 open→MT.init→OP.init→close 生命周期初始化。`:167-180` 做prefix×material枚举，`:188` 起 first-wins 去重，`:201` 生成 snake_case registry ID，`:259-277` 注册现代物品。MaterialGraph:300-306 实际校验合金组件并建引用。
- 可吸收材料图、坩埚和稳定身份理念，但需先与项目1的 material numeric ID、alias、配方单位、prefix naming逐条核对。first-wins 是特定碰撞政策，不能无记录地用于三家同名内容的取舍。

### 配方

- `recipes/Recipe.java`、`RecipeMap.java` 为Minecraft ItemStack/FluidStack依赖的共享算法；`GT6RecipeMaps.java:253-269` 维护 OPEN/FROZEN 注册期，`:315` 起多个实际map字段。大量静态loader与动态GT6RecipeMap子类在；`GT6RecipesOreChain.java:163-173` 遍历矿材料并向CRUSHER加入行及统计skip，说明不只是JSON外观/空注册。
- `GT6RecipeMapJsonLoader.java:58-81` 声明并实现 recipe_maps datapack层、每次reload替换自己持有的recipe子集；多owner共享map（:84-88）没有内容级dedup，这是脚本重复输入风险。
- 已知缺口是可执行流程缺口：`docs/TODO.md:14-17` 明记SHARPENING map空、12个raw工具头死端及其他工具行。源码中SHARPENING只有map构造 `GT6RecipeMaps.java:1324-1327` 和loader路由 `GT6RecipeMapJsonLoader.java:604`，搜索静态配方目录未找到SHARPENING stock注入。仍不能拿GUI/机器已注册当玩法完成。
- datapack客户端同步明确 v1-out（`GT6RecipeMapJsonLoader.java:138-143`）：专服客户端收不到新增运行时行。删除/覆盖静态行亦不支持。KubeJS plugin/rowbuilder四类存在，但必须真机验证专服同步与recipe viewer，而不是从plugin存在推定完成。

### 机器与能源

- `tileentity/machines/TileEntityBasicMachine.java:337-353` 按RecipeMap创建库存和流体罐；`:402,458,492,634,643,818` 为tick、功耗进度、配方查找、输出罐fallback、能量注入实代码。大型机器、蒸汽、核反应、聚变、蒸馏等注册和BE均存在，不是三套名义内容拼表。
- `tileentity/multiblocks/TileEntityCrucible.java:221-243` 保存温度/材料列表；`:473,512-513` 实际tick合金扫描，纯Java `gregapi/util/CruciblePhysics` 提供共享热物理。这部分非常适合作为两腿共享内核候选。
- `gregapi/tileentity/energy/EnergyBridge.java:122-130,151-160` 有FE收/发整包对齐、模拟/执行与入站比例，`:105` int clamp；能源接口与EnergyGate/adjacency/TD为root纯Java。`GT6FeConverterBlockEntity.java:240-259` 两腿capability取FE、`:309-332` overload检查+tick、`:431-441` 持久化。
- 三源合并时必须统一 EU/FE比例、HU热单位、RU/KU方向/交变含义、包大小/包数/过压语义；不能用同名 energy字段直接互换。当前读取不能证明能量守恒、故障爆炸或完整时代升级可运行。

### 物流与流体

- `connectors/GTItemPipeBlockEntity.java:207-220,237-245,462` 实际tick传输、升序网络路由与迭代扫描；`:675` 起保存库存/预算/方向。`GTFluidPipeBlockEntity.java:402-411,431,475-495` 实际压力均衡、模拟试探和执行填充。
- `multiblocks/GT6LogisticsCoreBlockEntity.java` 与多种过滤/进出口/CPU cover共存；类文档 :84-98 写范围/资源预算/按物品和流体计EU的取舍。能吸收完整物流概念与测试，仍需实际检验卸载区块、循环网络、过滤、速率、save/reload中不丢失/复制物料。

### 世界生成

- `worldgen/GT6Worldgen.java:128,372,389` 有地层透镜、主世界和深层大型矿脉；有基岩矿、流体泉、地牢、蜂巢/倒木/树木、Nether等 feature/datagen。
- `GT6StrataLensFeature.java:57,92-96` 从origin-seed计算slice后setBlock；`GT6VeinGenerator.java:134` 有确定性 generateSlice接口，worldgen单测有negative coord/dimension/切片一致性；应吸收适合现代区块边界的确定性方案，避免三家矿脉重复灌世界。
- worldgen有丰富实现，不能据文件覆盖断言矿分布可玩/矿石处理可达；需新世界新区块、负坐标、三维度的生成与掉落/名称/贴图实测。

### 渲染、GUI、可选集成

- `client/wire/GTWireBakedModel.java:105,187-204,212-222,290` 动态baked model、渲染层与几何/quad缓存；`client/render/GTRenderSnapshot.java:8-16,26` 规定深度不可变snapshot避免异步chunk渲染读取活BE。现代渲染平台缝与该线程安全契约值得保留。
- `gui/machines/GTBasicMachineMUI.java:3-14,77` 真正消费ModularUI库存/进度/流体控件；源提供JEI/EMI、Jade与双语datagen，并有素材manifest/crop脚本和geometry/layout/census测试。
- 具体可选依赖缺陷：`jei/GT6RecipeMapViewerMeta.java:354` 直接调用 `jade.GT6MachineProvider.energyTypeShortCode`；该类 `GT6MachineProvider.java:10-15,55` import并implements Jade接口。Jade拔除时可能触发类链接错误，且 `docs/TODO.md:20` 已明确记录 nojade recipe-page draw NCDFE。这与README:72“无需任何可选前置，不影响游戏”冲突，须作为集成门禁病例。
- 视觉债/大型机器罐遮蔽/破坏掉落覆盖见 `docs/TODO.md:30-46`，不要搬运“全部完成”标签。运行中截图和GUI交互未验证。

## 测试与真实验收差距

- 单测不只是声明：`src/test/.../CruciblePhysicsTest.java`、`.../EnergyBridgeTest.java:101-128` 有整包/模拟/余量断言；MaterialStackSerializerTest:82-86 为序列化round-trip。`mdk/src/test/.../TileEntityBasicMachineNBTTest.java:30-62` 和 `.../GTMultiBlockCruciblePhysicsTest.java:376-385` 都save/load恢复。`TileEntityBase03TicksAndSyncNbtAccessTest.java:290-302` 检验Neo动态registry组件保存。
- 常规CI `.github/workflows/build.yml:31-53,72-92` 两个独立runner、JDK17/21、recursive submodules、双腿build、jar上传；Neo job:69-71 明确隐式依赖runner预装JDK17供root编译。新CI应显式安装两套而非依赖镜像惯例。
- `.github/workflows/manual-rcon-sweep.yml:24-38,55-64` 有手动分组/版本选项。`tools/rcon/chains/framework.py:689-708` 实现启动专服、等Done、跑pass、最后stop；多数chains用setblock、命令注物料/热/电。例如 hu_steam_foundation.py:54-67 用gt6energy/gt6oven测试rig；engine-steam.py:10-20 明言直接注入而不是锅炉供汽。这是实服组件验证能力，**不是从零获取材料→合成→供能→生产→升级的生存可达证据**。
- framework所读生命周期在单次boot里跑多pass后stop，没有把验收要求的同世界保存→关闭进程→重启读取作为统一门禁。NBT单测有价值，但不能替代整个世界/玩家物品/机器连网状态的真实重启。
- `tools/gt6testgate.py`、`gt6server.py` 有 `/proc`、`/tmp`、Linux信号/systemd及WSL环境假设。新项目在Windows本机要明确WSL或portable harness，并仅在整合工作区运行，不能对来源直接跑旧机器级清扫。
- 本次没有执行构建、客户端、专服、RCON、单测或save/reload；构建缺件未恢复前不能出具可测试mod jar。来源的97–98%、v0.1.0与CI绿全属于未复验声称。

## P1结构取舍建议与关键门禁

项目1初始基线+抽共享core+独立Forge/Neo适配可行，但要冻结身份与语义再移动代码。项目2提供“同一核心+平台条件缝”的真实先例；无须为了统一而复制其整个registries/RecipeMaps，又建立第二套底层。

1. 统一MaterialRegistry、材料numeric ID/名称/alias、prefix定义、registry id和配方map身份。以导出的清单对比两腿；每个重名取舍有来源与理由。注册数量不能替代内容同义检验。
2. 抽core前固定测试样例，守住材料组成/合金、热学、能源包/守恒/溢出、配方消耗与产物一致。抽取后两腿消费同一个core对象模型；Minecraft ItemStack/FluidStack/能力不得流入纯Java模块。
3. 原项目1完整Forge作为功能保留基准，新增Neo最小纵切片不能算双腿功能一致。逐域建立parity清单、显式defer与阶段结束门，不把基线功能永久留在Forge。
4. registry/NBT/ItemStack组件/世界生成变动都需兼容面设计。项目2 `TileEntityBase03TicksAndSync.java:78` 明言无1.7世界迁移；不能承诺1.7存档、不同来源世界、1.20→1.21跨版本可直接互开。初期承诺范围应仅是同版本新整合世界保存/重启；任何扩大范围需真实migration测试和备份样例。
5. 每腿分别验证build、客户端画面/GUI、纯专服无client类加载、可选mod全拔/JEI/EMI/Jade组合、KubeJS/datapack专服显示、真实生存纵切片、同世界保存关闭重启。机器处理不能依赖debug energy fixture通过。
6. 使用一个物流/能源/渲染状态契约，验证区块卸载、循环线路、过滤和传输时库存/流体守恒；世界生成只注册一套chosen方案，检查负坐标/跨区块一致及新区块渲染。
7. CI可吸收此源双runner结构，但移除旧release自动发布/GitHub归属与旧机器环境依赖，明确pin缺的ModularUI fork、双JDK及资源授权资料，保留测试结果与hash关联。
