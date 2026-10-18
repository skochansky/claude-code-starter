---
name: debug-issue
description: Systematic debugging workflow - reproduce the bug end to end, write a failing test, find the root cause, fix, verify. Use when the user reports a bug, error, traceback, failing test or unexpected page or API behaviour.
when_to_use: "Tracebacks, 500 errors, failing tests, wrong responses, \"it does not work\", \"nie dziala\"."
argument-hint: "<bug description or traceback>"
---

# Debug: $ARGUMENTS

Do not guess-and-patch. Follow the steps and show evidence at each one.

1. **Reproduce like a user.** Start the dev server (`uv run python src/manage.py runserver 127.0.0.1:8765 --noreload &`) and hit the URL with `curl -i` (or open the page), or run the failing command exactly as reported. Capture the real output / traceback. Stop the server afterwards.
2. **Lock it in a test.** Write the smallest test that reproduces it (HTTP level preferred). Run it and confirm it fails for the same reason.
3. **Find the root cause.** Read the traceback bottom-up; read the involved code fully. For ORM issues print the SQL (`str(queryset.query)`) or use `django_assert_max_num_queries`. Form a hypothesis, confirm it (targeted print/log or a narrower test), then remove the instrumentation.
4. **Fix the cause, not the symptom.** Smallest change in the right layer. Search for the same pattern elsewhere (`grep`) and fix those too.
5. **Verify.** The new test passes; full suite passes (`make check`); repeat step 1 and show the corrected behaviour.
6. **Report**: root cause (one paragraph), fix, test added, other places fixed.
