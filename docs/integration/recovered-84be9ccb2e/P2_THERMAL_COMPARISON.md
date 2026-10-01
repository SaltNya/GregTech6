# P2 坩埚热力与合金行为比较

日期：2026-09-30。范围：源码阅读、单位归一化与固定算术金样；未运行 Gradle、游戏或玩法复现。本报告不改变 Java、Gradle、注册或存档。以下“预期结果”是可由列出的代码独立计算的结果，尚不是三套实际游戏执行报告。

决策：共享热力权威状态采用项目1现有整数 Kelvin、GT6 U 和材料整数 ID。从项目2的纯热步结构提取算法，但逐项校正；从 masson 吸收显式状态、显示投影和规则分层，不直接搬其摄氏浮点状态、144 单位存储或整套材料目录。项目1仍是功能保留基线，已确认的行为差异必须作为明确修正记录，不能默默随提取改变。

## 证据范围与来源

项目1（saltnya）使用整合目录内保留的 Forge 基线，根路径为 `src/main/java/com/gregtech/gregtech/`。项目2（brokestar233）路径前缀为 `../Libs/gregtech6-main/`，项目3（masson）为 `../Libs/cruciblecraft/`。本次只写此文档，来源目录保持原样。

GT6 对照固定为 `GregTech6/gregtech6@3703e40308c8c030763fd6297dea8b210d2a77b1`，即 CC 记录的原代码 revision，避免引用会变动的 master。直接读官方源码而非把移植注释当作行为证明：

上游行号口径：本报告按固定raw原始UTF-8字节的splitlines物理行、1起编号。2026-09-30独立Python urllib复核Smeltery为703行、SHA-256 `eaf9b833c4c439a102bb346c6c4e032d88b6d97b823003232f45d185f23597f1`，热步301–313、混温333、能源693。web工具抽取正文会去除空白行，其294/324/682等归一化位置不是该raw源码物理行号，不能直接用于GitHub源码定位。OreDictMaterial raw SHA-256 `768707d5eeeb6b60f0c5d0a24b39ab50f6f173a29a40f0fa3365308cf0688371`（1512行）；MT raw SHA-256 `12936831b1b5f419dc783c5f32f3cc07a329734ca6c5c11757d52e1be27904b2`（4118行）。

