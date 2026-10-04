# 验证账本

## 2026-10-04 / Nexus、道路、曲柄与正式双版

真实普通新世界：两版9群系/26设施、144箱格中96实际物品/26原版或外部空项/22待移植，曲柄30查询、火石刀真实火焰附加I、铁钢反应4项、66内容页/13齿轮箱库存模型、沥青808080/曲柄c8c8c8；规范输出75,871/75,948、配方42,610/42,726。Forge30世界帧，Neo3,729并等EMI；截图查看。

正式双版7m51s、665当前core字节与CRC/refmap/元数据/测试污染排除通过。实际安装Loader的独立Java25成品主菜单181/179帧、退出0、截图查看；258017df/ece6a94f成品备份后装入测试实例，仅改GT JAR。失败和验收边界见[本批结果](verification/origin-priority-20261004.md)。没有完整Nexus/旧存档/全生存验收声明，goal保持active。

## 2026-10-04 / 电池迁移与正式成品启动

两端普通世界实际各5旧ID别名/10原生栈读写/25来源标签/20钢工具行通过；Neo最终151,730ms/3,868帧、EMI36,180ms完成，Forge176,982ms/30帧。首次Neo提前退出引发EMI空指针及第二轮脚本已解析旧条件拒绝Forge无EMI，均保留失败边界，不重复成功客户端。初始10m45s打包暴露生产映射缺失，不当最终交付。Forge完整编译19s/最终双版探针4m37s，655共享class、Forge11/Neo8个原生类、完整refmap和全ZIP CRC通过。见 [电池验包与运行](verification/battery-cleanup-20261004.md)。

最终正式Forge47.4.26/Neo21.1.252与Java25.0.2均实际到主菜单，178/181帧、78,285/60,894ms、退出0，两张1280×720截图已查看。测试启动器编码、重复依赖和探针资源元数据警告页失败明确排除；旧安装Forge缺映射/Neo非法ZIP均被新版验包拒绝。完整复制的两版再次CRC/哈希通过后原子发布，[报告与稳定路径](verification/production-delivery-startup-20261004.md)。最终脚本只做语法和独立阶段实跑，未重复整段入口；未原地改变实例，未执行生产世界/旧存档/完整机器链。

## 2026-10-04 / 构建前实际新建世界

Neo实际创建世界131,850ms/Gradle3m07s成功，Forge最终184,720ms/Gradle4m成功；两端各30游戏画面帧、实际玩家和集成服务器、原生注册配方超过43,000，分别遍历75,945/75,868物品规范化。1280×720截图实际查看，包含HUD、roads和有文字的路牌。首次Forge360s超时停在失焦PauseScreen，尽管Gradle退出0也明确不计通过；关闭隔离实例失焦暂停后只重跑Forge。正式双版及最终Neo夹具编译9m15s、655共享类、每端两个原生类、metadata/NOTICE/夹具排除验包通过。没有重复共享全套或已通过Neo客户端，新增PowerShell交付脚本仅做语法检查；本批直接运行相同入口并核对回执后构建。[运行版本、报告与边界](verification/world-creation-fixes-20261004.md)明确未复测用户实例、成品安装、旧存档或完整机器链路。

## 2026-10-04 / 太阳能输出集中检查

64项固定来源样例独立通过；双端40模型、48状态、15纹理及既有语言值不变检查通过。正式双版与测试夹具编译5m58s终态成功；655当前共享class、metadata/NOTICE和夹具排除、每端14变更原生class及当前太阳能资源验包通过。Forge重混淆后存在/哈希，Neo逐字节核对编译输出。没有完整共享套件、客户端、GameTest、太阳能网络或存档的新运行证据；继承结构检查仍待接续，见 [本批证据](verification/solar-output-20261004.md)。

## 2026-10-04 / 启动崩溃集中修复

正式双版 assemble/测试夹具编译7m14s成功；独立执行10项初始化回归通过，107个绑定前缀/4,387个模板缺失0。653当前共享class、metadata/NOTICE、测试夹具排除验包通过；Forge五个变更原生class重混淆后存在，Neo七个逐字节等于编译输出，模具类不再引用全局 Minecraft。没有重复全套共享检查。用户本机 Neo 完整故障链确认了模具图集未就绪→资源重试→初始化两次；本轮一次 Neo 主菜单105.7s/151帧成功并自动退出，结果及未运行范围见 [本批记录](verification/startup-fixes-20261004.md)。

## 2026-10-04 / 原版粉末监听器与清洗

