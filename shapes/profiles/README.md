# Profile-scoped SHACL shapes

The shapes in this directory are the **OpenRiC SHACL shapes decomposed by conformance profile**. A server claiming only a subset of profiles should validate its data only against the shapes in those profiles; validating against shapes that cover endpoints the server doesn't implement produces irrelevant noise.

## Files

| File | Loads with | Shapes |
|---|---|---|
| [`always-on.shacl.ttl`](always-on.shacl.ttl) | every profile | `DateRangeShape` |
| [`core-discovery.shacl.ttl`](core-discovery.shacl.ttl) | `--profile=core-discovery` | `RecordSetShape`, `RecordShape`, `PersonShape`, `CorporateBodyShape`, `FamilyShape`, `AgentNameShape`, `RepositoryShape` |
| [`authority-context.shacl.ttl`](authority-context.shacl.ttl) | `--profile=authority-context` | `ProductionShape`, `AccumulationShape`, `ActivityShape`, `PlaceShape`, `PlaceNameShape`, `RuleShape` |
| [`digital-object-linkage.shacl.ttl`](digital-object-linkage.shacl.ttl) | `--profile=digital-object-linkage` | `InstantiationShape`, `FunctionShape` |
| [`graph-traversal.shacl.ttl`](graph-traversal.shacl.ttl) | `--profile=graph-traversal` | `RelationConsistencyShape`, `CreatorLinkShape`, `InstantiationLinkedFromRecordShape`, `OrphanedRecordShape`, `UnlinkedAgentShape`, `DuplicateIdentifierShape` |

The file naming matches the profile ids declared in `openric_conformance.profiles[].id` and accepted by `probe.sh --profile=<id>`.

## Usage

`pyshacl` (and every other SHACL engine I've tested) accepts multiple `-s` / `--shapes` flags and takes the union:

```bash
# Validate against Core Discovery
pyshacl -s always-on.shacl.ttl -s core-discovery.shacl.ttl \
        -d data.jsonld -f human

# Validate a full triple-store dump against every profile
pyshacl -s always-on.shacl.ttl \
        -s core-discovery.shacl.ttl \
        -s authority-context.shacl.ttl \
        -s digital-object-linkage.shacl.ttl \
        -s graph-traversal.shacl.ttl \
        -d full-store.nt -f human
```

## Relationship to `shapes/openric.shacl.ttl` and `shapes/full-graph.shacl.ttl`

The **parent-directory files are retained** for backward compatibility with existing CI pipelines and tooling that references them directly:

- `shapes/openric.shacl.ttl` — union of `core-discovery` + `authority-context` + `digital-object-linkage` + `RelationConsistencyShape` + `CreatorLinkShape` from `graph-traversal` + `DateRangeShape` from `always-on`.
- `shapes/full-graph.shacl.ttl` — the SPARQL-based shapes now also in `graph-traversal.shacl.ttl`.

**When editing a shape, edit both the per-profile file AND the parent-directory union file** until the parent files are retired (planned — they'll become generated artefacts of the per-profile sources).

## Extensibility

New profile shape files follow the same pattern: one Turtle file per profile id, loaded alongside `always-on.shacl.ttl`. Pure additions to an existing profile are non-breaking for clients already validating with that profile; adding a new shape to `always-on` affects every profile so changes there should go through the same review as spec changes.

## License

AGPL-3.0-or-later (same as the rest of the OpenRiC reference suite). The shapes themselves are normative parts of the [OpenRiC specification](https://openric.org/spec/) and are covered by its [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) licence.
