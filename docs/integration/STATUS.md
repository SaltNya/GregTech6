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
