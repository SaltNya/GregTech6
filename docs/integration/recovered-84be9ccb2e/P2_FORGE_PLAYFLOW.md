# P2 Forge 铜锡加工链验证

本批只新增 `src/bootstrapGameTest` 中的开发测试和模板，不修改生产机器、配方、材料、热规则、NBT或Gradle。运行验收仍由主线执行，本分支不启动游戏，不产出jar。它验证给定器材和原料的真实加工路径；取得矿石、制造器材/工具、制作并使用青铜工具、图形客户端操作、世界重载、成品jar专服均不在此测试的通过含义内。

## 测试入口与边界

测试类：`com.gregtech.gregtech.integration.gameplay.ForgeBronzeChainTests`。`@GameTestHolder("gregtech_playflow")`，`@PrefixGameTestTemplate(false)`，模板名 `test_bronze_chain`。父构建已有独立 `bootstrapGameTest` 源集，测试和模板不进入发布jar；正式机器仍使用主源码集的注册和生产BE。

模板逐字节复制自导入项目1的 `src/main/resources/data/gregtech/structures/test_blueprint_empty.nbt`，目标 `src/bootstrapGameTest/resources/data/gregtech_playflow/structures/test_bronze_chain.nbt`；112字节，SHA-256 `6c01f87bfc554e3e1ede220e784470c02b04ad9ada25cf366d4b1b9e157d8f0e`。物理NBT `size=[9,8,9]`。原 `test_empty` 只有 `[1,1,1]`，不足以表达器材布局和隔离测试范围，故使用既有大空模板，不添加另一套内容注册。

测试借用 `GameTestHelper.makeMockSurvivalPlayer()` 的官方非创造Player承载库存和工具磨损。煤炭/打火石使用正式Block的 `use`；模具使用实际 `PlayerInteractEvent.RightClickBlock` 和 `SmelteryInteractionHandler.onRightClickBlock`。没有假造客户端点击、网络、距离检查或资源取得的证据。

## 两条用例

`coalCopperTinToFourBronzeIngots`，9800 tick总超时，9700 tick主动失败门禁：

1. 放置正式 `gregtech:burning_box_solid_brick`、上方正式 `gregtech:smelting_crucible_ceramic`、侧邻正式 `gregtech:mold_ceramic`。新坩埚/模具初始293 K，热源未燃烧且HU为0。环境温度继续使用生产实现的真实biome，投料后自然混温，不把环境强改成293 K。
2. 给定正式钢凿子和钳子；5×5格中选3×5锭图案，逐格用实际事件点击15次。每次核对递增掩码，最终核对真实锭配方、1U需求、凿子15次磨损。没有调用 `setDungeonShape`、写形状NBT或直接调整掩码。
3. 三个正式铜锭和一个正式锡锭作为两个顶部ItemEntity，以正常重力落入生产吸取区；等候真实cache每tick消费，冷态观察3U Cu+1U Sn且实体/cache清空。没有调用 `addMaterialStacks`、写 `gt.materials`、直接调用 `react`。
4. 正面点击存入8个煤炭，正式打火石点击点火并磨损1次。由正常世界BE tick、邻居HU传输、原坩埚温升与反应执行。逐tick观察1357 K门槛；首次青铜必须有前一观察温度达到1357 K，且恰4U、无铜锡残料。观察燃煤消耗、连接升温与冷态前置条件。
5. 首次合金完成时移除热源，清理遗留燃料/热源影响。用钳子真实右键触发侧邻浇铸，每次只从坩埚转移1U。重复点击已填模具必须拒绝并不减坩埚量。等待真实模具tick自然冷却到青铜熔点以下，再由钳子交互提取正式青铜锭，直到4锭；钳子恰磨损4次。
6. 全流程每tick及各浇铸/提取阶段核对实体、cache、坩埚、模具、暂存成品和Player库存合计始终4U。完成后器材原料/成品缓存为空，再多一tick和一次真实空模具点击必须不能产生第五锭。任何断言或9700 tick门禁失败会清理热源并报告阶段/温度/HU/原料/cache/模具形状/铸造次数/成品库存。

`disconnectedHeatAndFullCrucibleRejectWithoutLoss`，480 tick总超时，400 tick检查：

