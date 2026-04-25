---
layout: default
title: OpenRiC Drift Log — Public known issues
permalink: /drift-log.html
---

# OpenRiC Drift Log

A public log of known drift between the OpenRiC specification and its public surfaces (reference API, viewer, capture client, OpenAPI metadata, conformance probe). Updated as items land or are resolved.

This page exists because the spec moves faster than the supporting implementations, and external reviewers need a single place to see *which* gaps are known, *where* they are, and *what's planned*. It is not a defect tracker — it tracks **deliberate** lag between the spec and downstream systems.

**Last updated:** 2026-04-25.

---

## Open drift items

### Reference API (`ric.theahg.co.za`) lag against spec v0.37.0

The reference Laravel service (openric/service v0.8.19) currently tracks spec v0.36.0. Migration to v0.37.0 is **Phase G**. Items pending in Phase G:

| Item | Currently emits | Target (spec v0.37.0) | ETA |
|---|---|---|---|
| Service description | `spec_version: "0.36.0"`, claims 6 of 7 profiles | `spec_version: "0.37.0"`, declares 6 of 7 + optionally `sparql-access` draft | Phase G |
| OpenAPI tags — Repository | `rico:Repository / Custodian` | `ISDIAH repository surface; canonical: rico:CorporateBody with hasOrHadHolder` | Phase G |
| OpenAPI tags — Function | `rico:Function (ISDF)` | `ISDF function surface; canonical: openricx:Function (interim) — see mapping §6.4` | Phase G |
| OpenAPI tags — SPARQL | `Subgraph walks + full SPARQL` | `Subgraph walks; SPARQL only if server declares sparql-access draft profile` | Phase G |
| Relation examples | `relation_type: hasInstantiation` | `rico:hasOrHadInstantiation` | Phase G |
| JSON-LD `@type` for events | `rico:Production` / `rico:Accumulation` (concrete classes) | `rico:Activity` + `rico:hasActivityType <vocab IRI>` (Activity+type per spec D.3) | Phase G |
| JSON-LD `@context` extension | no `openricx:` declaration | declares `openricx: https://openric.org/ns/ext/v1#` | Phase G |
| Hold-direction property names | `rico:heldBy`, `rico:hasInstantiation`, `rico:hasSubject`, `rico:hasLanguage`, `rico:hasMandate`, `rico:hasRecordPart`, `rico:isContainedIn`, etc. | Canonical 1.1 forms (`rico:hasOrHadHolder`, `rico:hasOrHadInstantiation`, etc. — full list in spec audit doc Phase B + D mappings) | Phase G |
| Provenance & Event profile claim | Not claimed (data-gap blocker — 177 productions missing creator) | Claim once data backfill completes | Phase G + data hygiene |

### Viewer (`viewer.openric.org`)

| Item | Issue | Plan |
|---|---|---|
| Node.type CURIE handling | Viewer must accept both `rico:Person` (CURIE, per spec v0.37 §8.6) and bare local names from older servers | Update viewer to canonicalize on read; emit only CURIEs in fresh requests |
| Activity-type rendering | Viewer currently dispatches on `@type` for Production/Accumulation/Activity; needs to also dispatch on `rico:hasActivityType` IRI | Add hasActivityType branch in node-classification logic |
| openricx prefix | Viewer must declare and resolve `openricx:` in JSON-LD contexts | Update bundled context |

### Capture client (`capture.openric.org`)

| Item | Issue | Plan |
|---|---|---|
| Activity entity entry form | Currently picks `Production` / `Accumulation` / `Activity` as the @type | Refactor to single `rico:Activity` + activity-type dropdown sourced from `/vocab/activity-type` |
| Repository entity | Form labels suggest `rico:Repository` is a class | Re-label as "ISDIAH repository — canonical: CorporateBody with holder relations" |
| Function entity | Form emits `rico:Function` | Switch to `openricx:Function` until ICA-EGAD upstream decision |

### Conformance probe (`/conformance/`)

| Item | Issue | Plan |
|---|---|---|
| Default probe checks `/sparql` | Spec v0.37 says SPARQL is optional under `sparql-access` profile | Skip `/sparql` checks unless server declares `sparql-access` |
| Profile-based probe modes | Currently only the legacy L1-L4 mode | Add `--profile=<id>` for each of the 7 normative + 1 draft profile |

### Documentation drift on the static site

| Item | Issue | Plan |
|---|---|---|
| Live homepage shows historical version pills (v0.1.0, v0.2.0) in the phase-cards section | These are accurate historical labels but reviewers may misread | Add a clearer "phase history" header above the cards |

---

## Closed (recent)

- **2026-04-25, v0.37.0** — RiC-O 1.1 namespace remediation, all 5 phases (A → E). Audit: 110 → 0 genuine emit-context violations.
- **2026-04-25, v0.37.0** — Per-document version headers (mapping/viewing-api/graph-primitives/conformance) bumped from `0.1.0-draft` to `0.37.0`.
- **2026-04-25, v0.37.0** — Mapping spec stale "review in progress" callout replaced with "REMEDIATION COMPLETE" callout.
- **2026-04-25, v0.37.0** — Audit doc opened with prominent STATUS banner.
- **2026-04-25, v0.37.0** — README current-version banner updated to v0.37.0.
- **2026-04-25, v0.37.0** — `drift-log.md` (this page) created.

---

## How to file a new drift item

Open a [discussion on openric/spec](https://github.com/openric/spec/discussions) with the label `drift`, or open a PR adding a row to this page. Format:

```md
| Surface | Currently observed | Target spec § | ETA / blocker |
|---|---|---|---|
| <which surface> | <what it does today> | <which spec section it should match> | <when, or what blocks it> |
```

OpenRiC's commitment: every open drift item is named, located, and either has an ETA or has a blocker explanation.
