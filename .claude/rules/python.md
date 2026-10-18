---
paths:
  - "**/*.py"
---

# Python style

- Target Python 3.12+. Use `X | None`, `list[int]`, `match`, `typing.Self`, PEP 695 generics where they help.
- Full type hints on every function, including `-> None`. No `Any` unless at a true boundary (JSON from outside), and then narrow it immediately.
- Prefer `pathlib` over `os.path`, f-strings over `%`/`format`, `django.utils.timezone.now()` over naive datetimes.
- Small functions with one job. Early returns over nested `if`.
- Raise specific exceptions (domain errors subclass `Exception` with a clear message). Never `except Exception: pass`.
- No mutable default arguments. No module-level side effects other than constants (settings modules are the exception).
- Imports: absolute (`from apps.orders.services import ...`), sorted by ruff. No wildcard imports.
- Docstrings only where the "why" is not obvious from the name and types; one line is usually enough.
- Logging via `logging.getLogger(__name__)`, never `print` in application code.
