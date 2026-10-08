# 原文汉化入口

唯一中文基准是用户提供的 `C:/Dev/GregTech_zh_cn.lang`，即本项目所指的 gregtech.lang。`GregTech_zh_cn.lang.gz` 保存该文件的完整原始字节；`source.json` 记录 SHA-256、来源和署名/许可现状。它只供开发工具和 CI 使用，不进入游戏 JAR。

`aliases.json` 将移植版语言键明确绑定到原文件的键。相同的中文字符串不代表相同物品；添加绑定应核对原注册 ID、材料或原文声明。已有历史来源见 `docs/integration/verification/original-zh-cn-source-20261005.json`。现代木板面板沿用原版通用木面板名称的例外列在 `source.json`，不伪造原版方块 ID。

中文文件由以下三项按顺序生成：英语回退、原文件所有 `S:` 项、明确的别名。逐字保留译文、空格、颜色、格式符和空值，不替换术语，不猜测新材料/档位的中文名。

```text
python -X utf8 tools/localization.py
python -X utf8 tools/localization.py --patch C:/Dev/GregTech_zh_cn.lang
python -X utf8 tools/localization.py --write --report work/language-report.json
python -X utf8 tools/integration/check_source.py
```

默认只检查，`--write` 才重建中文。报告单列没有原文绑定的英文回退项，不能把它们算成已汉化。需要新提示时，`tools/integration/import_source_tooltip_lang.py` 读取原 Java 声明并同时维护别名；全量来源发现工具 `tools/import_original_zh_cn.py --proposal ...` 只输出提案，不再覆盖语言或历史审计。

扁平化物品按原注册编号导入：`tools/integration/import_numbered_localization.py --source <原版检出目录> --audit <新审计文件>` 默认输出提案，增加 `--write` 才写入。当前覆盖 80 种熊蜂的 8 种状态/说明，以及 35 种铁砧；核对双平台状态编号、实际物品表、原版完整种类表和材质身份，缺失或冲突即停止。原文空值也照搬，显示端跳过空说明行。

旧 `generate_zh_cn.py`、`import_gt_lang.py`、`complete_registered_lang.py`、`generate_tech_lang.py`、`sync_standard_chinese.py` 转入统一入口，旧的拼词翻译表已退休。其它旧资源生成器若写回平台语言目录，源码检查会拒绝；更新它们时应只生成资源/英文，并通过本入口补原文绑定。

`sourcePolicyCheck` 经 `:core:check` 接入双平台构建。它检查纯 Java core 边界、GameTest 隔离、平台语言副本、重复 JSON 键及所有译文。验包再次检查当前语言来源，并比较 JAR 内的两份语言文件与共享资源字节是否一致。

英文也接受门禁检查：`english_source.json` 固定按原版身份核对的英文声明及来源文件哈希；`localization.py` 拒绝偏离原文、空物品名、乱码替换符、非法控制字符和中英文参数不一致。原版确实为空的 `.tooltip` 保留。格式检查采用 Minecraft 的数字格式归一和参数索引规则，保留无参数的原版百分比文字。

源码门禁还检查两平台实际 `translatable` / `I18n.get` 的静态语言键和参数数量，忽略注释、代码示例、原版 Minecraft 键，并单列动态键/变长参数边界。独立成品自检加载真实 `en_us` 资源并扫描全部 GT 注册物品名称，再切换 `zh_cn` 核对熊蜂、铁砧及流体实际回调；这不是完整世界或玩家悬停验收。

已有原版机器号、材料与流体身份可以导出并导入，避免英文词序影响匹配：

```text
java -cp core/build/classes/java/main tools/integration/LanguageIdentities.java > work/language-identities.tsv
python -X utf8 tools/integration/import_identity_localization.py --source <原版检出目录> --identities work/language-identities.tsv --audit work/language-identities-review.json
```

使用当前编译过的共享 core；默认仅生成提案，审阅后加 `--write`。运行前后均须保留审计。现代符号有歧义或原内名与现代名称不一致时不覆盖既有绑定；原补丁缺失条目保留在报告中。原文无法支持的英语表达式也不自行推导。

该入口也覆盖原材料管道的辅助注册偏移、便携容器、轨道/颜色/木材元数据、手动及电动工具、化学电池和紧凑组件。说明跟随同一物品的原编号；原版空说明仍保留为空。原 `getLocal()` 覆盖名和 `VN` 电压数组参与英文自检，不能以材料内名代替原显示名。历史配方生成器只读取字面量命名表，禁止为语言导入而执行其旧入口。

