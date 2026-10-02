# 验证账本

日期采用 Asia/Shanghai；日志存放于本地忽略的 `work/`，阶段收官时将必要摘要及校验和纳入记录。

## 2026-09-30 / P0

- 读取三源：通过，均存在。
- 项目1复制：工具报告 78,768 个文件、53.04 MiB，失败 0；随后逐文件SHA-256与来源全部一致。
- Java 17：Oracle 17.0.4，实际用于项目1基线 Gradle 构建。
- Java 21：Microsoft OpenJDK 21.0.7；java 与 javac 实测可用，后续NeoForge实际构建与GameTest服务器使用该工具链。
- 项目1原始基线 `gradlew.bat --no-daemon --console=plain build`：通过，13m37s，13项任务执行。日志 `work/baseline-forge-build.log`。`src/test` 的 main 合约没有接入 Gradle test，本次不称其行为已通过。
- 基线 jar `gregtech-1.0.0.jar` SHA-256：`095a11129dc903c7ecf62d85661665bfd47469d1cbee13ecbd1aacc3333b7837`；保存在 `work/artifacts/saltnya-forge-baseline-1.0.0.jar`。这是本地测试基线，授权核查仍未解决。
- saltnya 78,768文件逐文件 SHA-256：全部一致，无缺失/变化。原始导入本地 commit `41561782`，标签 `import/saltnya-snapshot`；该提交不是恢复的原始作者历史。
- 客户端/专服启动、完整玩法、真实存档重载、旧存档兼容：未执行。

## 外部构建条件核对

- Forge 1.20.1 官方文档要求 64 位 Java 17，并建议测试专服：https://docs.minecraftforge.net/en/1.20.1/gettingstarted/
- NeoForge 1.21.1 官方文档要求 64 位 Java 21：https://docs.neoforged.net/docs/1.21.1/gettingstarted/
- 上述是环境要求证据，不是本项目的运行成功证据。

## P1 / 共享核心与平台构建

- 8个纯Java类原字节搬迁，保留包名/调用签名；独立Java17编译、64断言/7组、来源SHA和jdeps java.base检查通过。
- `:core:check :compileJava :neoforge:build`：通过，5m28s，13项任务（11执行/2已有输出）。coreBehaviorContracts真实输出64断言通过；Neo为启动骨架，不含玩法内容。
- 初始Neo jar：13,392字节。后续双jar构建与bootstrap编译通过；仍需严格验包后关联最终校验和。
- 独立审查发现验包和CI只查部分core/metadata的问题，工具已改为全core与当前编译字节/真实TOML/版本依赖门禁，49验包场景和9CI场景通过。CI在授权未决时只允许私有仓上传二进制；公开二进制分发未发生。
- Bootstrap测试属于游戏开发服务器初始化/core接线验证，不能代替正常专服、客户端、核心玩法、真实世界重启。
- 后续 `:core:check :build :neoforge:build :compileBootstrapGameTestJava :neoforge:compileBootstrapGameTestJava`：通过，8m18s，24任务（13执行/11已有输出）。两平台jar及独立bootstrap源码编译通过。
- Neo首次 `:neoforge:runGameTestServer`：在资源处理失败（20s），默认sourceSet资源目录被再次srcDir添加导致test_empty.nbt重复。去掉重复目录配置，保留FAIL门禁后重跑。
- Neo重跑：通过（3m51s），3项required GameTests成功，实际服务器初始化/core调用/正常退出已验证。日志 `work/p1-neoforge-bootstrap-runtime-retry1.log`，测试通过日志时间20:43:29；不作为正式专服或玩法验收。
- Forge首次 `:runGameTestServer`：资源下载阶段SocketTimeoutException，57项资源失败，游戏尚未启动。`prepare_assets.py`校验3575对象并从已验证Neo缓存复用缺失57项（0额外下载/0错误），不关闭TLS或哈希校验。日志 `work/p1-forge-asset-recovery.log`。
- Forge重跑：通过（3m），3项required GameTests成功；实际同步38813运行时配方，服务器正常保存测试世界并退出。日志 `work/p1-forge-bootstrap-runtime-retry1.log`。这不是同一存档重启或完整配方玩法证明。
- 严格验包初次失败：Forge的9个core class字节与当前core编译不同，Neo一致。独立classfile语义检查证实9类指令/描述符/属性值相同，仅常量池/属性顺序重排及两个未引用Long项删除。仍保持SHA门禁，改用`jar`平台中间件→`reobfJar`→`distributionJar`追加原core，复验进行中。详见P1_REVIEW.md。
- 两阶段Forge打包 `:distributionJar :core:check`：通过，4m19s。最终严格验包通过9个当前core类，两平台逐字节一致、真实TOML/依赖/版本一致、无重复或测试条目。Forge中间件无core；最终与中间件完整manifest字节相同（含MixinConfigs），mixin与refmap也相同。最终Forge 38,105,750字节/80,435 ZIP条目（Zip64），SHA-256 `11c2483c39686b1d3878338fc5ebabf1555aa111670f2054b8d245857ce48cec`；Neo 13,392字节，SHA-256 `c7a8f0d1fcf0012abf9af487df5970b5ede4010be37bf13cd31f485f40da2dba`。报告在work/p1-artifact-verification.json与p1-forge-distribution-boundary.json，只代表该P1快照。

## P1 / 开发客户端和普通专服

