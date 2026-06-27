---
id: 17-semantic-entailment
mode: dense
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress for an LLM context window. Dense mode.

## Input

The service must remain available at all times. We require 100% uptime with zero
scheduled downtime. Latency should be acceptable to users. Specifically, the p99
response time must stay under 200 milliseconds. Our users are located all over the
world. The deployment spans every inhabited continent.

## Rubric

- [ ] Merges each vague/specific pair into the specific one: keeps "100% uptime / zero scheduled downtime" and drops the weaker "available at all times"
- [ ] Keeps "p99 < 200 ms" and drops the weaker "latency should be acceptable"
- [ ] Merges the worldwide-users / every-continent restatement into a single statement (they share no words but say the same thing)
- [ ] Dense telegraphic style; no meaning lost
- [ ] Reports an estimated size reduction
