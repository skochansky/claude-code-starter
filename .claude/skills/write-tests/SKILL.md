---
name: write-tests
description: Write or extend pytest tests for a module, endpoint or bug in this project, then run them with coverage. Use when the user asks for tests, more coverage, or a regression test for a bug.
allowed-tools: Bash(uv run pytest *)
argument-hint: "<path-or-feature>"
---

# Write tests for `$ARGUMENTS`

1. Read `.claude/rules/testing.md`, `tests/conftest.py` and one existing test of a similar kind.
2. Read the target code and enumerate behaviours in a short list:
   happy path, validation errors, not found, permission denied, boundaries (0, 1, max, empty, unicode), concurrency/ordering if relevant.
3. Check current coverage for the target: `uv run pytest --cov --cov-report=term-missing -q` and note uncovered lines.
4. Write the tests:
   - HTTP-level via `client` / DRF `APIClient` for views, including anonymous and other-user access.
   - Service / selector level for business rules (`pytestmark = pytest.mark.django_db`).
   - Query counts for list views (`django_assert_max_num_queries`).
   - `pytest.mark.parametrize` for variations; arrange / act / assert blocks.
5. Run the new file, then the full suite. All must pass; no flaky constructs (sleep, real network, time-of-day).
6. Report: tests added, coverage before -> after, and any production bug discovered (do not silently fix it; describe it and ask).

For a bug: the test must fail before the fix and pass after. Show both runs.
