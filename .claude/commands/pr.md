---
disable-model-invocation: true
description: Push the branch and open a pull request with a generated description
argument-hint: "[base-branch]"
allowed-tools: Bash(git status), Bash(git diff:*), Bash(git log:*), Bash(git push:*), Bash(gh pr create:*)
---

## Context
- Branch: !`git branch --show-current`
- Base branch: $ARGUMENTS (default: main)
- Commits vs main: !`git log --oneline main..HEAD 2>/dev/null || echo '(none)'`
- Diff stat vs main: !`git diff --stat main...HEAD 2>/dev/null || echo '(none)'`

## Task
1. Refuse if the current branch is `main`/`master`.
2. Make sure `make check` passes.
3. Write the PR body:
   - **Summary** - what and why (2-4 bullets)
   - **Changes** - grouped by layer (urls/views, services/selectors, models/migrations, templates, tests)
   - **Testing** - commands run and results
   - **Risks / rollout** - migrations, config changes, breaking changes
4. `git push -u origin HEAD`, then `gh pr create --base <base> --title "<conventional title>" --body "<body>"`.
5. Print the PR URL.
