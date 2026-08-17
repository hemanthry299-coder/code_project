$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir

$env:PYTHONPATH = Join-Path $repoRoot "src"

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$pythonExe = if (Test-Path $venvPython) { $venvPython } else { "python" }

$testArgs = @()
$smokePath = Join-Path $repoRoot "tests\smoke"
$unitPath = Join-Path $repoRoot "tests\unit"

if (Test-Path $smokePath) {
    $testArgs += $smokePath
}

if (Test-Path $unitPath) {
    $testArgs += $unitPath
}

if ($testArgs.Count -eq 0) {
    throw "No test directories found. Expected at least tests\unit or tests\smoke."
}

Write-Host "PYTHONPATH=$env:PYTHONPATH"
Write-Host ("Running pytest for: " + ($testArgs -join ", "))

& $pythonExe -m pytest @testArgs
