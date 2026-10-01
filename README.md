# GregTech 6 Integrated

目标：将 saltnya、brokestar233 和 masson 的三个移植项目整合为共享核心，同时支持 **Minecraft 1.20.1 Forge** 与 **1.21.1 NeoForge**。

当前优先按用户要求对齐 1.20.1 Forge 与 1.21.1 NeoForge（D011）。Forge 保留 saltnya 内容基线及已吸收改动；NeoForge 已逐系统接入大部分原注册、机器、物流、世界生成和原有配方，可选 JEI/Jade 现已补齐 Native 源码适配并完成一次主菜单启动；实际配方界面/HUD、客户端资源与完整玩法/存档验收仍有缺口。暂停新增三源差异融合；原始文档中的完成率不代表本项目结果。

两版模组名称统一为 **GregTech 6 Integrated**，加载 ID 为 **gregtech6**；现有内部注册/资源命名空间 `gregtech:` 保留。

## 构建

详细的双版本构建命令、项目结构与 Git 历史恢复/上传步骤见 [BUILDING.md](BUILDING.md)。当前为一个仓库中的 Forge 平台、NeoForge 平台和共用 `core`，不是两个完全独立的项目。

Gradle wrapper 8.8 使用 Java 17 启动；core/Forge 编译为 Java 17，NeoForge 使用 Java 21 toolchain。准备两套 JDK，并可设置 `JAVA17_HOME` 和 `JAVA21_HOME` 为安装目录（不是 bin）。依赖固定为 Forge 47.4.20、NeoForge 21.1.243；无可选模组作为玩家必需前置的新增承诺。

Windows：

```powershell
./scripts/build.ps1 -Target all
```

可用 `-Target forge` 或 `-Target neoforge` 分开执行；`-CheckEnvironmentOnly` 只检查 JDK，不启动构建。

其他系统显式设置 Java 环境后运行：

```sh
export JAVA_HOME="$JAVA17_HOME"
./gradlew --no-daemon :core:check :build
./gradlew --no-daemon :core:check :neoforge:build
```

两个调用串行执行。Forge最终 `distributionJar` 位于 `build/libs/`（重混淆平台中间件在`build/forge-intermediates/`），NeoForge jar 位于 `neoforge/build/libs/`。`core:check` 实际运行独立行为合约；原项目的普通 `test` 不会自动执行所有 main 合约或游戏测试。验包用Python3.11+执行`tools/integration/verify_artifacts.py`，检查两包与当前完整core一致；开发启动和成品启动/玩法各自记录。

## 继续开发与验证

- [阶段和验收合同](docs/integration/PLAN.md)、[当前状态](docs/integration/STATUS.md)、[验证账本](docs/integration/VERIFICATION.md)。
- [三源差异](docs/integration/COMPARISON.md)、[取舍记录](docs/integration/DECISIONS.md)、[来源与贡献](docs/integration/SOURCES.md)。
- [共享核心提取](docs/integration/CORE_EXTRACTION.md)、[NeoForge 平台迁移](docs/integration/NEOFORGE_PORT.md)、[协作说明](docs/integration/COLLABORATION.md)。
- 来源文件树保留在用户指定的 `../Libs`。`python tools/integration/verify_sources.py --list` 校验清单；不加 `--list` 会完整读取来源核对其未被改动。
- `.github/workflows/build.yml` 包含双版本构建矩阵及共享核心合约，没有自动发布。远程仓库尚未设置为新项目的 origin。

## 归属与发布状态

三份目录均未携带.git。已恢复brokestar和masson可获得的原始历史，逐文件匹配到准确原提交，并保留其作者信息与source/*标签；saltnya仍是原字节导入快照，原始仓库/历史待提供。本地导入提交不冒充原作者历史；上游远程不作为新项目origin。

保留原始许可证与各分项素材授权。saltnya 模组授权范围仍待核实，根 `LICENSE.txt` 目前是继承的 Forge MDK 文本，不能据它推定整个模组获得 LGPL 授权。详见 [许可证核查](docs/integration/LICENSE_REVIEW.md)。当前产物用于本地开发验证；公开发布须完成授权核查、双版本玩法及真实存档重载验收。
