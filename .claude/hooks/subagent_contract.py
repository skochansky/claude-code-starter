#!/usr/bin/env python3
"""SubagentStop: make review subagents return a report in the agreed format.

If `code-reviewer` or `security-auditor` finishes without the expected structure,
the subagent is sent back with instructions instead of returning a vague answer.
"""

import json
import re
import sys

from _common import read_event

CONTRACTS = {
    "code-reviewer": (
        r"\*\*(Critical|Warning|Suggestion)\*\*|no issues found",
        "Group findings under **Critical**, **Warning**, **Suggestion** with `path:line` "
        "for each, or reply exactly 'No issues found'.",
    ),
    "security-auditor": (
        r"\|\s*Severity\s*\||no vulnerabilities found",
        "Return the findings table (Severity | Location | Issue | Exploit scenario | Fix) "
        "and an overall risk verdict, or reply 'No vulnerabilities found'.",
    ),
}


def main() -> None:
    event = read_event()
    contract = CONTRACTS.get(event.get("agent_type", ""))
    if contract is None or event.get("stop_hook_active"):
        return
    pattern, instruction = contract
    message = event.get("last_assistant_message", "")
    if not re.search(pattern, message, re.IGNORECASE):
        print(json.dumps({"decision": "block", "reason": f"Report format: {instruction}"}))
        sys.exit(0)


if __name__ == "__main__":
    main()
