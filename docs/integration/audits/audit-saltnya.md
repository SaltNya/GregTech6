# saltnya / gregtech6reborn 源码审计

审计日期：2026-09-30。来源根目录：`F:\Dev\GregtTech6New\Libs\gregtech6reborn`。

本次仅阅读来源目录；未修改来源、未执行其中的构建、生成器或测试。下面的行号均相对来源根目录。代码存在、文档声称通过、当前实际运行通过是不同证据；本次没有当前构建/运行通过证据。

## 完整性与规模

- `rg --files --hidden` 清点：78,768 个文件，1,252 个主源码 Java 文件，10 个 `src/test/java` Java 文件，242 个 `gametest` Java 文件；GameTest 目录里有 1,042 个 `@GameTest` 注解，不等于实际被发现且通过的测试数。
- `src/main/resources` 有 76,907 个文件；全目录有 58,151 个 JSON、18,251 个 PNG；资源中的静态配方 JSON 有 2,192 个。`data/MachineRecipeMaps.java` 有 85 次 `new RecipeMap` 定义；实际运行配方还会动态生成，不能以 JSON 个数代表可运行配方总数。
- 62 个 `tools/test_*.py` 或 `tools/tests/test_*.py` 文件。来源内没有 `.git`、没有嵌套 `AGENTS.md`；本地原始提交历史未随该快照提供。`gradlew`、`gradlew.bat` 和 wrapper JAR 齐全。
- 这是单项目 Forge 源码，`settings.gradle` 只有 pluginManagement 与 Foojay resolver，没有 include 子项目。主入口与注册、核心内容及资源存在；没有检测到 NeoForge 构建/适配模块。
- 来源内的 `.jar/.log/.xml` 文件清单仅有 `gradle/wrapper/gradle-wrapper.jar`；无发布模组 JAR、构建日志、当前测试结果或客户端/专用服务器启动日志随包提供。
- 文档和生成器依赖旧工作目录：例如 `tools/extract_gt6_material_fields.py:18` 硬编码 `F:\Dev\GregTech6\gregtech6-master\gregtech6-master\src\main\java\gregapi\data\MT.java`；`tools/add_waterlogged_variants.py:20` 硬编码旧移植项目资源输出目录。现有生成结果可检查，但生成过程还不能当作自包含、可复现。

## 许可证与作者证据

- `gradle.properties:59` 为 `mod_license=All Rights Reserved`；`:67` 为 `mod_authors=YourNameHere, OtherNameHere`；`:69` 是 MDK 示例描述。
- `src/main/resources/META-INF/mods.toml:12` 从上述 `mod_license` 展开许可证，`:35` 从上述占位作者字段展开作者信息。
- `LICENSE.txt:1-7` 是 Minecraft Forge / FML 的 LGPL 2.1 MDK 文本，`:23-28` 明确区分 Forge 与通过 Java 普通引用使用 Forge 的模组代码。该文件没有明确标识 saltnya 移植代码、GT6 原始代码和复用纹理各自的授权。
- `CREDITS.txt:1-5`、`:38-65` 同样是 Forge/FML credits；未形成该 GregTech 移植项目的作者/素材来源清单。
- `PROJECT_HANDOFF_2026-09-13.md:14-16` 提到 GT6 原始参考源码、GTM 与中文语言文件；这属于参考来源说明，不能替代授权文件。
- 结论是**授权范围待核实**，而不是擅自选择 LGPL、MIT 或修改第三方许可。需取得可核实的 saltnya 代码许可、GT6 原始代码及纹理许可、语言/资源包许可，以及可获得的原始仓库历史和作者信息。该快照的 MDK 文本不足以消除元数据中的 All Rights Reserved 歧义。

## 构建条件与明显风险

