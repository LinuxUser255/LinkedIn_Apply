# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Selenium (Chrome-only) bot that searches LinkedIn jobs and auto-submits "Easy Apply" applications for one of several user profiles. Aimed at beginners: setup happens through an interactive wizard, not by editing config files. No build step or linter is configured yet (see Project rules for the target tooling).

## Commands

```shell
# Environment: the project venv is .venv/ (re-run the script after changing requirements.txt)
./setup_venv.sh && source .venv/bin/activate
pip install -r requirements-dev.txt   # adds pytest

# Unit tests (no browser/account needed; config in pytest.ini, testpaths = tests/)
pytest
pytest tests/test_setup_wizard.py::test_wizard_requires_email_and_keywords   # single test

# Profiles and running (run from repo root)
python3 main.py setup [NAME]      # wizard: create or update a profile
python3 main.py list
python3 main.py [--profile NAME]  # run the bot; menu if several profiles, wizard if none
./control_bot.sh pause|resume|status NAME   # bot polls data/NAME/pause_bot.txt between search URLs

# Manual smoke scripts (need Chrome, some need the legacy ~/.config/LinkedIn_Apply_Profile/ files)
python3 tests/setup_tests.py; python3 tests/selenium_test.py
python3 test_bot_init.py; python3 test_dynamic_forms.py; python3 test_follow_company.py
```

To exercise the CLI without touching real profiles, set `LINKEDIN_APPLY_HOME` to a temp dir. Don't run the bot against LinkedIn unprompted: it submits real job applications from the user's account.

## Architecture

Entry: `main.py` (argparse: `setup`, `list`, `--profile`) → pick/create a `Profile` → `LinkedIn(profile)` → `login()` → `generate_urls()` → `link_job_apply()`. All core logic lives in `src/bot/`.

