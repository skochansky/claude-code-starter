---
paths:
  - "**/templates/**/*.html"
  - "**/templates/**/*.txt"
---

# Django templates

- Auto-escaping stays on. `|safe`, `{% autoescape off %}` and `mark_safe()` only for content the code generated itself, never user input.
- Every POST form has `{% csrf_token %}`.
- Links via `{% url 'name' %}`, static files via `{% static %}`.
- No queries triggered in templates: the view passes prefetched data (watch for `obj.related.all` in loops).
- Inline JS that needs server data uses `{{ data|json_script:"id" }}`, not string interpolation.
