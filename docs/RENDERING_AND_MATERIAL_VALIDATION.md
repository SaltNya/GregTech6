# 渲染与材料校验记录（2026-09-11）

## 本轮修复

- 基岩钻机、聚变反应堆、聚爆压缩机、避雷针控制器改用存在的原版 orientable 模板，修复不存在的父模型引用，并关联项目中现有的金属墙贴图。
- 六种薄面板补齐朝上、朝下状态；模型改为与碰撞体一致的一像素薄板，并注册世界/物品两套材质染色。北向模型位于 z=0，其他方向由 blockstate 旋转。
- 基础机器按真实 BlockState 获取 Minecraft 已烘焙的模型，保留其朝向和 lit/running 状态后再包裹染色。背包模型独立选择，避免覆盖世界旋转。
- `BakedModelLookup` 排除 missing-model 哨兵。基础机器、材料物品、材料方块共用该判断。
- 方块物品的显示变换每次烘焙重新捕获，资源包变更后不保留旧缓存；没有可用模型时清空缓存。
- 修复图集定义的 void 资源路径；另修复 58 个模型里的过时金属墙路径，使用项目已有对应贴图。

这不是给所有缺失资源填占位图。全量扫描仍报告历史模型、缺失资源与可能未被使用的声明，不能把这个列表直接等同于当前画面故障数量。

## 材料承载能力

新增 `AtomicProperties` 保存 GT6 的质子、电子、中子和额外质量，额外质量可为负。元素工厂现在保存其原子参数；具名 Builder 支持 `.atomicProperties(protons, electrons, neutrons, additionalMass)` 和 `.alpha(0..255)`。RGB 颜色仍保持已有接口。

按原版 MT 定义补入 Photon、Neutrino、Neutron、Proton、Electron 五种隐藏粒子，使用原版 ID 1..5、原子数、颜色与透明度元数据，不生成物品形态。Magic 保存额外质量 -1；Empty 的原子数为零。

`Materials` 提供五种粒子的可读引用，生成脚本也会保留这些引用。旧材料 ID 与目录保持不变。

五个导入目录是维护分组，不是互斥类型。`CompoundMaterials` 是历史综合目录，包含合金及其他混合材料；其名称不应被理解为严格化学分类。运行行为仍由材料属性、组分和加工关系确定。

尚未完成：全量反物质/特殊材料、所有原版属性与组分原子统计的推导、完整流体关联、存档行为验收。新增原子字段本身不等于完整核物理或配方实现。旧导入数据的 ID 冲突仍需单独迁移方案，不能靠改 ID 顺带处理。

## 可重复检查

```text
python -m unittest discover -s tools/tests
python tools/check_registration.py --offline
python tools/check_render_resources.py
python tools/check_render_resources.py --all --report build/render-resource-audit.json
python tools/check_material_coverage.py
```

- Python 测试覆盖控制器父模型/贴图链、面板六方向、装饰模型资源、材料生成和覆盖解析。控制器与面板用例在修复前失败、修复后通过。
- 注册检查执行 Java 编译、注册契约、两种材料初始化顺序，并导出真实内置材料身份到 `build/registration-material-catalog.json`。导出使用单独 JVM，不包含测试用材料。
- 客户端辅助测试使用不同的烘焙模型测试替身，验证缺失模型回退与两次资源重载后变换缓存的更新、清空。它不模拟 GPU，也不是完整 Forge 启动。
- 资源检查默认只严格检查本轮控制器/面板及其引用；`--all` 包含历史模型声明，发现缺失就返回非零，不隐藏问题。只核对本模组的显式文件引用，不检查外部资源包、所有动态 Java 贴图引用或所有模型纹理变量。
- 材料覆盖检查读取原版 MT/AM 与最新运行时身份导出，列出身份已存在、缺失、ID 不一致和动态/虚拟定义待解析。身份存在不代表属性和行为一致；扫描还可能包含未启用的定义或需手工解释的动态工厂，因此不提供“移植百分比”。

本轮没有客户端画面和旧存档验收。下一次游戏内验收应覆盖四个控制器、六种面板的上下放置、基础机器四方向与三种工作状态、背包/手持显示，以及 F3+T 和切换资源包。
