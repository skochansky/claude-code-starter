---
paths:
  - "**/serializers.py"
  - "**/api/**/*.py"
  - "**/api.py"
  - "**/views.py"
---

# Django REST Framework

- Version public endpoints under `/api/v1/`. Resources are plural nouns.
- Global defaults in `REST_FRAMEWORK`: `IsAuthenticated` permission and pagination. Opt out per view only with a reason.
- `get_queryset()` returns a selector scoped to `request.user`. Foreign objects then return 404, which is the authorization check (no IDOR).
- Writes go through services: override `perform_create` / `perform_update` / `perform_destroy` and call `services.*`.
- Serializers validate and shape data only. Explicit `fields = [...]`, never `"__all__"`. Mark server-owned fields `read_only_fields`.
- Never accept owner/user IDs from the client; take them from `request.user`.
- Status codes: 201 create, 204 delete, 400 validation, 401/403 auth, 404 missing or not yours.
- Throttling on login, signup and any expensive or public endpoint.
