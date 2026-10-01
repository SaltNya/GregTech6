# 当前任务与继续执行入口

用户最新执行要求（2026-10-01）：继续优先快速合并，每完成几批进行一次小检查，重点检查 NeoForge。允许批次集中编译并修复阻断错误；不恢复每批全面测试或运行全套验收。未执行的客户端、专用服务器、玩法、世界重载验证继续标记未验证，不据此把整合标记完成。


更新：2026-09-30。Goal active；未验证阶段不得完成。

主工作区F:/Dev/GregtTech6New/gregtech6，main。../Libs三源只读；本工作区Gradle由主会话串行执行。

## 主线快照

- 41561782 / import/saltnya-snapshot：原始项目1复制，不是恢复的作者历史。
- 31b827601e / integration/p1-scaffold：双平台初始接线。
- ef90ee628d / integration/p1-dev-startup：P1打包/验包/CI和开发启动。
- 5098520551：39个材料领域类迁入core，平台seam留Forge。
- 5d2f4b008c：五份角色/石种表、统一角色应用、Neo目录初始化及四项新GameTests。
- e0c53d7dd4：纯整数有符号热规则候选与53合约，尚未接入生产机器。
- de18243bb9：Forge正式机器加工链两项GameTests；后续物理隔离夹具/XML报告版本已实际通过4m17s，回执verification/p2-forge-playflow.json及xml。

原历史标签：source/brokestar233-snapshot=3118acbf83a84d05fa37d57af1705cf00e423ca9；source/masson-snapshot=2ba4e4b60f7a770360b2ec7ca2adad3507ec4a28；source/modularui-brokestar-snapshot=ec524db7a5724f8cf3c837436b1ae742c778c62f。

## 当前验证及下一实现

P1主菜单/基础bootstrap通过属于历史快照。P2 core:check实际64+6154+53断言与Neo七项required GameTests通过；dee74fad39全构建7m23s、当前80个core类和3许可资源验包通过，回执verification/p2-materials-artifacts.json。不能复用P1九类报告或把打包当玩法完成。

两平台普通DedicatedServer两阶段重启已完成，开发探针限定原版箱子/库存/Dirt。Forge先被EULA阻止，用户“当然同意”后仅隔离测试目录写eula=true再跑。verify_dedicated_smoke.py验证真实日志/独立JVM/保存文件，报告见verification/p2-{forge,neoforge}-dedicated.json。生产jar/GT机器存档另验。

Forge两项实际加工检查已通过，命令新增显式 '-PgameTestReport=build/forge-playflow-isolated-run/playflow.xml'，PowerShell含点/路径参数整项加引号。日志work/p2-forge-bronze-playflow-isolated-retry1.log，XML两项均无failure/error/skip，正常保存退出。首跑吸入外来鞍与一次未引用参数被拆成.xml任务的失败保留；生产吸入和断言未放宽，冷坩埚用玻璃罩物理隔离。完整生存链仍待完成。

Forge原机器热边界首跑已结束5m11s：四项三过一失败，正HU余量/603K混温及自然青铜链通过，溢出包缺口真实重现；回执verification/p2-forge-thermal-before-fix.json/xml。随后Forge已接ThermalStep，连同材料物品/共享输入/Neo三机集中编译1m33s通过；双版本一次Gradle关键加工5m通过，Forge四项/Neo一项。回执verification/p2-first-machines-playflow.json，溢出拒绝已实际通过，不再每个抽取启动游戏。

首批Neo真实机器/材料物品/交互、共享热/合金/NBT平台实现已在给定器材加工链运行通过。继续生存配方/原料可达、视觉与真正机器世界重载；其余系统仍未整合完成，不能称双版本完整玩法完成。

## 可恢复隔离分支与协作

work/p2-shared-materials保留材料ffe109c883、thermal7d85a999、加工测试873db17e61，均已合入main。work/p2-neoforge-materials保留角色ec973694c9，已合入main。不要再次整块复制旧build配置覆盖主线。

work/p2-neoforge-materials工作区已在确认干净后切至新分支work/p2-machine-core（从de18243bb9），旧角色分支refs保留。audit_masson已完成MachineSpec/CrucibleSpec与材料物品定义，正在完整MoldShapes及Forge表接线；Root负责共享燃料/物品组成/相变及Neo三机平台。均不逐类启动游戏。已完成的只读迁移边界报告为P2_MACHINE_BOUNDARIES.md。

材料/角色独立审查通过。两名子代理因账号usage limit停止，主会话继续；已完成提交和审查保留。重新委派前确认外部限制变化，不重复失败操作。

## 环境与缺失信息

Java17=C:/Program Files/Java/jdk-17.0.4；Java21=C:/Users/Asus/AppData/Roaming/.minecraft/runtime/java-runtime-delta（用户bin所属根）。设置JAVA17_HOME/JAVA21_HOME后用scripts/build.ps1或gradlew，构建不写死路径。