快速双版编译27s通过；首次新增样例因超范围临时材料编号失败3s，修正后集中共享检查/正式双版50s成功，共10,108条断言。全图每阶段仅一条旧前缀重量修正，新增两个前缀/2,320形态，142,002条旧观察保留；前缀122。两版652当前共享类、Forge九个/NeoForge十一个变更原生类及两份语言资源验包通过。没有客户端、GameTest、清洗或真实标签/EMI重载新执行证据，见 [本批证据与边界](verification/dust-listeners-20261004.md)。

## 2026-10-04 / 外部熔炉与来源料理桥接

快速双版编译51s、最终正常classpath双版构建5m31s终态通过；一次共享10,037条断言通过，新增47项来源处理量/熔炼比例/经验/显示形态和七项完整材料样例。完整定义/post-init各保留139,681条旧观察，仅新增两个前缀和2,320条形态记录，前缀总数120。648个当前共享类及Forge十个/NeoForge八个变更原生类、metadata/NOTICE验包通过；已有熔炉 GameTest 夹具的错误平方比例同步修改，只参加编译，未执行。成品及未运行范围见 [本批记录](verification/external-thermal-20261004.md)。

外部 ingredient 的 DifferenceIngredient 收尾核对固定依赖源 test/Codec/网络行为；增量双版 assemble 50s通过，不重复共享检查。最终JAR重做648共享类及两平台全部变更原生类验包通过，依赖源哈希和收尾日志已记录；原生匹配/网络执行仍未验证。

## 2026-10-04 / 五种外部形态与余料数量

快速双版编译49s、正式双版构建2m06s终态通过；一次共享9,983条断言通过，新增102项固定来源重量/时间/产物/余料数量与自有物品边界、两项完整材料 MORTAR 样例。完整定义/post-init各保留133,876条旧观察，仅新增五个前缀及5,800条形态记录，类型前缀118个。646个当前共享类、每平台六个变更原生类及metadata/NOTICE验包通过，详见 [本批记录](verification/external-rest-20261004.md)。没有真实外部模组、原生研磨/空位/标签重载、客户端或存档的新实测。

## 2026-10-04 / 外部研磨分支与粉碎目标

快速双版编译37s、正式双版构建1m45s终态通过。一次共享9,879条断言通过，新增27项固定处理时间/产物/空位标记和四项完整材料 MORTAR/粉碎目标样例；完整材料图匹配前一批指纹，无新增前缀或物品。645个当前共享类、每平台四个变更原生类与metadata/NOTICE验包通过，详见 [本批记录](verification/external-grinding-20261004.md)。没有真实外部模组、原生空位执行、标签重载、客户端/机器或存档的新实测。

## 2026-10-04 / 可选外部矿物处理

一次共享检查9,848条断言通过，新增21项来源重量/时间/产物/机器/自有注册边界样例。快速双版编译1m1s、正式双版构建2m33s终态通过。完整定义与post-init各保留129,232条旧记录，只新增四个前缀及4,640条材料形态记录；据此更新指纹，类型前缀113个、自有物品定义流未增加。644个当前共享类、每平台七个变更原生类及metadata/NOTICE验包通过，详见 [本批记录](verification/external-ore-20261004.md)。没有真实外部模组、原生标签重载、客户端/机器或存档实测。

## 2026-10-04 / 材料别名与外部形态绑定

快速双版编译48s及正式共享检查/双版打包1m50s通过，共享行为2,094、机器34、材料7,646、温度53，合计9,827条断言；新增九项固定来源样例。完整材料指纹无需更新，仍有109个类型前缀。最终 NeoForge 标签重绑修正只增量双版 assemble，5m14s终态通过，没有重复共享检查。642个当前共享类、每平台两个变更原生类及成品 metadata/NOTICE 验包通过，详见 [本批记录](verification/prefix-aliases-20261004.md)。没有安装 Harder Ores 或运行客户端、原生标签重载、配方转移和存档实测。

## 2026-10-04 / #11–12 与统一材料转换

材料转换双版编译49s、issues双版编译58s通过。正式检查首次因新样例的完整目录初始化失败，修复后行为通过、旧材料指纹失败；隔离全图对比每阶段只有Gunpowder/Dynamite两条属性行不同、129,230条其余行相同，据此更新指纹。最终共享9,818条断言通过。正式双版打包5m51s终态成功，642个当前共享类与Forge13个/NeoForge20个变更原生类验包通过，详见 [本批证据](verification/issues11-12-20261004.md)。未运行客户端、Reliable EMI环境、真实重载耗时、原生瓶容器/爆炸场景或存档；不使用编译结果声称这些已通过。

## 2026-10-04 / 拆分格位与原始网格保存