- **`profiles.py`**: a profile is `~/.config/LinkedIn_Apply/profiles/<name>/` (`LINKEDIN_APPLY_HOME` overrides the root) containing `profile.json` (all settings, mode 0600), `dynamic_questions.json` (copied once from `config_forms/dynamic_questions.json`), and `chrome/` (that profile's Chrome user-data-dir, which keeps it logged in). Results go to `<repo>/data/<name>/`. `activate(profile)` is what makes a profile live — see Configuration below. `legacy_settings()` reads the pre-profiles `.env` / `~/.config/LinkedIn_Apply_Profile/credentials.json` to prefill a first profile.
- **`setup_wizard.py`**: `SECTIONS` is a declarative list of `Field`s (key, prompt, `kind`, default, choices) — add a profile setting by adding a `Field`. `kind` fixes the stored type: `yes_no` → `"Yes"`/`"No"` strings (used verbatim as form answers by `answer_from_config`), `flag` → bool, `choice`/`multi_choice` → list of strings (`config` code reads `[0]` of single choices). Choice strings must match what `utils.LinkedinUrlGenerate` maps to URL params. I/O is injected (`ask`, `ask_secret`, `say`) for tests.
- **`linkedin.py` — `LinkedIn` class** (the bulk of the code). Owns the WebDriver and the whole apply loop:
  - `generate_urls()` uses `utils.LinkedinUrlGenerate` to build search URLs from `config` filters (keywords × locations, with experience/date/job-type/remote/salary/sort query params) and writes them to `urlData.txt`.
  - `link_job_apply()` iterates search URLs → result pages (`constants.jobsPerPage` = 25) → job IDs → `/jobs/view/{id}`. Per job: skip if already seen, find Easy Apply button, try `try_submit_single_page()`, else `apply_process_multi_step()` (up to 8 modal steps). Stops entirely when LinkedIn's daily Easy Apply limit is detected. Jobs that can't be applied to are "saved for later" on LinkedIn.
  - Each modal step runs `_fill_current_step()`: hardcoded handlers first (`_fill_text_like`, `_upload_resume_if_needed`, `_fill_selects`, `_answer_yes_no` for work auth/sponsorship/W2/relocation, `_ensure_years_fields`, `_handle_follow_company`), then `DynamicFormHandler` for anything left unfilled.
  - `login()`: with no saved password it waits up to 5 minutes for the user to sign in by hand in the Chrome window.
- **`dynamic_form_handler.py` — `DynamicFormHandler`**: config-driven fallback. Scores each unfilled input's surrounding text against keyword lists in the profile's `dynamic_questions.json` and answers by type (`yes_no`, `dropdown`, `text`, `checkbox`) from a literal `answer`, an `answer_from_config` key in `profile.json`, or a named `answer_logic` function. Unmatched fields use `fallback_strategies`. Instantiated lazily. Schema: `docs/DYNAMIC_FORMS.md`.
- **Follow-company prevention**: the bot actively unchecks "Follow company" checkboxes before submit (`_handle_follow_company` and helpers). See `docs/FOLLOW_COMPANY_SUMMARY.md`.
- **`utils.py`**: URL generation, results/fail logging, and the "already applied" set (job IDs regex-scraped from every `Applied Jobs DATA - *.txt` and `failed_jobs.txt` in the data folder). All result files go through `utils.data_path(...)`; never hardcode `data/`.
- **`constants.py`**: `botSpeed` (upper bound for randomized sleeps between actions), `jobsPerPage`.

### Configuration — how settings reach the code

`profiles.activate(profile)` (called by `LinkedIn.__init__`) pushes one `profile.json` into three places, and existing code reads from all three:

1. **Environment variables**: every scalar setting (bools as `"true"`/`"false"`), plus `CHROME_PROFILE_PATH`/`CHROME_PROFILE_DIR` pointing at the profile's `chrome/`. Read by `LinkedIn` via `_env` / `_env_bool` for login, Chrome setup and form filling.
2. **`config` module globals**: `config.apply_settings()` rebinds `keywords`, `location`, `experienceLevels`, `followCompanies`, … (bools coerced with `config.to_bool`). Read them as `config.<name>` at call time — `from .config import x` captures a stale value.
3. **`utils.set_data_dir()`** → `data/<name>/`.

`LinkedIn()` with no profile keeps the legacy path (project `.env` → `$CHROME_PROFILE_PATH/credentials.env`/`.env` → `credentials.json`, and `config` loads `~/.config/LinkedIn_Apply_Profile/credentials.json` at import). `main.py` always uses a profile. Never commit real credentials.

### Browser / ChromeDriver

Two supported browsers, both documented in the README Quick Start: **Chromium** (the maintainer's long-time choice; system install or snapshot zips `chrome-mac/`, `chromedriver_mac64/`, …) and **Chrome for Testing** (zips `chrome-<platform>/`, `chromedriver-<platform>/`). Downloads unzip into the repo root and are gitignored. `chrome_paths.find_browser()` picks: `CHROME_BINARY` env → project-folder Chrome for Testing → project-folder Chromium → installed Chromium (`INSTALLED_CHROMIUM_PATHS`) → `None` (Selenium's default). Driver order in `_init_chrome()`: project-folder ChromeDriver → Selenium Manager (auto-downloads a matching driver into `~/.cache/selenium`) → `chromedriver` on PATH → system paths incl. snap's `chromium.chromedriver`. Driver and browser major versions must match. `_init_chrome()` reuses a persistent user-data-dir (`CHROME_PROFILE_PATH`, sub-profile `CHROME_PROFILE_DIR`) so a logged-in session survives runs. `HEADLESS` env or `config.headless` toggles headless.

### Runtime output (`data/<profile>/`, gitignored)

`urlData.txt` (search URLs; non-Easy-Apply job URLs are appended for manual follow-up), `progress.json` (resume point: base URL index + page, cleared when all URLs finish), `Applied Jobs DATA - YYYYMMDD.txt`, `failed_jobs.txt`, `pause_bot.txt`. Deleting the results/failed files makes the bot revisit those jobs; deleting `progress.json` restarts from the first URL.

## Project rules

### Python best practices

All code written or modified in this repo must follow this checklist:

@docs/python-best-practies-list.md

How it applies here:
- **Tooling it names isn't installed yet** (except pytest, in `requirements-dev.txt`). Black, isort, flake8, mypy, bandit, pre-commit, and safety are not configured. Don't claim to have run them; if a task calls for them, add them to the project explicitly (with config) rather than assuming they exist.
- **Existing code predates the rules** (e.g. bare `except:`, camelCase config names like `experienceLevels`, missing type hints/docstrings, long methods in `linkedin.py`). Apply the rules to code you write or touch; don't mass-refactor untouched code unless asked (YAGNI). Renaming the public names exported from `src/bot/__init__.py` is a breaking change — call it out first.
- **Tests:** new tests go in `tests/test_*.py` using pytest, written before the code they cover (TDD). `tests/conftest.py` restores env vars, `config` globals and the data dir after each test (activating a profile mutates all three) and provides `app_home`/`data_root` temp-dir fixtures. Keep anything that drives a real browser separate from unit tests.

### Git workflow (from `docs/workflow.md`)

All changes are made on the `dev` branch. Only when `dev` is in a good state is it merged into `main` — never commit directly to `main`. PRs (including feature branches like `feature/<name>`) target `dev`; `main` is for stable releases only.