Python3.12=C:/Users/Asus/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe。来源脚本支持3.10，TOML验包需3.11+。

项目1原仓/历史与模组授权仍待信息。新origin未到必需时，不猜测归属。发布门未决不妨碍本地授权开发测试。

快速源码合并批次（2026-10-01，未验证）：能源类型/轴/齿轮箱/线缆/节点规格与长整数缓冲迁共享core；接brokestar EnergyGate/FE packet bridge，两平台能力适配；Neo坩埚/模具使用同一ITileEntityCrucible/Mold及HU网络入口。该批没有执行构建、测试或启动。完整线缆/转换器注册继续移植。

快速源码合并批次（2026-10-01，未验证）：完整FL静态与派生流体目录/定义共享到core，RegisteredFluids仅为两平台纹理边界。Neo接静止/流动/流体类型/世界流体块/元数据显示物品及客户端extension；masson MoltenTransferMath按原字节保留，144mB与GT6 U在边界转换，实际Forge/Neo坩埚接熔融流体能力，余下分数保留在存量。流体物品完整载荷、饮用、纹理及水族Mixin仍待继续移植。此批未构建、未测试、未启动游戏。

快速源码合并批次（2026-10-01，未验证）：52份机器/引擎/锅炉/泵/管道/漏斗/坦克规格、活塞/蒸汽状态、批量存储、传感器、能源节点/电池定义、工具几何及制作目录按原字节整块迁core，Forge原调用类名保持，两平台共用。Neo整机注册和交互仍继续接入；此批未构建或测试。


2026-10-01：Neo大宗存储批量接入完整金属表、共享百万件状态/材料分量、组件存档、物品自动化能力、前面板与六格显示、材质模型和纹理。连通物流存储/金属箱、完整工具与胶带前端仍缺；注册入口由并行方块分支接线。未构建、未测试、未启动；不据此宣称功能完成。


2026-10-01：共享原物流覆盖物定义、优先级路由调度、CPU读数及核心几何/能耗规则；Forge原路由直接调用共享规则。Neo接真实物品/流体能力、组件过滤器存档、连通大宗存储、六面物流线和覆盖物渲染/资源。Neo核心控制器/多方块绑定及完整工具仍未迁，本批未构建/测试/启动，不能称端到端物流可玩。


2026-10-01：85个原机器RecipeMap定义/布局/标志、全部科技物品ID/别名/名称、食物发酵表和独立产出概率规则共享core；Neo真实Recipe/RecipeMap/RecipeInputs已薄适配组件与流体API，注册科技物品及食物发酵条目。覆盖物不重复注册；模具已接真实blockSolid材料块出口。多数机器配方loader、机器运行/界面与USB行为仍待移植，本批未构建/测试/启动，罐发酵待并行分支接线。


2026-10-01 批次：538d077740 完整普通罐/流体管道已接线；共享基础机器 catalog/faces/recipe aliases/menu layout、Neo 普通机器 BE/能力/GUI/payload 已写入。集中 :neoforge:compileJava 修复 core 边界遗漏与17个Neo API错误后通过（最终14秒、25 deprecated警告）。当前仅编译验证；Forge本批未编译，运行/世界/完整配方/多方块/USB未完成。详见 P3_BASIC_MACHINES.md。


2026-10-01 配方/制作批次：九组原生成表和手册正文共享 core，Neo 接十个加工入口、原基础机器制作图案/工具磨损 serializer、材料和电路 tags。两项编译阻塞修复后 :neoforge:compileJava 通过（13 秒）。首次隔离短专服失败于缺失 plant_remains，已补原四种非食用加工残渣，修复版本 Neo 专服启动/配方加载/200 tick/正常保存退出通过（4 分 22 秒）；没有客户端、完整玩法、机器世界重载验收，完整工具/电池/多方块仍未完成。详见 P3_RECIPES_AND_CRAFTING.md。


2026-10-01 工业加工源码批次：九份原参数表及回收数量/粉末选择逻辑共享 core；Neo 接入十一工业/原版加工入口，按原 phase C 相对顺序加载。石墨烯细线、炸药物理工厂未迁，相关 Neo loader 不假启用。本批未编译/启动，上一批成功回执不覆盖新增代码。详见 P3_INDUSTRIAL_RECIPES.md。


2026-10-01 电池物品源码批次：共享完整五个兼容电池定义和简易/化学电池包上限计量，Neo 接入原 IItemEnergy 与五个实际充电物品、模型纹理、完整 IV rechargeable tag。被动化学电池/掉落/充电器/电池盒/电动工具仍未迁完。本批未编译/运行，继续几批后集中小测，详见 P3_ITEM_BATTERIES.md。
