# P2 纯热步：独立领域模块，平台尚未接入

日期：2026-09-30。新增 ThermalState/ThermalStep，不修改 Forge BE、入口、正HU接受行为、NBT、合金或相变调度；NeoForge也未接入。共享材料迁移提交为 `ffe109c883`，本热步另作独立提交。

## 来源与选择

热步和混温结构来自 brokestar233 的 `gregapi/util/CruciblePhysics.java:118-127,155-199`；保留 LGPL-3.0-or-later 通知与来源署名，LICENSE/NOTICE原字节保存在 `core/provenance/licenses/brokestar/`。上游作者 Gregorius Techneticies、GregTech-6 Team 来源于原NOTICE和固定源码版权头；未捏造移植作者的提交历史。原NOTICE中其他组件描述属于来源仓库的原记录，不代表本次导入了 ModularUI、logo 或其他组件。

对照[固定 GT6 MultiTileEntitySmeltery 源码](https://github.com/GregTech6/gregtech6/blob/3703e40308c8c030763fd6297dea8b210d2a77b1/src/main/java/gregtech/tileentity/tools/MultiTileEntitySmeltery.java)，采用整数热步、有符号余量与整数质量混温。该raw文件SHA256为 `eaf9b833c4c439a102bb346c6c4e032d88b6d97b823003232f45d185f23597f1`，UTF8物理703行；热步301–313、混温333、HU/CU注入693。网页解析工具会去掉空行，不可将其渲染行号当作GitHub物理行号。

采用项目1的整数 Kelvin 与既有 CrucibleMath；不采用 masson 的 Celsius float 权威状态、零incoming时清除不足1K余量、200摄氏度温度下限，或新的停止tick判定。保留项目1已正确消费所选Reaction的合金执行器；不移入brokestar丢失替代配方身份的 applyAlloy。相变目标和服务器调度顺序仍是下一阶段独立决策。

许可证记录仅覆盖新适配热算法的来源；其他来源的待决授权仍保留，本文件不将整个项目重新授权。来源文件哈希、许可副本哈希、新文件哈希和算法边界在 `core/provenance/thermal-extraction.json`。

## 不可变状态与生命周期

`ThermalState(long temperatureK,long previousTemperatureK,long energyHU,int cooldownTicks)` 保存权威整数Kelvin、有符号能量及原倒计时。所有long能量值可表示，包括合法累加或加载的Long.MIN_VALUE；不得将负CU余量静默清零。负倒计时作为已到期legacy状态接受，advance按原规则将其规范到10。

`advance(state,ambientK,totalMassKg)` 只运行热步，totalMassKg由平台提供壳体加内容的真实质量。转换次数按Java signed整数除法取整，支付整转换能量后保留正/负余量；有转换重设100tick，否则到期后每10tick向环境漂移1K，最后保持 min(200K,ambientK) 下限。

前温映射是明确的：旧tick先完成材料/合金等前序规则，再执行 `previousTemperature=temperature` 并进入热步。本API将返回 state's current temperature 作为 previousTemperatureK，不把更早保存的state.previousTemperatureK继续传到下一个热步。`receive` 和 `mix`发生在热步之前，不改变previousTemperatureK；这是旧入料/能源改变当前状态但尚未更新前温的生命周期。平台日后必须在正确调度点调用，不能在一次tick中advance两次。

`receive` 使用 HEAT/COOLING kind决定能量正负，packetSize可为负并取幅值；因此负HU仍加热，负CU仍制冷。方向/能源tag/接收能力/simulation和对世界的操作均不在该API。它不意味着现在Forge坩埚已接受CU。

`mixTemperature`保留 original existing mass（含壳体）和总质量的long截断，再用既有CrucibleMath.units向下缩放；`mix`只更新当前温度，保留前温/余量/cooldown。没有材料添加、容量、熔化/固化/合金/危险副作用，也不把double质量写成另一套材料单位或存档格式。

## 新增输入与溢出政策

这些是新边界政策，不能声称旧GT6已具备，也不能未经记录直接改变现Forge：

- 权威/前温/环境/混温输入Kelvin必须非负；非法输入明确抛IllegalArgumentException。旧损坏负温度存档尚无适配/隔离设计，现Forge加载完全未改。
- 质量必须有限且非负，零质量的热需求仍为1；零总混温质量保留原温。合法小数仍先截断：250.75/175.5kg的比例使用250/426，不用连续浮点平均。
- 正总混温质量低于1kg会产生零整数divisor，新API明确拒绝；大于等于2^63kg、不可表示requiredEnergy、质量和变无限、温差×整质量乘积溢出也明确拒绝，不沿用JVM饱和cast或CrucibleMath的原始乘法溢出。正常含壳体坩埚不受这个亚kg边界影响；现Forge尚未接入，不能称fractional行为已无差异替换。
- packetCount负数拒绝；packetSize=Long.MIN_VALUE的幅值不可表示、幅值×count溢出、缓冲加法/温度加法溢出抛错，不饱和、不反转HU/CU。累加恰好到Long.MIN_VALUE的signed缓冲仍合法；再向下溢出才拒绝。immutable输入在失败后原样保留。

正HU正常结果保持项目1；signed非零转换参考原GT6/brokestar，区别于项目1当前 `conversions>0` 分支。将来接入CU必须作为独立的平台行为修正验收，不以“提取”掩盖。

## 执行证据与缺口

ThermalBehaviorContracts执行7组热步与2组混温，共53条固定结果/边界断言：1300K+8HU/250kg→1302K+2HU/cooldown100；2HU余量跨tick保留；CU-8→1298K/-2；HU/CU的负size符号；100/10窗口的连续tick；200K与150K环境floor；非法值与long极端；整数300kg混温797K（不接受CC的796显示结果）和截断250.75/175.5kg混温883K。另保留原bro测试的0/99.99/100/222.222222kg热需求、500K热步501K、同水质量混温400K等固定金样。预期是原代码/报告的明确数字，不在测试里重写待测热算法。

已独立Java17编译执行，53条通过，jdeps仅java.base。core/build.gradle新增thermalBehaviorContracts并挂core:check，运行main/test分开，测试不嵌入发布jar。本轮无需运行游戏；Gradle统一任务与双平台运行由主线继续验证。

```powershell
./core/verify-thermal.ps1 -JdkHome 'C:/Program Files/Java/jdk-17.0.4'
./core/verify-material-baseline.ps1 -JdkHome 'C:/Program Files/Java/jdk-17.0.4'
```

这两个helper每次创建新的GUID输出目录，避免删除或移动源码后被旧class掩盖。既有verify-core.ps1由主线维护其fresh目录补丁，本提交不覆盖它。

尚未验证：平台接入前温时机、真实能源包与余量、受负能量影响的服务器状态、正式机器tick、客户端显示、成品模组与真实存盘重启。纯热步的通过不改变这些状态，不宣布完整玩法完成。