- `build.gradle:5`：ForgeGradle `[6.0,6.2)`；`:10`：MixinGradle `0.7.+`。两者使用动态版本范围，需后续锁定已验证版本。
- `build.gradle:21`：Java toolchain 17；`gradle.properties:10` 将 Gradle Java home 固定为 `C:/Program Files/Java/jdk-17.0.4`，`gradlew.bat:36-38` 同路径作为 JAVA_HOME 回退。跨机器与 CI 必须解除机器路径绑定。
- `gradle.properties:16,22,24,26,45,48`：Minecraft 1.20.1、Forge 47.4.20、JEI 15.20.0.119、Jade 11.13.2+forge、官方 1.20.1 mappings；`gradle/wrapper/gradle-wrapper.properties:3`：Gradle 8.8。
- `build.gradle:157-168`：Forge userdev、JEI API/运行时、Jade API/运行时及 Mixin annotationProcessor；`:185-188` 配置 mixin refmap。需要联网 Maven/Gradle 仓库或完整缓存。
- `build.gradle:89-125` 配置 client/server/GameTestServer/data；GameTestServer 默认 1536m，可用 `gameTestHeap` 和 `gameTestJvmArgs` 覆盖（`:105-116`）。历史文档提过 OOM 与旧测试世界污染，第一次应使用全新、隔离的测试目录并记录内存。
- `build.gradle:194` 使用自定义增量资源脚本，`:233` 设置 zip64；76k 资源与大量注册使简单资源处理/模型烘焙成本显著，需要保留功能同时测量内存与启动时间。
- `build.gradle:224` 将当前时间写入 manifest，尚非字节级可复现构建。
- 1,069 个主 Java 文件直接 import `net.minecraft`，577 个 import `net.minecraftforge`，88 个 import `net.minecraft.client`（集合重叠，含 GameTests）。没有现成平台中立共享核心；1.21.1 适配不能用机械包名替换验收。
- `src/test/java` 中已阅读的测试使用 `public static void main` 而非 JUnit 注解；例如 `api/definition/DefinitionCatalogTest.java:8`。`build.gradle` 未接这些 main 合约测试到 `check`。`tools/check_preview_viewport.py:18-22` 会显式 javac/java 调用；普通 Gradle test 不能代表这些合约已运行。
- 没有 `.github` CI 文件随此快照提供。构建本身尚未执行，故没有确认实际编译成功或具体编译失败。

## 系统实现证据与可复用部分

- **材料**：`api/material/GTMaterialRegistry.java:25-43` 定义 10k 上限、名字与数字 ID 索引及 DEFINITIONS/LINKS/READY/FAILED 阶段；`:82-87` 检查 ID 重复；`:99` 处理别名，`:154-194` 完成初始化/链接/原版统一。`api/material/GTMaterial.java:18,26,86-184` 保存原子、熔点/沸点、密度、工具性质、燃烧/粉碎等属性；`content/material/Materials.java:7-29` 是按 Element/Ore/Compound/Particle 分组定义的统一引用层。这些是材料目录与数据规范化的候选基础，仍直接关联 MC 类型。
- **配方**：`api/recipe/RecipeMap.java:51-52,94-97` 有全局 map 与物品/流体索引；`:217-225` 提供碰撞检查注册；`:29-48` 动态配方接口。`data/MachineRecipeMaps.java:28-39` 等定义 85 张机器表。`GregTech.java:75-190` 按顺序注册手写、材料、批量移植与兼容配方，不能和另外两套初始化顺序直接拼接。`gametest/RuntimeRecipeReloadTests.java:34-87` 实现真实数据包 reload/覆盖/撤销检查和网络配方 round trip（代码存在，未执行）。
- **机器**：`blockentity/machine/BasicMachineBlockEntity.java:45-106` 是统一机器 BE，含规格、RecipeMap、库存、输入输出罐、方向配置、能量/进度、控制与 cover；`:160,641,1129` 有服务端 tick、配方选择和注入；`:1281,1288,1359` 有菜单与保存/加载。`SmeltingCrucibleBlockEntity.java:215-299` 有温度、相变、坩埚反应和熔毁；`:790,809` 有 NBT 加载/保存。烧燃箱、锅炉、蒸汽 KU 引擎、各多方块控制器均有实际类，不能因注册名相同重复导入。
- **能源**：`api/energy/EnergyNet.java` 有 wire 网络与接收者搜索；`IEnergyBlock`、`EnergyPackets`、`EnergyTransfer`、`GTEnergyStore`、`GTVoltageTiers` 等构成 GT 多能量 packet API。`gametest/SteamChainTests.java:19-67` 检查蒸汽拒收水、200L 蒸汽转换、锅炉 1 水+80HU→160 蒸汽与蒸汽引擎阻塞行为。**明确缺口**：`api/energy/EnergyCompat.java:9-15` 注明 IC2/RF stubs，实际函数恒返回 0；外部能源兼容不能宣布完成。
- **物流**：物品管 `ItemPipeBlockEntity.java:184,603,882,1064,1120` 与流体管 `FluidPipeBlockEntity.java:181,557,826,898,950` 有 tick、Forge capability IO 与 NBT 持久化，均有覆盖板宿主逻辑。实际物流核心已经实现：`registry/GTLasers.java:101` 注册 `LogisticsCoreControllerBlock`，`LogisticsCoreControllerBlockEntity.java:109-153` 每秒扫描/能源门控/路由，`:271-280` 保存缓冲、罐与 cover；`content/logistics/LogisticsCoreStructure.java:47-163` 定义结构与 CPU 参数。十个 logistics GameTest 文件含 core/network/filter/item/fluid/storage/display 等。**旧 `PORTING_AUDIT.md:65` 声称核心是占位、只有结构 W1，已被当前代码推翻；不能据旧文档重做或遗漏核心。**
- **世界生成**：`worldgen/GTFeatures.java:25-70` 实际 DeferredRegister 注册矿脉、小矿、石层、地表、基岩矿、树、flora、bush、rock、deep ocean 等，`GregTech.java:31` 接线；另外有地下城、泉与水体。`block/OreBlock.java:39-80` 已将宿主石与 broken 状态放入 BlockState，明确不再给每个矿石建 BE；`blockentity/OreBlockEntity.java:85-95` 为旧 BE tag 做 host-state 迁移并移除旧实体。旧文档中的“每矿一 BE 导致内存灾难”同样不能直接当作当前未修复状态。
- **渲染**：`client/OreBakedModel.java:44,77` 使用 Forge IDynamicBakedModel 和 512 有界 quad 缓存；pipe/wire、坩埚、蒸汽引擎、cover、显示器、反应堆等有专门 renderer/model 类。这些资产/行为需要客户端视觉验收，GameTest 无法证明画面正确。`client/GregTechClient.java:67` 作为 Dist.CLIENT 订阅；server classloading 仍须启动验证。
- **界面**：`client/gui/BasicMachineContainerMenu.java:23,32-69` 建机器/流体/玩家 slot 并同步数据，尽管包名为 client，服务器机器 `BasicMachineBlockEntity.java:1281` 也创建菜单；迁移须按类依赖区分 common menu 与 client screen。`BasicMachineScreen.java:29-88` 渲染机器与流体/tooltip。`client/GregTechClient.java:784-786` 等注册 MenuScreens。JEI 另有配方表、多方块、世界生成及预览类别。
- **版本适配**：只有 Forge 1.20.1；主/客户端/GUI/JEI/GameTest 直接依赖 Forge/MC API。现有独立参数、数据定义、坩埚反应、机器耗能/输出算法适合逐步抽成共享核心，其注册、ItemStack/NBT、能力、网络、worldgen 和渲染留在版本平台层。

