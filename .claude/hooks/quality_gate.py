#!/usr/bin/env python3
"""Stop: do not let Claude finish a turn with failing lint, types or tests.

Runs only when Python files changed in the working tree, so plain Q&A turns stay fast.
Django checks (system checks, forgotten migrations) join once src/manage.py exists.
If a check fails, the turn is blocked and Claude gets the failure output to fix.
"""

import json
import subprocess
import sys

from _common import project_dir, read_event

CHECKS: list[tuple[str, list[str]]] = [
    ("ruff", ["uv", "run", "--quiet", "ruff", "check", "."]),
    ("ruff format", ["uv", "run", "--quiet", "ruff", "format", "--check", "."]),
    ("mypy", ["uv", "run", "--quiet", "mypy"]),
    (
        "pytest",
        ["uv", "run", "--quiet", "pytest", "-x", "-q", "--no-header", "-p", "no:cacheprovider"],
    ),
]
DJANGO_CHECKS: list[tuple[str, list[str]]] = [
    ("manage.py check", ["uv", "run", "--quiet", "python", "src/manage.py", "check"]),
    (
        "missing migrations",
        [
            "uv",
            "run",
            "--quiet",
            "python",
            "src/manage.py",
            "makemigrations",
            "--check",
            "--dry-run",
        ],
    ),
]


def python_files_changed() -> bool:
    out = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=project_dir(),
        capture_output=True,
        text=True,
        check=False,
    )
    if out.returncode != 0:
        return True  # not a git repo yet: be safe and check
    return any(
        line.rstrip().endswith((".py", ".pyi", "pyproject.toml"))
        for line in out.stdout.splitlines()
    )


def main() -> None:
    event = read_event()
    # Claude is already fixing a previous failure: don't loop forever.
    if event.get("stop_hook_active") or not python_files_changed():
        return
    root = project_dir()
    if not (root / "pyproject.toml").is_file():
        return
    checks = CHECKS + DJANGO_CHECKS if (root / "src" / "manage.py").is_file() else CHECKS

    for name, cmd in checks:
        result = subprocess.run(
            cmd, cwd=root, capture_output=True, text=True, timeout=300, check=False
        )
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip()[-3000:]
            print(
                json.dumps(
                    {
                        "decision": "block",
                        "reason": f"Quality gate failed on `{name}`. Fix it first:\n{output}",
                    }
                )
            )
            sys.exit(0)


if __name__ == "__main__":
    main()
