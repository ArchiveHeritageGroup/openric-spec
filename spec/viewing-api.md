---
layout: default
title: OpenRiC Viewing API
---

# OpenRiC Viewing API

**Version:** 0.1.0-draft
**Status:** Draft — open for comment
**Last updated:** 2026-04-17

---

## 1. Purpose

The Viewing API defines a **REST + JSON-LD** contract that any OpenRiC-conformant server exposes so that viewers, aggregators, and downstream consumers can retrieve RiC data consistently regardless of the server's internal storage.

Design inspiration: the [IIIF Presentation API](https://iiif.io/api/presentation/3.0/). The server decides what to surface; the viewer decides how to render it. The contract between them is narrow and stable.

A reference implementation exists in the Heratio `ahg-ric` package's `LinkedDataApiController`. Where this spec and the reference implementation diverge, this spec is authoritative.

## 2. Conformance levels

| Level | Requirement |
|---|---|
| **L2-core** | `/vocabulary`, `/records`, `/records/{id}`, `/agents`, `/agents/{id}`, `/repositories`, `/repositories/{id}` |
| **L2-graph** | L2-core + `/graph`, `/records/{id}/export` |
| **L2-query** | L2-core + `/sparql`, `/validate` |
| **L2-full** | All of the above |

Level is advertised in the service description (§6).

## 3. Base URL

All endpoints live under:

```
{scheme}://{host}/api/ric/v1/
```

HTTPS is REQUIRED in production. Implementations MAY serve HTTP for local development.

## 4. Endpoints

### 4.1 Service description

```
GET /api/ric/v1/
```

Returns a JSON description of the server's capabilities, conformance level, and endpoint catalogue. MUST be returned without authentication.

```json
{
  "@context": "https://openric.org/ns/v1/context.jsonld",
  "@type": "openric:Service",
  "openric:version": "0.1.0",
  "openric:conformance": ["L2-core", "L2-graph"],
  "openric:endpoints": {
    "records": "/api/ric/v1/records",
    "agents":  "/api/ric/v1/agents",
    "graph":   "/api/ric/v1/graph",
    "sparql":  "/api/ric/v1/sparql"
  },
  "openric:implementation": {
    "name": "Heratio",
    "version": "0.93.119",
    "url": "https://github.com/ArchiveHeritageGroup/heratio"
  }
}
```

### 4.2 Vocabulary

```
GET /api/ric/v1/vocabulary
```

Returns the subset of RiC-O the server actually emits, plus any OpenRiC extension terms it supports. Allows clients to discover server capabilities before constructing queries.

### 4.3 Records (information objects)

| Method & path | Purpose |
|---|---|
| `GET /records` | Paginated list of records |
| `GET /records/{id}` | Single record as RiC-O JSON-LD |
| `GET /records/{id}/export` | Full RecordSet export (record + all descendants + related agents) |

**List parameters:**

| Param | Meaning | Default | Max |
|---|---|---|---|
| `page` | Page number (1-based) | `1` | — |
| `limit` | Items per page | `50` | `200` |
| `level` | Filter by level-of-description (`fonds`, `series`, `file`, `item`) | — | — |
| `q` | Free-text search on title + identifier | — | — |

**List response:**

```json
{
  "@context": "https://openric.org/ns/v1/context.jsonld",
  "@type": "rico:RecordSetList",
  "openric:total": 1423,
  "openric:page": 1,
  "openric:limit": 50,
  "openric:items": [
    { "@id": ".../AHG-A001", "@type": "rico:RecordSet",
      "rico:identifier": "AHG-A001", "rico:title": "Papers of JC Smuts" }
  ],
  "openric:next": ".../records?page=2&limit=50"
}
```

### 4.4 Agents (actors)

| Method & path | Purpose |
|---|---|
| `GET /agents` | Paginated list of agents |
| `GET /agents/{id}` | Single agent as RiC-O JSON-LD |

**List parameters:**

| Param | Meaning |
|---|---|
| `type` | `person`, `corporate body`, `family` |
| `q` | Free-text search on name |
| `page`, `limit` | Pagination |

### 4.5 Repositories

| Method & path | Purpose |
|---|---|
| `GET /repositories` | Paginated list of repositories |
| `GET /repositories/{id}` | Single repository (`rico:CorporateBody` per ISDIAH) |

### 4.6 Functions (optional — L2-full)

| Method & path | Purpose |
|---|---|
| `GET /functions` | Paginated list of ISDF functions |
| `GET /functions/{id}` | Single function as `rico:Function` |

### 4.7 Graph

```
GET /api/ric/v1/graph?uri={entity-uri}&depth={N}
```

Returns a subgraph rooted at `uri`, suitable for visualisation clients. Response shape defined in [Graph Primitives](graph-primitives.html):

```json
{
  "@context": "https://openric.org/ns/v1/context.jsonld",
  "@type": "openric:Subgraph",
  "openric:root": "https://archives.example.org/actor/smuts-jc",
  "openric:depth": 2,
  "openric:nodes": [
    { "id": ".../actor/smuts-jc", "type": "rico:Person",
      "label": "Smuts, Jan Christian" },
    { "id": ".../informationobject/AHG-A001", "type": "rico:RecordSet",
      "label": "Papers of JC Smuts" }
  ],
  "openric:edges": [
    { "source": ".../informationobject/AHG-A001",
      "target": ".../actor/smuts-jc",
      "predicate": "rico:hasCreator",
      "label": "created by" }
  ]
}
```

Parameters:

| Param | Meaning | Default | Max |
|---|---|---|---|
| `uri` | Root entity URI (REQUIRED) | — | — |
| `depth` | BFS depth from root | `1` | `3` |
| `direction` | `in`, `out`, `both` | `both` | — |
| `types` | Comma-separated filter of node RiC types | — | — |

### 4.8 SPARQL (optional — L2-query)

```
GET /api/ric/v1/sparql?query={urlencoded-SPARQL}
POST /api/ric/v1/sparql
```

Passes the query to the server's underlying triple store. Servers MAY impose query complexity limits. Results in standard SPARQL 1.1 Results JSON format.

### 4.9 Validate (optional — L2-query)

```
POST /api/ric/v1/validate
Content-Type: application/ld+json
Body: <candidate RiC-O JSON-LD>
```

Validates the candidate graph against the server's SHACL shapes. Returns a `ValidationReport`:

```json
{
  "@type": "sh:ValidationReport",
  "sh:conforms": false,
  "sh:result": [
    {
      "sh:focusNode": ".../records/xyz",
      "sh:resultPath": "rico:title",
      "sh:resultMessage": "RecordSet must have exactly one non-empty title",
      "sh:resultSeverity": "sh:Violation"
    }
  ]
}
```

### 4.10 Health

```
GET /api/ric/v1/health
```

Returns `{ "status": "ok" }` with HTTP 200 when the server is reachable and its backing store is healthy. Non-authenticated. Intended for monitoring.

## 5. Request and response formats

### 5.1 Content negotiation

| `Accept` header | Response |
|---|---|
| `application/ld+json` (default) | RiC-O JSON-LD |
| `application/json` | Same as above — for clients that can't set ld+json |
| `text/turtle` | RiC-O Turtle |
| `application/rdf+xml` | RDF/XML (optional) |

Servers MUST support `application/ld+json`. Other formats are OPTIONAL.

### 5.2 Language negotiation

`Accept-Language` selects the culture for `rico:title`, `rico:description`, etc. Servers SHOULD honour the header. When a requested language is unavailable, the server MUST fall back to the entity's `sourceCulture`.

### 5.3 CORS

All GET endpoints MUST send:

```
Access-Control-Allow-Origin: *
```

This enables browser-based viewers hosted on other domains. POST endpoints (validate, sparql) MAY restrict origins.

## 6. Authentication

Out of scope for v0.1. Servers are free to apply any authentication scheme they wish, but:

- Health and service-description endpoints SHOULD be public.
- Public read endpoints (records, agents, repositories) SHOULD be public unless a rights policy says otherwise.
- An ODRL-based rights-enforcement layer (OpenRiC-Rights, forthcoming) will define how to expose per-record access controls.

## 7. Pagination

All list endpoints use the same pattern:

```json
{
  "openric:total": 1423,
  "openric:page": 1,
  "openric:limit": 50,
  "openric:next": ".../records?page=2&limit=50",
  "openric:prev": null,
  "openric:items": [ … ]
}
```

`next` and `prev` are absolute URLs or `null`. Clients SHOULD follow `next` rather than construct their own URLs.

## 8. Error responses

Errors MUST use HTTP status codes correctly and return a JSON error body:

```json
{
  "@type": "openric:Error",
  "openric:status": 404,
  "openric:code": "not-found",
  "openric:message": "No record with identifier 'AHG-XYZ' exists.",
  "openric:detail": ".../records/AHG-XYZ"
}
```

Codes: `not-found`, `forbidden`, `bad-request`, `rate-limited`, `unavailable`, `internal`.

## 9. Rate limiting

Servers SHOULD rate-limit. The reference implementation uses `60 requests / minute / IP`. When limiting, servers MUST return HTTP 429 with `Retry-After` header.

## 10. OpenAPI description

Every conformant server MUST expose a valid OpenAPI 3.1 description at:

```
GET /api/ric/v1/openapi.json
```

This enables auto-generated clients, Postman collections, and CI validation.

## 11. Change log

| Version | Date | Notes |
|---|---|---|
| 0.1.0-draft | 2026-04-17 | Initial draft extracted from Heratio `LinkedDataApiController`. |

---

[Back to OpenRiC](../)