快速双版编译 25s，通过；一次共享检查 9,810 条断言，通过。新增三十项原版格位固定样例，输出权限增加两项边界。脚本解析 456 个变更共享资源并逐字节同步缓存；1,272 条静态来源绑定复查 0 pending。正式双版打包 5m08s 终态成功，641 个当前共享类、每包 456 条配方、Forge 七个/NeoForge 十个原生类验包通过，详见 [本批记录](verification/form-conversions-20261004.md)；没有客户端、Mixin 执行、网络往返或存档证据。

## 2026-10-04 / 源转换权限与材料别名

快速双版 compileJava 29s；一次正式共享检查/双版 assemble 1m08s，9,778 条断言。十五项源边界样例覆盖统一别名、不同材料、占用格数、允许管道与禁止导线、不可变快照及同名不同身份。脚本按源数量/前缀/材料绑定 1,272 条静态数据，重新检查 0 pending；ALLOWED 初始化收尾仅双版 assemble 50s，未重复共享测试。

最终 640 个共享 class、每包 1,272 条改变资源、Forge 九个与 NeoForge 十个改变原生 class 及 metadata/NOTICE 验包通过；NeoForge 字节相同，Forge 仅声明重混淆后存在。没有客户端、网络往返、机器生存操作或存档证据。[详情与剩余转换缺口](verification/autocrafting-permissions-20261004.md)。

## 2026-10-04 / 自动合成与蓝图程序

局部参数重名导致首轮快速编译失败，修复后两版编译 22s 成功。一次正式共享检查与双版 assemble 5m 成功，共享 9,763 条断言；蓝图取得/扫描/打印原生收尾仅增量 assemble 55s，无重复共享测试。最终 637 个共享 class、Forge/NeoForge 各 38 个变更原生 class、两份语言资源及 metadata/NOTICE 验包通过；NeoForge 逐字节匹配，Forge 原生类仅声明重混淆后的存在。[记录与边界](verification/autocrafting-20261004.md)包含失败日志、来源和全局 NO_AUTO 缺口。没有实际原生配方注册、客户端、生存加工或存档运行证据。

## 2026-10-04 / 扫描仪能量与可选作物契约

第一次集中编译暴露替换分支的多余结束括号，已修正；第二次双版编译 14s 成功。一次共享检查及双版 assemble 56s 通过，共享 9,747 条断言；额外九项中性 ICropTile 契约样例检查首次/再次成本、扫描等级提升顺序及非公开实现类访问。最终 632 个当前共享 class、Forge 13 / NeoForge 11 个变更原生 class、两份语言资源及 metadata/NOTICE 验包通过。Forge 原生类仅声明重混淆后的存在，NeoForge 原生类与当前编译字节相同。详见 [验证记录与边界](verification/scanner-energy-20261004.md)。没有真实 IC2、客户端、生存充电链路或存档证据。

## 2026-10-04 / 黏土模具路线、形状保存与预览

422 条配方注册名/ResourceLocation 对照通过，完整 549 形状查表与中性化原版输出逐项相等。正式共享检查及双版 assemble 9m02s 通过，9,726 条断言；收尾原生改动增量 50s，空行格式清理只重编 core 7s，未重复共享检查。最终 623 个当前共享 class、422 个变更资源、Forge 15 / NeoForge 18 个变更原生 class 与 metadata/署名验包通过。详情与 39 个空生成形态、泥砖原料限制见 [本批记录](verification/clay-molds-20261004.md)。没有实际客户端、生存炉加工、放置拆除或存档重载证据。

## 2026-10-04 / Technology 配方与合成工具

双平台编译通过；正式共享检查及双版 assemble 9 分钟通过，9,726 条断言。完整材料图只有十行源文件对应变化；二十条新增工作台物品引用、七个材料族及二十四条电路原版等级对照通过。工具 ingredient 加载收紧后双版增量 51 秒，USB 替代接续 49 秒，无重复共享测试。最终 619 个当前共享 class、46 个变更 JSON、两版变更原生 class 和 metadata/NOTICE 验包通过，详情见 [本批记录](verification/technology-20261004.md)。这些证据不证明实际机器加工、客户端或存档重载。

## 2026-10-04 / 箭与装药弹壳

双平台快速编译 20 秒通过，正式共享检查及双版 assemble 9m32s 通过。材料图只有五个 EMPTY 形式变更，全部其他快照行不变；最后默认箭替换仅复跑受影响材料检查，当前合计 9,726 条断言。默认箭替换后增量打包 4m21s 通过；第一次验包拦截包内旧 NOTICE，已同步源资源与输出副本，只重打包 1m11s，不复跑测试；最终 614 个共享 class、两版各 29 个变更原生 class、13 个变更资源及当前署名验包通过。详细日志、固定样例和验包范围见 [本批记录](verification/ammunition-20261004.md)。客户端、成品射击、旧存档重载及特殊弹药附魔未验证。

## 2026-10-04 / Nexus、roads 与彩色建筑泡沫

