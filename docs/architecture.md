# Architecture

`src/` is empty on purpose: this repository is the Claude Code setup, the Django code comes later.
The layout below is the target every new file must follow.

```
src/
  manage.py
  config/                 project package
    settings/             base.py (shared), dev.py, test.py, prod.py - env vars for anything per environment
    urls.py               includes each app's urls under a prefix (/api/v1/<app>/ for DRF)
    asgi.py, wsgi.py
  apps/
    users/                custom user model (AUTH_USER_MODEL) - exists before the first migration
    <app>/
      models.py           fields, constraints, Meta
      selectors.py        reads: querysets scoped to the user, select_related / prefetch_related
      services.py         writes: business rules, transaction.atomic, full_clean
      views.py            thin views / DRF viewsets: input -> selector or service -> response
      serializers.py      DRF only: validation and shape, explicit fields
      urls.py, admin.py, apps.py (name = "apps.<app>")
      migrations/
      templates/<app>/
tests/
  conftest.py             shared fixtures (users, API client)
  <app>/test_*.py         mirrors src/apps/
  test_claude_hooks.py    contract tests for .claude/hooks
```

Request flow: `urls.py` -> view -> `selectors` (read) or `services` (write) -> models / ORM.

## Starting the Django project

Only when the user asks for it:

1. `uv add django djangorestframework dj-database-url` and `uv add --dev pytest-django django-stubs djangorestframework-stubs`.
2. `uv run django-admin startproject config src`, then split `src/config/settings.py` into the `settings/` package above.
3. Create `apps/users` with `class User(AbstractUser)` and set `AUTH_USER_MODEL` before running any migration.
4. `pyproject.toml`: pytest `DJANGO_SETTINGS_MODULE = "config.settings.test"`; mypy `files = ["src", "tests"]`, `plugins = ["mypy_django_plugin.main", "mypy_drf_plugin.main"]`, `[tool.django-stubs] django_settings_module = "config.settings.test"`.
5. `make check` must be green (it then also runs `manage.py check`, `makemigrations --check` and `check --deploy`).
