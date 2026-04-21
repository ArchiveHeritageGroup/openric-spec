# Fixture — write-response-success

**Endpoint:** Any `PATCH /{type}/{id}`, `DELETE /{type}/{id}`, or relation write (POST / PATCH / DELETE `/relations[/{id}]`) that completed successfully.
**Schema:** [write-response.schema.json](../../schemas/write-response.schema.json) *(`$defs/success`)*
**HTTP status:** `200 OK` (not `201 Created` — that's the sibling `write-response-create` fixture for POST on a type).

This is the canonical "success, no new resource" envelope. Exact content:

```json
{ "success": true, "id": 912401 }
```

`success` is a literal `true` (not just truthy). `id` is the entity id that was mutated. Additional fields MAY be emitted by implementations and MUST be tolerated by clients (the schema declares `additionalProperties: true`).

**When NOT to return this shape:**

- On `POST /{type}` — use the `write-response-create` fixture (`{id, slug, type, href}`, HTTP 201).
- On any 4xx or 5xx — use RFC 7807 per Core Discovery §4 (`application/problem+json`).
- On `POST /upload` — Digital Object Linkage profile defines its own richer response shape (`{id, url, thumbnail_url, mime, size, filename, path}`).