双平台快速编译 30 秒通过。共享 9,703 条断言通过，其中 86 条新增源文件固定样例检查 Nexus、全部 16 个广场区块、三种道路模式、半砖、道路线及 512 格坐标路标。一次失败来自桥墩脚座颜色样例写错，已按原版浅灰色修正，失败没有计作成功。正式双版构建与平台增量修正日志、验包范围见 [本批记录](verification/origin-worldgen-20261004.md)及[成品回执](verification/origin-worldgen-artifacts-20261004.json)。

静态检查九个建筑模型的 tint 与贴图引用，源文件散列一致；不能据此宣称自然生成、原点出生、实际渲染或旧存档运行通过。按用户减少测试的要求没有启动客户端或 GameTest。

## 2026-10-04 / 原版设备与地形

244 个当前变更资产 JSON 解析及模型/贴图引用检查通过。第一次与第二次集中编译发现的 NeoForge 内部交互方法适配错误已修正；最终正式双版 assemble 及共享检查 9m11s 成功，9,617 条断言通过；600 个当前共享 class、平台元数据、重复条目和测试排除验包通过。已有 GameTest 夹具同步更新，只参加编译，未运行。详见 [本批来源与范围](verification/machines-source-20261004.md)及[验包回执](verification/machines-source-artifacts-20261004.json)。

## 2026-10-04 / 验证范围收缩

按用户明确要求减少测试，后续修复统一编译和验包，不再每个反馈都启动双平台服务器或客户端。共享检查保留一次；未运行的游戏回归不写为通过。水兼容与原版普通木材阶段的 `water-woods-native3.log` 两版各 11 项通过发生在该要求之前；本批 RGB、酒瓶箱、自然方块配方、地牢连接、非法图标注册、旋转泵和箱子修复仅使用后续构建证据。箱子延迟 tick 回归被主动取消，其 Gradle 非零退出是取消结果。详见 [本批记录与余项](verification/user-reports-20261004.md)。

正式双版 assemble 和轻量 core 检查 12m1s 通过，共享 9,587 条断言及 598 个当前共享 class 验包通过。成品见 [验包回执](verification/user-reports-artifacts-20261004.json)；该结果不替代新增修复的游戏实测。

## 2026-10-03 / 原版工具、无转子蒸汽链与 GitHub #7–10

最终生产提交 070d4077 的共享 8,139 条断言、Forge 22:23:40 / NeoForge 22:25:08 各 8 项实际世界 GameTest 通过。两版合成 81 条工具矩阵及 9,053 条材料目录样例，检查产物和工具磨损；由原生锅炉产蒸汽，经无转子涡轮/RU 发电机让电解机将六份产物送入箱中。测试外供热量和蒸馏水、手动 tick 机器，不宣称自然生存全链。四项 issue 的真实矿物配方、管道覆盖层合同、前面投入焦炭燃烧和压力拆除爆炸通过。

两版客户端默认状态扫描及 NeoForge 细线/工具分层检查通过；实际 EMI-only 22:10:20 正常保存退出，204,863 条机器配方和七类矿物处理输入/产出索引查询成功，截图已查看。末影紫水晶实际注册名修正在客户端之后，由最终合成及验包覆盖，未把早期客户端当作名称修正后的运行证据。正式双版构建与世界回归 4m18s；594 个当前共享 class、平台元数据和测试排除通过。全部日志哈希、来源、截图范围、失败修正与成品哈希见 [本批记录](verification/tools-power-issues-20261003.md)。

## 2026-10-03 / 重复提示、双层材质、光莲、灌木与蜂巢

最终共享 8,107 条断言及 Forge 18:32:50 / NeoForge 18:34:14 各 17 项世界回归通过。光莲使用真实物品水面射线放置并检查消耗、流动水拒绝和船碰撞；灌木检查真实六面放置、支撑继承、掉落、成熟生成、棉花采摘和剩余生长计数；蜂巢检查 16 个不带变种数据的不同物品及全部九槽的迁移保留。回归通过不扩大为独立旧世界重启。

Forge 18:46:52 / NeoForge 18:42:11 客户端正常截图退出；两版 tooltip 与植物模型检查通过，Neo 细导线、电动工具及手动工具所有被绘制层均通过不透明颜色检查。截图已实际查看。正式双版构建 4m32s 通过；589 个当前共享 class、元数据和测试排除检查见 [成品验包](verification/visual-plants-artifacts-20261003.json)。过程、失败重试及准确范围见 [本批记录](verification/visual-plants-20261003.md) 与 [运行回执](verification/visual-plants-runtime-20261003.json)。

## 2026-10-03 / 六项 Issues 与工具、EMI、液体泉

