#!/usr/bin/env python3
"""PostToolUse(Edit|Write|MultiEdit): format and lint the Python file Claude just changed.

Formatting is applied silently. Lint errors that ruff cannot fix are reported back
to Claude (exit code 2 + stderr) so it fixes them in the same turn.
"""

import subprocess
import sys
from pathlib import Path

from _common import project_dir, read_event


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", "--quiet", *args],
        cwd=project_dir(),
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> None:
    raw = read_event().get("tool_input", {}).get("file_path", "")
    path = Path(raw)
    if path.suffix not in {".py", ".pyi"} or not path.exists():
        return
    if not path.resolve().is_relative_to(project_dir().resolve()):
        return  # scratch files etc. are not governed by this project's lint config

    run("ruff", "check", "--fix", "--quiet", str(path))
    run("ruff", "format", "--quiet", str(path))
    result = run("ruff", "check", "--output-format=concise", str(path))
    if result.returncode != 0:
        print(f"ruff found issues in {raw}:\n{result.stdout}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
