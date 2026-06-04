Set-Location -LiteralPath $PSScriptRoot

$codexPython = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (Test-Path -LiteralPath $codexPython) {
    & $codexPython run_app.py
} else {
    python run_app.py
}
