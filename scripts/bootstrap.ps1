$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $root '.venv\Scripts\python.exe'

if (-not (Test-Path $venvPython)) {
    py -3.11 -m venv (Join-Path $root '.venv')
}
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -e "${root}[test,dev]"
& $venvPython -m playwright install chromium
