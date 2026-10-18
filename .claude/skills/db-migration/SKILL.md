---
name: db-migration
description: Plan and create a safe Django schema or data migration (zero-downtime steps, review of the generated file, migrate forward and back). Use when adding/removing/renaming fields or models, adding indexes or constraints, or moving data.
allowed-tools: Bash(uv run python src/manage.py makemigrations *) Bash(uv run python src/manage.py sqlmigrate *) Bash(uv run python src/manage.py showmigrations *) Bash(uv run pytest *)
argument-hint: "<describe the schema change>"
---

# Database migration: $ARGUMENTS

## 1. Classify the change
| Change | Safe in one step? |
| --- | --- |
| New model, nullable field, field with a default | Yes |
| New index on a large Postgres table | Only with `AddIndexConcurrently` in a migration with `atomic = False` |
| NOT NULL field on an existing table | nullable -> backfill (data migration) -> NOT NULL |
| Rename field/model | Check Django asks "Did you rename...?" and answer yes; otherwise add -> copy -> switch -> remove |
| Remove field/model | Stop using it in code first, remove in a later release |
| Change type | Usually new field + backfill |

Explain the classification to the user before writing anything that is not "Yes".

## 2. Change the model
Follow `.claude/rules/database.md` (explicit `on_delete`, `related_name`, constraints, indexes).

## 3. Generate
`uv run python src/manage.py makemigrations <app> --name <short_description>`
Always give a descriptive `--name`, never the auto `0007_auto_...`.

## 4. Review the file line by line
- Remove + add instead of a rename? Fix it (`RenameField`).
- `uv run python src/manage.py sqlmigrate <app> <number>` - read the SQL: table rewrites, locks, missing indexes.
- Data migration: `migrations.RunPython(forward, reverse)`, models through `apps.get_model("app", "Model")`, batch large tables, `reverse` implemented (or `RunPython.noop` with a reason).

## 5. Verify
```bash
uv run python src/manage.py makemigrations --check --dry-run   # nothing left to generate
uv run python src/manage.py migrate <app>                       # forward (asks for confirmation)
uv run python src/manage.py migrate <app> <previous_number>    # and back
uv run python src/manage.py migrate <app>
uv run pytest -q
```

Never edit a migration that is already committed (a hook blocks it).
Applying migrations asks the user for confirmation (hook).
