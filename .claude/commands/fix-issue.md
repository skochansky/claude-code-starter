---
disable-model-invocation: true
description: Fix a GitHub issue end to end (reproduce, test, fix, verify, commit on a branch)
argument-hint: "<issue-number>"
allowed-tools: Bash(gh issue view:*), Bash(git checkout:*), Bash(git switch:*), Bash(uv run:*), Bash(make check), Read, Edit, Write, Grep, Glob
---

Issue details: !`gh issue view $ARGUMENTS --json number,title,body,labels,comments`

1. Create a branch: `git switch -c fix/$ARGUMENTS-<short-slug>`.
2. Use the `debug-issue` skill: reproduce the bug end to end, then write a failing test.
3. Fix the root cause. Keep the diff minimal and in the right layer.
4. Run `make check` until green.
5. Delegate a final review to the `code-reviewer` subagent and address Critical/Warning findings.
6. Propose a Conventional Commit message `fix: <summary> (#$ARGUMENTS)` and ask me before committing.
