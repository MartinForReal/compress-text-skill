---
id: 19-negation-exception
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress this access policy. Keep every rule exact.

## Input

Access policy for production logs. As a general rule, all engineers may read the
production logs, and reading the production logs is a normal part of an engineer's daily
work. To restate the access rule: engineers are allowed to read production logs. However,
engineers must never export those logs to personal devices or personal cloud accounts.
Contractors are different: contractors may not read production logs at all, except when
they have signed the current NDA and a manager has granted them temporary, time-boxed
access. Finally, under no circumstances may anyone disable audit logging, not even
briefly for debugging.

## Rubric

- [ ] Keeps that engineers may read production logs (the three redundant restatements collapse to one)
- [ ] Preserves the prohibition intact: engineers must NEVER export logs to personal devices or personal cloud accounts
- [ ] Preserves the contractor rule WITH its exception: contractors may not read, EXCEPT with a signed NDA and manager-granted temporary access
- [ ] Preserves the absolute rule: never disable audit logging
- [ ] Drops or weakens no negation ("never", "not", "no") and no exception ("except", "unless")
- [ ] Reports an estimated size reduction