工具提示中的通用 LH 操作说明和标签可复用唯一且完全相同的原英文短语，并逐字采用该原键的中文；此规则仅适用于 `tooltip.gregtech.*`，不用于按名称推断物品或方块身份。已有原编号声明却没有现代语言键时，可从该原声明创建英文条目。实际双语自检覆盖曾绕开注册译名的机器、管道、储罐与书架物品类。

后备键总数含旧生成键与无文字的格式模板，不能直接当成游戏内缺译物品数。原补丁中的英语正文也是原文；严格来源检查通过不代表全部文字已变为中文。未明确允许补译时，将缺少源译文的条目保留在审计中。

修改原文件基准需要同时更新压缩快照、哈希和绑定，检查译文差异后再生成。现有汉化文件未声明作者/许可，沿用历史来源记录；本次仅在本地保存与核对，未发布。

建筑方块的颜色名按原 `BlockColored` 元数据整句导入，不拼接 Minecraft 颜色译名与英文块名。英文门禁核对原颜色数组、构造器和全块/半砖名称公式；成品自检在中英两种实际资源环境分别调用 9 类 × 16 色物品的名称入口。原文树苗大小元数据、季节/不透明树叶名称也由原树种身份绑定。

材料旧别名冲突由当前导出的正数 ID 与原 MT 内部名共同确认；ID 0 不作证明。英文解析保留 `woodnormal`、材料工厂、`setLocal` 和注册前 `ANY.init` 的实际显示名。同名字段若没有唯一实际材料身份，保留歧义而非最后写入者覆盖；原内部名大小写不能归并（如 MoonStone/Moonstone）。地表方块按原方块元数据绑定，球类与整块保持各自来源。

原17类石材的16种整块/半砖名称按原构造链展开，保留实际形容词顺序及半砖命名空间；十种移植新增石材不能套用其它原岩石译文。扁平化灌木使用原32759通用名称，实际产物在tooltip中本地化显示。独立成品自检同时扫描所有注册物品的英/中文名称，另存 `language-names.json`（默认物品，不含玩家数据）；含英文只是候选，须结合原文身份区分合法专名和缺译，不以候选数宣告汉化覆盖率。

材料形态的完整名称键通过共享 `PrefixRegistry.sourceTranslationKey` 读取原前缀别名；`itemCasing` 对应 `casingSmall`，不改注册身份。硬币按原32700使用通用名，单列材质。成品自检逐项验证所有存在的完整原名，同时记录缺键形态；缺独立形态键的unit等代理可能已有正确材料译名，不以该计数冒充缺译数。原文件中仍含英文的分类/专名保持原值。

科技物品的 IL 字段顺序与移植注册名不同（USB、晶体电路、食物模具等）时，在身份导入器中显式核对；原英文名称和说明随数字编号一同导入。喷漆使用原染料序号和完整/使用中配对元数据的整句名称，不拼接颜色译名。选择标签各配置沿用原通用名，数字由独立原文配置提示显示，不能通过删除数字信息来达到汉化。

电力导线按原辅助函数的 OP 尺寸、非连续电缆偏移和 `aCable` 条件绑定完整名称；不再拼接材料与 Wire/Cable。特殊矿石按原构造器元数据绑定，不能把贴图枚举顺序当作矿石编号。成品探针将这些实际名称入口与语言资源对照，英文和中文均检查。

流体英文同时读取原 `FL.create` 字面量及实际正数材料 ID 对应的生成公式；显式名称优先，保留材料 `setLocal` 的最终显示名。英文公式检查独立于原中文键是否存在；它证明当前流体的命名规则，不证明原版生成过该流体。已有完整键和旧路径一并核对。缺完整中文且没有完整英文键的流体保留材料本地化后备，避免补英文时遮住现有中文；报告单列 `runtime_fluid_fallbacks`。成品探针对已声明名称和材料后备逐项验证实际回调。战利品箱复用原 32745 家族名，18 张表的来源提示使用原 `loot.*`，已生成战利品的物品状态不再宣传未开启内容。

原英文存在、原中文缺失时，身份导入器仍将英文固定到 `english_source.json`，并标记 `chinese_source_missing: true`。语言门禁核对该原键确实不在用户补丁中、没有相冲突的中文别名，且中文暂用完全相同的英文；不能用这个标记绕过已有原译文。报告将此类条目单独计数，不将其当成汉化完成。
