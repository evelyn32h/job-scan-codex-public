param([switch]$FetchOnly, [switch]$ScoreOnly, [switch]$Review, [ValidateSet(7,30)][int]$Days = 7, [int]$MaxJobs = 20)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$env:PYTHONUTF8 = '1'
$scanArgs = @('scripts/codex_scan.py', '--days', $Days, '--max-jobs', $MaxJobs)
if ($FetchOnly) { $scanArgs += '--fetch-only' }
if ($ScoreOnly) { $scanArgs += '--score-only' }
if ($Review) { $scanArgs += '--review' }
python @scanArgs
if ($LASTEXITCODE -ne 0) { throw "Scan failed: $LASTEXITCODE" }
