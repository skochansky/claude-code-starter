#!/usr/bin/env python3
"""PreToolUse(Bash): block destructive commands and steer Claude to project tooling.

Settings `permissions.deny` match on prefixes only; this hook inspects the whole
command (pipes, `&&` chains, `sh -c`), which prefix rules cannot do.
"""

import re

from _common import ask, deny, read_event

# (pattern, reason) - hard block
BLOCKED: list[tuple[str, str]] = [
    (
        r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+(/|~|\$HOME|\.)(\s|$)",
        "Recursive delete of /, ~ or the project root.",
    ),
    (
        r"\bgit\s+push\b.*(--force\b|-f\b)(?!-with-lease)",
        "Force push. Use --force-with-lease on your own branch, never on main.",
    ),
    (
        r"\bgit\s+push\b.*\s(\S+:)?(main|master)(\s|$)",
        "Direct push to main/master. Open a pull request instead.",
    ),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard discards work. Ask the user first."),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "git clean -f deletes untracked files. Ask the user first."),
    (
        r"\b(DROP|TRUNCATE)\s+(DATABASE|TABLE|SCHEMA)\b",
        "Destructive SQL. Write a migration instead.",
    ),
    (
        r"\bmanage\.py\s+(flush|reset_db|sqlflush)\b",
        "Wipes all data in the database. Ask the user to run it themselves.",
    ),
    (r"\bmanage\.py\s+migrate\s+\S+\s+zero\b", "Unapplies every migration of an app."),
    (r"(curl|wget)\b[^|]*\|\s*(ba|z)?sh\b", "Piping a remote script into a shell."),
    (r"\bchmod\s+-R\s+777\b", "World-writable permissions."),
    (
        r"\bgit\s+((commit|push|merge|rebase|am)\b.*(--no-verify|--no-gpg-sign)\b"
        r"|commit\b.*\s-[a-zA-Z]*n[a-zA-Z]*(\s|$))",
        "Skipping git hooks / signing. Fix what the pre-commit hook reports instead.",
    ),
    (
        r"(^|[;&|]\s*)(export\s+)?SKIP=|\bPRE_COMMIT_ALLOW_NO_CONFIG=",
        "Bypassing pre-commit checks via environment variables.",
    ),
    (
        r"\b(cat|less|more|head|tail|bat|grep)\b[^|;&>\n]*(\s|/)\.env(\.local|\.production)?(\s|$)",
        "Reading .env exposes secrets. Use .env.example.",
    ),
]

# (pattern, hint) - project uses uv; plain pip/python would bypass the lock file
REDIRECT: list[tuple[str, str]] = [
    (
        r"(^|[;&|]\s*)pip3?\s+install(\s|$)",
        "This project uses uv. Use `uv add <pkg>` (or `uv add --dev <pkg>`).",
    ),
    (r"(^|[;&|]\s*)python3?\s+-m\s+pip\b", "This project uses uv. Use `uv add <pkg>`."),
    (
        r"(^|[;&|]\s*)(pytest|ruff|mypy)(\s|$)",
        "Run tools through uv so the locked versions are used: `uv run <tool>`.",
    ),
    (
        r"(^|[;&|]\s*)(python3?\s+)?(\S*/)?(manage\.py|django-admin)(\s|$)",
        "Run Django through uv so the project environment is used: "
        "`uv run python src/manage.py ...`.",
    ),
]

# (pattern, reason) - allowed, but the user must confirm
CONFIRM: list[tuple[str, str]] = [
    (r"\bgit\s+push\b", "Pushing publishes commits to the remote."),
    (r"\bgh\s+(pr\s+(create|merge)|release\s+create|repo\s+create)\b", "This publishes to GitHub."),
    (r"\bmanage\.py\s+(migrate|squashmigrations)\b", "This changes the database schema."),
    (r"\bmanage\.py\s+(createsuperuser|changepassword)\b", "This creates or changes credentials."),
]


def main() -> None:
    command = read_event().get("tool_input", {}).get("command", "")
    for pattern, reason in BLOCKED:
        if re.search(pattern, command, re.IGNORECASE):
            deny(f"Blocked by .claude/hooks/guard_bash.py: {reason}")
    for pattern, hint in REDIRECT:
        if re.search(pattern, command):
            deny(hint)
    for pattern, reason in CONFIRM:
        if re.search(pattern, command):
            ask(reason)


if __name__ == "__main__":
    main()
