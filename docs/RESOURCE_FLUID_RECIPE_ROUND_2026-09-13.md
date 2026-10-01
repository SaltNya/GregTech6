# 资源增量同步、流体外观与染料配方（2026-09-13）

## processResources 九分钟的原因与修复

实际强制运行原任务复现：总耗时 8 分 50 秒，其中 processResources 为 8 分 46.740 秒。资源只有 24.34 MB，却有 60,271 个小文件。原 ProcessResources 在需要执行时先清理旧输出、再全量复制；线程采样还发现输出快照逐文件打开并计算哈希的耗时。未变更时原任务 UP-TO-DATE 只需 1.490 秒，因此不能把每次启动慢都归因于编译或堆内存。

新增 gradle/incremental-resources.gradle，保留 Forge 所依赖的 ProcessResources 类型和 CopySpec，使用 Gradle InputChanges 只更新变更文件，并删除移除的资源。保留 mods.toml / pack.mcmeta 的变量展开。首次建立新任务历史仍需全量处理，本机已完成（10 分 5 秒）；后续恢复 12 张 PNG 的真实生产任务只处理 12 个文件，processResources 为 4.322 秒。全次 Gradle 命令包含配置阶段共 43 秒，不能把 4.322 秒当成整个 runClient 启动时间。

集成验证覆盖新增、修改、删除、未变更文件时间戳、模板变量变化、外部改动输出后的修复、UP-TO-DATE 和清空输入。tools/sync_test_resources.py 改为调用 Gradle，避免直接写 build/resources/main 破坏任务输出快照。以后正常使用 runClient 即可；clean、任务实现变化等仍会触发全量同步。没有修改全局防病毒配置，也没有证据将底层文件延迟归因于某个杀毒软件。

性能记录：项目上级 resources-diagnose-recopy.log、resources-incremental-delta.log、resources-sync-integration.log；Gradle profile 位于 build/reports/profile。

## 流体外观

- 修复气体无条件采用通用贴图、生成液体/气体被旧枚举误判为熔融金属的问题。
- 优先存在的原版专属 PNG；没有专属资源才按气体、液体、熔融金属、等离子体选择模板并染色。
- 专属已着色 PNG 避免重复乘材料颜色；共享染料/泡沫贴图使用原版染料色，熔融材料采用对应液态颜色。
- 将贴图与 tint 作为同一个外观结果，供实际流体、展示流体物品、GUI/JEI 及坩埚流体使用，避免各自选色。
- 原版 350 张流体 PNG 及动画元数据逐一核对，恢复其中被改动的 12 张。保留动态贴图元数据，没有把动画帧拼图当成普通静态贴图。
- 恢复工具 tools/restore_fluid_textures.py 同步更新纹理来源记录。

## 新增配方：348 条

- 64 条染料与四种水的混合配方。
- 192 条水染料/花染料与六种植物油的化学染料配方。
- 48 条泡沫染色与钯粉处理配方。
- 26 条原版花卉挤压/榨汁配方，保留产量与植物残渣概率。
- 8 条小麦、甜菜、南瓜、西瓜种子的植物油配方。
- 2 条向日葵加工配方：挤压 100 mB / 榨汁 75 mB 葵花油，均产出两个黄色染料。
- 8 条基础泡沫上游配方：四种水下的石粉、二氧化硅粉、黏土粉大小批次混合。

依据原版 Loader_Recipes_Other、Loader_Recipes_Crops、Loader_Recipes_Vanilla；注册入口为 DyeProcessingRecipes。当前基础泡沫使用 Stone / SiO2 / Clay 组合，尚未展开原版所有岩石和等价材料替代。建筑泡沫粉当前未生成物品，粉末水合配方暂未注册；其他植物油的上游、彩色泡沫世界放置与所有权行为、完整化工与回收链仍待移植，不能把新增流体配方视为这些系统全部完成。

## 验证

- Python：88 项通过。
- 渲染资源检查：775 个受检文件，0 个未解析引用。
- 增量资源集成测试通过。
- 服务器 GameTest：补入 18 条上游配方后的最终复测 174 项全部通过，BUILD SUCCESSFUL（3 分 17 秒）；日志位于项目上级 fluid-recipes-precursors-final-2.log。
- 未构建 JAR，未启动实际客户端进行目视验收。

## runClient 验收顺序

1. 重启客户端，在 JEI 和机器储罐中比较啤酒、原油、重油、蜂蜜、杂酚油：应使用各自专属纹理。
2. 比较氢气、硫酸、熔融铁/钢，以及红色/蓝色/绿色染料：模板与颜色应随类型变化；对比展示流体与实际槽内流体是否一致。
3. 用小麦种子加工植物油；罂粟加工红色花染料；混合 216 mB 花染料与 20 mB 油得到 288 mB 化学染料。
4. 6 石粉 + 2 二氧化硅粉 + 1 小堆黏土粉 + 1000 mB 水得到 1000 mB 建筑泡沫；再用化学染料染色。配方入口可在 JEI 查看。
5. 正常再次运行 runClient，未修改资源时 processResources 应为 UP-TO-DATE；仅改少数贴图后应输出相应 changed 数量，不应重写六万文件。
