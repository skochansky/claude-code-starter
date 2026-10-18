---
description: Run the full quality gate (ruff, format, mypy, pytest + coverage, Django checks) and fix what fails
allowed-tools: Bash(uv run:*), Bash(make check), Read, Edit
---

Run `make check`.

If everything passes, reply with one line: "All checks passed" plus the coverage percentage.

If something fails:
1. Fix lint and formatting first (`uv run ruff check --fix . && uv run ruff format .`).
2. Fix type errors properly (no `# type: ignore` without a specific error code and a reason).
3. Fix failing tests by fixing the code, unless the test itself is wrong - then explain why.
4. Re-run `make check` until it is green, then summarise what you changed.
