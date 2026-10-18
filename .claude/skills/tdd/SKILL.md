---
name: tdd
description: Strict test-driven development loop (red -> green -> refactor) for a new behaviour in this Django project.
when_to_use: When the user asks for TDD, "test first", or a feature with precisely specified behaviour (validation rules, business rules, status codes).
argument-hint: "<behaviour to implement>"
arguments: behaviour
---

# TDD: $behaviour

Work in short cycles. Show the test output at every step - it is the evidence.

## 1. List the behaviours
Break `$behaviour` into 3-8 small, observable behaviours (HTTP status + body / rendered page, or service return / exception).
Write them as a checklist and confirm with the user if anything is ambiguous.

## 2. For each behaviour
1. **Red** - write one test in `tests/<app>/` (HTTP via `client` / `APIClient`, or a service call). Run only that test:
   `uv run pytest tests/<file>.py::<test> -q`
   It must fail, and fail for the expected reason (assertion, not an import error or typo).
2. **Green** - write the minimum production code that makes it pass. Run the test again.
3. **Refactor** - clean up code and test while the full suite stays green: `uv run pytest -q`.
4. Tick the behaviour in the checklist.

## 3. Finish
Run the `verify` skill. Report the checklist and the final test count.

Rules: never write production code without a failing test that demands it; never change an existing test's expectation to get to green.
