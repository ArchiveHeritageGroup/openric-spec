---
layout: default
title: Related Implementations & Reference Projects
permalink: /related-implementations.html
---

# Related Implementations and Reference Projects

OpenRiC is one of several initiatives building practical, RiC-aligned archival linked-data infrastructure. This page lists external projects that OpenRiC tracks as implementation references, interoperability benchmarks, or external authority targets.

These projects are **independent** from OpenRiC. They are listed here because they demonstrate patterns OpenRiC adopts or learns from — not because OpenRiC has any formal partnership, endorsement, or dependency relationship with them. When citing or linking to data from these projects, follow the source attribution and licensing requirements of each.

---

## Garance — Archives nationales de France

**Project URL:** [`https://rdf.archives-nationales.culture.gouv.fr/garance/pages/en/`](https://rdf.archives-nationales.culture.gouv.fr/garance/pages/en/)
**Repository:** [`github.com/sparna-git/garance`](https://github.com/sparna-git/garance)
**Reference data:** [`github.com/ArchivesNationalesFR/Referentiels`](https://github.com/ArchivesNationalesFR/Referentiels)
**SPARQL endpoint:** [`https://sparql.archives-nationales.culture.gouv.fr/garance/sparql`](https://sparql.archives-nationales.culture.gouv.fr/garance/sparql)
**Lead:** Archives nationales de France (with Sparna).

**Garance** (*Graphe des Archives nationales pour la Recherche, l'Accès et la Navigation des Connaissances Enrichies* — Graph of the Archives nationales de France for Research, Access and Navigation of Enriched Knowledge) is the public RDF/SKOS dissemination platform for AnF reference datasets. Approximately:

- 18,400 agents
- 54,000 places
- 3,400 concepts (controlled vocabularies)

modelled in RiC-O 1.1 + SKOS, exposed as dereferenceable URIs with content negotiation, RDF/XML and CSV downloads, EAC-CPF for archival creators, generated entity pages, and a SPARQL 1.1 endpoint backed by QLever.

### Why OpenRiC tracks Garance

Garance demonstrates several patterns that OpenRiC adopts:

| Garance pattern | OpenRiC adoption |
|---|---|
| Stable semantic entity URIs separate from API endpoints | [Viewing API §3.1](spec/viewing-api.html) — semantic URI policy |
| Content negotiation (HTML / JSON-LD / Turtle / RDF/XML) | [Viewing API §3.2](spec/viewing-api.html) — content-negotiation policy |
| SKOS Concept Schemes for controlled vocabularies (place types, agent roles, etc.) | [`/vocab/`](/vocab/index.html) — OpenRiC vocabularies (activity-type, rule-type) |
| RiC-O + SKOS coexistence rather than `rico:` namespace minting | OpenRiC v0.37 namespace-remediation policy: "openricx never mints in rico:" |
| Generated static entity pages from RDF | Roadmap — Phase G |
| SPARQL 1.1 query endpoint | [`sparql-access` profile](spec/profiles/sparql-access.html) (draft) |

### How OpenRiC uses Garance

Three permitted uses, with attribution and original-URI preservation:

1. **As an architecture reference** — for the publication patterns above.
2. **As an interoperability benchmark** — for SHACL / vocabulary / entity-page conformance discussions.
3. **As an external authority-linking target** — Garance entity URIs MAY be used in OpenRiC graphs via `skos:exactMatch` / `skos:closeMatch`. Example:

```turtle
<.../agent/local-123> a rico:Person ;
    rico:name "Example Person" ;
    skos:closeMatch <https://rdf.archives-nationales.culture.gouv.fr/agent/009941> .
```

Use `skos:closeMatch` unless identity equivalence is confirmed strongly enough for `owl:sameAs`.

### What OpenRiC does NOT do with Garance

- **Does not** copy or rebrand AnF data as OpenRiC content.
- **Does not** make Garance a required dependency for OpenRiC conformance.
- **Does not** mint new OpenRiC URIs for Garance entities; the original Garance URI is the canonical identity.
- **Does not** imply ownership, endorsement, or formal partnership unless such a relationship is explicitly established with AnF.

The AnF [Referentiels repository](https://github.com/ArchivesNationalesFR/Referentiels) states that the metadata may be reused (commercially and non-commercially) provided redistribution carries precise origin attribution to "Archives nationales de France" and the date of the metadata. When citing entity descriptions, prefer the Garance entity URI.

---

## ICA-EGAD RiC-O 1.1 (canonical ontology)

**Documentation:** [`ica-egad.github.io/RiC-O/about.html`](https://ica-egad.github.io/RiC-O/about.html)
**Repository:** [`github.com/ICA-EGAD/RiC-O`](https://github.com/ICA-EGAD/RiC-O)

The canonical Records-in-Contexts ontology that OpenRiC implements. OpenRiC tracks RiC-O 1.1 (released 2025-05-22) as the authoritative source for `rico:*` terms; the OpenRiC [extension namespace](/ns/ext/v1.html) covers terms not defined in canonical 1.1. The [audit document](/audit/ric-o-1.1-audit.html) records every disposition decision.

ICA-EGAD also maintains:
- **[RiC-AG (Application Guidelines)](https://ica-egad.github.io/RiC-AG/)** — practical guidance on applying RiC-CM / RiC-O, including an EAD 2002 → RiC-O 1.1 mapping. OpenRiC's Phase F upstream-proposal candidates draw from RiC-AG patterns.
- **[RiC-O Converter](https://github.com/ArchivesNationalesFR/rico-converter)** — open-source tool converting EAD 2002 / EAC-CPF to RiC-O. Useful for institutions migrating existing finding aids.

---

## Heratio (OpenRiC reference consumer)

**Project URL:** [`heratio.theahg.co.za`](https://heratio.theahg.co.za/)
**Lead:** The Archive and Heritage Group.

A production GLAM platform (AGPL-3.0) that consumes the OpenRiC reference API for every mutating administrative action. Heratio proves the OpenRiC contract is sufficient for a real archive, but **Heratio is one consumer of OpenRiC, not a special-cased dependency** — any conformant OpenRiC server can be substituted. See the [home page](/) "If you only remember one thing" callout for the contract/consumer separation.

---

## Reciprocal listings welcome

If you maintain a public RiC-O / SKOS / archival-linked-data project and would like OpenRiC to track it as a related implementation, open a pull request against [openric/spec](https://github.com/openric/spec) adding a section to this page. The minimum bar is: public URL, lead institution, what it demonstrates, and a clear statement of how OpenRiC users may interact with it (link target, fixture source, architectural reference, etc.).