- 一个冷陶瓷坩埚与真实燃煤/打火石点火的砖燃烧室间留一格空气。检查热源确实消耗煤且还在燃烧，坩埚HU仍0且无升温/原料，证明邻接断开没有凭空输热。
- 另一无热源的正式陶瓷坩埚顶部投17个正式铜锭。检查16U容量、1锭留在cache、原实体已吸收，总量17U且无热量。拒绝通过真实吸取/缓存处理出现，不调用内部补料函数。
- 正常完成及断言失败时清理热源。此用例与整链仅2项，未扩大到完整原GameTest套件。

## 生产代码证据（当前整合树的一起始物理行号）

- 注册与参数：`registry/GTMachines.java:79` 砖燃烧室25%效率/16HU每tick；`:334` 陶瓷坩埚。`api/machine/MachineRegistry.java:149` 同一坩埚参数建立正式模具伴件，`:171` 注册MoldBlock与正式Item。
- 煤炭/点火：`blockentity/machine/SolidBurningBoxBlockEntity.java:71` 正常tick向UP发HU并消费燃料；`:242` 正面交互；`:255` 正式打火石调用点火并磨损。`api/machine/FurnaceFuelHelper.java` 使用原燃料值/效率规则，测试不模拟正HU。
- 顶部投料/容量：`blockentity/machine/SmeltingCrucibleBlockEntity.java:343` 吸取真实ItemEntity；`:363` 每tick解析一个实际缓存物品；`:380` 超16U拒绝；`:269` 正常tick合金反应；`:940` 真实侧面浇铸与扣料。
- 凿子/钳子事件：`event/SmelteryInteractionHandler.java:36` 正式右键入口，`:118` 钳子先取出/再尝试浇铸与凿子判定、磨损。
- 模具：`blockentity/machine/MoldBlockEntity.java:131` 15格锭图案；`:318` 每tick自然冷却/固化；`:503` 真实格点凿形；`:527` 邻接浇铸；`:585` 钳子提取；`:736` 已占用/数量不足拒绝。
- 实际材料：共享 `content/material/generated/CompoundMaterials.java:436` Bronze熔点1357 K；铜锡反应执行/目录沿项目1原实现，金样见P2材料合约。本次没有接入尚未平台启用的 `ThermalStep`，因此通过不能声称Forge冷却能源或signed HU已改造。

## 验证状态与主线运行

静态入口已核对；隔离Forge编译实际通过7m46s，日志work/p2-shared-materials/work/p2-forge-playflow-compile.log。已提交873db17e61并合入主线de18243bb9。主线两项实际测试最终通过4m17s，XML零failure/error/skip，正常保存退出；耐久回执verification/p2-forge-playflow.json及xml。只执行gregtech_playflow两项，不把旧242类全部执行作为本批前置，也不把仅编译当加工通过。

首跑2m42s：主流程tick3011合金/tick3020四锭通过，但断热负例冷坩埚吸入了Leather6U+Steel2U，整体失败；组成恰对应vanilla_compositions.json的一个鞍。模板gzip/NBT完整解析确为air palette、blocks[]、entities[]，mock survival Player只new未spawn。新world加只读诊断后两项通过3m32s，未重现外来输入；不能宣称已定位鞍的具体产生源。

夹具修正仅给明确不投料的冷坩埚加玻璃顶和四侧罩，保留底部一格空气断热；正常投17铜锭的满容量坩埚不加罩。未改生产吸入/热量/容量或放宽断言，新增冷坩埚初始空状态检查。临时DEBUG日志已移除。最终tick400负例空冷坩埚287K/0HU、满16U铜+cache1锭；tick3017达1357K生成4U青铜、tick3026得4正式青铜锭，逐tick守恒及额外空取不复制通过。

ForgeGameTestReports为另一个开发专用类，只在GameTestServer及显式报告路径启用，组合原LogTestReporter和原版JUnitLikeTestReporter保留日志并写XML；默认关闭，不进jar。初次报告命令未整项引用含点参数，PowerShell把.xml拆为任务，32s配置失败（游戏未启动）；整项加引号后重跑通过，失败日志单独保留。

主线可用现有配置运行：

```powershell
./gradlew.bat :runGameTestServer '-PgameTestNamespaces=gregtech_playflow' '-PgameTestDirectory=build/forge-playflow-isolated-run' '-PgameTestReport=build/forge-playflow-isolated-run/playflow.xml' --max-workers=2 --console=plain
```

路径/属性名以主线接线为准；任何运行缺口应修改可审查测试或生产入口并重新验证，不允许以写温度、灌HU、补成品或绕过凿形让测试“通过”。当前没有发现必然阻断该给定器材链的生产入口缺失，但真实tick时序/物品吸取/烧煤供热/模具回收仍须运行核实。