共享 8,107 条断言、Forge / NeoForge 各 56 项 GameTest 通过。NeoForge JEI 客户端实际检查 74 个真实/占位工具模型和泉库存模型；原生 JEI 分类工具槽合同通过。EMI-only 客户端在第二轮排序结束后查询 187,788 条机器配方及金属板产出、打开实际挤压机页面并检查同步的世界泉模型，正常保存退出；截图已查看。详见 [本批记录](verification/github-issues-20261003.md) 与 [运行回执](verification/github-issues-runtime-20261003.json)。成品验包和开发运行是分别记录的证据，不扩大为发布包安装启动或完整移植。

正式双版本构建 7m38s 与 589 个当前共享 class 验包通过；额外确认成品未捆绑 EMI 或本批测试夹具。见 [成品验包回执](verification/github-issues-artifacts-20261003.json)。

## 2026-10-02 / 超温起火与双版成品

共享 8,107 条断言通过，Forge / NeoForge 各 47 项游戏回归通过。正式双版构建 9m34s 成功；在当前 `C:\Dev\GregTech6` 下重新验包，587 个当前共享 class、元数据、许可、重复及测试条目检查通过，另确认两包都不含测试用保护标签。见 [验收记录](verification/fluid-pipe-overheat-20261002.md) 和 [验包回执](verification/fluid-pipe-overheat-artifacts-20261002.json)。不作为客户端、生存链路、独立世界重载或成品安装运行的证明。

## 2026-10-02 / 当前 C 盘快照：魔法流体管道危害

共享 7,821 条断言通过；Forge 18:24:06 / NeoForge 18:27:09 各 `All 39 required tests passed`，新增五项魔法分类、范围中毒、防护、残液损失和损毁回归，原 34 项全部通过，两服务器正常保存退出。合并测试 7m35s、正式双版构建 6m43s，均退出 0。双包 587 个当前共享 class、元数据、许可/NOTICE、无重复与测试专用条目校验通过；详见 [验收记录](verification/fluid-pipe-magic-20261002.md) 与 [验包回执](verification/fluid-pipe-magic-artifacts-20261002.json)。世界场景采用魔法液体；魔法气体数值有共享合同，未扩展为注册魔法气体实体行为或第三方污染兼容验收。不是客户端、生存、独立存档重载或成品安装运行证明。

## 2026-10-02 / 当前 C 盘快照：管材目录与旧容量迁移

共享 7,814 条断言通过，包括新增 1,430 条固定目录合同。Forge 18:02:38 / NeoForge 18:05:42 各 `All 34 required tests passed`，新增注册规格与容量加载/同步场景，既有 31 项回归全部通过，两服务器正常保存退出。测试任务 7m53s、正式双版构建 6m31s，均退出 0。双包 587 个当前共享 class、元数据、许可/NOTICE、无重复与测试条目检查通过；见 [验收记录](verification/fluid-pipe-catalog-20261002.md) 和 [验包回执](verification/fluid-pipe-catalog-artifacts-20261002.json)。目录验收限容量、四耐性、通道数及耐温参数；不包含魔法/过热行为、独立 JVM 存档重载或成品运行。

## 2026-10-02 / 当前 C 盘快照：流体管安全第一批

共享 6,384 条断言通过；Forge 17:43:05 / NeoForge 17:46:09 各 `All 31 required tests passed`，两服务器保存并正常退出。新增 7 项管道温度、复合危害、泄漏统计、腐蚀销毁和蒸汽活体伤害回归，原 24 项交互/分配场景全部通过。合并测试任务 7m41s，正式双平台构建 3m05s，均退出 0。双包 587 个当前共享 class、元数据、许可/NOTICE、无重复和测试专用条目校验通过；见 [验收记录](verification/fluid-pipe-safety-20261002.md) 与 [验包回执](verification/fluid-pipe-safety-artifacts-20261002.json)。这些开发服务端场景不证明材质目录已完全对齐、魔法/过热完整实现、客户端或成品安装运行。

## 2026-10-02 / 当前 C 盘快照：玩家流体容器

最终 `:core:check :runGameTestServer :neoforge:runGameTestServer` 成功（7m09s）：共享 6,370 条断言通过，Forge 17:12:49 / NeoForge 17:15:52 各 `All 24 required tests passed`，两服务器正常保存退出。9 项新增容器场景覆盖所用手的回写、点击面、过滤配置和双向过滤、整桶容量、堆叠、满背包实物掉落、创造模式标志、储液桶及倒桶回流；另回归 15 项管道场景。使用 3g 测试堆，修复了测试 API 差异、实体查询区域及复用世界的夹具污染；先前失败不计通过。正式双版完整构建通过（6m11s），585 个当前 core class、模组信息、许可/NOTICE、无重复及测试专用条目验包通过。完整过程与最终校验值见 [本批记录](verification/fluid-container-interaction-20261002.md) 和 [验包回执](verification/fluid-container-artifacts-20261002.json)。开发环境直接调用方块使用入口，不等于客户端网络交互或成品安装运行。

