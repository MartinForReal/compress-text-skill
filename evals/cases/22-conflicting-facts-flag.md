---
id: 22-conflicting-facts-flag
mode: readable
aggressiveness: conservative
should_trigger: true
---

## Prompt

Compress this project brief. Don't lose any requirement.

## Input

Project brief: Apollo. The kickoff is scheduled for March 15. The service must handle
1,000 requests per second at peak. The kickoff is scheduled for March 30. Marketing will
prepare the launch announcement. The service must sustain 1,000 requests per second at
peak load. Budget is capped at $50k.

## Rubric

- [ ] Consolidates the genuinely duplicated requirement (1,000 requests per second at peak, stated twice -> once)
- [ ] Detects that the kickoff date is INCONSISTENT: "March 15" and "March 30" both appear and conflict
- [ ] Keeps BOTH conflicting dates and flags the conflict; does NOT silently pick one, assume the later one wins, or merge them into a single date
- [ ] Preserves the other facts: 1,000 requests/second at peak, marketing launch announcement, $50k budget
- [ ] Conservative: reports an estimated size reduction (modest is fine — both dates plus a flag must survive)
