# P2：统一材料与坩埚核心迁移设计

日期：2026-09-30。本文是源码设计证据与实施门禁，不是材料迁移、玩法或存档验证完成声明。路径除另注明外均相对于 `src/main/java/com/gregtech/gregtech/` 的 saltnya 导入快照 `import/saltnya-snapshot`（`41561782`）。三份来源保持只读；具体采用代码仍须保留来源哈希、原始署名和许可证据。

## 结论与对象边界

推荐把现有 `GTMaterial`、`GTMaterialRegistry`、生成材料定义、组成和前缀规则，以及 `CrucibleMaterialStack` 的领域算术、`CrucibleReactions` 移入同一个 Java 17 core。两平台引用相同全限定类和同一份目录，不新增另一套 MaterialCatalog、镜像 DTO 或独立注册器。Forge 现有调用中的对象身份、`resolve()`、注册 ID、名称/别名、物质量和反应顺序是保留基准。平台负责 ItemStack/FluidStack 映射、显示 Component、模组是否加载、NBT、游戏注册、世界交互和渲染。

可以迁移材料领域闭包，但无法同时把 `GTMaterial` 做成纯 Java 并原样保留它的 `Component getDisplayName()` 二进制签名：`GTMaterial.java:4,423-424` 直接返回 Minecraft 类型，而且类本身是 final。保留一个名字相同的 Forge 子类、在两个平台各造一套材料、或用泛型强制转换隐藏 Component 都不能解决同一模型的问题。

建议 core 保留 `getTranslationKey()` 和 `getDisplayNameFallback()`；各平台增加 `MaterialPresentation.name(GTMaterial)`，执行原 `Component.translatable(key, fallback)`。逐个确认接收者类型后迁移 Forge 材料调用，保留 `.copy()`/样式与显示结果。主要调用在 `item/MaterialItem.java:60`、`item/GTToolItem.java:223,226`、`item/ElectricToolItem.java:181`、`item/WireBlockItem.java:22`、`client/MaterialTooltips.java:104,194,200`、`client/CrucibleTooltips.java:114`、`client/GTToolTooltips.java:41`、`block/MaterialBlock.java:58,100`、`block/OreBlock.java:130` 与 `block/MaterialBlockItem.java:40-52`。同名流体、菜单或游戏 API 调用不可全局替换。非 Minecraft 公共方法保留原签名；第三方调用已移走显示方法的二进制兼容不能据此承诺，必须在兼容说明中记载。

## 待核实的最小依赖闭包

P1 的 `GTValues` 和 `AtomicProperties` 已在 core。本批候选闭包按职责列出，实施时用无游戏 classpath 的 javac/jdeps 核实实际文件数和余留依赖；不能仅凭没有 net.minecraft import 就宣布纯 Java。

1. 材料模型：`api/material/{GTMaterial,GTMaterialRegistry,MaterialDefinition,MaterialProperty,MaterialTextureSet,MaterialComponent,MaterialSentinels,MaterialFactories,MaterialChemistry,MaterialMass}`。`MaterialDefinition.java:8-10,26` 已明确 Kelvin；GTMaterial 的 Nullable 注解没有运行时领域职责，可移除该注解而保持可空行为，或使用独立编译注解，不能为此引入游戏依赖。
2. 来源/常量：`api/mod/ModData`、`data/{GregTechConstants,ModReferences,ImportedMaterialData,AntimatterMaterials,MaterialGroups}`。`GregTechConstants.java:3,12-18` 依赖已共享的 GTValues；`ModReferences` 的未使用 GregTech import 应移除。ModData 的游戏/Forge 依赖须先拆边界。
3. 原有完整材料目录：`content/material/{Materials,MaterialDefinitions,MaterialFormCorrections,ParticleMaterials,SupplementalMaterials,VanillaMatterMaterials}` 与 `content/material/generated/{ElementMaterials,CompoundMaterials,OreMaterials,StoneMaterials,WoodMaterials}`；`data/generated/{GT6Materials,MaterialModTags,MaterialRegistryExtras,MaterialCompositionData,MaterialForms}`。这些文件构成既有 declare/link 过程，不能只搬铜锡青铜并把其他 Forge 材料变成第二个目录。
4. 物品前缀领域规则：`data/MaterialPrefix` 和 `api/prefix/PrefixRegistry`。前者 import 闭包（`MaterialPrefix.java:3-10`）没有 ItemStack/Component；配合 MaterialForms 和 WoodMaterials 迁移后，可以完整保留 MaterialChemistry 的 prefixMaterialWeights，而无需复制另一套公式。`api/prefix/BlockMaterialPrefix` 的 SoundType/MapColor 属于平台，不能因此把全部块前缀拖入 core。
5. 坩埚物质量与反应：`api/machine/crucible/{CrucibleMaterialStack,CrucibleReactions}`。CrucibleMaterialStack 的 `saveList/loadList`（`94-122`）含 NBT，应迁至平台 `CrucibleContentsNbt`；保留原领域 class 的 material/long amount、合并、复制和质量算法。反应输入输出继续使用同一 GTMaterial 对象。

