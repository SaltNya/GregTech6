# P3 物理线缆、红石信号与关联配方

2026-10-01：saltnya 原 30 个电线系列共享 WireCatalog，保留 1..16 裸线和 1/2/4/8/12 绝缘线规格，共 620 个实际方块及物品。Forge 原 WireDefinitions/GTWires 使用共享表和堆叠上限，Neo 注册一次独立原生 DeferredRegister 并保持 gregtech 路径。红石信号线另有共享 SignalWireCatalog 的 redalloy/signalum/lumium 三系列裸线/绝缘线，共 6 个实际方块；不向其提供 EU 传输。

WirePacketRules 共享有符号电压线损、工作包可转移条件及饱和电量/电流计数。两平台实际 ElectricWireBlockEntity 调用相同规则，Minecraft 世界邻接遍历留在平台边界。保留递归传输、已访问节点检查、模拟仅报告本地接纳、GT6 过载包消耗与16次烧毁行为、区块卸载清理。并未宣称接线无损。红石原实现按整型分数衰减、每 tick 求解已加载连通组件，从外部源重建以防断开环路锁存；未引入永久缓存或强制加载区块。

Neo 电线使用原动态 PipeWireBakedModel、粗细接头、绝缘外皮环、物理碰撞、水浸和原材料色。信号线保留光度、brown insulation tint 与螺丝刀模式代码。剪线钳使用原3×3面选择与双向连接校正、权限和邻块检查；完整手动/电动工具、操作覆盖层、工具制作仍待整合。本批不伪造工具使链条看似完成。

原完整 WireProcessingRecipes 与 GrapheneNanofabricationRecipes 已在 Neo 接线，使用实际 wire_01_graphene 和六种信号线工厂。保留原线材拉丝、确定性拆分、织机组合、橡胶板/箔覆膜和45条石墨烯参数/严格缺失及冲突检查。按已迁入 phase C 相对次序置于 electronics→wire→polymer→graphene，其余工业入口和生成表仍在后方。线材/石墨烯原参数没有换用占位内容。电池制作仍需要完整工具注册，因此尚未启用；能源转换器、发电机、电池盒和旋转传输仍待整合。

来源及资源闭包 SHA 见 electric-wire-source-integration.json（1285引用）及 signal-wire-recipes-source-integration.json（20引用）。模型/纹理按原字节保留，已有共享纹理只引用一次，新增绝缘纹理搬至 core，来源项目不修改。公开分发授权问题仍保持原状态。

集中 :neoforge:compileJava :compileJava 首轮36秒通过，core/Neo/Forge Java均成功，回执 verification/p3-wires-compile.json。后续隔离 Neo 专服加载小检查已通过，详见下方回执；没有客户端、实际线路过载/信号行为、机器加工、存档重新加载或旧存档验证，没有新 jar 验包。


后续集中短启动（2026-10-01）：Neo 普通 DedicatedServer 配方/标签/掉落数据包加载、200 tick、正常保存退出通过，耗时4分37秒。工业源入口加载含5661弹药/2709焊接/444高压釜/1796破碎/8激光/5电池填充行；新线材和石墨烯入口未抛缺失或冲突异常。回执 verification/p3-neoforge-wires-startup.json。Yggdrasil公钥获取超时为隔离offline启动的非阻塞网络异常，未使游戏失败。没有客户端、真实线路/充放电/机器加工、独立进程世界重载或旧存档通过结论，也没有新 jar 验包。
