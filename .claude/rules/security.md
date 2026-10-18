# Security rules (always loaded)

- Secrets only from environment / secret manager. Never hard-code tokens, passwords or keys, not even in tests (use obvious fakes like `"test-secret"`).
- `DEBUG = False`, `SECRET_KEY` and `ALLOWED_HOSTS` from env in production. `manage.py check --deploy` must be clean.
- Never log secrets, tokens, passwords or full request bodies with personal data.
- Validate all external input with forms / serializers. Authorization by scoping querysets to `request.user`; never trust IDs from the client.
- SQL only through the ORM or parameterized `cursor.execute(sql, params)`. No f-strings in `raw()`, `extra()`, `RawSQL`.
- CSRF protection stays on. `@csrf_exempt` only for webhooks that verify a signature.
- No `mark_safe` / `|safe` on user input. No `eval`, `exec`, `pickle.loads` on untrusted data, `yaml.load` without `SafeLoader`, `subprocess` with `shell=True`.
- Passwords only via Django auth (`set_password`, `check_password`). Tokens: `secrets.token_urlsafe`.
- File uploads: validate type and size, store outside code dirs, never build paths from user input.
- CORS (`django-cors-headers`): explicit origins, never allow-all together with credentials.
- New dependency? Prefer well-maintained packages; mention why in the commit.
