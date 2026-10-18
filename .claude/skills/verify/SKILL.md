---
name: verify
description: Full verification loop before claiming work is done - lint, format, strict types, tests with coverage, Django system and deploy checks, missing migrations, security lint, and a real end-to-end check against a running dev server.
when_to_use: After finishing a feature, fix or refactor; before /commit or /pr; when the user asks "does it work?", "verify", "sprawdz czy dziala".
allowed-tools: Bash(make check) Bash(uv run *) Bash(curl *) Bash(git status *) Bash(git diff *)
---

# Verification loop

Run every phase, in order, and do not skip one because an earlier one passed.
Report a table at the end: Phase | Result | Details.

## Changed files
!`git status --short`

## Phase 1 - Static checks, tests, Django checks
`make check`: ruff, ruff format, mypy --strict, pytest + coverage >= 90%, and once `src/manage.py` exists also `manage.py check`, `makemigrations --check` and `check --deploy` on production settings.
If it fails: fix, re-run. Never weaken a test or add `# type: ignore` without an error code.

## Phase 2 - Security lint
`uv run ruff check --select S --output-format=concise src`
Every finding is either fixed or explicitly justified to the user.

## Phase 3 - End to end, like a user (skip only while `src/` is empty)
1. Apply migrations to a throwaway database and start the server in the background:
   `DATABASE_URL=sqlite:///$(mktemp -d)/e2e.sqlite3 uv run python src/manage.py migrate` (if settings read `DATABASE_URL`; otherwise use the dev DB), then `uv run python src/manage.py runserver 127.0.0.1:8765 --noreload &`.
2. Call every changed URL with `curl -i`: happy path, one validation error, anonymous access. For HTML pages check the status and that the page renders without template errors.
3. Stop the server and show the responses you got.

## Phase 4 - Diff review
`git diff` - look for leftover debug code (`print`, `breakpoint`), commented-out code, TODOs without an issue, secrets, forgotten migrations, unrelated changes.

Only say the work is done when all four phases pass.
