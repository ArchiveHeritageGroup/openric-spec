# OpenRiC conformance fixtures

Each fixture is a folder containing a paired input + expected output, used by the conformance validator to check that an implementation maps archival-description data to RiC-O correctly.

## Shape

Two fixture shapes are in use. Newer fixtures pin a live reference URL and
capture its response; older fixtures ship hand-authored input + expected
pairs. Both are valid.

### Live-capture shape (preferred)

```
fixtures/<case-name>/
├── source-url.txt       # Live reference-implementation URL
├── expected.jsonld      # Canonical JSON-LD captured from source-url.txt
└── notes.md             # What this case exercises, what it doesn't
```

### Offline shape (pre-capture and hand-authored cases)

```
fixtures/<case-name>/
├── input.json           # Hand-authored input payload
├── expected.jsonld      # Expected JSON-LD output
└── notes.md             # What this case exercises
```

## Running against a fixture

```bash
openric-validate --fixture fonds-minimal
```

## Current fixtures

The reference host is `https://ric.theahg.co.za/api/ric/v1/` (OpenRiC reference
implementation, extracted from Heratio). Every `source-url.txt` points there.

| # | Case | Status | Purpose |
|---|---|---|---|
| 1 | `fonds-minimal` | done | Smallest valid record — title + creator |
| 2 | `fonds-with-children` | done | Hierarchy: fonds + children |
| 3 | `record-multilingual` | done | Multiple `@language` titles |
| 4 | `agent-person-simple` | done | Minimal Person agent |
| 5 | `agent-corporate-body` | done | CorporateBody |
| 6 | `agent-family` | done | Family agent |
| 7 | `place-country` | done | Place with GeoNames authority URI, lat/long |
| 8 | `place-with-parent` | done | Place nested under a parent place |
| 9 | `place-list` | done | Place list endpoint |
| 10 | `rule-law` | done | Rule — law/mandate |
| 11 | `activity-production` | done | Creation/production event |
| 12 | `activity-accumulation` | done | Accumulation event |
| 13 | `instantiation-tiff` | done | Instantiation — TIFF |
| 14 | `instantiation-application` | done | Instantiation — application/pdf etc. |
| 15 | `record-list` | done | Record list endpoint |
| 16 | `hierarchy-with-children` | done | Nested-set hierarchy walk |
| 17 | `relation-list` | done | Relation list endpoint |
| 18 | `relations-for-place` | done | Relations filtered to one entity |
| 19 | `subgraph-depth-1` | done | Rooted subgraph exercising the six graph invariants |
| 20 | `subgraph-depth-2` | done | Graph: 2-hop BFS |
| 21 | `autocomplete-egypt` | done | Cross-entity autocomplete |
| 22 | `entity-info-place` | done | Entity info card |
| 23 | `entity-write-place` | done | Entity write — create Place |
| 24 | `write-response-create` | done | Canonical write-response envelope |
| 25 | `vocabulary` | done | RiC-O vocabulary listing |
| 26 | `service-description` | done | Service description root document |
| 27 | `error-not-found` | done | 404 error envelope |
| 28 | `agent-with-relations` | planned | Successor / predecessor chains |
| 29 | `repository-with-holdings` | planned | ISDIAH repository + ≥3 fonds |
| 30 | `function-with-activities` | planned | ISDF function + ≥2 activities |
| 31 | `record-in-container` | planned | Record held in rico:Thing container |
| 32 | `record-security-classified` | planned | Classification level |
| 33 | `record-personal-data` | planned | `containsPersonalData = true` |
| 34 | `record-with-access-restriction` | planned | Restriction scope |
| 35 | `subgraph-filtered-by-type` | planned | Graph filtered by node type |
| 36 | `validation-failure` | planned | Deliberately broken input → expected SHACL failures |

## Principle

For v0.1.0 the `expected.jsonld` outputs are what the reference implementation
produces. This is intentionally circular: v0.1.0 freezes the reference output
as the canonical target, reviewed and committed. Future implementations match
this target, or the target changes via a spec PR.

Starting from v0.2.0, fixtures are expected to drive implementations rather
than follow them.

### Refreshing fixture captures

When the reference implementation ships a breaking change to response shape,
re-capture every fixture with source-url.txt:

```bash
for dir in fixtures/*/; do
  [ -f "$dir/source-url.txt" ] && \
    curl -sk "$(cat "$dir/source-url.txt")" | \
      python3 -m json.tool > "$dir/expected.jsonld"
done
```
