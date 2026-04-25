# Fixture — activity-production-full

**Profile:** `provenance-event`
**Endpoint:** `GET /api/ric/v1/activities/{id}` on a record-producing event
**Shape:** `:StrictProductionShape` in [shapes/profiles/provenance-event.shacl.ttl](../../shapes/profiles/provenance-event.shacl.ttl)

Pins the **full-context** Production shape: name, date range (both endpoints + expressed), resulting record, participating agent, and location. This is what Provenance & Event requires a Production event to look like; the shorter `activity-production` fixture (tagged `authority-context` only) has just name + date and would fail `:StrictProductionShape`.

Three invariants this fixture proves:

1. `rico:resultsOrResultedIn` → RecordSet stub, not a loose `@id` string (the link is typed so SHACL can validate the target is actually a record).
2. `rico:hasOrHadParticipant` → CorporateBody stub. Person or Family also valid. A rico:Place or rico:Thing as the target is a `:ParticipantTypeShape` Violation.
3. `rico:isAssociatedWithDate` → structured `openricx:DateRange` object, not a bare `xsd:date` string. Both endpoints + `rico:expressedDate` recommended when the source data is a date range.

`rico:hasOrHadLocation` is optional (Warning at most) — included here because the reference mapping spec (§5.2.1 / §5.2.3) suggests it for events with a known place.

## Reference-implementation status (2026-04-21)

The reference OpenRiC service at `ric.theahg.co.za` currently emits Production events **without** `rico:resultsOrResultedIn` and `rico:hasOrHadParticipant` — see `packages/ahg-ric/src/Services/RicSerializationService.php::serializeActivity`. A future service release will close this gap; until then, the reference service does NOT conform to `provenance-event` even though it satisfies `authority-context`.
