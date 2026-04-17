# Fixture: `agent-person-simple`

**Source:** [`https://heratio.theahg.co.za/api/ric/v1/agents/d6mh-ktzy-h6qz`](https://heratio.theahg.co.za/api/ric/v1/agents/d6mh-ktzy-h6qz)

A single Agent response (in this case resolved as rico:Agent because the underlying actor has no entity_type_id). Exercises: @context prefix bindings, @id/type/name minimal Agent payload, schema selection by @type, SHACL AgentShape with rico:name shorthand.

**Validation:** `expected.jsonld` MUST validate against the schema selected by its `@type`.
