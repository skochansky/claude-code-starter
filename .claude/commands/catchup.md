---
description: Rebuild context after /clear or a break - read everything changed on this branch and summarise where the work stands
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git branch *) Read Grep Glob
---

## Branch state
- Branch: !`git branch --show-current`
- Commits not on main: !`git log --oneline main..HEAD 2>/dev/null | head -20`
- Uncommitted: !`git status --short`
- Changed files vs main: !`git diff --name-only main 2>/dev/null; git ls-files --others --exclude-standard`

## Task
Read every changed file listed above in full (skip `uv.lock`).
Then give me, briefly:
1. What this branch is doing (one paragraph).
2. What looks finished vs. in progress (bullets with `path:line`).
3. Anything broken or suspicious (failing tests, TODOs, debug leftovers).
4. The most sensible next step.
