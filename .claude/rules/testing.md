---
paths:
  - "tests/**/*.py"
  - "**/test_*.py"
  - "**/conftest.py"
---

# Testing conventions (pytest-django)

- pytest only, with pytest-django fixtures (`client`, `admin_client`, `rf`, `settings`, `django_assert_max_num_queries`). No `unittest.TestCase`.
- DB access must be explicit: `pytestmark = pytest.mark.django_db` or the `db` fixture.
- Tests live in `tests/` mirroring `src/apps/` (`tests/<app>/test_api.py`, `test_services.py`).
- Name tests `test_<unit>_<behaviour>`. One behaviour per test. Arrange / act / assert separated by blank lines.
- Test through HTTP first (`client` / DRF `APIClient`); unit-test services for complex rules.
- Every endpoint: happy path, validation (400), anonymous (401/403), other user's object (404), list pagination and query count.
- Test data via fixtures or factories (`factory_boy`), not shared global state. Passwords like `"test-password"`.
- `settings` fixture to override settings; `freezegun` / `time-machine` for time; `responses` / `respx` to mock outbound HTTP. Never hit real services.
- A flaky test is a bug: fix the cause, never add retries or `sleep`.
- Coverage gate 90% (`make test`). No assertion-free tests to game it.