- [MultiTileEntitySmeltery](https://github.com/GregTech6/gregtech6/blob/3703e40308c8c030763fd6297dea8b210d2a77b1/src/main/java/gregtech/tileentity/tools/MultiTileEntitySmeltery.java)：301–313 热步；330–352 混温和入料目标；186–244 合金选择、按所选配方消费；360–362 上限；688–697 能源注入。
- [MultiTileEntityCrucible](https://github.com/GregTech6/gregtech6/blob/3703e40308c8c030763fd6297dea8b210d2a77b1/src/main/java/gregtech/tileentity/multiblocks/MultiTileEntityCrucible.java)：大坩埚对照，不能用小坩埚参数覆盖其容量和壳体。
- [OreDictMaterial](https://github.com/GregTech6/gregtech6/blob/3703e40308c8c030763fd6297dea8b210d2a77b1/src/main/java/gregapi/oredict/OreDictMaterial.java#L1391)：1391–1401 重量；[MT](https://github.com/GregTech6/gregtech6/blob/3703e40308c8c030763fd6297dea8b210d2a77b1/src/main/java/gregapi/data/MT.java#L1705)：Bronze=3Cu+1Sn，熔点/沸点继承 Cu，3374 增加 AnnealedCopper 替代配方。

GT6 原行为摘要：热步以整 K 消费缓冲，可正可负，不清不足一度的余量；供热/制冷发生后等待100 tick，再每10 tick向环境移动1 K；温度下限是 min(200 K,环境 K)。入料按含壳体的密度重量混合，整数缩放向下舍入。合金必须达到产物熔点，最多一个组分仍固态，选择产量最大的一条，消费所选配方而非固定主成分。来源以上固定代码，以下每一差异还列本地实现行号。

关键本地证据：

- 项目1 `blockentity/machine/SmeltingCrucibleBlockEntity.java`：66、70–78、96–100 容量与状态；216–293 服务端顺序与热步；379–408 混温/入料；790–820 NBT；924–933 注入。
- 项目1 `api/machine/crucible/CrucibleReactions.java`：61–99 配方构建、候选选择与消费；`api/material/MaterialMass.java`：9–10 重量；`api/machine/CrucibleSpec.java`：23–34 壳体、倍率与热量参数，49–54 上限/重量。
- 项目2 `src/main/java/gregapi/util/CruciblePhysics.java`：53–55 小/大参数；118–143 入料；158–199 热步；207–208 上限；249–296 扫描；308–319 消费；363–409 相变。
- 项目3 `src/main/java/com/masson/cruciblecraft/heat/CrucibleThermalModel.java`：19–63 热步；97–148 混温；168–174 符号加法。`machine/component/ThermalComponent.java`：28–49 HU/CU；58–79 步进/混温；127–132 客户端显示与权威状态分离。
- 项目3 `recipe/AlloyIndex.java`：159–192 候选选择；319–362 转换与消费 DTO。`machine/component/CrucibleProcessCore.java`：125–179 顺序；479–530 浮点温度及字符串材料存档；540–548 入料。

## 统一单位与比较输入

权威量是 `U=648,648,000` 每锭，`U9=72,072,000`，`U1000=648,648`。小坩埚 `16U=10,378,368,000`；大坩埚 `432U=280,215,936,000`。材料量必须是 long，不能放入 int。

CC `material/GT6ImportUnits.java:11–14,42–54` 定义144单位/锭，每CC单位=4,504,500 GT6 U。整锭、U9可精确表示；U1000和单个GT6最小单位不能。该类选择拒绝非整除输入，不能在整合时通过舍入“解决”。144只适合作为明确可逆的外部流体边界，不能代替权威材料量或旧存档容量。

同一物理输入换成 CC 时只在比较边界使用 `Celsius=Kelvin-273.15`，实际参数是 Java float；CC 原宿主固定环境20°C（`CrucibleProcessCore.java:49,69`），相当于293.15 K，而项目1默认环境为293 K（`data/GregTechConstants.java:17–18`）。金样统一显式环境293 K；宿主默认环境差异另列，不能在测试中混用。

GT6重量为 `density * 111.111111 * amount/U`，该数值是游戏体积/重量约定，不是现实一锭金属重量。项目1按同一式；CC `content/sensor/ItemMass.java:42–48` 按其144单位计算同类式，实际采用运行thermal密度。必须把壳体加到已有内容重量，再混入新材料。原材料导入元数据不是运行thermal的自动替代品。

## 热步：实现、差异与固定金样

共同正常公式为 `required=1+floor(totalMassKg/100)`，`conversions=energy/required`（Java有符号整数除法向0截断），支付 `conversions*required` 后升降同样数量 K。项目1使用正转换分支，项目2和CC使用非零分支。

1. 正常供热。输入 T=1300 K、环境293 K、总质量250 kg、缓冲8 HU、cooldown=7、无额外输入。required=3，conversions=2。原GT6/项目1/项目2结果均为 `(T=1302 K,energy=2,cooldown=100)`。CC 从1026.85°C的float执行，换回K约1301.9999756，显示四舍五入1302 K；正常显示相同仍不证明权威值相同。

2. 余量保留。输入 T=1300 K、质量250 kg、缓冲2 HU、cooldown=7、无输入。原GT6/项目1/项目2为 `(1300 K,2,6)`。CC `CrucibleThermalModel.java:41–44` 因无incoming、无转换且余量为正而改成 `(约1300 K,0,6)`。下一次1 HU到来时，前三者立即升1 K，CC只剩1 HU而不升温。这是跨tick玩法差异，不是显示优化。

3. 冷却包。T=1300 K、质量250 kg、原缓冲0，接收8 CU后实际缓冲为-8，cooldown=7。原GT6/项目2热步结果 `(1298 K,-2,100)`；CC queueCooling/有符号step也得到约1298 K、-2、100。项目1当前不接受CU（仅底部HU，877、917、925），应返回未接收；若仅用NBT预置energy=-8，其tick `conversions>0` 不消费，结果 `(1300 K,-8,6)`，负缓冲冻结到后续正HU抵销。共享算法必须保留CU负转换，平台接受能力需作为单独修正发布，不能伪称当前项目1已支持。

4. 负HU包不等于CU。原GT6能源入口为HU取绝对值、CU减绝对值（原693）；项目1 `doInject:928` 同样对amount*size取绝对值；CC `ThermalComponent:36–47` 也按能源种类决定加/减。故size=-8、amount=1的HU仍是+8 HU，不能把所有负包直接当制冷。项目1该乘积及累加没有防溢出；共享入口应拒绝MIN_VALUE/溢出的非法包或采用明确饱和策略并记账，不能让溢出改变HU/CU符号。

5. 冷却窗口。T=1300 K、环境293 K、质量250 kg、energy=0、cooldown=1。三个整数实现均为 `(1299 K,0,10)`，下一9 tick不继续降温，第10 tick再降1 K。CC远离环境时同样；但当T恰等于环境时，整数实现保留递减窗口，到期仍重设10，CC `47–57` 立即将cooldown清0供停tick判定。可吸收停tick优化，但必须证明下一次输入/环境变化会唤醒且不改变残余能量，不应改变权威窗口以方便优化。

6. 温度下限的单位错误。输入 T=200 K、环境293 K、energy=0、质量250 kg、cooldown=100。原GT6/项目1/项目2为 `(200 K,0,99)`。CC把T传为-73.15°C，`62` 的 `min(200.0f,ambientC)` 得19.85°C，下限直接把T升到293 K。再用环境600 K，CC下限为200°C=473.15 K，而原下限仍200 K。该行注释“Exact GT6”不能抵消数值证据；不得直接移植。

7. 非法质量与极值。CC对NaN、无限/非正质量返回required=1（121–125）；项目1/项目2没同样校验。合法机器的壳体/内容重量应非负有限，共享core宜在输入边界拒绝非法质量，另建极值契约。旧NBT的signed energy必须按long原样解码；不能以“负数非法”为由静默抹去CU余量。溢出保护属于记录过的稳健性修正，不声称旧GT6原来已有。

## 入料混温、壳体与相变顺序

项目1 `379–392`、项目2 `118–127` 的混温为：

`newK = incomingK + sign(oldK-incomingK) * units(abs(oldK-incomingK), (long)(wExisting+wIncoming), (long)wExisting, false)`

质量先转long，缩放向下取整。不能改成每种材料平均温度、按材料量加权或平滑浮点平均。CC `97–117`也刻意模仿这一截断，但其先将摄氏float差转long，出现第二重量化。

- 整数质量金样：old=1301 K、incoming=293 K、wExisting=300 kg（含壳体）、wIncoming=300 kg，GT6/项目1/项目2取1008*300/600=504，新温797 K。CC float oldC=1027.8499755859375、incomingC=19.850000381469727，差1007.9999752044678被转long1007，保留503，新温约795.9999756 K，舍入796 K。差1 K可以跨熔点。此值已以IEEE754 float32等价运算独立算出，尚待对实际Java类契约执行确认。
- 截断质量金样：old=1300 K、incoming=293 K、已有250.75 kg、新增175.5 kg，整数算法取1007*250/426=590，新温883 K，不能用双精度连续混合的约885.387683 K替代。
- 密度金样：以声明的十进制密度归一化，3U铜密度8.96、1U锡密度7.287，内容总重≈3796.333 kg；不是4kg、不是4个“计数”的算术平均。项目1陶瓷壳7U、密度0.8181818181818182，总壳重≈636.364 kg，总重≈4432.697 kg，required=45 HU/K。铜锡生成4U青铜密度8.54175时该内容重量一致。项目1密度常量的float32表示会带来微小质量差，不能把这些近似kg小数当作实际类执行到末位的证明，required仍45。

项目1壳体63U用于石质、7U用于默认材料（CrucibleSpec:23–24），但小坩埚实际 `maxMaterialAmount:170`仍16U；“9x capacity”注释不能当作144U内容容量。不能从壳体重量推导容量。

相变差异也必须独立处理：原GT6和项目2 `addStacks:130–141` 入料混温后就按smelting/solidifying目标及目标物质量转换；项目1 `394–405`仅加入原材料，后续tick熔化才在 `251–257` 投影smelting，降温分支 `258–262`重新加入同材料，未投影solidifying目标。CC `applyAdditions:540–548`仅混温并加内容，其CompositionTank `153–169`在跨阈值/内容变化时投影两种目标。提取纯thermal不能顺带把这些不同的材料规则拼入热步。

相变金样应使用具有非自映射目标的明确材料定义，例如A在1300 K熔化为B、目标量U/2：混温后1400 K、冷入1U A时，原/项目2立即得到0.5U B；项目1入料返回仍1U A，后续tick才转换。再测试降到1299 K且solidifying目标C、目标量U/2，项目1当前保留A而原/项目2得到0.5U C。这是指定小型测试材料域的规则金样，不向正式游戏注册假材料。

服务端顺序不能只按最后温度比对：原GT6是入料→合金→相变/危险→称重/展示→保存前温→热步→熔毁；项目1 `tickServer:216–299`是入料→相变/危险→合金→称重/展示→保存前温→热步→熔毁；CC `advance:125–179`与原合金优先更接近。项目2热步函数本身没有调度语义。共用Snapshot需要显式前温/内容变化输入，先保留项目1顺序，再用具体反应/固化金样决定是否修正顺序。

上限也有小差异：原GT6、项目2取 `floor(meltingK*bonus)`，项目1 `CrucibleSpec:49–50`是Math.round。例如1357*1.25=1696.25时相同1696；1986*1.25=2482.5时原2482而项目1为2483。CC `machine/MachineMaterialRules.java:167–176`先加273.15转绝对温，再倍率，但对摄氏结果floor，因而不是同一整K边界。需把已有壳体规格和新兼容修正分开，不能用模糊“125%”掩盖1 K。

## 合金金样与材料目录差异

项目1材料域：Copper id290，mp1357 K、bp2835 K、density8.96；Tin id500，mp505 K、bp2875 K、density7.287（ElementMaterials:52,73）；Bronze id8610，mp1357 K、bp2835 K、density8.54175（CompoundMaterials:436）。MaterialCompositionData:1045–1047绑定3Cu+1Sn；CrucibleReactions:40还含3AnnealedCopper+1Sn的替代配方。项目2 MT:1019,1061,2453相同主熔点。

项目1算法 `CrucibleReactions:78–88`达到产物熔点、最多1个固体组分、至少1组分熔融、取整数转换次数并按最大产量选一条；`91–98`消费所选Reaction。项目2扫描遵循同样主门槛，CC `AlloyIndex:159–192,319–339`也遵循同样门槛。部分代码门槛相似不能推出目录实际温度相同。

- B1：3U铜=1,945,944,000，1U锡=648,648,000，在1356 K时，原GT6/项目1/项目2不生成青铜；1357 K时正好生成4U青铜=2,594,592,000。1357 K是边界，不允许用1356.9显示四舍五入绕过。
- B2：4U铜+1U锡、1357 K，生成4U青铜并留1U铜；不是强制整份比例匹配后拒绝。CC对应576Cu+144Sn，生成576Bronze并留144Cu，只有其运行材料定义达到阈值时成立。
- B3：3U AnnealedCopper+1U锡、1357 K，AnnealedCopper熔点2800 K，允许这一项仍固态，生成4U青铜，不留输入。不得把“所有组分必须熔化”作为更安全的新规则。
- B4：替代配方消费漏洞。项目2 `AlloyResult:221`（record声明）、`alloyScan:249–296`只返回alloy和conversions，没有所选配方；`applyAlloy:308–319`却消费 `aAlloy.mComponents` 的主成分。对B3扫描选替代配方后，消费主Cu时找不到Cu、不报错，锡被扣1U，添加4U青铜，原3U AnnealedCopper仍在，物质量从4U增为7U。实际MDK调用在 `mdk/src/main/java/gregtech6/tileentity/tools/TileEntitySmeltery.java:216–218`及大坩埚513–514存在。必须返回所选recipe/consumption DTO后应用，不能直接迁入applyAlloy。
- B5：目录实际阈值。CC资源 `src/main/resources/data/cruciblecraft/materials/bronze.json:249–250`元数据是1357 K，但运行 `thermal:267`为950°C（1223.15 K）；copper:446–447元数据1357 K，运行465为1085°C（1358.15 K）；tin:378–379元数据505 K，运行397为231.9°C（505.05 K）。`material/def/MaterialDefinition.java:321`直接返回thermal，377–395添加metadata时不改thermal。在1300 K（1026.85°C）下，CC默认目录中的锡已熔、铜未熔、产物已熔，只有1个固体组分，3铜+1锡能变4青铜；原/项目1/项目2因青铜未熔而拒绝。该推导以无配置/startup调优的已提交默认目录为前提，未在游戏中复现。不能只导入metadata后宣称恢复GT6行为。

CC铜锡运行密度也有差异：锡thermal=7.31（tin:396），青铜thermal=8.8（bronze:266），并非各自metadata的7.287/8.54175。`ItemMass:47`实际用thermal；故热步参数不能靠metadata比较后默认相同。共享目录应保留项目1id/量/整数温度，必要的来源调优另记为明确选项。CC的AlloyMatch/Conversion思路值得吸收，其String/int/全局MaterialCatalog依赖不能原封迁为第二目录。

选择理由：项目2最适合提取纯热步，但替代合金消费需修复；项目1所选配方消费已经正确，应继续保留；CC把“选配方及消费列表”表达为DTO利于无MC核心，可参考结构。三者均按规则和金样选择，不按完成度声明评优。

## 共享 ThermalState / Snapshot 的提取边界

建议只有一份平台无关权威状态：`ThermalState(long temperatureK,long previousTemperatureK,long energyHU,int cooldownTicks)`。温度绝不在权威状态中先转Celsius；有符号energy包含CU，保留正负余量。Snapshot包含不可变的材料整数id+long amount列表、壳体规格/重量、long maxAmountU、显式ambientK、前温、内容变化标志。核心可以持有验证过的double重量，但材料量/温度/配方换算始终GT6整数域。

建议步骤：

1. 从项目2tickHeat结构提取 `ThermalStep`，用现有共享CrucibleMath计算混温。热步只接收状态、环境和质量，返回状态；能源类型判定/包绝对值转换在同一共享入口定义，世界面方向仍在平台适配。
2. Forge/Neo只负责把原字段读到状态、把结果写回、事件/库存/注册/同步。不得有两套材料目录，也不得把CC温度float、单位int渗入保存字段。客户端摄氏显示、插值可做单独DisplaySnapshot，不写回权威状态。
3. 配方选择返回recipe identity、精确consumption列表和output量；选中与消费必须使用同一对象。规则Outcome只包含boiling/acid/explosion/phase转换等事实，平台执行伤害、声音、火和方块替换。
4. 阶段A以正HU、原NBT载入与原Forge结果一致为提取验收；阶段B单独引入CU、余量/下限修正、目标固化和顺序校正，每项给兼容记录。不能在一次“重构”中隐含修复一切。

旧NBT必须保留项目1 `gt.temperature` long、`gt.temperature.old` long、`gt.energy.buffer` long、`gt.cooldown` int；`gt.materials`是 `{id:int,amount:long}`列表（CrucibleMaterialStack:94–120）。现阶段没有证明GT6 1.7.10 NBT键/方块注册、CC字符串存档或项目2存档能直接加载；“整数语义相同”不是全存档兼容声明。

加载边界：保留缺省temperature=293 K、oldTemperature缺省取current、cooldown缺省100（SmeltingCrucibleBlockEntity:792–795），保留signed energy和原始容量/物质量；不要从已加载Kelvin减273.15，也不要把U除以4,504,500保存。未知材料ID现基线会丢弃（CrucibleMaterialStack:116–119），后续若改为隔离保留需单独迁移设计和损坏/未知ID测试。过容量旧内容应按明确政策隔离/只阻止入料，不能静默截断。有效负余量不是损坏存档。

## 项目1真实铜锡玩法依赖闭包与最早Neo场景

源码存在可闭合路径，但本次尚未运行它：固体燃烧室→底部HU坩埚→铜锡配料/合金→相邻模具浇铸→冷却→玩家取锭。首次Neo移植必须是真实链条，不用entrypoint自检或注入温度NBT替代热源。

最小正式场景建议使用已有id：`gregtech:burning_box_solid_brick`（GTMachines:79–80，效率2500、16 HU/t）、`gregtech:smelting_crucible_ceramic`（334–335，壳mp2000 K、极限2500 K）、`gregtech:mold_ceramic`（MachineRegistry:149–176由坩埚规格生成，不是GTMachines显式字段）；材料与物品采用Cu290、Sn500、Bronze8610及现有ingot前缀和注册id。验证夹具给定这些正式物品和工具可以早于完整生存配方迁移，但必须标记“给定器材的加工链”。

源闭包和实际交互：

- 燃料入口 `SolidBurningBoxBlockEntity:242–283` 正面放燃料，打火石点火；407要求正面空气，不能堵住。`71–83`顶面发HU并扣能量；`107–131`消耗一份燃料、生成容器/灰。`FurnaceFuelHelper:26–41`使用燃值*25*efficiency/10000；`FurnaceFuelValue:23–45`材料燃值优先，否则Forge燃料钩子。Neo需换平台燃料查询，保留燃值与灰规则；不能把“发16 HU/t”错当每份燃料总16HU。
- 能源接口是 `api/energy/EnergyTransfer` / `GTEnergyBlockEntity` / `ITileEntityEnergy`，燃烧室Direction.UP连接坩埚Direction.DOWN；需同一HU tag身份和真实邻居查找。项目1发出的能量即使没有接收方仍扣除（SolidBurningBoxBlockEntity:75–76），夹具应断连对照验证，不能人工补回。
- 入料 `SmeltingCrucibleBlockEntity:342–375`吸取顶部ItemEntity到单缓存、每tick解析一件、只有成功添加才扣物品。`CrucibleItemInput:29–41`从正式MaterialItem前缀得到材料量；不把右键拿矿当入料路径。最小Neo可从3个正式铜锭和1个正式锡锭开始，以减少矿物还原依赖；后续才纳入矿石/石灰/碳、工具和世界生成。
- 合金由共享材料组成/反应域选择，1357 K至少可成青铜；不要以JEI/文档显示有配方作为实际成品证据。陶瓷容错比石质更好：石壳极限1375 K与青铜熔点1357 K仅差18 K，还含63U大热质量；因此第一个可调试场景选陶瓷，石质行为后续同样保留验证。
- 模具是实际5×5凹槽形状。`MoldBlockEntity:129–132`三列×五行的15格为ingot，所需量由前缀给U（719–731）；空形状没有产物，不用GameTest直接改moldShape当玩家交互完成。`SmelteryInteractionHandler:118–151`空手/钳子先取件再tryPour，凿子顶面逐格修改并磨损工具。
- 相邻空模具 `tryPour:527–537`调用坩埚 `fillMoldAtSide:939–945`，仅浇熔融内容；模具 `fillMold:736–760`一次接收精确所需量，记录真实K，已有内容拒绝。模具每tick最多向环境降5 K（318–324），低于内容熔点才solidify（371–372），`tryPickupWithPincers:602–629`用正确GTItems/前缀产出且扣空内容、保留烫伤或钳子语义。
- 最小Neo仍需正式block/item/BE、材料ItemPayload、工具交互、热源库存、NBT/data components适配、tick/同步/模型资源，不能只注册三个方块外壳即称玩法完成。形状/配方、材料目录、热步可共享；Forge事件/Capability与Neo事件/平台NBT接口放适配层。

配方扩展的现有证据：`data/gregtech/recipes/smeltery_survival/clay_crucible.json`用粘土球、正式刀/擀面杖的tool_shaped制作clay_crucible；`ceramic_crucible_firing.json`用真实熔炉烧成ceramic；`burning_box_solid_brick.json`使用brick ingot tag+打火石。配方JSON存在不证明标签、工具制作与模具获取全部可达，最早场景需明确给定器材范围，再验证从资源获取器材的完整生存入口。

建议验收记录：

1. 独立core契约执行上述热步与混温金样，特别是signed余量、200K下限和1K量化；对原GT6/项目1/项目2逐项保留对照结果，不能只比较新core与自身计算。
2. 两平台正式注册与结构启动后，从冷环境用正式燃料/点火升温，投3Cu+1Sn，观察材料量与HU账本，再通过正式模具形状交互取4个Bronze ingot；检验满容量不吞物品、断连不供热、余料不凭空消失。
3. 分别在冷炉、持续供热、含正余量、含CU负余量、已浇未固、已固未取这六个状态保存/关服/重载；断言id、U、K、前温、cooldown、energy与物品完全保留。客户端观察与专用服务器证据分别登记。
4. 只有P1 bootstrap启动而无上述操作时，仍记“热力/玩法移植未验证”。本报告给出实施选择和验收输入，不把编译、金样推导或源项目测试声明升级为完成证据。
