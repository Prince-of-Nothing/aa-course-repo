$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$latexDir = Join-Path $root "latex"
$python = Join-Path (Split-Path -Parent $root) ".venv\Scripts\python.exe"
$miktexBin = "C:\Users\Unknown\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
$pdflatex = Join-Path $miktexBin "pdflatex.exe"

Push-Location $latexDir
try {
    & $python ".\generate_report_assets.py"

    foreach ($report in @("lab3_report.tex", "lab4_report.tex", "lab5_report.tex")) {
        & $pdflatex "-interaction=nonstopmode" "-halt-on-error" $report
        & $pdflatex "-interaction=nonstopmode" "-halt-on-error" $report
    }
}
finally {
    Pop-Location
}
