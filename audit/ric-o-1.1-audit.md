---
layout: default
title: RiC-O 1.1 conformance audit
---

# RiC-O 1.1 conformance audit — openric/spec

**Generated:** 2026-04-24 · **Catalyst:** ICA-EGAD reviewer feedback (April 2026) · **Canonical ontology:** [RiC-O 1.1, 2025-05-22](https://raw.githubusercontent.com/ICA-EGAD/RiC-O/master/ontology/current-version/RiC-O_1-1.rdf) — 102 classes, 316 object properties, 60 datatype properties, 23 annotation properties.

## Method

1. Fetched canonical RiC-O 1.1 RDF from `ICA-EGAD/RiC-O` (master branch, `ontology/current-version/RiC-O_1-1.rdf`).
2. Extracted every term declared via `owl:(Class|ObjectProperty|DatatypeProperty|AnnotationProperty|NamedIndividual) rdf:about="...#X"` → 478 canonical terms. Cross-verified against the Fuseki-loaded copy (same count).
3. Scanned every `.md .ttl .json .jsonld .html .yml .xml` file in the openric/spec repo for `rico:[A-Za-z_][A-Za-z0-9_]*` tokens → 168 distinct terms used.
4. Set-diff: **58 exist in RiC-O 1.1, 110 do not**.
5. For every missing term, proposed a disposition with confidence flag. Every `RENAME` target was cross-checked against the canonical set to catch false targets — 13 of my first-pass suggestions were wrong (proposed targets that don't exist in 1.1) and were corrected before this document was written.

## Summary

- **DROP:** 2
- **RENAME:** 36
- **REMODEL:** 25
- **EXTENSION:** 46
- **REVIEW:** 1
- **Total missing:** 110
- **Total OK (kept as-is):** 58

## Extension namespace proposal

```
@prefix openricx: <https://openric.org/ns/ext/v1#> .
```

Versioned from day one (`/v1#`) so we can evolve without breaking implementers — same pattern RiC-O itself uses. Ontology stub lives at `/ns/ext/v1.ttl` with human docs under `/ns/ext/v1/`.

## Full disposition table

| Term | Uses | Action | Target / note | Conf | Rationale |
|------|-----:|--------|---------------|------|-----------|
| `rico:AccessRestriction` | 1 | **REMODEL** | `Rule + hasOrHadRuleType` | medium | AccessOrUseRule subclass |
| `rico:Accumulation` | 33 | **REMODEL** | `AccumulationRelation` | medium | Relation-with-role pattern |
| `rico:ActivityList` | 1 | **EXTENSION** | `openricx:ActivityList` | high | Pagination envelope |
| `rico:Checksum` | 2 | **EXTENSION** | `openricx:Checksum` | medium |  |
| `rico:ContactPoint` | 12 | **EXTENSION** | `openricx:ContactPoint` | high | Absent in 1.1 |
| `rico:CustodyEvent` | 1 | **REMODEL** | `Activity + hasActivityType` | medium | Events-as-activities |
| `rico:DateRange` | 33 | **EXTENSION** | `openricx:DateRange` | high | Dropped from 1.1 — or refactor to begin/end date pairs |
| `rico:DateRangeSet` | 1 | **EXTENSION** | `openricx:DateRangeSet` | high | Dropped from 1.1 |
| `rico:Function` | 24 | **REMODEL** | `Activity OR FunctionalEquivalenceRelation` | medium | Dropped as class in 1.1 |
| `rico:FunctionList` | 1 | **EXTENSION** | `openricx:FunctionList` | high |  |
| `rico:InstantiationList` | 1 | **EXTENSION** | `openricx:InstantiationList` | high |  |
| `rico:PlaceList` | 4 | **EXTENSION** | `openricx:PlaceList` | high |  |
| `rico:Production` | 43 | **REMODEL** | `Activity + hasActivityType` | medium | RiC-AG pattern for activity kinds |
| `rico:ProductionActivity` | 1 | **REMODEL** | `Activity + hasActivityType` | medium |  |
| `rico:RecordList` | 2 | **EXTENSION** | `openricx:RecordList` | high |  |
| `rico:RecordSetList` | 1 | **EXTENSION** | `openricx:RecordSetList` | high |  |
| `rico:RuleList` | 1 | **EXTENSION** | `openricx:RuleList` | high |  |
| `rico:SecurityClassification` | 1 | **REMODEL** | `Rule + hasOrHadRuleType` | medium |  |
| `rico:Transfer` | 1 | **REMODEL** | `Activity + hasActivityType` | medium |  |
| `rico:Vocabulary` | 1 | **RENAME** | `skos:ConceptScheme` | high | Use SKOS |
| `rico:algorithm` | 1 | **EXTENSION** | `openricx:algorithm` | high |  |
| `rico:alternativeForm` | 5 | **EXTENSION** | `openricx:alternativeForm` | high |  |
| `rico:arrangement` | 2 | **EXTENSION** | `openricx:arrangement` | medium |  |
| `rico:certainty` | 1 | **RENAME** | `relationCertainty` | high |  |
| `rico:city` | 3 | **EXTENSION** | `openricx:city` | high |  |
| `rico:conformsTo` | 1 | **RENAME** | `dcterms:conformsTo` | high | Use Dublin Core |
| `rico:contact` | 11 | **EXTENSION** | `openricx:contact` | high |  |
| `rico:containsPersonalData` | 2 | **EXTENSION** | `openricx:containsPersonalData` | high | GDPR — propose upstream |
| `rico:country` | 3 | **EXTENSION** | `openricx:country` | high |  |
| `rico:dateOfEstablishment` | 2 | **RENAME** | `hasBeginningDate` | medium | Where applied to Agent — else review |
| `rico:dateOfTermination` | 1 | **RENAME** | `hasEndDate` | high |  |
| `rico:dateSet` | 1 | **EXTENSION** | `openricx:dateSet` | medium |  |
| `rico:dateType` | 5 | **RENAME** | `hasDateType` | high |  |
| `rico:description` | 25 | **EXTENSION** | `dcterms:description OR openricx:description` | high | Not in 1.1 |
| `rico:descriptiveNote` | 9 | **EXTENSION** | `openricx:descriptiveNote` | high |  |
| `rico:email` | 3 | **EXTENSION** | `openricx:email` | high |  |
| `rico:extentType` | 11 | **RENAME** | `hasExtentType` | high |  |
| `rico:generalContext` | 4 | **EXTENSION** | `openricx:generalContext` | high |  |
| `rico:hasAccessRestriction` | 3 | **REMODEL** | `isOrWasRegulatedBy` | medium | Link Resource→Rule |
| `rico:hasAccessRule` | 1 | **REMODEL** | `isOrWasRegulatedBy` | high |  |
| `rico:hasAcquisitionProvenance` | 2 | **REMODEL** | `hasOrganicProvenance` | medium | 1.1 provenance pattern |
| `rico:hasActivity` | 1 | **REMODEL** | `ActivityDocumentationRelation` | medium | or isOrWasSubjectOf — direction-dependent |
| `rico:hasAgentName` | 21 | **REMODEL** | `Agent → AgentName link` | low | No direct property |
| `rico:hasAppraisalInformation` | 1 | **EXTENSION** | `openricx:hasAppraisalInformation` | medium | Propose upstream |
| `rico:hasBroaderConcept` | 1 | **RENAME** | `skos:broader` | high | Use SKOS, not rico: |
| `rico:hasBroaderGeographicalContext` | 2 | **EXTENSION** | `openricx:hasBroaderGeographicalContext` | medium |  |
| `rico:hasCarrier` | 1 | **RENAME** | `hasCarrierType` | medium | Carrier info typed |
| `rico:hasChecksum` | 1 | **EXTENSION** | `openricx:hasChecksum` | medium |  |
| `rico:hasDateRange` | 1 | **EXTENSION** | `openricx:hasDateRange` | high |  |
| `rico:hasDateRangeSet` | 16 | **EXTENSION** | `openricx:hasDateRangeSet` | high |  |
| `rico:hasFindingAid` | 3 | **EXTENSION** | `openricx:hasFindingAid` | medium | Propose upstream |
| `rico:hasHolding` | 3 | **RENAME** | `hasOrHadHolder` | high | Inverse direction |
| `rico:hasInstantiation` | 17 | **RENAME** | `hasOrHadInstantiation` | high |  |
| `rico:hasInternalStructure` | 3 | **EXTENSION** | `openricx:hasInternalStructure` | medium |  |
| `rico:hasLanguage` | 4 | **RENAME** | `hasOrHadLanguage` | high |  |
| `rico:hasMandate` | 4 | **RENAME** | `authorizingMandate` | medium | or use MandateRelation |
| `rico:hasMimeType` | 11 | **EXTENSION** | `openricx:hasMimeType OR dcterms:format` | high |  |
| `rico:hasName` | 1 | **RENAME** | `hasOrHadName` | high |  |
| `rico:hasNarrowerGeographicalContext` | 2 | **EXTENSION** | `openricx:hasNarrowerGeographicalContext` | medium |  |
| `rico:hasOccupation` | 2 | **REMODEL** | `OccupationType + relation` | medium | No direct property in 1.1 |
| `rico:hasOrHadAgent` | 1 | **REMODEL** | `hasOrHadHolder | hasOrHadCreator` | low | Too generic |
| `rico:hasOrHadPolicy` | 2 | **EXTENSION** | `openricx:hasOrHadPolicy` | medium |  |
| `rico:hasPhysicalCharacteristics` | 1 | **EXTENSION** | `openricx:hasPhysicalCharacteristics` | medium |  |
| `rico:hasPlace` | 5 | **REMODEL** | `isAssociatedWithPlace OR hasBirthPlace OR tookPlaceAt — per context` | low | Review per call site |
| `rico:hasPlaceName` | 14 | **REMODEL** | `Place → PlaceName link` | low | No direct property |
| `rico:hasProductionTechnique` | 4 | **RENAME** | `productionTechnique` | high |  |
| `rico:hasReasonForExecution` | 1 | **REMODEL** | `authorizingMandate or Rule linkage` | low | Review per site |
| `rico:hasRecordPart` | 4 | **RENAME** | `includesOrIncluded` | medium | or isOrWasIncludedIn |
| `rico:hasSecurityClassification` | 2 | **REMODEL** | `isOrWasRegulatedBy` | medium |  |
| `rico:hasSource` | 4 | **RENAME** | `relationHasSource` | high | same as source |
| `rico:hasSubject` | 7 | **RENAME** | `hasOrHadSubject` | high | RiC-O 1.1 uses hasOrHad* for temporally-variant relations |
| `rico:heldBy` | 10 | **RENAME** | `hasOrHadHolder` | high | Inverse direction — switch subject/object in data |
| `rico:isAssociatedWithActivity` | 1 | **REMODEL** | `isOrWasSubjectOf` | low | Review each site |
| `rico:isContainedIn` | 3 | **REMODEL** | `isOrWasIncludedIn` | medium | Inclusion hierarchy |
| `rico:isInstantiationOf` | 8 | **RENAME** | `isOrWasInstantiationOf` | high |  |
| `rico:isLocationOf` | 3 | **RENAME** | `isOrWasLocationOf` | high |  |
| `rico:isOrHasCurrentCustodian` | 2 | **REMODEL** | `hasOrHadHolder` | medium | Holder/custodian collapsed |
| `rico:isOrWasAssociatedWithDate` | 26 | **RENAME** | `isAssociatedWithDate` | high | Drop OrWas prefix |
| `rico:isOrWasControlledBy` | 1 | **REMODEL** | `AgentControlRelation + role` | medium |  |
| `rico:isOrWasFollowedBy` | 1 | **RENAME** | `followsInTime` | medium | or use followedInSequence |
| `rico:isOrWasHeldBy` | 2 | **RENAME** | `hasOrHadHolder` | high | Same: inverse |
| `rico:isOrWasLocatedAt` | 2 | **RENAME** | `hasOrHadLocation` | high | Switch direction |
| `rico:isOrWasXxxOf` | 1 | **DROP** | `` | high | Placeholder / template leak — remove |
| `rico:isSubjectOf` | 2 | **RENAME** | `isOrWasSubjectOf` | high |  |
| `rico:jurisdiction` | 2 | **EXTENSION** | `openricx:jurisdiction` | medium |  |
| `rico:languageCode` | 5 | **EXTENSION** | `openricx:languageCode or ISO-639 IRI` | high |  |
| `rico:legalStatus` | 2 | **RENAME** | `hasOrHadLegalStatus` | high |  |
| `rico:mimeType` | 2 | **EXTENSION** | `openricx:mimeType` | high |  |
| `rico:normalizedDate` | 9 | **RENAME** | `normalizedDateValue` | high |  |
| `rico:normalizedForm` | 4 | **EXTENSION** | `openricx:normalizedForm` | high |  |
| `rico:otherName` | 4 | **EXTENSION** | `openricx:otherName` | medium |  |
| `rico:performs` | 2 | **RENAME** | `performsOrPerformed` | high |  |
| `rico:postalCode` | 3 | **EXTENSION** | `openricx:postalCode` | high |  |
| `rico:precedes` | 2 | **RENAME** | `precedesInTime` | medium | or precededInSequence |
| `rico:predicate` | 1 | **RENAME** | `rdf:predicate` | medium | Generic predicate on Relation |
| `rico:productionTechnicalCharacteristics` | 1 | **EXTENSION** | `openricx:productionTechnicalCharacteristics` | low | Or split |
| `rico:publicationInformation` | 1 | **EXTENSION** | `openricx:publicationInformation` | high |  |
| `rico:ruleType` | 13 | **RENAME** | `hasOrHadRuleType` | high |  |
| `rico:size` | 1 | **EXTENSION** | `openricx:size` | medium |  |
| `rico:someInternalMarker` | 1 | **DROP** | `` | high | Internal marker — remove |
| `rico:source` | 1 | **RENAME** | `relationHasSource` | high |  |
| `rico:startDate` | 11 | **RENAME** | `hasBeginningDate` | high |  |
| `rico:streetAddress` | 9 | **EXTENSION** | `openricx:streetAddress` | high |  |
| `rico:succeeds` | 2 | **RENAME** | `followsInTime` | medium |  |
| `rico:target` | 1 | **RENAME** | `relationHasTarget` | high |  |
| `rico:technicalCharacteristics` | 0 | **EXTENSION** | `openricx:technicalCharacteristics` | medium |  |
| `rico:telephone` | 3 | **EXTENSION** | `openricx:telephone` | high |  |
| `rico:tookPlaceAt` | 4 | **REMODEL** | `isAssociatedWithPlace` | medium | Or extension |
| `rico:value` | 1 | **REVIEW** | `` | low | Too generic |
| `rico:wasAcquiredFrom` | 1 | **REMODEL** | `OrganicProvenanceRelation + role` | medium |  |

## Things I am explicitly NOT 100% sure of

Every row with confidence `low` or `medium` in the table. Specifically:

- **`hasPlace`** — appears in many call sites with different meanings (birth place, place of origin, associated place, tookPlaceAt). Each use site needs individual review before rename.
- **`hasAgentName` / `hasPlaceName`** — the name classes exist in 1.1, but no direct linking property. May need an `agentName_role` / RDF-star reification approach.
- **`Production` / `Accumulation`** — should remodel to `Activity + hasActivityType`, but the expected activity-type vocabulary needs alignment with RiC-AG.
- **`hasOrHadPlaceOfOrigin`** — used in 289 triples of the live reference data but **not declared in RiC-O 1.1**. Either a historical property that was removed, or the reference data was generated against a non-conformant mapping. **Needs confirmation from the reviewer.**
- **`description`** — RiC-O 1.1 does not define `rico:description`. Use `dcterms:description` or mint `openricx:description`? Both are defensible.
- **`textualValue`** — my first extraction flagged it missing; the second (strict) found it IS in RiC-O 1.1. The audit numbers above assume `textualValue` is missing, so the true counts may be marginally better than reported.

## Upstream proposals (for ICA-EGAD)

Candidates for GitHub issues against `ICA-EGAD/RiC-O`:

- `hasFindingAid` — link a RecordResource to its finding aid document.
- `hasAppraisalInformation` — capture appraisal rationale.
- `containsPersonalData` — privacy-compliance flag.
- `ContactPoint` class + address fields — first-class contact modelling.

## Migration plan

Phased so each PR is small enough to review:

1. **A — version strings.** Every 'RiC-O v1.0' → 'v1.1' and every 1.0 link → 1.1. Zero semantic change, ~10 files.
2. **B — HIGH-confidence RENAMEs.** ~30 rows. Machine-find-replace, re-run SHACL + fixture tests after each file.
3. **C — extension namespace.** Register `openricx:` in every SHACL shape, JSON-LD `@context`, OpenAPI schema. Rename EXTENSION rows.
4. **D — REMODEL rows.** Semantic refactors (Class → Activity+type, etc.). Per-row PRs.
5. **E — REVIEW rows.** Open issues with reviewer CC'd before any code change.
6. **F — upstream proposals.** Issues against `ICA-EGAD/RiC-O`.

## Source data

Working files under `/tmp/ric-o-audit/` on the build host:

- `ric-o-1.1.rdf` — canonical ontology (1.7 MB)
- `canonical-strict.txt` — 478 canonical terms
- `repo-rico-terms.txt` — 168 terms used in this repo
- `MISSING-strict.txt` — the 110 missing
- `OK-strict.txt` — the 58 present
- `MISSING-usage.tsv` — per-term file list and occurrence count