不属于本闭包的 `GTMaterialStack.toStack`、`MaterialDisplayBinding`、GTItems/GTBlocks、ForgeRegistries、世界生成和原版物品组成注册仍留平台。完整材料迁移后可由两平台逐步消费同一对象；它本身不自动补齐 NeoForge 的物品/机器/世界生成内容。

## 生命周期与平台接线

`ModData.java:3-6,22-28` 把元数据构造与 `Forge ModList.isLoaded` 绑在一起，`owns(Item/Block)`（`40-53`）再查 ForgeRegistries。迁移时保留 id/name/prefix、MODS 映射、`equals/hashCode` 和 `owns(String)`；提供纯 Java presence predicate，在任何 `ModReferences` 或材料定义静态初始化之前由平台绑定。Forge predicate 使用原输入 id 调用 ModList；NeoForge 使用对应 loader。游戏对象的所有权查询放入平台 helper，按实际调用方迁移。当前树未找到 `.owns(...)` 调用，不代表外部 API 无兼容影响。不得用“默认全部已加载”掩盖初始化错误。

`data/ModReferences.java:19-21` 的 MC/GT/GAPI 创建顺序与同 id 的多个 ModData 实例当前会影响全局映射；本次不顺手改变其覆盖规则。纯核心测试可明确绑定假 presence 后启动完整目录，避免依赖本机安装模组列表。

`GTMaterialRegistry.init()`（`154-169`）是一次性的 DEFINITIONS → LINKS → READY；异常进入 FAILED，随后调用不可当作恢复成功。它的 Mojang/SLF4J logger 与 GregTech entrypoint 引用需要改为 Java logger 或平台日志 callback，不能为日志把 loader 引入 core。`postInit()`（`172-195`）前部燃料/粉碎规则属于领域，尾部 `VanillaUnificationLoader.register()` 和 `VanillaCompositionLoader.register()`（`193-194`）必须移到平台材料后处理调用，保持原先相对顺序。

Forge 原入口在 `GregTech.java:35-43` 顺序构造/运行 phase A loader，commonSetup 的 phase C（`73-79`）执行 Loader_MaterialPost；因此 presence 与日志 adapter 必须早于 phase A 构造绑定。`loaders/a/Loader_Materials.java:9-10` 还给世界生成材料打 ORE flags。这些 flags 会影响 item form；两平台必须在各自内容生成前有明确、相同的领域标记规则，不能只有 Forge 世界生成 bootstrap 才补标记。

`CrucibleReactions.allRecipes()`（`60-71`）第一次调用会缓存显式配方与当前目录生成的合金。严禁 NeoForge 为一个测试提前访问空目录后永久缓存缺失配方。初始迁移保留排序/选择语义；如要追加 READY 校验或稳定排序，应作为独立行为变更，记录旧行为与固定测试，不能混入搬迁。`allMaterials()` 目前来自 HashSet（Registry `29,139`），反应同输出量 tie 取先遇到配方（Reactions `77-98`）；盲目排序会改变选择结果。

## 冻结的数据与算法合同

- 物质量：`GTValues.U=648648000` 每锭；所有坩埚 amount 保持 long。`GregTechConstants.java:12-16` 中 U 的分数与外部流体 L=144 保持区别。144 不是全局材料精度。不可表示的外部单位转换必须有明确拒绝/取整合同。
- 温度：材料定义/机器温度保持原整数 Kelvin。`GregTechConstants.java:17-18` 中 C=273、环境293；不得顺手改成273.15。masson 摄氏度数据只可经显式边界导入，不能直接塞入 getMeltingPoint/getBoilingPoint。
- 身份：MAX_MATERIALS=10000（Registry `25`），Invalid=-1/NULL=0、原 sanitized 名称、别名与 registration target 继续保留；`GTMaterial.java:226-231` 的 resolve 链和调用中的引用相等不得换成一组另造 DTO。`registerAlias`（Registry `99-118`）保护 canonical name，并有 antimatter 特例。
- 物理/组成：Copper id290、1357K/2835K；Tin id500、505K/2875K（ElementMaterials `52,73`）；Bronze id8610、1357K/2835K、density8.54175、Cu3Sn（CompoundMaterials `436`）。`MaterialCompositionData.java:1045-1047` 绑定3U Cu+1U Sn；CrucibleReactions `40` 另有3 AnnealedCopper+1 Tin→4 Bronze。AnnealedCopper 的2800K熔点（CompoundMaterials `398`）与“至多一种仍固态”的反应门槛须验证，不能自动抹平差异。
- 反应执行：保留输出熔点门槛、各 part ratio、固态计数、最大产量选择、Math.multiplyExact 与先消费后合并行为（Reactions `74-119`）。合金测试同时检查剩余输入和总单位，不只检查存在 Bronze。
- 精确存储：CrucibleMaterialStack `94-122` 的 ListTag 项仍写 `id` int、`amount` long，并保留无效/非正条目的过滤。坩埚 `SmeltingCrucibleBlockEntity.java:70-78,790-821` 的 `gt.materials`、`gt.temperature`、`gt.energy.buffer`、旧温度、cooldown、熔化/显示状态保持原 schema。模具 `MoldBlockEntity.java:76-83,790-814` 的 material 保存为名称字符串、amount 为 long，并支持旧 `gt.mold.has_content`；不能为统一外观擅自改成坩埚的数值 ID schema。
- 注册内容：`gregtech` namespace、现有物品/方块/机器路径、工具材质编码不因移动 Java 包改变；核心迁移不重新注册一份平台材料对象。manifest 记录所有原文件 SHA 与必要边界修改，不能把已修改文件仍标为 byte-identical。

