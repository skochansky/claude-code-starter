---
paths:
  - "src/**/*.py"
  - "src/manage.py"
---

# Django conventions

## Project layout
- Code lives in `src/`: project package `config/` (settings, urls, asgi/wsgi) and one package per domain in `apps/<name>/`.
- Settings are split: `config/settings/base.py` (shared), `dev.py`, `test.py`, `prod.py`. Values that differ per environment come from env vars, never from code.
- A custom user model (`AUTH_USER_MODEL`) exists before the first migration. Swapping it later means rewriting migrations.
- New app: `mkdir -p src/apps/<name> && uv run python src/manage.py startapp <name> src/apps/<name>`, set `name = "apps.<name>"` in `apps.py`, add it to `INSTALLED_APPS`, include its `urls.py` under a prefix.

## Layers inside an app
- `models.py` - fields, constraints, `Meta`, `__str__`. Small invariants in `clean()`, no workflows.
- `selectors.py` - read side: functions returning querysets, already scoped to the user and with `select_related` / `prefetch_related`.
- `services.py` - write side: keyword-only functions with `@transaction.atomic`, call `full_clean()`, no `request` objects.
- `views.py` (or DRF views) - thin: parse input, call one selector or service, return a response.
- No business logic in views, serializers, forms, signals or `save()` overrides. Avoid signals for domain logic; call the service explicitly.

## Views and URLs
- Every URL has a `name`; build links with `reverse()` / `{% url %}`, never hard-coded paths.
- Restrict methods (`@require_POST`, `@require_GET`, `http_method_names`).
- Login protection by default (`LoginRequiredMixin`, `@login_required`, or `LoginRequiredMiddleware`); public views are the explicit exception.
- Object access always through a queryset scoped to the current user (`get_object_or_404(selectors.x_list(owner=request.user), pk=pk)`).

## Admin
- Register every model. Set `list_display`, `search_fields`, `list_select_related` and `raw_id_fields` / `autocomplete_fields` for large foreign keys.

## Settings access
- Read settings via `django.conf.settings`, never `os.environ` outside `config/settings/`.
