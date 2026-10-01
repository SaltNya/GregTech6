# P3 齿轮箱、旋转变压器与工具制作目录

来源为 saltnya 原实际实现，保留作者、历史及授权原文；公开发布授权仍未决。原文件 SHA-256 和资源来源见 core/provenance/native-gearbox-source-integration.json、manual-tool-definitions-source-integration.json。没有复制新的注册底层或材料身份表。

## 已接入

- 共享 GearboxCatalog 的原 13 档材料/速度/功率显示及 RU 变比表；Forge 原注册调用共享规格，Neo 注册真实 13 个齿轮箱和 13 个旋转变压器。
- GearboxRotationRules 共享原齿轮布局合法性和各面有符号旋转方向；两平台保留原世界能源传输逻辑。
- Neo 原完整齿轮箱实体保留齿轮装卸、轴选择、卡死、递归 RU 传输、速度超载和循环顺序，原存档键保持。掉落物通过原生 BLOCK_ENTITY_DATA 保存齿轮和轴，包含 1.21 组件要求的实体 id。
- 旋转变压器接既有单一 energy_node 实体类型；有效方块集合包含原 70 种节点、本批 13 种变压器、5 个保留化学电池路径，未建第二套能源实体。
- 原动态齿轮/轴纹理与动画元数据迁共享资源；Neo 客户端模型/颜色事件独立于专服。原生 QuadBakingVertexConsumer 改为无参构造及 bakeQuad 导出。
- ToolDefinition 共享完整 37 类工具的 GT6 id、材料前缀与门槛、图标标识、耐久/伤害/品质/速度、磨损和采掘标志。Forge GTToolType 为 Minecraft 类型适配，原物品及交互不删除；Neo 同名边界供后续完整工具接线。
- ManualToolRecipeCatalog 共享所有原整件工具、工具头、早期燧石/骨/石材图案，保留顺序、材料条件、工具条件、镜像和手柄规则；固定原版物品在核心中使用稳定 id。两平台 GTToolRecipes 只转换平台 Item/Tag 类型。
- Neo 现有真实凿子和钳子继续原注册并调用共享耐久倍率；本批没有重复注册其余 35 种工具，没有宣称完整工具制作已可玩。

## 验证与缺口

三个源码批次后集中小检查。首轮 Neo 编译发现一个客户端顶点 API 错误，按当前固定 Neo 源码接口修复；最终 core/Neo/Forge Java 编译通过（26 秒）。详见 verification/p3-gearboxes-tool-catalogs-compile.json。

Neo 普通 DedicatedServer 短启动通过（4分38秒）：配方/数据包加载、200 tick、正常保存退出。回执 verification/p3-neoforge-nodes-gearboxes-startup.json；没有独立 JVM 世界重载。编译不证明客户端模型、旋转传输、超载、齿轮装卸/掉落/世界重载、完整手工/电动工具和制作 serializer 或生存可达性。剩余工具动作、组件存档、属性/渲染/配方注册按依赖继续接入；旧存档及新生产 jar 未验证。
