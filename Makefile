.PHONY: install run migrate lint format types test django-check check require-app

MANAGE := uv run python src/manage.py
# Django targets switch on once the project exists (src/ starts empty).
HAS_APP := $(wildcard src/manage.py)
PROD_SETTINGS ?= config.settings.prod

install:
	uv sync

run: migrate
	$(MANAGE) runserver

migrate: require-app
	$(MANAGE) migrate

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

types:
	uv run mypy

test:
	uv run pytest $(if $(HAS_APP),--cov)

# System checks, missing migrations, and production settings sanity.
django-check: require-app
	$(MANAGE) check --fail-level WARNING
	$(MANAGE) makemigrations --check --dry-run
	DJANGO_SECRET_KEY="$$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')" \
	DJANGO_ALLOWED_HOSTS=example.com \
	$(MANAGE) check --deploy --fail-level WARNING --settings=$(PROD_SETTINGS)

check: lint types test $(if $(HAS_APP),django-check)

require-app:
	@test -f src/manage.py || { echo "No Django project yet (src/ is empty). See docs/architecture.md."; exit 1; }
