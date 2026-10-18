"""Shared helpers for Claude Code hooks. Standard library only, so hooks start fast."""

import json
import os
import sys
from pathlib import Path
from typing import Any, NoReturn


def read_event() -> dict[str, Any]:
    """Parse the hook event JSON that Claude Code sends on stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def project_dir() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd()))


def deny(reason: str) -> NoReturn:
    """Block a PreToolUse call. The reason is shown to Claude so it can adjust."""
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    sys.exit(0)


def ask(reason: str) -> NoReturn:
    """Force a PreToolUse call to ask the user, even if settings would allow it."""
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    sys.exit(0)


def add_context(event_name: str, text: str) -> NoReturn:
    """Inject extra context into the conversation (SessionStart, UserPromptSubmit, PostToolUse)."""
    print(
        json.dumps({"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": text}})
    )
    sys.exit(0)
