# 整合状态

更新：2026-09-30。Goal active。

- P0：三源审计、全部逐文件清单、项目1副本校验及原始Forge构建已完成；项目1授权和历史仍待用户信息。
- P1：实现进行中。双平台构建、64条core合约、两平台各3项开发GameTests及9类完整core逐字节验包通过（两阶段Forge打包保留manifest/mixin）。两开发客户端主菜单截图视觉通过（Forge首跑超时、重试82566ms成功），Neo普通开发专服启动及存盘退出通过。成品生产环境/两平台同一world重启仍待验。
- P2–P4：未完成，未满足验收。P2完整共享材料模型在隔离分支实施；独立Java17的6154材料断言已通过，Forge调用闭包编译及独立审查进行中。热量/合金源码比较发现三家各有问题，不以来源总体完成度直接判定单项最佳实现。
- 项目1基线：Forge 1.20.1 / 47.4.20、Gradle 8.8、Java 17，原始构建通过（13m37s）。全部78,768源文件副本SHA-256一致。本地导入标签 import/saltnya-snapshot；不代表玩法或启动已通过。
- 本机 Java 21：用户提供 `.minecraft/runtime/java-runtime-delta`，已执行 `java -version` 和 `javac -version`，均为 Microsoft OpenJDK 21.0.7。
- 原始 Git 历史：提供目录均无.git；已获取 brokestar 3055个提交及masson 202个提交，保留原作者。逐文件Git blob核对：brokestar快照准确对应3118acbf83a84d05fa37d57af1705cf00e423ca9（220275/220275文件），masson对应2ba4e4b60f7a770360b2ec7ca2adad3507ec4a28（61192/61192文件）。本地source/*标签保留对应原提交；项目1远程和原历史仍缺失。
- brokestar 的 ModularUI 子模块目录为空；已从对应原始Git树恢复gitlink ec524db7a5724f8cf3c837436b1ae742c778c62f，并获取其公开原仓历史，保存source/modularui-brokestar-snapshot标签。尚未导入其运行时。
- 授权未决：项目1 `mod_license=All Rights Reserved`，LICENSE.txt 是 Forge MDK 文本；保留原文，待作者明确适用授权。后续发布门禁未通过。
- 双版本开发服务器接线已通过；客户端、正常专服、完整玩法、真实世界保存重载、旧存档迁移仍未验证。

## 当前任务

1. 完成整合双jar打包及字节级共享core门禁，修复独立审查发现的验包/CI缺口。
2. 实施开发专用客户端截图/正常退出探针，真实检查画面；另验正常专服。
3. 按P2材料设计实施同一材料模型/注册底层迁移，再打通首条玩法链。
4. 明确公开发布许可和项目1可获得原始历史；保持未验证项未完成。


## 2026-10-02 / 双语 README 与 Community Edition 名称

用户明确指定新工作目录 F:\Dev\GregtTech6New\GregTech6，并要求英文主 README、可切换的中文版本，以及两版统一名称 GregTech 6 Community Edition。当前用户仓库分支为 main，源提交 f8d76b3b882c74c098b2ffbdddf910711a4fcb01。

已重写 README.md / README.zh-CN.md，包含介绍、目标版本、状态、双版本构建、开发运行、贡献、分项许可和署名。根 mod_name 和 Native 元数据共用根配置；新目录旧入口/事件订阅 ID 同步为 gregtech6，既有 gregtech: 注册、资源与保存身份保留；材料来源存在性查询同步。默认 GameTest 资源命名空间保持原样。BUILDING.md 同步品牌及当前目录名，未更改第三方许可或发布到远程。

一次资源处理 9m 22s 通过，实际生成的两份 TOML 显示名称均为 GregTech 6 Community Edition、modId 与 dependencies 所属 ID 均为 gregtech6；双向语言链接及 18 个本地文档链接检查通过。此批未编译 Java、未重打 JAR、未启动游戏，不能作为玩法/世界重载或完整整合完成证据。回执：verification/community-readme-branding-20261002.json。

原完整整合 goal 继续保留。新仓库由用户重新初始化，当前源树与此前 84be9ccb2e 上传快照存在差异，历史快照仍保存在此前 Git bundle 和聊天 work/gregtech6-identity-build-20261002；后续代码对齐应依据当前源树逐项核实，不假定旧运行证据覆盖新树。
