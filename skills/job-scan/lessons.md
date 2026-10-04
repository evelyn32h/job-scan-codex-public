# Job-Scan Lessons Learned

Operational pitfalls discovered during use. Read before troubleshooting.

## Daily scan has two log streams

`daily_scan.sh` splits output across two logs:

- **launchd stdout log**: captures script's own stdout/stderr — fetch, diff, dedup, gate, merge, render.
- **Run log** (`$RUNLOG`): captures timestamped `log()` entries AND `claude -p` auto-scoring output, which is redirected via `>>"$RUNLOG" 2>&1`.

When verifying whether auto-scoring ran, always check the run log. The launchd stdout log will show no trace of the scoring step because its output is redirected elsewhere.

Both log paths are defined in `daily_scan.sh` and the launchd plist — grep for `RUNLOG` and `StandardOutPath` to find current locations.

## Data file path: ~/Projects/job-scan/output/ is authoritative

`daily_scan.sh`'s actual output directory is `~/Projects/job-scan/output/`, including:

- `job-scan-results.jsonl` (primary data)
- `job-scan-results.md`
- `job-scan-results.html`

`~/Documents/job/job-scan-output/` was an earlier manual-use path and is no longer updated by `daily_scan`. When scoring/querying interactively, always read `~/Projects/job-scan/output/job-scan-results.jsonl`, otherwise the latest scan results will be missed.

In SKILL.md, `PLUGIN_ROOT` = `~/Projects/job-scan/` (i.e. `scripts/`, `output/`, `profile.md`, etc. all live under this directory).

## CERN LD positions have nationality restrictions

CERN Limited Duration (LD) contracts are restricted to citizens of CERN Member States or Associate Member States. Check whether the user's nationality is on the list. If not, cap at ≤15. CERN Fellow/Student programs may not have this restriction — check each posting individually.
