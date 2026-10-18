# CLAUDE.md

Project memory for Claude Code.
Keep it short: details live in `.claude/rules/` (loaded automatically, some only for matching paths) and `docs/`.

## What this is

A Claude Code setup for a Django project (Django, Django REST Framework, Django ORM, pytest-django, uv).
`src/` is still empty; the rules, hooks, skills and agents are ready for the code that will go there.

@docs/architecture.md

## Commands

All tools run through `uv`; never call `pip`, bare `pytest`, bare `ruff` or bare `python manage.py` (a hook blocks them).

| Task | Command |
| --- | --- |
| Install deps | `uv sync` |
| Run the dev server (migrates first) | `make run` |
| Apply migrations | `make migrate` |
| New migration | `uv run python src/manage.py makemigrations <app> --name <what>` (see `db-migration` skill) |
| All checks (CI equivalent) | `make check` (lint, mypy, pytest + coverage, Django system/deploy checks, missing migrations) |
| Tests | `uv run pytest` (single: `uv run pytest tests/<app>/test_api.py::test_name`) |
| Lint / format | `uv run ruff check --fix . && uv run ruff format .` |
| Types | `uv run mypy` |
| Add a dependency | `uv add <pkg>` / `uv add --dev <pkg>` |
| Git hooks | `uv run pre-commit install` (never bypass with `--no-verify`) |

## Non-negotiables

- Layering inside an app: `views` -> `selectors` (reads) / `services` (writes) -> `models`. No business logic in views, serializers, forms, signals or `save()`.
- Every queryset a user can reach is scoped to `request.user`; never trust IDs from the client.
- Every behaviour change ships with a test. Write the failing test first when fixing a bug.
- Every model change ships with a migration; `makemigrations --check` must be clean.
- Type hints everywhere; `mypy --strict` must pass.
- Never edit `uv.lock`, committed migrations, `.env`, `staticfiles/` or `CHANGELOG.md` by hand (hooks enforce this).
- Never commit secrets. Settings come from env vars (`DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL`).
- Use `-` (plain hyphen), never the em dash, in any text you write.
- Never commit or push unless the user explicitly asks; the user commits.
- Commit messages: Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`), no AI co-author lines.

## How Claude should work here

- Before coding, read the relevant rule file in `.claude/rules/` and the nearest existing app in `src/apps/`.
- Do not create the Django project or new apps unless the user asks; `src/` stays empty until then.
- Prefer the project skills: `tdd`, `write-tests`, `db-migration`, `debug-issue`, `verify`, `security-scan`, `upgrade-deps`.
- Before saying a task is done, run the `verify` skill and show its result.
- Delegate focused work to subagents: `code-reviewer` after changes, `test-writer` for coverage, `security-auditor` before release, `db-expert` for models/migrations/queries, `performance-engineer` for slow pages, `refactorer` (isolated worktree) for refactors, `api-designer` before new endpoints.
- Plans for non-trivial features go to `docs/plans/` (`/plan-feature`).
- When you finish, the `Stop` hook runs ruff, mypy and pytest (plus Django checks once `src/manage.py` exists). If it blocks, fix the failure; do not disable the hook.

## Personal overrides

Put machine-specific notes in `CLAUDE.local.md` (git-ignored).
