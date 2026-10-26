$ErrorActionPreference = 'Stop'

$condaExecutable = 'C:\Users\Fatima\miniconda3\Scripts\conda.exe'

if (-not (Test-Path -LiteralPath $condaExecutable)) {
    throw "No se encontro Conda en $condaExecutable"
}

(& $condaExecutable 'shell.powershell' 'hook') | Out-String | Invoke-Expression
conda activate video-motion

Write-Host "Entorno activo: $env:CONDA_DEFAULT_ENV"
python --version

