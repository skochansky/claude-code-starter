---
name: security-scan
description: Run a full security audit of the project in a separate security-auditor subagent (OWASP review, bandit rules, dependency vulnerabilities, secrets) and return only the report.
when_to_use: Before a release, after touching auth/permissions/uploads/raw SQL, after adding dependencies, or when the user asks for a security review or audit.
context: fork
agent: security-auditor
background: false
---

Audit this repository.

Scope: !`git diff --stat HEAD 2>/dev/null | tail -1`

1. Run `uv run ruff check --select S --output-format=concise .`.
2. Run `uv run --with pip-audit pip-audit` (skip with a note if there is no network).
3. Search for hard-coded secrets: `git grep -nIE "(api[_-]?key|secret|password|token)\s*=\s*['\"][^'\"]{8,}" -- ':!tests' ':!*.md'`.
4. Once `src/manage.py` exists: `uv run python src/manage.py check --deploy --settings=config.settings.prod` (with fake `DJANGO_SECRET_KEY` / `DJANGO_ALLOWED_HOSTS`).
5. Review every view, viewset and serializer for permissions, queryset scoping (IDOR), `fields = "__all__"`, `csrf_exempt`, `mark_safe` / `|safe`, raw SQL.
6. Review `src/config/settings/` for DEBUG, SECRET_KEY, ALLOWED_HOSTS, cookie/HSTS settings and CORS.

Return the findings table and the overall verdict defined in your agent instructions.
