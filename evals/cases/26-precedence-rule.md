---
id: 26-precedence-rule
mode: readable
aggressiveness: conservative
should_trigger: true
---

## Prompt

Compress this on-call policy. Keep every rule.

## Input

On-call policy. The primary on-call engineer acknowledges every page within 15 minutes. If
the primary does not acknowledge within 15 minutes, the page automatically escalates to the
secondary on-call engineer. The runbook is the source of truth: if the runbook and the
monitoring dashboard disagree about an incident's severity, follow the runbook, not the
dashboard. During a Sev-1 incident, the incident commander has final authority and may
override the standard change-freeze rules. Outside of an active incident, the change-freeze
rules always apply and no one may override them. After every incident, write a blameless
postmortem within three business days.

## Rubric

- [ ] Keeps the 15-minute acknowledgement window and escalation to the secondary on-call engineer
- [ ] Keeps the precedence rule: when the runbook and the dashboard disagree, the runbook wins
- [ ] Keeps that during a Sev-1 the incident commander has final authority and may override the change-freeze
- [ ] Keeps that outside an incident the change-freeze always applies and cannot be overridden
- [ ] Keeps the blameless postmortem within three business days
- [ ] Preserves the authority/precedence relationships (does not drop "source of truth" / "final authority" / override scope)
- [ ] Reports an estimated size reduction