## 2026-10-02 / 当前 C 盘快照：流体分配第二批

最终共享 6,370 条断言通过；Forge 16:23:14、NeoForge 16:24:48 各 `All 15 required tests passed`，两测试服务器保存并正常关闭，任务退出 0（3m55s）。新增真实拆管回调、炼药锅各档消耗、源与多目标统一均值、二次压力、拒收机器排除、连接关闭及外部通道回流场景。正式 `:build :neoforge:build` 通过（3m59s），双包 585 个当前 core class 逐字节一致，元数据/NOTICE/许可、重复项和测试专用条目检查通过。最终 [验收记录](verification/fluid-pipe-distribution-20261002.md) 与 [验包回执](verification/fluid-pipe-distribution-artifacts-20261002.json) 已保存。不是客户端、独立 JVM 世界重载、完整生存或成品安装运行证明。

## 2026-10-02 / 当前 C 盘快照：多通道流体管

当前树双平台完整构建与 bootstrap 测试编译通过（32m46s），共享 core 四组合同 6,360 条断言通过；Forge 15:27:08、NeoForge 15:34:42 各有 `All 5 required tests passed`，两测试服务器正常保存关闭，合并运行任务退出 0（10m12s，含首次下载）。测试使用真实管道、给定流体和直接单 tick 调用，不计作玩家生存、独立 JVM 重载或成品安装验收。首次验包发现 NOTICE 副本未同步，修正后最终双包构建通过（7m53s），585 个当前共享 class、元数据、许可声明及无重复/测试条目验包通过。完整证据与最终产物记录见 [本批记录](verification/fluid-pipe-channels-20261002.md)。

日期采用 Asia/Shanghai；日志存放于本地忽略的 `work/`，阶段收官时将必要摘要及校验和纳入记录。

## 2026-09-30 / P0

- 读取三源：通过，均存在。
- 项目1复制：工具报告 78,768 个文件、53.04 MiB，失败 0；随后逐文件SHA-256与来源全部一致。
- Java 17：Oracle 17.0.4，实际用于项目1基线 Gradle 构建。
- Java 21：Microsoft OpenJDK 21.0.7；java 与 javac 实测可用，后续NeoForge实际构建与GameTest服务器使用该工具链。
- 项目1原始基线 `gradlew.bat --no-daemon --console=plain build`：通过，13m37s，13项任务执行。日志 `work/baseline-forge-build.log`。`src/test` 的 main 合约没有接入 Gradle test，本次不称其行为已通过。
- 基线 jar `gregtech-1.0.0.jar` SHA-256：`095a11129dc903c7ecf62d85661665bfd47469d1cbee13ecbd1aacc3333b7837`；保存在 `work/artifacts/saltnya-forge-baseline-1.0.0.jar`。这是本地测试基线，授权核查仍未解决。
- saltnya 78,768文件逐文件 SHA-256：全部一致，无缺失/变化。原始导入本地 commit `41561782`，标签 `import/saltnya-snapshot`；该提交不是恢复的原始作者历史。
- 客户端/专服启动、完整玩法、真实存档重载、旧存档兼容：未执行。

## 外部构建条件核对

- Forge 1.20.1 官方文档要求 64 位 Java 17，并建议测试专服：https://docs.minecraftforge.net/en/1.20.1/gettingstarted/
- NeoForge 1.21.1 官方文档要求 64 位 Java 21：https://docs.neoforged.net/docs/1.21.1/gettingstarted/
- 上述是环境要求证据，不是本项目的运行成功证据。

## P1 / 共享核心与平台构建

