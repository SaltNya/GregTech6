param(
    [string]$Gradle,
    [switch]$PreflightOnly
)
$ErrorActionPreference = 'Stop'
$repoPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
if (-not $Gradle) { $Gradle = Join-Path $repoPath 'work/gradle-runtime/gradle-8.8/bin/gradle.bat' }
if (-not (Test-Path -LiteralPath $Gradle)) { throw 'Pass -Gradle with an installed Gradle 8.8 executable.' }
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
        if ($receipt.platform -ne $platform -or $receipt.renderedWorldFrames -lt 30 -or $receipt.recipes -lt 1000 -or $receipt.canonicalItemsChecked -lt 1000) {
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
        Write-Host 'Dual assemble and artifact verification passed.'
    }
} finally { Pop-Location }
