---
id: 02-duplicate-notes
mode: dense
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Deduplicate and compress these notes for an LLM context. Show the candidate comparison.

## Input

- Decision: we will migrate the database to Postgres by Q3.
- The team agreed to move the DB to Postgres before Q3 ends.
- Owner: Priya owns the migration.
- Action: Priya to draft the migration plan.
- Note: migration target is Postgres (not MySQL).
- The migration must finish in Q3; Priya is the owner.
- Reference: see RFC-128 for the schema diff.

## Rubric

- [ ] Consolidates the repeated "migrate to Postgres by Q3" statements into one
- [ ] Preserves owner = Priya, target = Postgres, deadline = Q3, action = draft migration plan
- [ ] Keeps the reference "RFC-128" intact (verbatim)
- [ ] Output is dense (telegraphic acceptable)
- [ ] Includes a candidate-comparison table per the skill's output template
- [ ] Fidelity coverage reported as 100%
