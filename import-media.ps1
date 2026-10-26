param(
    [Parameter(Mandatory = $true, Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$Paths,
    [string]$Collection,
    [switch]$NewCollection
)

$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$condaExecutable = 'C:\Users\Fatima\miniconda3\Scripts\conda.exe'

if (-not (Test-Path -LiteralPath $condaExecutable)) {
    throw "No se encontró Conda en $condaExecutable"
}

$arguments = @("$projectRoot\src\import_media.py")
if ($NewCollection) {
    $arguments += '--new-collection'
} elseif ($Collection) {
    $arguments += @('--collection', $Collection)
}
$arguments += $Paths

& $condaExecutable run --no-capture-output -n video-motion python @arguments

exit $LASTEXITCODE
