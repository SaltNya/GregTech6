# 第五十六批：电池盒真实物品充放电

## 实现

- 新增 content/energy/BatteryBoxEnergy，独立管理工作缓冲、每 tick 接收预算、逐槽充放电和输出模式。普通电池盒仍复用已有注册 ID 和四槽 GUI，非电池盒能源节点不走这套逻辑。
- 电池盒接受实际 IItemEnergy 物品，不再接受灌注电芯。第五十四批 25 种化学电池可放入，实际充放电取决于额定电压；电动工具可充电，但不能反向供电。
- 每秒（世界时间 %20==1）按原版 buffer/(input*40*slotCount) 的区间 0/1/6/7 向物品请求抽取/注入 40/20/20/40 包，其它区间不交换。物品自身的包数量限制仍生效，例如 LV 化学电池单次最多 32 包。
- 工作缓冲上限为 input*320*slotCount，与电池容量分开；取出物品不再裁剪缓冲。每 tick 输入预算按理论可充电物品数量计算，保留原版最后一包预算规则，模拟不修改数据，巨大 amount 使用除法避免乘法溢出。
- 前面输出，其余面输入；输出包大小固定，数量取决于可放电电池数量和 0–15 模式。停止状态禁止输出，保留充电；禁止任意拉取重复取电。
- 接通 MachineControl.Provider，现有控制转发器可读取/修改模式、启停和进度。直接贴控制覆盖板的宿主接口还需后续接线，没有宣称本批已经支持直接贴板。
- Jade 的储能值与容量来自槽内物品，工作缓冲另外保存。取出、掉落、存档分别保留电池 NBT 和工作缓冲，模式/停止状态也保存。
- 过压使用项目现有机器爆炸配置；模拟过压不改世界。此次未做真实爆炸强度的原版完整对齐测试，不将其列为已完整验证项目。

## 物品能源接口和工具

IItemEnergy 增加理论 canEnergyInjection/canEnergyExtraction 查询，独立于剩余电量。化学电池按各自电压范围实现。旧通用 BatteryItem 保留历史电压行为（尚未等同原版化学电池），修正乘法溢出和非法电量 NBT；它的完整电压规则仍待归并。

GT6 MultiItemTool.getEnergyStats 调用 EnergyStat.makeTool(...,64,...)，makeTool 的 mCanDecharge=false。电动工具据此改成最多 64 个输入包、对应电压范围、只充不放；不足一个输入包的剩余容量按原版接受末包并丢弃溢出。正常工具使用仍消耗内部能量。

纠正了两个旧测试的错误假设：电钻可以无限包充电并反向发电、LV 电钻可以接受 128 EU。保留并更新材料 NBT、容量、工具使用耗电和打开 GUI 时电量同步等原有检查。

## 原版定位

- gregapi/tileentity/energy/TileEntityBase10EnergyBatBox.java:105-197：定期均衡、数量能力、输入预算和缓冲。
- 同类后续方法：输入/输出面、储能统计、模式/停止、固定槽位。
- gregapi/tileentity/energy/TileEntityBase08Battery.java:228-229：理论能力不检查电量是否满/空。
- gregapi/item/multiitem/MultiItemTool.java:378-383，energy/EnergyStat.java:64-85：工具只充不放、64 包及末包规则。

## 验证

compileJava 通过。新增 BatteryBoxEnergyTests 四项，覆盖原版缓冲区间、理论能力与电压/输入预算/模拟、真实相邻能源节点输出/模式/停止、Jade 取值及取出/存档/实际破坏保电。

完整门禁在 build/gametest-batch56-battery-energy 新世界完成：2026-09-28 04:15:13 **998/998 required tests passed**，Gradle 退出码 0，BUILD SUCCESSFUL in 8m 57s。日志 build/gametest_batch56_battery_energy.log 无 failed! 或 Parsing error；Java 和资源在整个运行期间冻结。

## 手工验收

1. 重启 runClient，放 LV 电池盒，插入完整 LV 化学电池；灌注电芯应不能再放入。旧存档已经塞进去的电芯保留且可取出，但不提供容量或电量。
2. 输入 EU 给空电池充电；等工作缓冲达到充电区间后，约每秒更新一次物品电量。不是每包立即写入物品。
3. 满电电池接电池盒前方的用电设备可供电。两颗同电压电池比一颗允许更高安培；错误电压电池不参与充放电。
4. 取出电池、关开 GUI、退出重进、拆掉电池盒，确认物品电量保留。Jade 显示物品能量总和，可能与工作缓冲不同。
5. 放 LV 电钻只能充电，不会给设备供电；用 LV EU 测试，不能再用 128 EU。

## 明确剩余

大型十六槽版本、全十档系列注册与生存配方、直接控制覆盖板、原版空/满/工作纹理状态和对应 Tooltip 尚待补齐。当前普通电池盒资产生成器已使用 energystorages/battery_electric，Java spec.texture 仍指向 advanced battery 路径，后续应统一并接原版 overlay_active/overlay_blinking；不能只修改资源后宣称状态模型完整。未进行客户端目视验收。

整个移植目标仍在进行。本轮不构建 jar，没有执行 git commit。

## 文件清单

新增 `content/energy/BatteryBoxEnergy.java`、`gametest/BatteryBoxEnergyTests.java`。修改 `api/energy/item/IItemEnergy.java`，三个物品类 `ChemicalBatteryItem`、`BatteryItem`、`ElectricToolItem`，`EnergyNodeBlockEntity`、`EnergyNodeBlock`、`EnergyNodeDefinitions`，以及 `BatteryBoxInventoryTests`、`ElectricToolAssemblyTests`、`ChargingCraftingRepairTests`。本批没有修改纹理或模型资源。

最终审计已刷新 porting-progress.json，日志 build/audit_batch56.log，缺失 token 仍 49。最新 Java 修改时间 2026-09-28T04:06:44，早于最终门禁日志 2026-09-28T04:15:42。注册统计不等同功能完整度。
