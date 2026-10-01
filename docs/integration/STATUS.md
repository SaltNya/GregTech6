# 整合状态

更新：2026-10-02。Goal active。当前工作目录为 `F:\Dev\GregtTech6New\GregTech6`；优先对齐 Forge 1.20.1 与 NeoForge 1.21.1，继续采用集中小检查节奏。

- P0：三源审计、全部逐文件清单、项目1副本校验及原始Forge构建已完成；项目1授权和历史仍待用户信息。
- P1：恢复完整后续移植源码，最新两平台构建与 572 个共享 core class 验包通过；NeoForge 当前源码的游戏服务器实际启动及指定青铜/蒸汽动力链通过。客户端旧证据不覆盖当前全部改动，成品生产环境启动仍待验。
- P2：NeoForge 给定设备/原料的煤炭供热、铜锡合金、四次青铜铸锭通过，并验证叠放模具逐次消费 9U 盆内容。生存取得设备与原料、制作工具及 Forge 对应运行流程仍未满足完整验收。
- 世界重载：NeoForge 普通专服独立进程同一世界检查已覆盖铜模具/青铜盆、粉碎机未完成作业继续完成、搅拌机命名库存/流体，以及实际蒸汽动力链的产物和竖直冷凝水保留。不是全部机器、精确热量快照、跨版本或旧存档证明。
- P3–P4：原完整快照的机器、能源、物流、世界生成、渲染、界面与配方移植源码已恢复；各系统的双平台运行、世界持久化和旧存档范围继续逐批补证，不按源码数量声明完成。
- 项目1基线：Forge 1.20.1 / 47.4.20、Gradle 8.8、Java 17，原始构建通过（13m37s）。全部78,768源文件副本SHA-256一致。本地导入标签 import/saltnya-snapshot；不代表玩法或启动已通过。
- 本机 Java 21：用户提供 `.minecraft/runtime/java-runtime-delta`，已执行 `java -version` 和 `javac -version`，均为 Microsoft OpenJDK 21.0.7。
- 原始 Git 历史：提供目录均无.git；已获取 brokestar 3055个提交及masson 202个提交，保留原作者。逐文件Git blob核对：brokestar快照准确对应3118acbf83a84d05fa37d57af1705cf00e423ca9（220275/220275文件），masson对应2ba4e4b60f7a770360b2ec7ca2adad3507ec4a28（61192/61192文件）。本地source/*标签保留对应原提交；项目1远程和原历史仍缺失。
- brokestar 的 ModularUI 子模块目录为空；已从对应原始Git树恢复gitlink ec524db7a5724f8cf3c837436b1ae742c778c62f，并获取其公开原仓历史，保存source/modularui-brokestar-snapshot标签。尚未导入其运行时。
- 授权未决：项目1 `mod_license=All Rights Reserved`，LICENSE.txt 是 Forge MDK 文本；保留原文，待作者明确适用授权。后续发布门禁未通过。
- 双版本开发服务器接线与上述指定 NeoForge 普通专服/世界重载已通过；两版完整客户端、专服玩法、所有状态重载和旧存档迁移仍未满足完整验收。

## 当前任务

1. 修复两版实际玩法阻塞，优先 NeoForge；集中完成一批再编译/短运行。
2. 模具/盆与基础机器指定作业已通过 NeoForge 世界重启；继续覆盖热量、燃料、其他配方状态与 Forge 对应运行。
3. 继续梳理生存链可达性、配方缺口和客户端交互/渲染，补齐两版差异。
4. 保留来源、贡献、许可、历史与未验证范围记录；完整三源整合 goal 保持 active。


## 2026-10-02 / 双语 README 与 Community Edition 名称

用户明确指定新工作目录 F:\Dev\GregtTech6New\GregTech6，并要求英文主 README、可切换的中文版本，以及两版统一名称 GregTech 6 Community Edition。当前用户仓库分支为 main，源提交 f8d76b3b882c74c098b2ffbdddf910711a4fcb01。

已重写 README.md / README.zh-CN.md，包含介绍、目标版本、状态、双版本构建、开发运行、贡献、分项许可和署名。根 mod_name 和 Native 元数据共用根配置；新目录旧入口/事件订阅 ID 同步为 gregtech6，既有 gregtech: 注册、资源与保存身份保留；材料来源存在性查询同步。默认 GameTest 资源命名空间保持原样。BUILDING.md 同步品牌及当前目录名，未更改第三方许可或发布到远程。

一次资源处理 9m 22s 通过，实际生成的两份 TOML 显示名称均为 GregTech 6 Community Edition、modId 与 dependencies 所属 ID 均为 gregtech6；双向语言链接及 18 个本地文档链接检查通过。此批未编译 Java、未重打 JAR、未启动游戏，不能作为玩法/世界重载或完整整合完成证据。回执：verification/community-readme-branding-20261002.json。

原完整整合 goal 继续保留。新仓库由用户重新初始化，当前源树与此前 84be9ccb2e 上传快照存在差异，历史快照仍保存在此前 Git bundle 和聊天 work/gregtech6-identity-build-20261002；后续代码对齐应依据当前源树逐项核实，不假定旧运行证据覆盖新树。

## 2026-10-02 / CI 修复与 0.0.0 双版本产物

改名影响材料来源显示名称，从而使包含该字段的旧完整快照哈希失效。已通过仅恢复旧名称的临时探针核对原始两项哈希，更新改名后基准，保留所有材料字段和断言。Forge CI 任务限定为 `:build`；补回当前 Forge 模具代码引用但缺失的共享规则类。用户要求根版本设为 `0.0.0`。

用户推送的 dbd38be9 已在 GitHub Actions 运行 36903728760 全部通过（4m 43s）。本地双平台构建通过（11m 17s），两最终 JAR 的 89 个共享核心 class、两平台元数据及无重复/测试污染打包检查通过，复制产物校验值一致。交付两个 JAR、双语 Release 说明、校验值与打包记录。详细证据：verification/ci-material-rename-20261002.md。本批未运行游戏，完整玩法、世界重载、旧存档及完整双版本对齐仍未完成。

## 2026-10-02 / 恢复遗漏的后续移植源码

用户指出此前 NeoForge 完整移植产物约 35.9 MB，而上述 5.8 MB 产物仅包含材料系统。已确认当前重新初始化源码树缺少后续适配，并按用户要求从保留的 84be9ccb2e 快照恢复 src/core/neoforge 及配套资源、构建配置、来源记录；保留当前名称、ID、0.0.0、双语 README 和用户文档。恢复后有 Forge 1,117、core 351、NeoForge 941 个 Java 源文件。原历史保留在 recovery/complete-main 本地引用，来源目录未修改。

同步后来修复过的贴图文件名小写规则所对应的材料快照基准；差异探针证明名称与贴图路径大小写之外的原始材料观察字段一致，断言均保留。纯 Java 合约去掉不使用的大型资源 classpath，打包新增按平台选择的关键玩法类门禁。

最终本地构建通过（8m 12s），全部 571 个当前编译核心 class 的双版一致性与关键玩法类、元数据、无重复/测试内容打包检查通过。新 NeoForge JAR 为 35,890,474 字节，含 1,955 class / 73,730 assets / 228 data；旧完整包的全部 1,954 个 class 路径均已恢复。Forge 新 JAR 为 38,527,588 字节。聊天 release-0.0.0 交付目录中的旧产物已替换，校验值及双语说明更新。详细记录：verification/full-source-restoration-20261002.md。

用户报告运行 36909053404 的旧提交 3f0fad2 材料快照失败；本地 92fb199fd 修复该基准，随后的按平台验包类名修复也需推送最新提交。不得把更早的材料预览树 CI 成功当作恢复后源码的验证。此批未运行客户端、服务器、完整玩法或世界重载，整体 goal 保持未完成。

## 2026-10-02 / 恢复后的熔炼运行与存档推进

两平台同步修复叠放模具余料清空/温度判定、盆缺失块输出清空、龙头负高度查找及交叉流道异常锁释放。NeoForge 实际煤炭供热铜锡青铜链及叠放盆九次精确取出通过；普通专服两个独立 JVM 的同一世界重启检查保留铜模具形状/材料/1U 内容及青铜盆 8U 余料。集中双版编译和最后双 JAR 构建通过，571 个共享 class 与平台打包检查通过。来源哈希、完整结果和未验边界见 verification/smeltery-parity-20261002.md / .json 与 core/provenance/smeltery-parity-20261002.json。未完成生存获取、Forge 对应运行、当前客户端视觉、成品安装、全部机器和旧存档验收；goal 继续 active。

## 2026-10-02 / 基础机器库存与配方恢复

两平台六个生产文件同步修复库存待保存标记、物品搬运实际余量、完整流体附加数据与实际填充量记账；复用既有共享搬运引擎，覆盖取物覆盖物和压力阀。NeoForge 普通专服两个独立 JVM 对同一世界运行，读出并完成粉碎机原已消耗输入/64 工作量的作业，保留搅拌机命名铜锭和带 components 的水，并拒绝不同 components 的混合/指定排出。设备、输入、KU 由检查提供，处理 tick 直接调用，不作完整生存/发电链声明。两版构建 4m 3s 和 571 共享类验包通过；覆盖物实际搬运、Forge 运行、当前客户端及旧存档仍待验。记录：verification/machine-io-parity-20261002.md / .json 与 core/provenance/machine-io-parity-20261002.json。Goal active。

## 2026-10-02 / 共享引擎面与实际蒸汽供能

两平台 EngineBaseBlockEntity 委托新的共享 EngineFaceRotation，保持既有能力面约定并修复水平左右/竖直排水的逆映射。Neo 普通专服给定设备/煤炭/蒸馏水，以零热量、零 KU 冷启动，通过真实右键点火、强化锅炉及自动补水/钢管输汽/强化活塞，完成已注册粉碎配方并自动输出到箱子；竖直活塞 200mB 蒸汽回收 1mB 冷凝水。prepare 使用原生 tick sprint 执行 12000 个真实世界 tick，未注能量或手动机器 tick；第二独立 JVM 同一世界读出结果和冷凝水，再运行 200 普通 tick 并保存退出。两版构建与 572 共享类验包通过。完整生存、设备制作入口、Forge 运行、当前客户端、成品安装、完整状态精确快照及旧存档仍未完成。失败准备反馈也保留于 verification/engine-steam-parity-20261002.md / .json；goal active。
