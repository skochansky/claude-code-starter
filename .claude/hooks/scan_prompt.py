#!/usr/bin/env python3
"""UserPromptSubmit: stop prompts that contain credentials before they reach the model."""

import re
import sys

from _common import read_event

SECRET_PATTERNS = {
    "Anthropic API key": r"sk-ant-[A-Za-z0-9_-]{20,}",
    "OpenAI API key": r"sk-(proj-)?[A-Za-z0-9]{32,}",
    "AWS access key": r"\bAKIA[0-9A-Z]{16}\b",
    "GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{36,}\b",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "connection string with password": r"\b(postgres(ql)?|mysql|mongodb(\+srv)?)://[^:\s]+:[^@\s]+@",
}


def main() -> None:
    prompt = read_event().get("prompt", "")
    found = [name for name, pattern in SECRET_PATTERNS.items() if re.search(pattern, prompt)]
    if found:
        print(
            f"Prompt blocked: it looks like it contains a {', '.join(found)}. "
            "Remove the secret (put it in .env) and send the prompt again.",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
