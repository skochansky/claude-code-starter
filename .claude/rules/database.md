---
paths:
  - "**/models.py"
  - "**/models/**/*.py"
  - "**/selectors.py"
  - "**/services.py"
  - "**/migrations/*.py"
---

# Database rules (Django ORM)

- Querysets only. Raw SQL only when the ORM cannot express it, always with parameters: `cursor.execute(sql, [param])`, never f-strings.
- Prevent N+1: `select_related` for FK/one-to-one, `prefetch_related` for reverse/M2M. Tests assert query counts with `django_assert_max_num_queries`.
- Lists are always bounded (pagination or slicing). `.iterator()` for large batch jobs.
- `DateTimeField` with `USE_TZ = True`; use `django.utils.timezone.now()`, never naive `datetime.now()`.
- `ForeignKey` always with an explicit `on_delete` and `related_name`.
- Data integrity in the database: `UniqueConstraint`, `CheckConstraint`, `null=False` by default. Text fields use `blank=True`, not `null=True`.
- Indexes (`Meta.indexes`) for fields used in `filter()` / `order_by()` on large tables.
- Multi-step writes in `transaction.atomic()`; `select_for_update()` for read-modify-write races; `F()` expressions for counters.

## Migrations
- Every model change ships with `makemigrations`. `makemigrations --check` in CI catches forgotten ones.
- Never edit a migration that is already committed (a hook blocks it). Write a new one.
- Review generated migrations: a rename can show up as remove + add and lose data.
- Data migrations use `RunPython(forward, reverse)` with `apps.get_model()`, never direct model imports.
- Destructive changes in two releases: stop using the field in code, then drop it.
- Adding a NOT NULL field to a big table: nullable first, backfill, then make it required.
- Postgres: big indexes with `AddIndexConcurrently` in a migration with `atomic = False`.
