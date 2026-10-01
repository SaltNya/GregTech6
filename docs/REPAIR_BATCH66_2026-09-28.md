# 第六十六批：电动扳手生存拆卸

## 原版依据

GT_Tool_Wrench_LV 继承普通扳手目标集合，额外识别活动扳手采掘类型，速度倍率 2，方块损耗基数 50。MultiItemTool.getDigSpeed 使用工具头材料品质对比方块采掘等级，并乘材料工具速度；onBlockDestroyed 以 ceil(50×方块硬度) 交给 doDamage，同时扣电并按上一批概率磨损。普通扳手 canCollect=true。

Loader_MultiTileEntities:101 的 aMachine 使用 TOOL_wrench、采掘等级 0；MultiTileEntityBlock:275 返回该工具类型。注册行中的材料品质参数不能直接当作所有机器的采掘等级。本轮保留通用机器等级 0，仅按现有明确的材料方块/标签规则校验高等级目标。

## 实现

- 新增 ElectricWrenchHarvest 统一目标、材料品质和速度。识别本模组 wrench/monkey_wrench 采掘标签、GT 栏杆以及原版明确列出的活塞、活塞头、红石灯、漏斗、发射器/投掷器；不是通用镐。
- 木质/橡胶流体管和物品管排除，继续使用既有斧/剪刀规则。未宣称完整还原旧版跨模组名称前缀兼容名单。
- ElectricToolItem 接入实际 getDestroySpeed / isCorrectToolForDrops / mineBlock：有电且未损坏时按头部材料工作，服务端破坏扣一次 ceil(50×hardness)，通过已实现耗电路径同时计算材料磨损及废料。
- 修复 TieredItem 遗留的原版 isDamageable=true：此前 getMaxDamage=0 与此标志冲突，GTToolHelper 的收集检查会得到 0<0=false，使有电工具也无法自动收集。现在明确禁用原版耐久机制，材料寿命仍由 GT.ToolStats.k 管理，并新增实际收集资格断言。
- GTToolHelper 开放符合条件的电动扳手机器收集；现有 GTMachineBlock 的 playerDestroy 负责把机器装入背包，满时沿用落地逻辑。
- BlockHarvestEvents 高等级校验改读电动工具头部品质，不再把全部型号当作固定 Tiers.IRON。空电/损坏/等级不足不能取得扳手目标掉落。
- 11 个旧机器/管道类的 canHarvestBlock 和 getDestroyProgress 原先会直接认任何扳手并写死速度。为电动工具转到统一资格与原生/Forge 进度，保留其它工具的既有行为；SafeBlock 的所有者检查未改动。
- EnergyNodeBlock 增加扳手采掘分类，运行时标签随策略生成；木质优先分类仍在前面。

## 验证

新增 ElectricWrenchHarvestTests 三项：

1. 真正的 FakePlayer SURVIVAL gameMode.destroyBlock 拆基础机器，检查材料速度、硬度耗电一次、机器入包一次、内部三颗钻石落地一次且不重复机器。
2. 高等级方块使用合法钢工具头失败，使用实际高品质材料成功，空电后失败；覆盖 Forge 等级超过 3 时的钩子。
3. 原版明确列出的 Minecraft 目标、错误目标拒绝及能源节点扳手标签。

初次启动后复核发现测试用纯铜不符合电动装配 typemin/品质规则，主动停止并改用合法钢工具头，确认旧进程退出后换新世界。随后 MagnetMachineRepairTests 的旧断言要求电磁铁使用镐标签，与上述原版 aMachine 定义冲突，已改为检查扳手标签。再运行发现真实生存收集失败，定位到上述原版耐久标志冲突并修复。每次修改前均停止旧测试、确认退出再换新世界。最终在新世界 build/gametest-batch66-electric-harvest-complete 完整重跑：build/gametest_batch66_electric_harvest_complete.log 于 07:57:23 报告 All 1027 required tests passed，07:57:56 正常关闭，进程退出码 0，BUILD SUCCESSFUL（8m52s）。运行期间 Java/资源冻结，未构建 jar。已刷新 docs/porting-progress.json。

## 剩余工作与测试

IDEA 重启后，用充电电动扳手拆基础机器，观察机器进入背包、内部物品独立掉落、按硬度扣电以及不同材料速度差异。空电不能正常拆出机器；红石灯/漏斗等原版目标可用。客户端画面及大型坩埚仍待实测。

后续仍需扳手/活动扳手模式切换、电锯剪叶/冰块/采掘、工具在配方中的替代，以及全部机器的原版材料采掘等级逐族复核。本批使用当前 BlockHarvestPolicy 与原版等级标签，不能据此声称每个机器的等级都已与 GT6 完全对齐。旧版外部模组前缀名单未照搬到现代环境。

没有执行 git commit。
