# 第七十二批：工具方块自动化接口恢复

## 与完整目标的关系

继续补齐已注册工具方块的实际功能。回查书架、硬币和工具方块时，没有把历史未勾选清单当成当前缺失：这些族已有模型/几何及专属行为。本轮确认 tool 包中的四类方块实体在 Forge capability 生命周期上存在实际缺口，影响卸载/恢复后的自动化。

## 复现

新增 ToolCapabilityLifecycleTests，通过真实注册方块创建方块实体，执行 capability 查询、失效、重复查询、恢复和再次读取内容物。旧实现的完整门禁 build/gametest_batch72_lifecycle_red.log 退出码 1，恰好三项新测试失败：

- 便携容器：失效后查询会自行恢复。
- 混合盆：reviveCaps 后没有新句柄。
- 粉末漏斗：reviveCaps 后没有新句柄。

养蜂箱也持有 final LazyOptional 且没有 reviveCaps；此前同组测试在漏斗处提前失败，不能把这一红色运行误写成已逐个复现所有方块。

## 修改

- ProcessingToolBlockEntity：保留原有 IItemHandler 和流体 handler，在 reviveCaps 重建两个 LazyOptional。库存、罐和输入/输出限制不重建。覆盖混合盆/桌式混合盆、榨汁器、金属与木质浸洗盆及桌式变体，共七种。
- DustFunnelBlockEntity：恢复时为同一粉末库存重建接口。
- BumbliaryBlockEntity：普通/高级养蜂箱恢复时按原有 Layout 重建 AutomationHandler，保留槽位权限。普通只开放死蜂槽，高级另外开放蜂巢槽。
- PortableContainerBlockEntity：构造时提供初始接口，invalidateCaps 标记失效，查询和 setContents 不得提前恢复，只有 reviveCaps 开启新句柄。保留 removed 状态检查与容器物品/NBT 单一存储。

这里的接口生命周期是 Minecraft 1.20.1 Forge 适配工作；没有给 GT6 原版臆造新的自动化权限。

## 测试说明

新三项测试检查旧句柄保持失效、通知 listener、新句柄恢复六面访问、内容物不丢失/不复制，以及失效期间更新容器内容也不能重新开放接口。通过注册表遍历覆盖实际家族，不能只测试默认材质。

第二次验证 build/gametest_batch72_lifecycle_fixed.log 被主动中止，未计为成功。复核测试装置发现榨汁器没有液体输入、普通养蜂箱不能自动抽蜂巢，因此调整测试：榨汁器从存档恢复已有输出液体，普通蜂巢保持手动槽，高级蜂巢允许输出。生产规则未为迎合测试而放宽。中止后确认没有残留测试 JVM，再换新世界。

最终门禁：build/gametest-batch72-lifecycle-verified；日志 build/gametest_batch72_lifecycle_verified.log。10:40:40 全部 1041 项必需测试通过，10:41:11 正常关闭；退出码 0，BUILD SUCCESSFUL（9m9s）。进度审计已刷新 docs/porting-progress.json。

## 游戏内验收

1. 给粉末漏斗放入粉末、让下方小坩埚接收；卸载并重进区块，确认仍能继续输入，不复制库存。
2. 混合盆/浸洗盆放少量水或配方原料，保存退出再进，检查管道仍能访问且数量正确。
3. 普通养蜂箱仍不能自动抽蜂巢，高级可以；恢复接口不应改变这一区别。
4. 放置式杯/壶/量杯等保存后重进，检查液体和容量设置保留，破坏后旧位置不再可访问。

自动测试覆盖显式 invalidateCaps/reviveCaps，不宣称已经代替客户端区块卸载、模组管道缓存和多人服务器兼容实测。本轮未打包 jar，使用重启后的 IDEA runClient 验收。

完整目标仍未完成；客户端板锭/硬币/书架与大型坩埚外观仍待实际验收，占位功能全量核对继续保留。没有执行 git commit。
