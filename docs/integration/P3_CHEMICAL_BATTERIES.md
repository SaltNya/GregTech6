# P3 化学电池、掉落与采掘批次

2026-10-01：本批接入 saltnya 的 25 个化学电池与 5 个保留放置 ID，配合上一批 5 个简易电池共有 35 个实际电池物品。保留原命名空间、规格、包计量、潜行放置、掉落/拾取电量、被动方块与电量显示代码；被动电池没有擅自添加能源网络发射行为。来源与 183 份资源引用 SHA 见 core/provenance/chemical-battery-source-integration.json，第三方许可和作者记录保持原样。

NeoForge 使用 CUSTOM_DATA 保存 gt.charge，充电时 MAX_STACK_SIZE 组件设为 1，空电池为 16；方块实体按 HolderLookup API 保存/加载与同步。原 cuboid UV、光照、化学色和电量模型属性接客户端绑定，客户端类仅在 Dist.CLIENT 加载。原 ULV..EV rechargeable_batteries 标签全部必需成员现已实际注册，未改 optional。充电器、电池盒、FE 物品桥接及完整工具仍待整合，原制作配方依赖实际线缆/工具工厂，尚未启用。

原通用掉落包接入 Neo 单数 loot_table 和 tags/block 目录。采掘工具和等级依据实际已迁入的方块类型及原木命名规则；尚未迁入的书架、草捆、信号线等工厂仍需随工厂补全对应判断。共享 BlockHarvestNames 只包含命名/标签领域规则，平台 BlockHarvestPolicy 保留 Minecraft 类型判断。StatefulBlockLoot 共享状态属性契约，Forge 原 SpikeBlock 的 mode/secondary 拷贝掉落规则不变；原自定义 NBT 掉落继续由方块执行。此实现尚无游戏内掉落/采掘行为证据。

累计工业配方、简易电池、化学电池/掉落三批后集中执行 :neoforge:compileJava :compileJava。首轮 27 秒失败于两个 Neo API 适配错误；修复 clone 的 LevelReader 签名与焊接配方 logger 后，第二轮 27 秒成功，core/Neo/Forge Java 均通过。回执 verification/p3-industrial-batteries-compile.json 保留两轮日志 SHA。只有编译检查，没有新游戏启动、客户端电量显示、充放电/simulate、完整生存流程、世界重新加载或旧存档验证，也没有新模组 jar 验包。前一批的专服成功不能代表本批运行成功。


后续集中短启动（2026-10-01）：Neo 普通 DedicatedServer 配方/标签/掉落数据包加载、200 tick、正常保存退出通过，耗时4分37秒。工业源入口加载含5661弹药/2709焊接/444高压釜/1796破碎/8激光/5电池填充行；新线材和石墨烯入口未抛缺失或冲突异常。回执 verification/p3-neoforge-wires-startup.json。Yggdrasil公钥获取超时为隔离offline启动的非阻塞网络异常，未使游戏失败。没有客户端、真实线路/充放电/机器加工、独立进程世界重载或旧存档通过结论，也没有新 jar 验包。
