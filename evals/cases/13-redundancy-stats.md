---
id: 13-redundancy-stats
mode: dense
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress this for an LLM context and report how much redundancy you removed.

## Input

The cache layer improves performance. The cache layer improves performance significantly
for read-heavy workloads. Our system is read-heavy. Because our system is read-heavy, the
cache layer improves performance. Cache entries expire after 300 seconds. Cache entries
have a TTL of 300 seconds. The TTL for cache entries is 300 seconds. Invalidate the cache
on write. On every write, invalidate the cache. Writes must invalidate the cache.

## Rubric

- [ ] Consolidates the repeated "cache improves performance for read-heavy workloads" sentences into one
- [ ] Consolidates the three TTL statements into one (TTL = 300 seconds / 300s)
- [ ] Consolidates the three "invalidate the cache on write" statements into one
- [ ] Preserves the verbatim facts: 300 seconds (or 300s), read-heavy, invalidate on write
- [ ] Reports a statistical redundancy measure (e.g. count of duplicate/near-duplicate sentences removed) alongside the size reduction
- [ ] Output is dense and clearly shorter than the input; fidelity reported as 100%
- [ ] Includes a candidate-comparison table per the skill's output template
