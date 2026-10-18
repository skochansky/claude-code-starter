#!/usr/bin/env python3
"""Notification: desktop notification when Claude waits for input (macOS / Linux, best effort)."""

import json
import shutil
import subprocess

from _common import read_event


def main() -> None:
    message = read_event().get("message", "Claude Code needs your attention")
    if shutil.which("osascript"):
        script = f'display notification {json.dumps(message)} with title "Claude Code"'
        subprocess.run(["osascript", "-e", script], check=False)
    elif shutil.which("notify-send"):
        subprocess.run(["notify-send", "Claude Code", message], check=False)


if __name__ == "__main__":
    main()
