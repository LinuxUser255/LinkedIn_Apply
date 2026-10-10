# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Selenium (Chrome-only) bot that searches LinkedIn jobs and auto-submits "Easy Apply" applications. No build step, linter, or test framework is configured yet — current tests are standalone scripts that print results (see Project rules for the target tooling).

## Commands

```shell
# Environment: the project venv is .venv/ (re-run the script after changing requirements.txt)
./setup_venv.sh && source .venv/bin/activate

# Run the bot (must run from repo root: all data/ paths are relative to CWD)
python3 main.py

# Pause/resume a running bot (it polls for data/pause_bot.txt between search URLs)
./control_bot.sh pause|resume|status

# Setup / smoke checks (each is a plain script, run individually)
python3 tests/setup_tests.py        # python, pip, selenium, dotenv present
python3 tests/selenium_test.py      # selenium can fetch a page
python3 tests/LinkedinTest.py       # Chrome profile session is logged in
python3 test_bot_init.py            # LinkedIn() + ChromeDriver start headless
python3 test_dynamic_forms.py       # dynamic_questions.json loads / patterns match
python3 test_follow_company.py      # follow-company checkbox config
```

Tests that touch the browser or `~/.config/LinkedIn_Apply_Profile/` depend on the local machine's Chrome, ChromeDriver, and personal config — they are not hermetic.

## Architecture

Entry: `main.py` → `src.bot.LinkedIn` → `login()` → `generate_urls()` → `link_job_apply()`. All core logic lives in `src/bot/`.

- **`linkedin.py` — `LinkedIn` class** (the bulk of the code). Owns the WebDriver and the whole apply loop:
  - `generate_urls()` uses `utils.LinkedinUrlGenerate` to build search URLs from `config.py` filters (keywords × locations, with experience/date/job-type/remote/salary/sort query params) and writes them to `data/urlData.txt`.
  - `link_job_apply()` iterates search URLs → result pages (`constants.jobsPerPage` = 25) → job IDs → `/jobs/view/{id}`. Per job: skip if already seen, find Easy Apply button, try `try_submit_single_page()`, else `apply_process_multi_step()` (up to 8 modal steps). Stops entirely when LinkedIn's daily Easy Apply limit is detected. Jobs that can't be applied to are "saved for later" on LinkedIn.
  - Each modal step runs `_fill_current_step()`: hardcoded handlers first (`_fill_text_like`, `_upload_resume_if_needed`, `_fill_selects`, `_answer_yes_no` for work auth/sponsorship/W2/relocation, `_ensure_years_fields`, `_handle_follow_company`), then `DynamicFormHandler` for anything left unfilled.
- **`dynamic_form_handler.py` — `DynamicFormHandler`**: config-driven fallback. Scores each unfilled input's surrounding text against keyword lists in `~/.config/LinkedIn_Apply_Profile/dynamic_questions.json` and answers by type (`yes_no`, `dropdown`, `text`, `checkbox`) from a literal `answer`, an `answer_from_config` key in `credentials.json`, or a named `answer_logic` function. Unmatched fields use `fallback_strategies`. Instantiated lazily. Schema and how to add patterns: `docs/DYNAMIC_FORMS.md`.
- **Follow-company prevention**: the bot actively unchecks "Follow company" checkboxes before submit (`_handle_follow_company` and helpers). See `docs/FOLLOW_COMPANY_SUMMARY.md`.
- **`utils.py`**: URL generation, results/fail logging, and the "already applied" set (job IDs regex-scraped from every `data/Applied Jobs DATA - *.txt` and `data/failed_jobs.txt`).
- **`constants.py`**: `botSpeed` (upper bound for randomized sleeps between actions), `jobsPerPage`.

### Configuration — two parallel paths

Settings are read in two different ways; know which one a value goes through before changing it:

1. **`config.py`** reads `~/.config/LinkedIn_Apply_Profile/credentials.json` **at import time** (hardcoded path) into module-level variables (search filters: `KEYWORDS`, `LOCATION`, `EXPERIENCE_LEVELS`, blacklists, `FOLLOW_COMPANIES`, …), falling back to built-in defaults. Used for URL generation.
2. **Environment variables**, used by `LinkedIn` for login, Chrome setup, and form filling (`_env` / `_env_bool`). `LinkedIn.__init__` loads, with later overriding earlier: project `.env` → `$CHROME_PROFILE_PATH/credentials.env` / `.env` → `$CHROME_PROFILE_PATH/credentials.json` (every key copied into `os.environ`).

`DynamicFormHandler` independently reads `credentials.json` and `dynamic_questions.json` from the hardcoded `~/.config/LinkedIn_Apply_Profile/` path. Templates: `.env.example`, `config_forms/credentials.json`. Never commit real credentials.

### Chrome / ChromeDriver

`_init_chrome()` reuses a persistent Chrome user-data-dir (`CHROME_PROFILE_PATH`, sub-profile `CHROME_PROFILE_DIR`) so a logged-in session survives runs. Chrome binary: `CHROME_BINARY` env, else `./chrome-linux64/chrome` if present. Driver lookup falls back through Selenium's default, `chromedriver` on PATH, `./chromedriver`, and common system paths. ChromeDriver must match the Chrome major version. `HEADLESS` env or `config.headless` toggles headless.

### Runtime output (`data/`, gitignored)

`urlData.txt` (search URLs; non-Easy-Apply job URLs are appended for manual follow-up), `progress.json` (resume point: base URL index + page, cleared when all URLs finish), `Applied Jobs DATA - YYYYMMDD.txt`, `failed_jobs.txt`, `pause_bot.txt`. Deleting the results/failed files makes the bot revisit those jobs; deleting `progress.json` restarts from the first URL.

## Project rules

### Python best practices

All code written or modified in this repo must follow this checklist:

@docs/python-best-practies-list.md

How it applies here:
- **Tooling it names isn't installed yet.** Black, isort, flake8, mypy, bandit, pre-commit, pytest, and safety are not configured or in `requirements.txt`. Don't claim to have run them; if a task calls for them, add them to the project explicitly (with config) rather than assuming they exist.
- **Existing code predates the rules** (e.g. bare `except:`, camelCase config names like `experienceLevels`, missing type hints/docstrings, long methods in `linkedin.py`). Apply the rules to code you write or touch; don't mass-refactor untouched code unless asked (YAGNI). Renaming the public names exported from `src/bot/__init__.py` is a breaking change — call it out first.
- **Tests:** new tests go in `tests/` using pytest, written before the code they cover (TDD). Keep anything that drives a real browser or reads `~/.config/LinkedIn_Apply_Profile/` separate from unit tests that can run without them.

### Git workflow (from `docs/workflow.md`)

All changes are made on the `dev` branch. Only when `dev` is in a good state is it merged into `main` — never commit directly to `main`. PRs (including feature branches like `feature/<name>`) target `dev`; `main` is for stable releases only.
