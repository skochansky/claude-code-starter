#!/usr/bin/env python3
"""SessionStart: give Claude a fresh snapshot of the repo state at the start of every session."""

import platform
import subprocess

from _common import add_context, project_dir


def sh(*args: str) -> str:
    try:
        out = subprocess.run(
            args, cwd=project_dir(), capture_output=True, text=True, timeout=5, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return out.stdout.strip()


def main() -> None:
    branch = sh("git", "branch", "--show-current") or "(no git / detached)"
    status = sh("git", "status", "--short") or "clean"
    commits = sh("git", "log", "--oneline", "-5") or "(no commits yet)"
    todo = sh("git", "grep", "-n", "-E", "TODO|FIXME", "--", "src")

    lines = [
        "## Repository snapshot (from SessionStart hook)",
        f"- Python: {platform.python_version()}",
        f"- Branch: {branch}",
        f"- Working tree:\n```\n{status[:1500]}\n```",
        f"- Recent commits:\n```\n{commits}\n```",
    ]
    if not (project_dir() / "src" / "manage.py").is_file():
        lines.append(
            "- Django project not created yet: `src/` is empty. When the user starts it, "
            "follow 'Starting the Django project' in docs/architecture.md."
        )
    if todo:
        lines.append(f"- Open TODO/FIXME in src:\n```\n{todo[:1500]}\n```")
    add_context("SessionStart", "\n".join(lines))


if __name__ == "__main__":
    main()
