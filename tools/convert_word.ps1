$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath 'output\document\Relatorio_AgroSmart_Fase7.docx').Path
$outputDir = Join-Path (Get-Location) 'output\pdf'
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
$target = Join-Path $outputDir 'Relatorio_AgroSmart_Fase7.pdf'

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $document = $word.Documents.Open($source, $false, $true)
    try {
        $document.ExportAsFixedFormat($target, 17)
    }
    finally {
        $document.Close($false)
    }
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}

Get-Item -LiteralPath $target | Select-Object FullName,Length