- 8个纯Java类原字节搬迁，保留包名/调用签名；独立Java17编译、64断言/7组、来源SHA和jdeps java.base检查通过。
- `:core:check :compileJava :neoforge:build`：通过，5m28s，13项任务（11执行/2已有输出）。coreBehaviorContracts真实输出64断言通过；Neo为启动骨架，不含玩法内容。
- 初始Neo jar：13,392字节。后续双jar构建与bootstrap编译通过；仍需严格验包后关联最终校验和。
- 独立审查发现验包和CI只查部分core/metadata的问题，工具已改为全core与当前编译字节/真实TOML/版本依赖门禁，49验包场景和9CI场景通过。CI在授权未决时只允许私有仓上传二进制；公开二进制分发未发生。
- Bootstrap测试属于游戏开发服务器初始化/core接线验证，不能代替正常专服、客户端、核心玩法、真实世界重启。
- 后续 `:core:check :build :neoforge:build :compileBootstrapGameTestJava :neoforge:compileBootstrapGameTestJava`：通过，8m18s，24任务（13执行/11已有输出）。两平台jar及独立bootstrap源码编译通过。
- Neo首次 `:neoforge:runGameTestServer`：在资源处理失败（20s），默认sourceSet资源目录被再次srcDir添加导致test_empty.nbt重复。去掉重复目录配置，保留FAIL门禁后重跑。
- Neo重跑：通过（3m51s），3项required GameTests成功，实际服务器初始化/core调用/正常退出已验证。日志 `work/p1-neoforge-bootstrap-runtime-retry1.log`，测试通过日志时间20:43:29；不作为正式专服或玩法验收。
- Forge首次 `:runGameTestServer`：资源下载阶段SocketTimeoutException，57项资源失败，游戏尚未启动。`prepare_assets.py`校验3575对象并从已验证Neo缓存复用缺失57项（0额外下载/0错误），不关闭TLS或哈希校验。日志 `work/p1-forge-asset-recovery.log`。
- Forge重跑：通过（3m），3项required GameTests成功；实际同步38813运行时配方，服务器正常保存测试世界并退出。日志 `work/p1-forge-bootstrap-runtime-retry1.log`。这不是同一存档重启或完整配方玩法证明。
- 严格验包初次失败：Forge的9个core class字节与当前core编译不同，Neo一致。独立classfile语义检查证实9类指令/描述符/属性值相同，仅常量池/属性顺序重排及两个未引用Long项删除。仍保持SHA门禁，改用`jar`平台中间件→`reobfJar`→`distributionJar`追加原core，复验进行中。详见P1_REVIEW.md。
- 两阶段Forge打包 `:distributionJar :core:check`：通过，4m19s。最终严格验包通过9个当前core类，两平台逐字节一致、真实TOML/依赖/版本一致、无重复或测试条目。Forge中间件无core；最终与中间件完整manifest字节相同（含MixinConfigs），mixin与refmap也相同。最终Forge 38,105,750字节/80,435 ZIP条目（Zip64），SHA-256 `11c2483c39686b1d3878338fc5ebabf1555aa111670f2054b8d245857ce48cec`；Neo 13,392字节，SHA-256 `c7a8f0d1fcf0012abf9af487df5970b5ede4010be37bf13cd31f485f40da2dba`。报告在work/p1-artifact-verification.json与p1-forge-distribution-boundary.json，只代表该P1快照。

## P1 / 开发客户端和普通专服

- 独立两平台客户端探针编译：通过，38s。源集不进入生产jar；默认关闭，显式参数才截图/退出。
- Neo `:neoforge:runClient -PclientSmoke=true`：通过，38s，主菜单真实绘制149帧，8034ms后原版后台写完截图并正常退出。1280×720 PNG SHA-256 `320fddd04b5e23310b9fc66f8381f841dabf939cf95f22aca9c03d31aeb3a8ed`；主会话实际查看图片，主菜单/文字/背景正常。严格日志/PNG结构/CRC/解码验收通过，日志work/p1-neoforge-client-smoke.log。未进世界，未验证Neo内容渲染或成品jar加载。
- Forge首次客户端：失败，120s探针超时；即使Gradle输出BUILD SUCCESSFUL/退出0，verify_client_smoke.py也正确拒绝。有实际资源atlas、配方和成就加载记录，未获得主菜单截图。不把加载日志当视觉通过。失败日志work/p1-forge-client-smoke.log；新增当前screen/overlay诊断和30–300s有界超时参数，以240s重试。
- Forge客户端240s上限重试：通过，Gradle2m11s，实际82566ms/152帧后保存1280×720截图并正常退出，未用满240s。主会话实际查看主菜单/文字/背景正常；严格机器验收通过。PNG SHA-256 `c97b7750d10cc1c5d8750a89dbc9410b662a3d00f2e2a66b952a0d9e13f37e46`，日志work/p1-forge-client-smoke-retry1.log；仍是开发源集环境，不是成品jar或模组世界内渲染证明。
- 客户端测试选项只写各自build/client-smoke-run/options.txt（跳过首次辅助功能介绍、静音），未改用户.minecraft选项。不是生产EULA接受。
- Neo普通开发DedicatedServer实际启动：版本1.21.1，Done(4.147s)，创建真实world，随后正常保存三维度并退出。日志work/p1-neoforge-dedicated-first-start.log（Gradle6m57s含人工检查窗口）。首次运行没有保留stdin，停止时用仅针对已核对PID及隔离工作目录的JDK attach请求server.halt(false)，服务器自行存盘退出；后续使用有限自动停服探针。未测试同一world重启或GT机器状态。
- Neo官方本机源证据：SharedConstants IS_RUNNING_IN_IDE为非production，Eula构造以IDE或GameTest条件短路。因此普通开发专服也无需readFile生成eula.txt；本会话未写eula=true，不能把这种开发启动当成生产专服EULA同意。生产成品加载、Forge普通专服、实际世界重启及完整玩法仍待验证。