## 验证现状与第一条玩法切片

- `PROJECT_HANDOFF_2026-09-13.md:113-114` 的 196 GameTests/94 Python tests 与 `PORTING_AUDIT.md:65` 的 681 GameTests 是历史文档声明，对应外部绝对日志路径并未随快照提供。当前 1,042 注解明显说明历史数字不代表当前测试集。
- 覆盖强项：大量功能 GameTest，真实配方重载与 packet round trip，机器 IO/控制/cover、锅炉蒸汽、坩埚温度、制造材质守恒、物流路由及矿石旧 tag 迁移。弱项：本包未提供自动化客户端互动、专用服务器实际启动记录、完整世界关服重启验收、两版本相同流程或相互旧存档兼容证明。
- NBT `saveWithoutMetadata()/load()` 的对象测试不等于世界实际保存、关服、重新启动后的磁盘往返。`RuntimeRecipeReloadTests` 证明的是待执行的资源 reload 测试实现，也不等于旧世界兼容。
- 推荐完整的首条玩法切片：新生存世界采集地表石/铜锡资源→手工具/坩埚及烧燃箱→熔化铜锡并合金/浇铸青铜→合成并放置青铜锅炉/蒸汽引擎→真实流体管输送蒸汽→KU 驱动一个基础处理机→产物由物品管送入箱子→打开机器界面观察进度/罐→存档关服重启并确认库存、流体、能量、配置、运行进度与继续加工。
- 该切片在两平台必须使用同一套材料/配方/耗能语义，既自动化也做客户端真实操作。现有 `CrucibleSurvivalTests:15-34`、`CrucibleTemperatureTests`、`SteamChainTests:19-67`、`BasicMachineCraftingTests:50-172`、`ManufacturingTests:33-142`、`MachineOutputTests:60-124` 可作为单环节基础，但尚无一项现成测试完整执行以上整条链。制作可控种子/测试世界时不能把直接 NBT 注入温度、能量或创意发放材料当作生存可达性证据。

## 首阶段建议

1. 保存此来源完整文件快照、许可/credits/文档与 SHA-256 清单；无 `.git` 时记录历史缺失，不伪造原作者提交。
2. 在整合目录先原样建立 Forge 基准构建，去除硬编码 JDK 路径，固定依赖版本，保存 build 与 fresh GameTest 报告；确认完整集被发现以及动态注册/配方数。
3. 为 NeoForge 1.21.1 建平台模块，优先抽出材料规范、配方定义与玩法切片算法，建立同一语义的两平台测试。原 saltnya 现有内容作为保留清单，逐步迁移；不能先丢弃大部分内容后把精简示例称为完整整合。
4. 采集客户端、专用服务器、玩法、世界磁盘往返证据；清楚限制旧存档范围，保留原 registry ID/NBT 字段到确认迁移方案。
5. 授权及作者/素材来源核实前保留其原文元数据，不自行更改第三方授权或发布模组。结合另外两家逐系统选择实现，而不是在注册层并入三套底座。
