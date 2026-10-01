# GregTech 6 Community Edition

**English** | [简体中文](README.zh-CN.md)

A community integration project bringing GregTech 6 to modern Minecraft, with a shared core and dedicated Forge and NeoForge implementations.

## About

GregTech 6 Community Edition combines work from **saltnya's gregtech6reborn**, **brokestar233's gregtech6**, and **lombinaxmasson's cruciblecraft**. The project uses saltnya's implementation as its initial content baseline while comparing and integrating the strengths of all three ports.

The goal is a coherent, maintainable mod with shared materials, recipes, machines, energy, and logistics, supported by the platform adaptations needed for each Minecraft version.

GregTech 6 centers on technology, resource processing, and industrial progression. This integration focuses on materials and alloys, tools, heat and crucibles, casting, steam, machines and generators, automation, multiblock machinery, and world generation.

## Minecraft Versions

- **Minecraft 1.20.1 — Forge**, targeting Forge **47.4.20**.
- **Minecraft 1.21.1 — NeoForge**, targeting NeoForge **21.1.243**.

Both platforms live in this repository and share the `core` module. Each produces a separate mod JAR with the shared core included. Install the artifact matching your Minecraft version and loader; no separate core JAR is required.

The mod name is **GregTech 6 Community Edition** and its loader ID is **`gregtech6`**. Existing content and resource identifiers retain the `gregtech:` namespace.

## Project Status

The project is under active integration. Version parity, the complete survival progression, client behavior, dedicated servers, and world persistence are still being validated. Compatibility with source-project worlds and across Minecraft versions has not been established.

Use separate instances for development builds and back up existing worlds. Progress and known gaps are recorded in the [integration status](docs/integration/STATUS.md) and [verification records](docs/integration/VERIFICATION.md).

## Building from Source

### Requirements

- **JDK 17** for the Gradle launcher, Forge, and the shared core.
- **JDK 21** for NeoForge.
- Internet access for the initial dependency download.

The repository includes **Gradle wrapper 8.8**. Run commands from the repository root. Set `JAVA17_HOME` and `JAVA21_HOME` to your JDK installation directories, and set `JAVA_HOME` to `JAVA17_HOME`.

Windows PowerShell example; replace the paths with your own installations:

```powershell
$env:JAVA17_HOME = 'C:\path\to\jdk-17'
$env:JAVA21_HOME = 'C:\path\to\jdk-21'
$env:JAVA_HOME = $env:JAVA17_HOME
```

### Build the Mod

Forge 1.20.1:

```powershell
.\gradlew.bat --console=plain :distributionJar
```

NeoForge 1.21.1:

```powershell
.\gradlew.bat --console=plain :neoforge:jar
```

Both versions:

```powershell
.\gradlew.bat --console=plain :distributionJar :neoforge:jar
```

On Linux or macOS, set the same environment variables and use `./gradlew` instead of `.\gradlew.bat`. Run `chmod +x gradlew` if necessary.

Final artifacts are written to `build/libs/` for Forge and `neoforge/build/libs/` for NeoForge. Forge's `build/forge-intermediates/` directory contains intermediate output. The mod version is configured in `gradle.properties`.

See [BUILDING.md](docs/work/BUILDING.md) for complete setup, additional build options, and Git handoff instructions.

## Development Environment

Open the repository root as a Gradle project in IntelliJ IDEA or another IDE with Gradle support. Use the appropriate JDK for each module.

Forge development commands:

```powershell
.\gradlew.bat :runClient
.\gradlew.bat :runServer
```

NeoForge development commands:

```powershell
.\gradlew.bat :neoforge:runClient
.\gradlew.bat :neoforge:runServer
```

Run each command separately. Server setup requires acceptance of the Minecraft EULA. The existing Windows helper can also run shared-core checks and build both platforms:

```powershell
.\scripts\build.ps1 -Target all
```

### Repository Layout

```text
GregTech6/
├── src/                  Forge platform code and resources
├── core/                 Shared logic, data, and resources
├── neoforge/             NeoForge platform code and resources
├── gradle/               Gradle wrapper
├── scripts/              Build and development helpers
├── .github/workflows/    Dual-platform CI
└── docs/integration/     Plans, attribution, decisions, and verification
```

## Support and Contributions

Use this repository's issue tracker for bug reports and feature suggestions. Include the Minecraft version, loader version, mod version, relevant logs, and clear reproduction steps in bug reports.

Contributions to code, documentation, translations, testing, and assets are welcome. Preserve original attribution and license notices, explain the source and purpose of changes, and document which platforms were checked. Shared gameplay rules belong in `core`; loader and Minecraft API adaptations belong in the platform modules.

Read the [collaboration guide](docs/integration/COLLABORATION.md), [integration plan](docs/integration/PLAN.md), and [source records](docs/integration/SOURCES.md) before preparing substantial changes.

## License

Project-wide licensing is still under review. The current mod metadata retains the baseline declaration, **`All Rights Reserved`**; it does not replace the licenses of incorporated third-party work.

- **Original GregTech 6:** its code is declared [LGPL-3.0-or-later](https://github.com/GregTech6/gregtech6/blob/master/LICENSE).
- **brokestar233 and masson ports:** their code declares LGPL-3.0-or-later. Original notices are retained in the source records.
- **saltnya port:** the scope of permission for port-specific code and resources remains to be confirmed.
- **Assets:** upstream GregTech 6 default assets are [CC0 1.0 unless otherwise stated](https://github.com/GregTech6/gregtech6/blob/master/src/main/resources/LICENSE.assets). The GregTech logo and its derivatives are [CC BY-NC 4.0](https://github.com/GregTech6/gregtech6/blob/master/src/main/resources/LICENSE.logos). Additional third-party assets retain their own licenses.

The root `LICENSE.txt` is an inherited Forge MDK license document. Applicable licenses and attribution are tracked in the [license review](docs/integration/LICENSE_REVIEW.md). A unified LGPL declaration for this integration has not yet been adopted.

## Credits

- **Gregorius Techneticies and the GregTech 6 team** — original GregTech 6.
- **saltnya** — gregtech6reborn and the initial content baseline.
- **brokestar233** — gregtech6-main and its porting work.
- **Lorbineitte Masson** — cruciblecraft and its porting work.
- Original contributors, translators, artists, and third-party authors identified in retained source notices.

Detailed provenance and available history records are maintained in [SOURCES.md](docs/integration/SOURCES.md) and `core/provenance/`.