- 独立两平台客户端探针编译：通过，38s。源集不进入生产jar；默认关闭，显式参数才截图/退出。
- Neo `:neoforge:runClient -PclientSmoke=true`：通过，38s，主菜单真实绘制149帧，8034ms后原版后台写完截图并正常退出。1280×720 PNG SHA-256 `320fddd04b5e23310b9fc66f8381f841dabf939cf95f22aca9c03d31aeb3a8ed`；主会话实际查看图片，主菜单/文字/背景正常。严格日志/PNG结构/CRC/解码验收通过，日志work/p1-neoforge-client-smoke.log。未进世界，未验证Neo内容渲染或成品jar加载。
- Forge首次客户端：失败，120s探针超时；即使Gradle输出BUILD SUCCESSFUL/退出0，verify_client_smoke.py也正确拒绝。有实际资源atlas、配方和成就加载记录，未获得主菜单截图。不把加载日志当视觉通过。失败日志work/p1-forge-client-smoke.log；新增当前screen/overlay诊断和30–300s有界超时参数，以240s重试。
- Forge客户端240s上限重试：通过，Gradle2m11s，实际82566ms/152帧后保存1280×720截图并正常退出，未用满240s。主会话实际查看主菜单/文字/背景正常；严格机器验收通过。PNG SHA-256 `c97b7750d10cc1c5d8750a89dbc9410b662a3d00f2e2a66b952a0d9e13f37e46`，日志work/p1-forge-client-smoke-retry1.log；仍是开发源集环境，不是成品jar或模组世界内渲染证明。
- 客户端测试选项只写各自build/client-smoke-run/options.txt（跳过首次辅助功能介绍、静音），未改用户.minecraft选项。不是生产EULA接受。
- Neo普通开发DedicatedServer实际启动：版本1.21.1，Done(4.147s)，创建真实world，随后正常保存三维度并退出。日志work/p1-neoforge-dedicated-first-start.log（Gradle6m57s含人工检查窗口）。首次运行没有保留stdin，停止时用仅针对已核对PID及隔离工作目录的JDK attach请求server.halt(false)，服务器自行存盘退出；后续使用有限自动停服探针。未测试同一world重启或GT机器状态。
- Neo官方本机源证据：SharedConstants IS_RUNNING_IN_IDE为非production，Eula构造以IDE或GameTest条件短路。因此普通开发专服也无需readFile生成eula.txt；本会话未写eula=true，不能把这种开发启动当成生产专服EULA同意。生产成品加载、Forge普通专服、实际世界重启及完整玩法仍待验证。

## 原始历史匹配

- brokestar当前远程HEAD f009fc3c与用户快照不同（1123文件变化/1077缺失），没有错误关联为同一版本。通过来源PROJECT_STATE blob追溯，快照的220275文件全部字节吻合3118acbf83a84d05fa37d57af1705cf00e423ca9；gitlink单独记录ec524db7a5724f8cf3c837436b1ae742c778c62f。
- masson快照61192文件全部字节吻合2ba4e4b60f7a770360b2ec7ca2adad3507ec4a28。
- 对比结果保存在provenance/*history*match.json；对应完整原历史和作者信息在本地Git upstream-* refs及source/*标签中。上游remote不是新项目origin。


## 2026-10-02 / 双语 README 与 Community Edition 名称

用户明确指定新工作目录 F:\Dev\GregtTech6New\GregTech6，并要求英文主 README、可切换的中文版本，以及两版统一名称 GregTech 6 Community Edition。当前用户仓库分支为 main，源提交 f8d76b3b882c74c098b2ffbdddf910711a4fcb01。

已重写 README.md / README.zh-CN.md，包含介绍、目标版本、状态、双版本构建、开发运行、贡献、分项许可和署名。根 mod_name 和 Native 元数据共用根配置；新目录旧入口/事件订阅 ID 同步为 gregtech6，既有 gregtech: 注册、资源与保存身份保留；材料来源存在性查询同步。默认 GameTest 资源命名空间保持原样。BUILDING.md 同步品牌及当前目录名，未更改第三方许可或发布到远程。

一次资源处理 9m 22s 通过，实际生成的两份 TOML 显示名称均为 GregTech 6 Community Edition、modId 与 dependencies 所属 ID 均为 gregtech6；双向语言链接及 18 个本地文档链接检查通过。此批未编译 Java、未重打 JAR、未启动游戏，不能作为玩法/世界重载或完整整合完成证据。回执：verification/community-readme-branding-20261002.json。

原完整整合 goal 继续保留。新仓库由用户重新初始化，当前源树与此前 84be9ccb2e 上传快照存在差异，历史快照仍保存在此前 Git bundle 和聊天 work/gregtech6-identity-build-20261002；后续代码对齐应依据当前源树逐项核实，不假定旧运行证据覆盖新树。


## 2026-10-02 / NeoForge 成品专服

交付的 bc89c7201 生产 JAR 用官方安装的 NeoForge 21.1.243 和用户 Java21 独立加载，两个不同 JVM 正常保存/停服，铜原矿库存和青铜粉碎机实际保存身份读取通过。控制台放置不视作生存玩法，外部 Addon 未安装，Forge 成品和两版成品客户端仍待验。生产源码与二进制本批不变，不重复大资源构建。见 [验证回执](verification/installed-neoforge-20261002.md)。
