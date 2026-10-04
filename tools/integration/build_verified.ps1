param(
    [string]$Gradle,
    [string]$ProductionEnvironment,
    [switch]$PreflightOnly
)
$ErrorActionPreference = 'Stop'
$repoPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
if (-not $Gradle) { $Gradle = Join-Path $repoPath 'work/gradle-runtime/gradle-8.8/bin/gradle.bat' }
if (-not (Test-Path -LiteralPath $Gradle)) { throw 'Pass -Gradle with an installed Gradle 8.8 executable.' }
if (-not $ProductionEnvironment) { $ProductionEnvironment = Join-Path $repoPath 'work/production-smoke.json' }
Push-Location -LiteralPath $repoPath
try {
    $logDirectory = Join-Path $repoPath 'build/preflight'
    New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
    $gradleArguments = @('--offline')
    $localInit = Join-Path $repoPath 'work/emi-local.init.gradle'
    if (Test-Path -LiteralPath $localInit) { $gradleArguments += @('-I', $localInit) }
    foreach ($platform in @('neoforge', 'forge')) {
        $logPath = Join-Path $logDirectory ($platform + '-world-creation.log')
        $runTask = if ($platform -eq 'forge') { ':runClient' } else { ':neoforge:runClient' }
        Write-Host "Starting ${platform}: create a fresh normal world and enter the game. Log: $logPath"
        & $Gradle @gradleArguments '-PdirectCoreClasspath=true' '-PdirectCoreResources=true' '-PclientCreateWorldSmoke=true' '-PclientSmoke=false' '-PclientSmokeTimeout=360' '-PclientSmokeHeap=4g' '-PemiSmoke=true' '-PemiOnlySmoke=true' $runTask *> $logPath
        if ($LASTEXITCODE -ne 0) { throw "$platform preflight Gradle failed; see $logPath" }
        $logText = Get-Content -LiteralPath $logPath -Raw -Encoding utf8
        if ($logText -match 'WORLD_CREATION_SMOKE_FAILED|java\.lang\.NullPointerException|Encountered an unexpected exception') {
            throw "$platform preflight reported an exception; see $logPath"
        }
        $receipts = [regex]::Matches($logText, 'WORLD_CREATION_SMOKE_SUCCESS (\{[^\r\n]+\})')
        if ($receipts.Count -ne 1) { throw "$platform needs exactly one actual world success receipt." }
        $receipt = $receipts[0].Groups[1].Value | ConvertFrom-Json
        if ($receipt.platform -ne $platform -or $receipt.renderedWorldFrames -lt 30 -or $receipt.recipes -lt 1000 -or $receipt.canonicalItemsChecked -lt 1000 -or ($platform -eq 'neoforge' -and $receipt.emiLoaded -ne $true) -or $receipt.legacyBatteryAliasesChecked -ne 5 -or $receipt.chemicalBatteryStackRoundTrips -ne 10 -or $receipt.sourceChemicalBatteriesChecked -ne 25 -or $receipt.sourceLvPoweredAssemblyRowsChecked -ne 20) {
            throw "$platform preflight receipt is incomplete."
        }
        $screen = Test-Path -LiteralPath $receipt.screenshot
        if (-not $screen) { throw "$platform preflight screenshot is missing." }
        $receipts[0].Groups[1].Value | Set-Content -LiteralPath (Join-Path $logDirectory ($platform + '-world-creation.json')) -Encoding utf8
        Write-Host "$platform world creation passed: $($receipt.recipes) recipes, $($receipt.canonicalItemsChecked) canonical item outputs."
    }
    if (-not $PreflightOnly) {
        $buildLog = Join-Path $logDirectory 'dual-assemble.log'
        Write-Host "Both client preflights passed. Building dual artifacts. Log: $buildLog"
        & $Gradle @gradleArguments ':assemble' ':neoforge:assemble' *> $buildLog
        if ($LASTEXITCODE -ne 0) { throw "Dual assemble failed; see $buildLog" }
        & python 'tools/integration/verify_artifacts.py' --forge 'build/libs/gregtech6-1.20.1-forge-0.0.0.jar' --neoforge 'neoforge/build/libs/gregtech6-neoforge-1.21.1-0.0.0.jar' --output (Join-Path $logDirectory 'artifacts.json')
        if ($LASTEXITCODE -ne 0) { throw 'Artifact verification failed.' }
        if (Test-Path -LiteralPath $ProductionEnvironment) {
            $production = Get-Content -LiteralPath $ProductionEnvironment -Raw -Encoding utf8 | ConvertFrom-Json
            & $Gradle @gradleArguments ':productionSmokeJar' ':neoforge:productionSmokeJar' *> (Join-Path $logDirectory 'production-probes.log')
            if ($LASTEXITCODE -ne 0) { throw 'Production startup probes did not build.' }
            foreach ($platform in @('forge', 'neoforge')) {
                $platformBuild = if ($platform -eq 'forge') { 'build' } else { 'neoforge/build' }
                $jarName = if ($platform -eq 'forge') { 'gregtech6-1.20.1-forge-0.0.0.jar' } else { 'gregtech6-neoforge-1.21.1-0.0.0.jar' }
                & python 'tools/integration/launch_production_smoke.py' --platform $platform --minecraft-root $production.minecraft_root --version $production.versions.$platform --java $production.java --jar "$platformBuild/libs/$jarName" --probe "$platformBuild/production-probe/gregtech-delivery-probe-0.0.0.jar" --output (Join-Path $logDirectory ($platform + '-production.json'))
                if ($LASTEXITCODE -ne 0) { throw "$platform distribution client did not reach the title screen." }
            }
        }
        & python 'tools/integration/publish_verified_artifacts.py' --verification-report (Join-Path $logDirectory 'artifacts.json') --output (Join-Path $logDirectory 'publication.json')
        if ($LASTEXITCODE -ne 0) { throw 'Verified artifact publication failed.' }
        Write-Host 'Dual assemble, artifact verification and stable publication passed.'
    }
} finally { Pop-Location }
