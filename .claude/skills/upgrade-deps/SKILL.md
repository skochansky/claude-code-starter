---
name: upgrade-deps
description: Upgrade Python dependencies with uv safely - one group at a time, read changelogs for major bumps, run the full verification after each step.
when_to_use: When the user asks to update/upgrade packages, fix a vulnerable dependency, or refresh uv.lock.
argument-hint: "[package ...]"
disable-model-invocation: true
allowed-tools: Bash(uv lock *) Bash(uv tree *) Bash(uv sync *) Bash(make check) Bash(uv run *) Bash(git diff *)
---

# Upgrade dependencies: $ARGUMENTS

## Current state
```!
uv tree --depth 1 --outdated 2>/dev/null | head -40
```

## Steps
1. Decide the scope: the packages named above, or all outdated direct dependencies when none are named.
2. Group them: (a) patch/minor bumps, (b) each major bump on its own.
3. For each group:
   - `uv lock --upgrade-package <pkg>` (repeat per package) and `uv sync`.
   - For a major bump, read the package's changelog/migration guide (use the context7 MCP server or WebFetch) and list breaking changes that affect `src/`.
   - Django major/feature release: read the release notes' "Backwards incompatible changes" and deprecations, run `uv run python -Wd src/manage.py check` and `uv run --with django-upgrade django-upgrade --target-version <X.Y> $(git ls-files 'src/*.py')`.
   - Fix the code, then run the `verify` skill.
   - If it cannot be made green quickly, revert that group (`git checkout uv.lock pyproject.toml && uv sync`) and report why.
4. If a minimum version in `pyproject.toml` should change, update it there - never edit `uv.lock` by hand.
5. Report a table: Package | From | To | Breaking changes | Status.

Do not commit; the user commits.
