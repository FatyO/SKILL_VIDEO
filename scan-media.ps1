$ErrorActionPreference = 'Stop'

$projectRoot = $PSScriptRoot
$condaExecutable = 'C:\Users\Fatima\miniconda3\Scripts\conda.exe'

if (-not (Test-Path -LiteralPath $condaExecutable)) {
    throw "No se encontro Conda en $condaExecutable"
}

& $condaExecutable run --no-capture-output -n video-motion `
    python "$projectRoot\src\catalog_media.py"

exit $LASTEXITCODE

