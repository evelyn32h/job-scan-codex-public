param([string]$Time = '14:00')
$ErrorActionPreference = 'Stop'
$python = (Get-Command python -ErrorAction Stop).Source
$codex = (Get-Command codex -ErrorAction Stop).Source
# Scheduled process inherits a saved PATH including the npm/Codex installation.
$runner = Join-Path $PSScriptRoot 'Scheduled-Scan.ps1'
$taskPath = $env:PATH.Replace("'", "''")
@"
`$env:PATH = '$taskPath'
`$env:PYTHONUTF8 = '1'
Set-Location '$($PSScriptRoot.Replace("'", "''"))'
& '$($python.Replace("'", "''"))' scripts/codex_scan.py *> output/scheduled-scan.log
exit `$LASTEXITCODE
"@ | Set-Content -Encoding UTF8 $runner
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$runner`"" -WorkingDirectory $PSScriptRoot
$trigger = New-ScheduledTaskTrigger -Daily -At ([datetime]::Parse($Time))
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 45)
$principal = New-ScheduledTaskPrincipal -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName 'JobScan-Codex' -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force
Write-Host 'Installed. Runs while your Windows account is logged in. Remove: Unregister-ScheduledTask JobScan-Codex'
