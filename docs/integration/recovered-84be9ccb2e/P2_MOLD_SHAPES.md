# 完整共享模具形状表

2026-09-30；材料物品230e709d之后的独立提交。`core/api.machine.crucible.MoldShapes` 提取原Forge MoldBlockEntity完整5×5表，包括所有基础pattern、滑动位置、90度旋转、镜像、原HashMap覆写顺序，以及最后添加的blockSolid和nugget十字。只把输出值包装为纯 `Recipe(MaterialPrefix itemPrefix, boolean blockSolid)`，blockSolid的itemPrefix为null，平台负责对应真实方块；没有只写ingot示例。

API为 `recipe(rawShape)`、`isNuggetFallback(rawShape)`、`requiredMaterialUnits(rawShape)`、只读 `recipes()`。lookup沿原25bit mask，未知非零形状fallback nugget，0返回null；fallback量沿原rawshape的Integer.bitCount×U9，未静默更改旧NBT高位语义。已知nugget十字是1U9；原blockSolid20格是9U（MaterialPrefixes.java:780–785），不能按格数推算。已知形状枚举仍排序，trySetMoldShape仍按未mask的raw key校验。

Forge只消费共享lookup/量与表，blockSolid映射回原BlockMaterialPrefix，实际Item/Block输出、凿刻/工具/取物、NBT、输入面、酸检查及basin转发留在平台。按主线约定另接 `MoldCastingRules.cool` 和 `acceptedAmount`：输入side/acid/basin处理顺序不变，仍在真实内容/输出空闲检查后接受完整要求量。该规则类由主线另一个提交提供，本隔离分支没有复制影子类。

原blob、SHA、对应行号及迁移范围见 `core/provenance/mold-shapes-extraction.json`；原作者历史和适用授权未决，未自行改许可。一次直接源码比较确认：撤销输出token包装与Map泛型差异后，完整builder的bit操作和写入顺序与原import逐字相同。此次没有新增测试、运行javac、Gradle、游戏或成品打包；主线统一构建和既有实际加工链回归仍需验证，此文不记为玩法完成。