## 原始历史匹配

- brokestar当前远程HEAD f009fc3c与用户快照不同（1123文件变化/1077缺失），没有错误关联为同一版本。通过来源PROJECT_STATE blob追溯，快照的220275文件全部字节吻合3118acbf83a84d05fa37d57af1705cf00e423ca9；gitlink单独记录ec524db7a5724f8cf3c837436b1ae742c778c62f。
- masson快照61192文件全部字节吻合2ba4e4b60f7a770360b2ec7ca2adad3507ec4a28。
- 对比结果保存在provenance/*history*match.json；对应完整原历史和作者信息在本地Git upstream-* refs及source/*标签中。上游remote不是新项目origin。


## 2026-10-02 / 双语 README 与 Community Edition 名称

用户明确指定新工作目录 F:\Dev\GregtTech6New\GregTech6，并要求英文主 README、可切换的中文版本，以及两版统一名称 GregTech 6 Community Edition。当前用户仓库分支为 main，源提交 f8d76b3b882c74c098b2ffbdddf910711a4fcb01。

已重写 README.md / README.zh-CN.md，包含介绍、目标版本、状态、双版本构建、开发运行、贡献、分项许可和署名。根 mod_name 和 Native 元数据共用根配置；新目录旧入口/事件订阅 ID 同步为 gregtech6，既有 gregtech: 注册、资源与保存身份保留；材料来源存在性查询同步。默认 GameTest 资源命名空间保持原样。BUILDING.md 同步品牌及当前目录名，未更改第三方许可或发布到远程。

一次资源处理 9m 22s 通过，实际生成的两份 TOML 显示名称均为 GregTech 6 Community Edition、modId 与 dependencies 所属 ID 均为 gregtech6；双向语言链接及 18 个本地文档链接检查通过。此批未编译 Java、未重打 JAR、未启动游戏，不能作为玩法/世界重载或完整整合完成证据。回执：verification/community-readme-branding-20261002.json。

原完整整合 goal 继续保留。新仓库由用户重新初始化，当前源树与此前 84be9ccb2e 上传快照存在差异，历史快照仍保存在此前 Git bundle 和聊天 work/gregtech6-identity-build-20261002；后续代码对齐应依据当前源树逐项核实，不假定旧运行证据覆盖新树。


## 2026-10-02 / NeoForge 成品专服

交付的 bc89c7201 生产 JAR 用官方安装的 NeoForge 21.1.243 和用户 Java21 独立加载，两个不同 JVM 正常保存/停服，铜原矿库存和青铜粉碎机实际保存身份读取通过。控制台放置不视作生存玩法，外部 Addon 未安装，Forge 成品和两版成品客户端仍待验。生产源码与二进制本批不变，不重复大资源构建。见 [验证回执](verification/installed-neoforge-20261002.md)。


## 2026-10-02 / 基础机器能源共享

共享整包需求、限容接收/累加、额定放电和不溢出的作业推进；停机拒绝实际/模拟输入，邻居拉取限制为实际需求，保留原注册/配方/NBT。两版编译与88项合同通过，Neo既有普通专服作业保存/独立进程继续加工通过；给定KU/手动machine tick不扩大为完整自然生存。交付JAR仍为bc89c7201，本批源码待下一次生产打包。见 [验证记录](verification/machine-energy-parity-20261002.md)。


## 2026-10-02 / 物品管道共享第一跳搜索

两版合法邻居共同执行一次加权搜索，保留第一侧等成本顺序；出口探测与拆管回送统一有效余量/实际送达合同，非正提取拒绝。32,768预算现按共同搜索计，未完成大网络/盖板/存档全范围运行。一次双版编译与102项合同通过，本批按少检查节奏未启动游戏/重打JAR；此前成品包和旧物流记录不视作新源码运行证据。见 [本批记录](verification/item-pipe-selection-20261002.md)。


## 2026-10-02 / 原矿显示对齐与 NeoForge 实际采矿铸锭

共享原矿 crushing payload 作为展示与实际输入依据，不采用 2U prefix 壳重量。NeoForge 实际工作台制镐、采矿、煤炭 HU、合金及四次浇铸通过；规范铜锭采用原版统一项，修正测试 ID 假设。给定设备、放置矿块，没有此世界独立重载或完整生存证明。详见 [本批记录](verification/raw-ore-playflow-20261002.md)。
