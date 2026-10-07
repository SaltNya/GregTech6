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

修改原文件基准需要同时更新压缩快照、哈希和绑定，检查译文差异后再生成。现有汉化文件未声明作者/许可，沿用历史来源记录；本次仅在本地保存与核对，未发布。
