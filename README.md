# job-scan — Windows + Codex Edition

Automated job scanning and LLM-powered scoring for IT positions in Sweden.

This fork fetches jobs from the Swedish JobTech API and target company career pages, scores them against your profile using the **[Codex CLI](https://github.com/openai/codex)** (ChatGPT Plus login, no API key needed), and supports fully unattended daily runs on Windows via Task Scheduler.

> Forked from [1carusalwayswa/job-scan](https://github.com/1carusalwayswa/job-scan) (MIT licensed), which is a Claude Code plugin for macOS/Linux. This fork replaces Claude Code with the Codex CLI and runs on Windows. The original Claude Code / macOS-Linux workflow is preserved near the bottom of this file for anyone who prefers that setup.

## Install & Usage (Windows + Codex)

Full step-by-step instructions, including first-run verification and daily scheduling, are in **[README-WINDOWS.md](README-WINDOWS.md)**. Summary:

- **Prerequisites:** Python ≥ 3.11, Node.js LTS, the Codex CLI (`npm install -g @openai/codex`, then `codex login` with a ChatGPT Plus account).
- **Run a scan:** `powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1`
- **Review results:** `powershell -ExecutionPolicy Bypass -File .\Open-Review.ps1` → http://localhost:8765
- **Daily automated run:** `powershell -ExecutionPolicy Bypass -File .\Install-Schedule.ps1 -Time '07:00'`


## Alternative: Original Claude Code Workflow (macOS/Linux)

> Everything below this point describes the **original upstream** project ([1carusalwayswa/job-scan](https://github.com/1carusalwayswa/job-scan)), which uses Claude Code on macOS/Linux instead of Codex on Windows. If you're using this fork as intended, you don't need anything in this section — see [README-WINDOWS.md](README-WINDOWS.md) instead.

### Prerequisites

- **Claude Code** CLI (with an active plan or API key)
- **Python ≥ 3.11** (uses `tomllib` from the standard library)
- **macOS** or **Linux** (for automated scheduling)

### Install

```bash
# Option 1: as a Claude Code plugin
claude plugin install https://github.com/evelyn32h/job-scan-codex-public

# Option 2: manual
git clone https://github.com/evelyn32h/job-scan-codex-public ~/.claude/plugins/job-scan
```

### Quick Start

```
/job-scan setup
```

The interactive setup will:
1. Generate your `profile.md` (background, skills, experience)
2. Generate `preferences.toml` (language ability, eligibility, gate toggles, schedule)
3. Generate `search_config.json` (search lanes and keywords based on your career goals)
4. Optionally generate `target_companies.json` (specific company career pages to watch)
5. Install a daily scheduler (launchd on macOS, cron on Linux)

### Usage

#### Interactive (in a Claude Code session)

```
/job-scan              # Score pending backlog jobs
/job-scan setup        # First-time setup or re-configure
```

In the conversation you can also:
- "Confirm #3" / "Ignore #5" — change job status
- "Apply to #2" — prepare application materials
- "Run a full scan now" — fetch + score from scratch

#### Automated (daily via launchd/cron)

After setup, `scripts/daily_scan.sh` runs daily:
1. Fetches new jobs from JobTech API
2. Runs deterministic gates (language, citizenship, staffing, occupation)
3. Merges into results and renders HTML
4. If `auto_score = true` in preferences, invokes `claude -p` to LLM-score pending jobs

#### Review

Open the HTML dashboard:
```bash
python3 scripts/review_server.py   # http://localhost:8765
```
Or directly open `output/job-scan-results.html` in a browser.

## Project Structure

```
skills/job-scan/SKILL.md      — Skill definition (scoring methodology, flows)
scripts/
  config.py                   — Central path resolution
  codex_scan.py                — Windows/Codex fetch + score entry point
  daily_scan.sh               — Daily unattended scan pipeline (original macOS/Linux + Claude Code)
  setup_scheduler.sh          — Install launchd/cron scheduler (original macOS/Linux)
  fetch_jobtech.py            — JobTech API fetcher
  results_io.py               — JSONL fact-source read/write/merge
  dedup.py                    — Fuzzy dedup against application tracker
  lang_gate.py                — Swedish language requirement gate
  citizenship_gate.py         — Security clearance / citizenship gate
  pre_gate.py                 — Staffing company + occupation group gate
  audit_scores.py             — Post-scoring rule-violation audit
  render_html.py              — HTML dashboard renderer
  review_server.py            — Local HTTP server for status updates
  prep_apply.py               — Prepare application directories
assets/
  staffing_companies.json     — Known staffing/temp agency patterns
  restricted_employers.json   — Security-cleared employer patterns
templates/
  profile.example.md          — Example candidate profile
  preferences.example.toml    — Example preferences with all options
```

User-generated files (gitignored):
```
profile.md                    — Your candidate profile
preferences.toml              — Your runtime preferences
search_config.json            — Your search lanes and keywords
target_companies.json         — Your target company career pages
output/                       — Results (JSONL, Markdown, HTML)
calibration.jsonl             — Scoring feedback for continuous improvement
```

## Scoring Methodology

Scoring follows a **gate → cap → tier** framework:

1. **Deterministic gates** (pre-LLM, zero tokens): language requirements, security clearance, staffing agencies, occupation groups
2. **LLM scoring** reads your `profile.md` and applies:
   - **Cap rules**: senior/lead roles cap at ≤50, missing core stack caps at ≤55, staffing agencies cap at ≤58
   - **Evidence-level verification**: "used it" ≠ "built/debugged it"
   - **Tier anchors**: 80–90 (strong match), 70–79 (good match), 60–69 (partial), <60 (weak)
3. **Calibration loop**: when you mark a score as wrong, feedback is saved to `calibration.jsonl` and used as few-shot examples in future scoring

## License

MIT
