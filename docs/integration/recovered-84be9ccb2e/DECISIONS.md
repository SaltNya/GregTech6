# 实现选择记录

## D001 — 项目1初始基础，功能选择逐系统验证

来源：用户整合要求；三源均为不带 Git 元数据的文件树。

采用项目1完整文件树作为初始工作区。理由是用户将其指定为功能保留基准，而非已证明其每个实现优于其他来源。其他项目保持只读，禁止直接将三套注册和材料框架拼进同一个运行时。

验证：复制工具报告 78,768 文件成功，无失败；SHA-256 一致性检查正在运行。运行功能尚未验证。

## D002 — 保留授权原文，发布许可未决独立记账

来源：项目1 gradle.properties 的 All Rights Reserved、LICENSE.txt 的 Forge MDK 声明；masson 的 LGPL-3.0-or-later 声明；brokestar 许可证待完整审计。

不将 Forge 模板许可证当成模组代码授权，不自行改写第三方许可。可以继续用户授权的本地整合工作；对外发布等待来源授权与署名核实。未决事项已向用户询问。

## D003 — 分阶段建立共享核心

先将已证实不依赖 Minecraft/loader 的领域规则提取到 Java 17 core，两版本嵌入同一输出；Minecraft 类型、注册、能力和 NBT 读写留在平台边界。初始 NeoForge 内容仅覆盖逐步迁入的功能，不称其已达到项目1全功能。每次迁移以行为回归及源码来源记录为门禁。

## D004 — 物质量保持 GT6 精度，转换只发生在平台边界

来源：saltnya `api/material/GTValues.java`、masson `material/GT6ImportUnits.java` 和 `fluid/MoltenTransferMath.java`，详见各源码审计。

优先保留 GT6 的 U=648648000 每锭作为共享物质量单位。masson 的每锭144单位属于其流体/存储边界约定，不直接替换统一领域单位。不可表示的分数必须显式处理或拒绝，不能截断后宣称守恒。温度也要区分项目1的 Kelvin 和 masson 的摄氏度，禁止照搬数值。首阶段保留已有原始算法字节；溢出等缺陷候选另记决策并以行为测试修复。

## D005 — 用户改为快速源码合并

2026-09-30起按用户明确要求暂停构建、测试与游戏启动，整模块迁移并薄适配，新增代码标记未验证；原验收推迟。能源采用saltnya身份/规格及brokestar Gate/FE primitive，统一Tags，不另导入TD/CS材料底层。FE外部EU=4FE、MJ=10FE是整合接线政策，bro原快照主动切除的EU出站dispatch未被当作原有实现；整合版恢复此接口，未经运行确认。原通知/许可及来源SHA保留。


D006 (2026-10-01): User permits one small check after multiple integration batches, with NeoForge priority. Keep source integration fast; use grouped compile checkpoints and fix blocking API errors. Do not restore per-batch full checks or call runtime behavior verified from compilation.


D007 (2026-10-01): Item logistics uses the complete saltnya registration/interaction baseline (126 pipes, 60 normal and 60 queue hoppers) over shared catalogs/control/welding rules and native capabilities/components. Code comparison finds brokestar minimum-step relaxation and masson loaded-only weighted discovery/topology-validated delivery as candidates for the next shared-routing wave; the baseline first-exit BFS is not declared optimal. Neo count >99 is explicitly retained by a template plus gt.pipe_count inside gt.items; old-save/world migration remains unverified. Source recipe omissions and dynamic-handler conservation gaps are tracked in P3_ITEM_PIPES_AND_HOPPERS.md. Grouped checks follow D006.


D008 (2026-10-01): The scoped Neo FIFO checkpoint reproduced a baseline cooldown notification loss at second insertion. Both platforms retain inventory/block wake flags while a cooldown or redstone gate prevents processing, and mark real external extraction as an inventory change. The same FIFO fixture now also checks post-extraction advancement without manual wakeup; corrected-run outcome is recorded separately. brokestar keeps FIFO compaction outside its transfer gate and masson separates transfer/advance; a full shared tick-engine comparison remains pending. No source snapshot or old world is modified.


D009 (2026-10-01): Both platforms replace first-exit BFS with shared stable weighted relaxation (brokestar), loaded/accepting endpoint discovery and confirmed remainder accounting (masson), retaining saltnya identities and lifecycle. Cache/reservation topology is not adopted. Platform loader JSON is kept outside core after an actual native client failure; original Forge bytes and author/license records remain preserved. Scoped native weighted transfer and TitleScreen pass with explicit resource gaps; broader gameplay/reload remains pending. See P3_SHARED_ITEM_ROUTING.md.


D010 (2026-10-01): User explicitly requests the fastest possible merge, prioritizing buildable/runnable integration. This supersedes D006 scheduling: necessary grouped compilation and short startup only; no new subsystem-specific test fixtures or frequent validation. Preserve source attribution and track deferred gameplay/rendering/reload/old-save/release acceptance independently. Final objective remains active until its full scope is achieved.


D011 (2026-10-01): 用户明确要求“先只对齐1.20.1和1.21.1版本”。当前先以现有1.20.1 Forge源码及实际接线为基准补齐1.21.1 NeoForge功能和资源，暂停新增brokestar/masson差异融合；已合入的改动保留。忽略区彩色owned泡沫脚本尚未执行，未修改正式Java/资源。双版本对齐是当前优先阶段，原完整三源goal仍active，后续三源差异/验收不宣称完成。必要集中编译与短启动延续D010。


D012 (2026-10-02): 用户明确要求两版名称 GregTech 6 Integrated、加载 ID gregtech6，并准备 GitHub 上传包。统一根元数据及共享 Java 入口/订阅身份；现有 gregtech: 内部注册和资源 ID 保留，平台查询映射保留原材料来源前缀。此决定区分加载身份与保存/资源身份，不宣称旧存档兼容已验证。产物前缀与构建文档同步，保持单仓库共享 core，不改第三方授权、不设置或推送远程。详见 MOD_IDENTITY.md。
