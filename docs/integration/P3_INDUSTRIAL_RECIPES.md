# P3 工业配方参数与加工入口批次

更新：2026-10-01。仅源码合并；遵循每几批集中小检查，当前批次尚未编译或启动。上一批 796c76ed8c 的 Neo 启动结果不覆盖本批新代码。

## 来源与实现

来源 saltnya 原 LaserEmitter/BatteryCell/GrapheneNanofabrication/PolymerForming/PressAmmunition/Autoclave/CrusherFamily/WelderFamily/Implosion 九份配方参数表。原时长、数量、选择器、材料前缀及生成顺序保留，迁至 core 的对应 RecipeRows；Forge 委托共享目录。原 List.of 表保持不可修改，数组型目录返回克隆避免跨平台调用方改写。焊接物质量计算亦随原 Row 一同共享。

VanillaRecoveryRecipes 的目标材料 BigInteger 比例、研磨工作量与粉末形态选择提取到 MaterialRecoveryRules，双方调用同一逻辑。保留原不足 1/72 U 不产出、可表示份额向下取整和单堆 64 上限；未冒充无损回收，原舍弃分量行为仍是待评估取舍。

Neo 原生接入 LaserEmitter/BatteryCell/Electronics/PolymerForming/PressAmmunition/Autoclave/CrusherFamily/WelderFamily/VanillaRecovery/VanillaBlockProcessing/TextileFinishing 共十一入口及 OriginalRecipeBatch。只薄适配原生注册表、FluidStack、组件相等性和 DeferredHolder；原缺失源项、空输入/输出、重复源行和碰撞的严格检查保留。Native Recipe/RecipeMap 不迁入 core，电子元件等手写原生构造公式后续继续抽取。

NeoMachineRecipeLoader 按原 Forge phase C 的相对顺序初始化当前已迁入子集，而非按复制文件先后加载。生成表继续在最后填补未注册配方；保留既有具体配方的优先级。来源 SHA、原许可/作者及目标文件见 core/provenance/industrial-recipe-source-integration.json。

## 缺口与下一批

石墨烯所有参数和 Forge 行为已保留，但 Neo 图形细线物理方块工厂尚无，因此没有启用该 native recipe loader；同样 Implosion 的原炸药方块未迁入，保留完整共享参数及 Forge 工厂，没有用其他物品假替代。完整燃料、融合、物质、USB、食物/木材/结构加载器仍待依赖迁移。

Neo 配方数据包里电池 tag 需要原真实充电物品注册；接下来迁入被动化学电池及兼容电池 ID，以接通现有机器制作材料。工具总线/充电器与电池盒仍须独立整合，不能因电池物品存在宣称能源网络完整可用。

本批未进行编译、客户端/专服启动、机器实际加工或世界重载。将在后续几批完成后集中做 Neo 优先的小检查，修正已接线源码的类型和初始化错误；整体目标 active。


后续验证（2026-10-01）：本批已包含在三批集中 core/Neo/Forge 编译成功范围中，27 秒；运行行为仍未验证。化学电池和掉落批次接线及缺口详见 P3_CHEMICAL_BATTERIES.md。


后续集中短启动（2026-10-01）：Neo 普通 DedicatedServer 配方/标签/掉落数据包加载、200 tick、正常保存退出通过，耗时4分37秒。工业源入口加载含5661弹药/2709焊接/444高压釜/1796破碎/8激光/5电池填充行；新线材和石墨烯入口未抛缺失或冲突异常。回执 verification/p3-neoforge-wires-startup.json。Yggdrasil公钥获取超时为隔离offline启动的非阻塞网络异常，未使游戏失败。没有客户端、真实线路/充放电/机器加工、独立进程世界重载或旧存档通过结论，也没有新 jar 验包。
