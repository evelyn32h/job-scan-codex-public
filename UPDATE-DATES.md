# Date Filtering Update

## First run: backfill publication dates for existing jobs
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -FetchOnly
```
Re-fetching backfills dates for jobs still returned by the source. Existing scores, status, and `first_seen` are preserved; dates for old jobs that no longer reappear may remain unknown.
Jobs with unknown dates are kept separately — the real publication date cannot be inferred from `first_seen`.

## Phase 1: last 7 days
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -ScoreOnly -Days 7 -MaxJobs 20
powershell -ExecutionPolicy Bypass -File .\Open-Review.ps1
```
Re-running the scoring command continues scoring unscored jobs within that window; it won't re-consume already-scored jobs.
The dashboard defaults to the last 7 days, minimum score 75, hiding applied/rejected/reviewed jobs; you can lower the minimum to 65 or remove it to see candidates/pending jobs.
A batch of 20 is just a quota control, not proof all recent jobs are done; only `eligible pending batch: 0` means there are no pending jobs left in that window (when `auto_score` is enabled).

## Phase 2: last 30 days
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -ScoreOnly -Days 30 -MaxJobs 20
```
Set the dashboard date filter to the last 30 days. Already-scored/processed jobs are not re-scored; previous 7-day scores are kept.

## Daily at 14:00
First confirm manual fetch and scoring succeed, then run:
```powershell
powershell -ExecutionPolicy Bypass -File .\Install-Schedule.ps1 -Time '14:00'
```
Each day, all configured sources are fetched, merged by link, and only unscored jobs from the last 7 days are scored, newest first. Default 20 per run (`max_jobs_per_run` in `preferences.toml`); any excess continues next time.
This also keeps the recent backlog from failed runs/shutdowns, not just same-day postings. A backlog older than 7 days needs manual handling with `-Days 30`.
The default scheduled time is now 14:00, in the Windows local timezone; requires the computer on and the user logged in.
This only fetches and scores — it never submits applications automatically. Re-running the installer updates the existing scheduled task under the same name.

## Limitations
The dashboard's "found today" is based on first-seen date, not actual publication date. The very first batch of jobs may all show as found on the same day.
Jobs past their explicit deadline are hidden; a missing deadline doesn't guarantee a job is still open — check the original link before applying.
Company career-page sources without a date won't enter the 7/30-day window; view them under "All dates (including unknown)". Per-company date backfill is not implemented.
Boundaries are calculated by local calendar date: last 7 days = publication date 0–7 days ago, last 30 days = 0–30 days ago.
A score of 75+ is only the model's judgment, not an interview probability — review results and calibrate first.