已有潜在问题单独留账：Registry.register 先改 BY_NAME/ALL 再检查数值 ID（`82-90`），失败可能部分修改；GTMaterial.setComposition（`310-327`）求和没有严格溢出检查；oreMultiplier（`395`）转 byte；名称/texture lowerCase 使用默认 Locale。搬迁保留行为，后续如修复需独立用例，不以重构之名隐含改变存档/配方。

## 三家候选比较与采用顺序

saltnya 的完整材料与前缀目录、现有 Forge 全内容和调用关系，是本批保留和实际迁移对象；构建通过是当前证据，坩埚玩法仍需运行。其混在对象中的 Component、ModList、NBT 是边界债务，不能据此放弃完整目录并换一个小演示 catalog。

brokestar 的 `gregapi/oredict/MaterialRegistry.java` 有明确 open/close、转换图查询和 visited 防环；但 ID 范围32767及 OreDictMaterial 类型不同，不能直接替换现有注册器。`gregapi/util/CruciblePhysics.java:53-55,118-124,158-212,249-308,332-428` 是纯领域热/合金/phase outcome 候选；其 tests 的固定样本包括相同质量500K/300K→400K、SMALL17U拒绝、LARGE接受、requiredEnergy及热/冷 tick。完成同一材料身份迁移后，先用原固定样本比较 saltnya 实际算法；再将选中的热/phase 规则适配现有 GTMaterial/long U。保留 LGPL 源头通知，不能带入第二个 OreDictMaterial 注册宇宙。空 ModularUI 不影响阅读纯逻辑，但其整树构建不能被当作已验证。

masson 的 `material/GT6ImportUnits.java:6-14,18-54` 明确区分 GT6 Kelvin/U 与摄氏度/144。它的不可表示 U→CC 拒绝及 Math.multiplyExact 思路适合显式边界；若选用，保持 GT6 内部 U/Kelvin。`fluid/MoltenTransferMath.java:15-20,28-71` 的 GCD composition quantum、整批比例和不可满足返回空计划可作为防丢料候选，必须改用原 long U/GTMaterial，而非复制 string/int 存储。`material/MaterialFingerprint.java:20-98` 的排序哈希适合目录冻结/两平台一致性证据；`recipe/rule/MaterialChainReachability.java:17-85` 的实际展开配方可达性适合首链门禁。masson 下划线 MaterialId 与 double Celsius ThermalProperties 不替换原 CamelCase/整数 Kelvin schema；其含 Minecraft/Codec 的 definitions 不能原样称为纯 core。

这三项候选在本次设计中尚未合并。先迁移实际 saltnya 身份与模型，再比较、逐项采用完善部分；没有执行结果时不宣布任何候选优胜。

## 可执行迁移和验收次序

1. 在修改前保存原目录快照：numeric ID、canonical name、aliases/registration targets、物理值、flags、sourceMod、组成 divider/parts、prefix amounts/forms，按稳定键排序后生成哈希；不同 JVM/Locale 运行并说明 loader presence 和 worldgen flags 时机。快照是原对象的审计输出，不能成为另一个运行时模型。
2. 修改上述 MC/loader/NBT 边界，迁移完整领域闭包与来源 manifest；core 独立 Java17 编译和 jdeps 必须无 Minecraft/Forge/NeoForge，原 source 不留重复全限定类。根构建和平台接线由主线统一执行，避免并行 Gradle。
3. 在新 JVM 验证一次完整 init/postInit 后目录和固定铜/锡/青铜数值；比较迁移前快照。验证第二次 init 不重复、alias resolve 同一对象、失败不会被 READY 掩盖、反应不提前缓存；记录有意行为变化。
4. 保留 Forge 原内容注册顺序，替换显示/NBT 调用并跑既有相关 GameTests；NeoForge 引用同一 core 注册真实首链所需物品/机器，不只引用数学常量。两平台 jar 检查核心类只嵌一次。
5. 以真实机器 tick 完成燃烧箱→坩埚铜锡合金→浇铸模具→工具链，核实生存配方可达、热量、比例、输入剩余/材料守恒和工具消耗；随后专服/客户端联机、真实关服存盘/重启同一世界。NBT 方法往返仅是 schema 单元证据，不能替代世界重载。
6. 完成后记录每个系统的来源、取舍、哈希、构建/运行日志、旧存档支持边界与未覆盖项。完整世界样本和成品 jar 验证之前，P2 保持未完成。

当前 P1 bootstrap GameTests 只测共享核心被开发服务器加载及固定数值合同，不测真实坩埚/工具玩法，也不作为成品专用服务器与客户端启动的替代证据。
