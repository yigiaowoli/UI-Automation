param(
    [ValidateSet('smoke', 'regression', 'admin')]
    [string]$Suite = 'regression',
    [string]$EnvironmentFile = '.env'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { throw 'Run scripts/bootstrap.ps1 first.' }
if (Test-Path (Join-Path $root $EnvironmentFile)) {
    Get-Content (Join-Path $root $EnvironmentFile) | Where-Object { $_ -match '^[^#=]+=' } | ForEach-Object {
        $name, $value = $_ -split '=', 2
        Set-Item -Path "env:$name" -Value $value
    }
}
$marker = if ($Suite -eq 'smoke') { 'ui and p0' } elseif ($Suite -eq 'admin') { 'ui and admin' } else { 'ui' }
& $python (Join-Path $root 'run_ui.py') -m $marker
exit $LASTEXITCODE
