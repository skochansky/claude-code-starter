#!/usr/bin/env python3
"""Status line: model | branch (+dirty) | python | context usage."""

import json
import platform
import subprocess
import sys

data = json.load(sys.stdin)
cwd = data.get("workspace", {}).get("current_dir", ".")


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    return out.stdout.strip()


branch = git("branch", "--show-current") or "-"
dirty = "*" if git("status", "--porcelain") else ""
model = data.get("model", {}).get("display_name", "?")
parts = [
    f"\033[35m{model}\033[0m",
    f"\033[36mgit:{branch}{dirty}\033[0m",
    f"py{platform.python_version()}",
]

used = data.get("context_window", {}).get("used_percentage")
if used is not None:
    parts.append(f"ctx {used:.0f}%")
print(" | ".join(parts))
