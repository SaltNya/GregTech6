# P3 原手工工具与制作接线

来源：saltnya 的实际 GTToolItem/GTToolHelper、四类动作、工具客户端、工具制作器、工具清单及坩埚固态取料。作者和授权原文保持；公开发布授权未决。逐文件原 SHA-256、工作基准哈希及166条资源引用见 core/provenance/native-manual-tools-source-integration.json、native-manual-tool-recipes-source-integration.json。

## 本轮接入

Neo 注册原37个 tool_* 实际工具物品，调用上一轮共享 ToolDefinition / ManualToolRecipeCatalog；没有为每个材料另建工具身份。凿子和钳子的原 SmelteryRegistries 持有者变为 GTToolItems 别名，两个工具仍使用同一原 id；不重复注册。

GT.ToolStats 的 head/handle 键进入原生 CUSTOM_DATA；MAX_DAMAGE/DAMAGE 与原生属性组件承载耐久、攻击伤害与速度，采用稳定 gregtech 修饰符 id。原材料采掘条件、机器拆卸速度、工具点击换算、方块/实体磨损和创造模式分支保留。NeoToolBindings 委托完整 GTToolHelper，原机器/电线/管道/轴/齿轮箱入口无需各建识别底层。

完整四类原动作：流体疏通、燧石点火及苦力怕引燃、建造杖、木工用具放置。流体疏通按六面使用原生方块流体 capability，先模拟、再支付工具损耗、再实际排出；原实现仅直接检查 BE 的 IFluidHandler，不适合 Neo 注册能力边界。原手工点火优先询问 Ignitable，原生砖燃烧箱实现该协议，之后才走 TNT/原版火。建造杖保留原固定 reach=4 和原顶面放置行为，未自改其原规则。

Neo 坩埚接原完整手工/铲子固态刮料、最轻固态选择、双手筛选、64次上限、余量/缺失 scrap 清理、缓存取回、主手优先发放、温度伤害与工具磨损。原字段温度映射至共享 thermal state，仍保存原材料/缓存键；同一共享 GT6 U 与 scrap 前缀单位，没有换一套物质量模型。

客户端接原分层工具模型、柄/头材质、宝石镐与头无柄图标、覆盖层和工具信息。客户端事件限定 Dist.CLIENT；原无材料信息工具仍按原规则作为未组装工具，未把占位堆叠当成完整工具。

配方接原完整 GTToolPatternRecipe / GTToolAssemblyRecipe / GTFlintAndTinderRecipe / ToolAssemblyCatalog：同材料、头前缀、手柄和早期固定材料条件、偏移/镜像、工具剩余物及磨损保留。tool_assembly/tool_crafting/tool_head 通过原生 MapCodec/RegistryFriendlyByteBuf 注册，沿用 tool 与 pattern 数据契约。原表生成真实内建数据包的 recipe/tools/* 和 recipe/tool_heads/*；RecipeManager 正常加载、同步及重载该包，不手工复制第二套全局配方管理器。

## 验证与缺口

物品/动作、客户端、制作三批后集中编译；原生模型类型、点火协议和 toolsUsable 接线遗漏修正，core/Neo/Forge 编译14秒通过。原有限液体容器的特殊 Ingredient/剩余物仍属后续有限容器模块，不能从工具制作通过推断该分支已经完成。

一次短普通 Neo 专服检查通过（4分28秒），包含真实数据包扳手制作、错误位置拒绝、锤子返回磨损400、镐头制作、头柄组装、实际物品组件保存解析及三类配方 serializer 网络往返。开发夹具排除于生产 jar。它不覆盖客户端、实际世界中的点火/疏通/建造杖/刮料、全生存获取、世界独立进程重载或旧存档。

仍待继续：实际电动工具及其能源/材料磨损/装配，Neo 漏斗和队列漏斗的具体 screwdriver 协议实现，工具依赖的方块/管道/储物/能源手工制作表，完整创造菜单、相关高品质采掘事件及工具依赖的其他机器。实际数据包加载48条整件工具、20条头柄组装及35条工具头配方（共103条），37类工具均至少有一个手工配方类别；这不证明每种材料或工具已生存可达。回执 verification/p3-neoforge-manual-tools-checkpoint.json。工具头配方的代表性预览继承完整工具显示的原问题仍需后续修正，实际工具头制作输出已通过小检查。新生产 jar 尚未打包。
