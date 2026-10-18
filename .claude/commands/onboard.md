---
description: Explain this codebase to a newcomer - architecture, request flow, how to run and extend it
allowed-tools: Read, Grep, Glob, Bash(git log:*)
---

Read `CLAUDE.md` and `docs/architecture.md`.
If `src/manage.py` exists, also read `src/config/settings/base.py`, `src/config/urls.py`, one full app in `src/apps/` (urls -> views -> selectors/services -> models) and `tests/conftest.py`.
If `src/` is still empty, say so and explain how the project is meant to be started.

Then explain, concisely:
1. What the service does and its main building blocks.
2. The life of one request, file by file (pick a real URL from `urls.py`).
3. How to run, test and lint it.
4. How to add a new app or endpoint (point to `.claude/rules/django.md` and `/plan-feature`).
5. The Claude Code setup in `.claude/`: rules, hooks, skills, agents, commands - one line each.

Answer in the language the user writes in.
