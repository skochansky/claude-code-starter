#!/usr/bin/env python3
"""InstructionsLoaded (async): log which CLAUDE.md / rules files were loaded and why.

Answers "did my path-scoped rule actually load?" - see .claude/logs/instructions.log.
"""

from datetime import UTC, datetime

from _common import project_dir, read_event


def main() -> None:
    event = read_event()
    root = project_dir()
    path = event.get("file_path", "?").replace(str(root) + "/", "")
    trigger = event.get("trigger_file_path", "").replace(str(root) + "/", "")
    line = (
        f"{datetime.now(UTC):%Y-%m-%d %H:%M:%S} {event.get('load_reason', '?'):<17} "
        f"{event.get('memory_type', '?'):<8} {path}" + (f"  <- {trigger}" if trigger else "")
    )
    log = root / ".claude" / "logs" / "instructions.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


if __name__ == "__main__":
    main()
