# Fixture — revision-list

**Endpoint:** `GET /api/ric/v1/{type}/{id}/revisions`
**Schema:** SHACL `:RevisionListShape` + `:RevisionEntryShape` in [shapes/profiles/round-trip-editing.shacl.ttl](../../shapes/profiles/round-trip-editing.shacl.ttl)
**HTTP status:** `200 OK`
**Access:** Public (audit reads are public — sensitive keys are redacted at write time).

The audit trail for one entity, returned newest-first. Three entries shown: two updates and the original create. `actor` is either `api_key:<n>`, `session`, or `anonymous`; `payload` is an optional redacted snapshot of the request body (implementations MAY omit it for privacy reasons). `created_at` is an ISO-8601 datetime.

**Pagination:** the `total` field is the absolute count; clients that need paging append `?limit=N` (default 50, max 200). Pagination beyond `limit` is not part of this profile — an implementation that needs deeper history should expose a dedicated audit-export endpoint outside the profile's normative surface.

**Why this is in round-trip-editing, not a "provenance" profile:** every round-trip write creates exactly one audit row; the trail here is the canonical way a client can answer "was this mutation persisted, who did it, and when." Writes without audit would break the "round-trip" contract — a client that POSTed an entity could not later confirm the server accepted it the way it intended.
