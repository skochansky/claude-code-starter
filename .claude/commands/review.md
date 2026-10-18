---
description: Review current changes with the code-reviewer and security-auditor subagents
argument-hint: "[base-branch]"
allowed-tools: Bash(git diff:*), Bash(git status), Bash(git log:*)
---

## Context
- Status: !`git status --short`
- Uncommitted changes: !`git diff --stat HEAD 2>/dev/null || git status --short`
- Base branch argument (optional): $ARGUMENTS

## Task
If a base branch was given, review `git diff <base>...HEAD`; otherwise review the uncommitted changes.
Run two subagents in parallel on these changes:
1. `code-reviewer` - correctness, layering, tests, readability.
2. `security-auditor` - limited to the changed files.

Merge their findings into one list ordered Critical -> Warning -> Suggestion, de-duplicated, each with `path:line`.
Ask me before applying any fix.
