# 整合状态

更新：2026-10-02。Goal active。当前工作目录为 `F:\Dev\GregtTech6New\GregTech6`；优先对齐 Forge 1.20.1 与 NeoForge 1.21.1，继续采用集中小检查节奏。

- P0：三源审计、全部逐文件清单、项目1副本校验及原始Forge构建已完成；项目1授权和历史仍待用户信息。
- P1：恢复完整后续移植源码，最新两平台构建与 574 个共享 core class 验包通过；两版当前源码普通专服实际启动与指定蒸汽引擎制作产物保存重载通过；NeoForge 指定青铜/蒸汽动力链与 Forge 指定普通蒸汽动力/精确持久化状态重载通过。当前双版开发主菜单、Neo 材料/流体库存模型及六物品绘制已通过；Neo 客户端停机机器实际菜单/转移/流体更新/独立 JVM 保存重载已通过；Forge 客户端世界与成品生产环境启动仍待验。
- P2：NeoForge 给定设备/原料的煤炭供热、铜锡合金、四次青铜铸锭通过，并验证叠放模具逐次消费 9U 盆内容。生存取得设备与原料、制作工具及 Forge 对应运行流程仍未满足完整验收。
- 世界重载：两版普通专服已保存并重新读取实际制作查询的普通/强化青铜引擎物品。NeoForge 普通专服独立进程同一世界检查已覆盖铜模具/青铜盆、粉碎机未完成作业继续完成、搅拌机命名库存/流体，以及实际蒸汽动力链的产物和竖直冷凝水保留。不是全部机器、精确热量快照、跨版本或旧存档证明。
- P3–P4：原完整快照的机器、能源、物流、世界生成、渲染、界面与配方移植源码已恢复；各系统的双平台运行、世界持久化和旧存档范围继续逐批补证，不按源码数量声明完成。
- 项目1基线：Forge 1.20.1 / 47.4.20、Gradle 8.8、Java 17，原始构建通过（13m37s）。全部78,768源文件副本SHA-256一致。本地导入标签 import/saltnya-snapshot；不代表玩法或启动已通过。
- 本机 Java 21：用户提供 `.minecraft/runtime/java-runtime-delta`，已执行 `java -version` 和 `javac -version`，均为 Microsoft OpenJDK 21.0.7。
- 原始 Git 历史：提供目录均无.git；已获取 brokestar 3055个提交及masson 202个提交，保留原作者。逐文件Git blob核对：brokestar快照准确对应3118acbf83a84d05fa37d57af1705cf00e423ca9（220275/220275文件），masson对应2ba4e4b60f7a770360b2ec7ca2adad3507ec4a28（61192/61192文件）。本地source/*标签保留对应原提交；项目1远程和原历史仍缺失。
- brokestar 的 ModularUI 子模块目录为空；已从对应原始Git树恢复gitlink ec524db7a5724f8cf3c837436b1ae742c778c62f，并获取其公开原仓历史，保存source/modularui-brokestar-snapshot标签。尚未导入其运行时。
- 授权未决：项目1 `mod_license=All Rights Reserved`，LICENSE.txt 是 Forge MDK 文本；保留原文，待作者明确适用授权。后续发布门禁未通过。
- 双版本开发服务器接线与上述指定两版普通专服/产物世界重载已通过；两版完整客户端、专服玩法、所有状态重载和旧存档迁移仍未满足完整验收。

## 当前任务

1. 修复两版实际玩法阻塞，优先 NeoForge；集中完成一批再编译/短运行。
2. 模具/盆与基础机器指定作业已通过 NeoForge 世界重启；Forge 指定蒸汽链与11台实际持久化状态重载通过；继续覆盖其他配方和完整生存。柴油系列已同步恢复原 RU/完整燃料记账/背面排气；Neo 同一隔离旧世界和 Forge 新隔离世界实际旋转活塞动力链、产物自动出箱与保存重载通过；两版原精确输出 min/max 范围已同步。旧直接 KU 布局需增加旋转活塞；动画三态和全燃料/姿态继续对齐。
3. 已完成 Neo 指定机器客户端界面/方块画面/重载，下一批推进客户端实际动力制作与 Forge 对应运行，补齐生存链与两版差异；木辞典三种种类的原贴图缺口保持未完成。
4. 保留来源、贡献、许可、历史与未验证范围记录；完整三源整合 goal 保持 active。


## 2026-10-02 / 双语 README 与 Community Edition 名称

用户明确指定新工作目录 F:\Dev\GregtTech6New\GregTech6，并要求英文主 README、可切换的中文版本，以及两版统一名称 GregTech 6 Community Edition。当前用户仓库分支为 main，源提交 f8d76b3b882c74c098b2ffbdddf910711a4fcb01。

已重写 README.md / README.zh-CN.md，包含介绍、目标版本、状态、双版本构建、开发运行、贡献、分项许可和署名。根 mod_name 和 Native 元数据共用根配置；新目录旧入口/事件订阅 ID 同步为 gregtech6，既有 gregtech: 注册、资源与保存身份保留；材料来源存在性查询同步。默认 GameTest 资源命名空间保持原样。BUILDING.md 同步品牌及当前目录名，未更改第三方许可或发布到远程。

一次资源处理 9m 22s 通过，实际生成的两份 TOML 显示名称均为 GregTech 6 Community Edition、modId 与 dependencies 所属 ID 均为 gregtech6；双向语言链接及 18 个本地文档链接检查通过。此批未编译 Java、未重打 JAR、未启动游戏，不能作为玩法/世界重载或完整整合完成证据。回执：verification/community-readme-branding-20261002.json。

原完整整合 goal 继续保留。新仓库由用户重新初始化，当前源树与此前 84be9ccb2e 上传快照存在差异，历史快照仍保存在此前 Git bundle 和聊天 work/gregtech6-identity-build-20261002；后续代码对齐应依据当前源树逐项核实，不假定旧运行证据覆盖新树。

## 2026-10-02 / CI 修复与 0.0.0 双版本产物

改名影响材料来源显示名称，从而使包含该字段的旧完整快照哈希失效。已通过仅恢复旧名称的临时探针核对原始两项哈希，更新改名后基准，保留所有材料字段和断言。Forge CI 任务限定为 `:build`；补回当前 Forge 模具代码引用但缺失的共享规则类。用户要求根版本设为 `0.0.0`。

用户推送的 dbd38be9 已在 GitHub Actions 运行 36903728760 全部通过（4m 43s）。本地双平台构建通过（11m 17s），两最终 JAR 的 89 个共享核心 class、两平台元数据及无重复/测试污染打包检查通过，复制产物校验值一致。交付两个 JAR、双语 Release 说明、校验值与打包记录。详细证据：verification/ci-material-rename-20261002.md。本批未运行游戏，完整玩法、世界重载、旧存档及完整双版本对齐仍未完成。

## 2026-10-02 / 恢复遗漏的后续移植源码

用户指出此前 NeoForge 完整移植产物约 35.9 MB，而上述 5.8 MB 产物仅包含材料系统。已确认当前重新初始化源码树缺少后续适配，并按用户要求从保留的 84be9ccb2e 快照恢复 src/core/neoforge 及配套资源、构建配置、来源记录；保留当前名称、ID、0.0.0、双语 README 和用户文档。恢复后有 Forge 1,117、core 351、NeoForge 941 个 Java 源文件。原历史保留在 recovery/complete-main 本地引用，来源目录未修改。

同步后来修复过的贴图文件名小写规则所对应的材料快照基准；差异探针证明名称与贴图路径大小写之外的原始材料观察字段一致，断言均保留。纯 Java 合约去掉不使用的大型资源 classpath，打包新增按平台选择的关键玩法类门禁。

最终本地构建通过（8m 12s），全部 571 个当前编译核心 class 的双版一致性与关键玩法类、元数据、无重复/测试内容打包检查通过。新 NeoForge JAR 为 35,890,474 字节，含 1,955 class / 73,730 assets / 228 data；旧完整包的全部 1,954 个 class 路径均已恢复。Forge 新 JAR 为 38,527,588 字节。聊天 release-0.0.0 交付目录中的旧产物已替换，校验值及双语说明更新。详细记录：verification/full-source-restoration-20261002.md。

用户报告运行 36909053404 的旧提交 3f0fad2 材料快照失败；本地 92fb199fd 修复该基准，随后的按平台验包类名修复也需推送最新提交。不得把更早的材料预览树 CI 成功当作恢复后源码的验证。此批未运行客户端、服务器、完整玩法或世界重载，整体 goal 保持未完成。

## 2026-10-02 / 恢复后的熔炼运行与存档推进

两平台同步修复叠放模具余料清空/温度判定、盆缺失块输出清空、龙头负高度查找及交叉流道异常锁释放。NeoForge 实际煤炭供热铜锡青铜链及叠放盆九次精确取出通过；普通专服两个独立 JVM 的同一世界重启检查保留铜模具形状/材料/1U 内容及青铜盆 8U 余料。集中双版编译和最后双 JAR 构建通过，571 个共享 class 与平台打包检查通过。来源哈希、完整结果和未验边界见 verification/smeltery-parity-20261002.md / .json 与 core/provenance/smeltery-parity-20261002.json。未完成生存获取、Forge 对应运行、当前客户端视觉、成品安装、全部机器和旧存档验收；goal 继续 active。

## 2026-10-02 / 基础机器库存与配方恢复

两平台六个生产文件同步修复库存待保存标记、物品搬运实际余量、完整流体附加数据与实际填充量记账；复用既有共享搬运引擎，覆盖取物覆盖物和压力阀。NeoForge 普通专服两个独立 JVM 对同一世界运行，读出并完成粉碎机原已消耗输入/64 工作量的作业，保留搅拌机命名铜锭和带 components 的水，并拒绝不同 components 的混合/指定排出。设备、输入、KU 由检查提供，处理 tick 直接调用，不作完整生存/发电链声明。两版构建 4m 3s 和 571 共享类验包通过；覆盖物实际搬运、Forge 运行、当前客户端及旧存档仍待验。记录：verification/machine-io-parity-20261002.md / .json 与 core/provenance/machine-io-parity-20261002.json。Goal active。

## 2026-10-02 / 共享引擎面与实际蒸汽供能

两平台 EngineBaseBlockEntity 委托新的共享 EngineFaceRotation，保持既有能力面约定并修复水平左右/竖直排水的逆映射。Neo 普通专服给定设备/煤炭/蒸馏水，以零热量、零 KU 冷启动，通过真实右键点火、强化锅炉及自动补水/钢管输汽/强化活塞，完成已注册粉碎配方并自动输出到箱子；竖直活塞 200mB 蒸汽回收 1mB 冷凝水。prepare 使用原生 tick sprint 执行 12000 个真实世界 tick，未注能量或手动机器 tick；第二独立 JVM 同一世界读出结果和冷凝水，再运行 200 普通 tick 并保存退出。两版构建与 572 共享类验包通过。完整生存、设备制作入口、Forge 运行、当前客户端、成品安装、完整状态精确快照及旧存档仍未完成。失败准备反馈也保留于 verification/engine-steam-parity-20261002.md / .json；goal active。

## 2026-10-02 / 设备制作配方共享与 Native 入口

234 条熔炼、能源、轴向、磁体、电池、光学与 ZPM 原配方原字节迁至 core；Forge 原路径及 NeoForge 原生数据包消费同源。一次 Neo 普通专服全部条目/原料闭合检查、选定锅炉/燃烧箱/变压器/坩埚实际匹配、工具损耗、镜像规则及序列化通过，保存退出。两版最终构建、573 共享 class 及全部 234 资源 SHA 验包通过。没有把 RecipeManager 查询当作玩家炉子过程、全部制作或完整生存；普通活塞引擎制作入口、Forge 运行/当前客户端/成品安装/旧存档继续待验。见 verification/equipment-crafting-parity-20261002.md / .json。Goal active。

## 2026-10-02 / 部件与物流制作入口

185 条原部件、物流、覆盖物、木管和多方块配方共享；现有原生数据包加载共 419 设备条目。Neo 普通专服所有设备配方/原料候选闭合、实际空板→过滤器→物品过滤设备以及木管/电机/传送带制作查询和工具损耗通过；运行 200 tick 正常保存退出。573 共享类/本批 185 资源双版 JAR 验包通过。完整生存、覆盖物安装/实际路由、Forge 运行/客户端/成品/旧存档仍待验，见 verification/routing-crafting-parity-20261002.md / .json。Goal active。

## 2026-10-02 / 线材与模具制造入口

1,316 线材加工及 78 模具原配方共享，Neo 原生设备/制造目录累计 1,813 条，实际条目/原料候选闭合。全部线材 matches/assemble 比较导体原材质与数量守恒；双碳化钨板→空白→杆→线模具查询、原工具损耗/前模具消耗及选定杆非镜像/单图样唯一性通过。单次普通专服 200 tick 正常保存停止，最终两版 573 共享类和本批 1,394 资源 SHA 验包通过。玩家界面、全部模具制作/方向、电线实际运行、完整生存、Forge/客户端/成品/旧档仍待验。见 verification/manufacturing-crafting-parity-20261002.md / .json；goal active。

## 2026-10-02 / 剩余静态配方及原料标签

剩余 333 原 JSON 及七原标签共享，设备/制造目录现有 2,146 原静态配方均接 Native 原生数据包，另有动态/机器配方目录，不声明全部玩法完成。首轮实际大麦捆不匹配，补原四谷物标签；将原 Ingredient.isEmpty 弱检查改为 Ingredient.EMPTY 身份区分空格，当前全部 2,146 条非空产物/非空格原料候选检查通过。选择电路/USB/书架/脚手架/大麦往返/四锯斧工具半砖/陶碗烧制查询及短专服正常保存停止通过；两版 573 共享类、本批 333+7 资源验包通过。旧回执 resolvedIngredients 标志不能独立证明旧树空标签闭合。完整生存、普通活塞制作、USB/路由、Forge/当前客户端/成品/旧档待验；见 verification/survival-crafting-parity-20261002.md / .json。Goal active。

## 2026-10-02 / 客户端共享模型加载

两版补缺失库存引用并复用原模板缓存，缺失材料状态由同一原模板补齐，旧 items 图集、两单帧动画和树洞/分类图标/Blue Mahoe 路径同步。Native 57,462 加载失败降为零，56,036 材料/925 流体最终模型非 sentinel，六实际物品绘制及主菜单截图通过；Forge 当前开发主菜单通过。初轮接口编译、检查齿轮/水物品 ID 错误及 Forge 首次辅助页面超时均保留为失败。木辞典三种种类艺术、完整客户端世界/存档/成品运行仍待验，无启动性能承诺。573 共享 class/双包验证通过；见 verification/client-model-parity-20261002.md / .json，完整 goal active。

## 2026-10-02 / Native 客户端真实机器界面与世界重载

Neo 当前开发客户端对同一隔离世界的两个独立 JVM，真实右键/shift-click 命名输入、原命名铜锭/水、实际流体更新及正常保存重载通过，六截图实际查看。发现原搅拌机标题盖输入槽，两版同步移至面板上方，Native verify 画面通过。两个 probe 竞态/退出错误保留失败；原专服世界 SHA 未变。最终双包与 573 共享类/当前 GUI class 核对通过。给定停机设备和补水，不声明完整生存/客户端动力制作、Forge 客户端世界、成品安装或旧存档完成。详见 verification/client-world-parity-20261002.md / .json；goal active。

## 2026-10-02 / 普通与强化蒸汽活塞制作入口

补两版原来缺失的 28 蒸汽活塞制作配方，取原始 GT6 注册行图样/材料并复用共享静态目录和 Native 原生数据包，原 ANY.Steel/W 的十种形态标签同源。两平台真实 RecipeManager 全部图样/工具损耗/前缀区分通过；各版本普通专服两个独立 JVM 保存并重载实际制作查询的青铜普通/强化产物，再运行 200 tick 正常保存停止。2174 共享静态条目、17 原料标签，573 共享 class 和本批 28+10 资源双包核对通过。方法制作不等于玩家工作台/生存取得；电力/通量/柴油入口、对应动力运行、成品/旧档待验，见 verification/steam-engine-crafting-20261002.md / .json。Goal active。

## 2026-10-02 / 电力与通量活塞制作入口

补现有五电力+五通量入口为共享 JSON；通量消耗原注册号 10011..10015 的同级电力活塞，而非电动机。十条 Native 实际配方、候选、网络往返、全档电力制作产物→通量、线宽/退火铜/三重板/磁性长杆/级别与工具损耗检查通过，普通专服 200 tick 正常保存退出。两包与 573 共享 class 和十资源 SHA 核对通过，静态目录 2184。未声称新十行 Forge 运行、物理供电或生存取得，见 verification/electric-flux-crafting-20261002.md/.json；goal active。

## 2026-10-02 / 柴油引擎制作与工业润滑容器

八柴油原图样共享，四ANY钢形态标签补齐。两版原有限容器原料增加默认关闭的250工业瓶替代，柴油开启，原1000灌瓶仍隔离；双版真实八配方/容器返还/网络往返/非镜像/早期油拒绝通过，Native额外检查LubRoCant、999mB/空/显示拒绝。两普通专服各200tick正常保存退出，2192共享静态条目、573core类与8+4资源双包核对通过。原柴油RU与当前移植KU偏差未解决，供能/玩家制作/柴油产物重载待验，见 verification/diesel-crafting-20261002.md/.json；goal active。

## 2026-10-02 / 柴油原RU、燃料完整记账与背面排气

两版柴油修正输出RU/完整配方能量/一包每tick原浪费语义/背面排气，复用共享LiquidFuelCycle。Neo修复前真实1mB柴油只留32、KU链不能供RU旋转活塞；保存旧世界后，新独立JVM原数值读入再由柴油RU→旋转KU完成真实粉碎，完整512能量及背面1mBCO2铜鼓通过；第三独立JVM读取原余量/产物/排气后200tick正常保存。当前字段数值保留，旧直接KU布局需加旋转活塞，不称通用旧档迁移。两包574core类与当前柴油代码通过；Forge动力、客户端和全生存待验，见verification/diesel-power-parity-20261002.md/.json。Goal active。

## 2026-10-02 / Forge 柴油真实动力与双版额定输出



Forge 1.20.1 新隔离世界给定实际钢柴油机 100mB、青铜旋转活塞、青铜粉碎机一块注册钻石碎片，产物自动进入真实下方箱子。两个另置青铜柴油机各一 mB，观察真实单次燃烧 512 能量，并确认其中一台把 1mB CO2 自动排到后方青铜鼓。没有有效外部 HU/RU/KU 注能、手动机器 tick 或 tick sprint。200 普通世界 tick 后停止供新燃料及加工，正常保存退出。

第二个 Forge JVM 不供应任何燃料或新产物，先比较前一进程保存的三台引擎能量、燃料、排气和 stopped 全部精确数值，再确认箱中产物及鼓中 1mB CO2。三个实际引擎检查 RU 尺寸范围、KU 范围为零和拒绝外部 KU/RU 注能，继续 200 普通 tick 并正常保存退出。停止开关不保留残余功率，其随原每 tick 一包语义自然消耗，不误称全部状态不变。

Neo 1.21.1 对前批同一真实隔离柴油世界再次独立 JVM 重载，读原保存值、箱中产物和鼓中排气，执行新增精确额定范围检查，200 普通 tick 正常保存退出；没有补燃料或替换原状态。此前修复前 KU/32 与修复后 RU/512 的实际差分证据保留在 diesel-power-parity-20261002.md。

- forge_prepare：2m 24s，PID 75524，实际退出 0，200 普通 tick，正常保存停止。
- forge_reload：2m 42s，PID 13356，实际退出 0，200 普通 tick，正常保存停止。
- neo_rate_reload：1m 57s，PID 81096，实际退出 0，200 普通 tick，正常保存停止。

双版集中编译 29s，最终双包 3m 13s，574 共享 class 精确一致和生产柴油固定尺寸 class 验包通过。

- Physical Forge chain uses supplied registered machines, 100mB Diesel and one chipped-diamond input; no full survival acquisition or actual crafting UI.
- Selected steel/bronze horizontal machines prove this layout only; not all fuels/tier/orientations/activity animations/overvoltage.
- Selected Forge current-source world is saved/reloaded, not the earlier pre-RU Forge layout, original GT6 or cross-Minecraft/source save import.
- Client powered-world/GUI, installed production-JAR launch, Forge thermal steam chain and complete donor integration remain pending.

复现：Java17 Gradle，Neo 使用现有 Java21 工具链；Forge 新 flat/offline/loopback 隔离目录和既有获用户同意的 EULA 副本。`-PdirectCoreResources=true -PdirectCoreClasspath=true -PdieselPowerSmoke=true -PserverSmokePhase=prepare|verify -PserverSmokeId=<同UUID> -PserverDirectory=build/<新隔离目录> -PserverSmokeX=0 -PserverSmokeY=240 -PserverSmokeZ=0 :runServer`。Neo 同前批世界用 `verify` 加 `-PdieselPowerReadOnly=true :neoforge:runServer`。正式双包不加 directCoreClasspath。第三方许可未改，完整 goal active。

## 2026-10-02 / Forge 普通冷启动蒸汽动力与精确状态重载



准备进程在停止前记录11个实际block entity的完整持久化NBT：燃烧箱、锅炉、蒸汽管、强活塞、粉碎机、输出箱、两水管、自动供水鼓、竖直活塞、冷凝水鼓。正常关闭保存真实region。独立第二JVM从同一真实世界加载，先逐项对比block身份和完整NBT语义（TagParser/CompoundTag.equals），没有直接调用load或补造状态；验证原箱中产物与冷凝水后再运行200普通tick，正常保存退出。该证据覆盖持久化的热量/冷却/效率/压力库存、燃料灰、缓冲和管内容等，未保存的动画计时不扩大声明。

- prepare：6m 50s，PID 69008，5559普通tick，实际退出0、正常保存停止。
- verify：2m 40s，PID 79680，200普通tick，实际退出0、正常保存停止。

检查入口编译19s；双包仍为生产构建`4a8f7b246f54b5e430b8070fba7ce0ff16f166e3`，574共享class。

- Given machines, 64 coal, 4000mB boiler distilled water plus 50000mB supply and registered chipped-diamond feed; not full survival acquisition/tool crafting.
- Selected dense-bronze box/strong bronze boiler/steel pipes/strong bronze engine/bronze crusher and vertical bronze condensate path only.
- Actual exact persisted NBT before first reload tick covers selected heat/cooldown/efficiency/tanks/engine buffer and pressure state/fuel/ash/pipe inventory/temperature/transfer/sides/tank automation/output; volatile unsaved animation clocks are not claimed.
- Current local Forge world; no original GT6, other-source or cross-Minecraft save import. After reload normal machines continue changing state.
- No current Forge client powered-world or installed-JAR launch; full integration remains active. Existing Neo steam evidence retains its earlier snapshot/sprint scope.

复现：Java17 Gradle，显式同UUID和新的flat/offline/loopback隔离目录，既有获同意EULA副本。`-PdirectCoreResources=true -PdirectCoreClasspath=true -PsteamChainSmoke=true -PserverSmokePhase=prepare|verify -PserverSmokeId=<同UUID> -PserverDirectory=build/<新隔离目录> -PserverSmokeX=0 -PserverSmokeY=240 -PserverSmokeZ=0 :runServer`。prepare最多12000普通tick/660s，实际产物出箱后且至少200tick即停；verify固定200tick。第三方许可未改，完整goal active。

## 2026-10-02 / Neo 实际早期工作台与铜锡采矿

NeoForge 1.21.1 在生存模式服务器 FakePlayer 下实际右键拾取三个燧石石块和树枝，用所得原料填入原版 CraftingMenu，点击真正的结果槽得到 Flint 镐头/Wood 手柄的 GT 镐，九个输入槽全部消耗。随后用该成品经过 ServerPlayerGameMode.destroyBlock 采掉三个普通铜矿、一个普通锡矿，获得实际矿块生成的 ItemEntity：3 铜原矿、1 锡原矿；镐的损耗为300/4800，仍可用。

实际磨损镐和原矿置于箱子2/3/4槽，正常运行200tick并保存停止。独立第二JVM读同一真实世界，在任何tick前逐槽比较实际保存的完整ItemStack SNBT语义，继续200普通tick再比较并正常保存停止。verify没有重新采矿、合成、直接load或补造物品。工具属性、头/柄、损耗和两种原矿数量均保留。

复用已有 NeoForgeDedicatedSmoke，增加默认关闭的 earlyToolChainSmoke。生产代码与资源未变，不修改矿物等级或工具平衡来使检查通过；现有双JAR仍是4a8f7b246构建，实际SHA一致。本批只进行该流程和一次重载，不重复完整构建/客户端检查。

- prepare：1m 54s，PID 77032，200普通tick，实际退出0、正常保存停止。
- verify：1m 52s，PID 78896，200普通tick，实际退出0、正常保存停止。

检查入口最终编译20s。首次检查代码误用MaterialPrefix.ore，编译失败38s；改为BlockMaterialPrefix.ore后通过，失败日志保留，不计作模组功能故障。

## 范围与后续

- Standing flint rocks, twigs, crafting table, supports and normal copper/tin ore are placed by the opt-in checkpoint. Natural generation/discovery and survival workbench acquisition are not proved.
- A server FakePlayer in survival performs actual right-click collection, real CraftingMenu result-slot click and ServerPlayerGameMode.destroyBlock. No real client GUI or wall-clock mining delay is claimed.
- Actual ore ItemEntity drops are transferred to the actor inventory by the checkpoint; walking-based native client pickup is not proved.
- Exact saved chest ItemStack SNBT components are compared semantically using TagParser before any reload ticks and again at tick 200; no synthetic item load or stock repair. Only these selected three chest slots are claimed.
- Selected NeoForge Flint/Wood pick and four normal Cu/Tin ores; no all-tool/all-material/fortune/Forge counterpart runtime coverage this batch.
- Smelting these actual raw ores into bronze, bronze head casting/assembly, natural world survival, powered clients, installed JAR runtime and complete three-source integration remain pending.

复现：Java17启动Gradle、Neo使用已有Java21工具链，新的flat/offline/loopback隔离目录及既有获同意EULA副本。`-PdirectCoreResources=true -PdirectCoreClasspath=true -PearlyToolChainSmoke=true -PserverSmokePhase=prepare|verify -PserverSmokeId=<同UUID> -PserverDirectory=build/<新隔离目录> -PserverSmokeX=0 -PserverSmokeY=240 -PserverSmokeZ=0 :neoforge:runServer`。完整goal保持active，来源和许可不变。
