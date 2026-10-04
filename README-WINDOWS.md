# Job Scan — Windows + Codex Edition

Forked from https://github.com/1carusalwayswa/job-scan (MIT license retained).
The new entry point is `scripts/codex_scan.py`; do not use the original Claude `daily_scan.sh` / setup commands.

## Install
1. Install Python 3.11+ (check "Add Python to PATH") and Node.js LTS. Reopen VS Code / PowerShell afterwards.
2. Extract the whole `job-scan` folder to a fixed location, e.g. `C:\Users\<you>\Projects\job-scan`. Don't just copy the `scripts` folder.
3. Open PowerShell in that folder:

```powershell
python --version
node --version
npm install -g @openai/codex
codex login
codex login status
```
Log in with your ChatGPT Plus account — no API key needed, and no token is sent to anyone.
If your system already has `OPENAI_API_KEY` / `CODEX_API_KEY` or a custom provider configured, double-check which Codex account and billing it actually uses.

4. Review `profile.md` for accuracy (fill in your known background; do not include private health or relationship information). Edit `search_config.json` and `preferences.toml` as needed.

## First Verification & Usage
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -FetchOnly
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -ScoreOnly
powershell -ExecutionPolicy Bypass -File .\Open-Review.ps1
```
Local dashboard: http://localhost:8765; close the window or press Ctrl+C to exit.
For a full run afterwards:
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1
```
By default, up to 20 jobs are scored per run in batches of 5; failed batches stay pending and resume next time. Adjust this in `preferences.toml`.
No visa sponsorship / right to work / security clearance are shown as separate flags — they never exclude a job or lower the technical score. Jobs are only hidden when Swedish or EU/EEA citizenship is explicitly mandatory and the candidate doesn't meet it. Citizenship detection is conservative; ambiguous wording may need manual confirmation.
Jobs that explicitly require Swedish are hidden by the existing language gate; consulting/ops/network roles are not hard-excluded by category.
Jobs with a title/summary under 300 characters are kept, capped at score 59, and flagged as unconfirmed. There's currently no generic full-text re-fetch; company career pages need to be adapted and verified one by one.
Source: JobSearch (Platsbanken). `target_companies.json` starts empty — no company is monitored by default. You can configure career pages per the original README; failed fetches are logged as warnings and partial results are kept. LinkedIn, Indeed, Finland-specific APIs, and JobAd Links are not integrated.

## Daily Automated Run (after manual verification succeeds)
```powershell
powershell -ExecutionPolicy Bypass -File .\Install-Schedule.ps1 -Time '07:00'
```
Requires the computer to be powered on and the user logged in; the time follows the Windows local timezone. An expired quota/login may pause scoring.
Log: `output/scheduled-scan.log`. Uninstall: `Unregister-ScheduledTask -TaskName JobScan-Codex`.
If a forced process termination leaves a stale `scan.lock`, confirm no scan is running and delete `output/scan.lock`.
Avoid changing job status in the dashboard while a scan is running (batch saves re-read status, but there's a brief race window on the final write).

## Test Coverage
Automated tests are included: `python -m unittest discover -s tests -v`.
The Python logic has been verified on Linux; Windows PowerShell/Task Scheduler and actual scoring with your Plus account must be verified on your own machine. This does not log in on your behalf, nor is it deployed to your computer.
