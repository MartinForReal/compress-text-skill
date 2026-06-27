---
id: 20-conditional-branches
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress this deploy runbook without losing any rule.

## Input

Deployment rules. When the build is green, deploy to staging automatically. When the
build is red, do not deploy and page the on-call engineer. Deploying to production always
requires two approvals from senior engineers. Never deploy to production on a Friday, and
never deploy during a release freeze. If a production deploy fails, roll back immediately
and open an incident ticket. Remember that every production deploy needs two approvals
before it can go out.

## Rubric

- [ ] Preserves every branch: green build -> auto-deploy to staging; red build -> do NOT deploy and page on-call
- [ ] Keeps the production rule: two approvals from senior engineers
- [ ] Keeps both guards: never deploy to production on a Friday; never during a release freeze
- [ ] Keeps the failure branch: failed production deploy -> roll back immediately and open an incident
- [ ] Does not flip the "red build -> do not deploy" negation, and consolidates the duplicated "two approvals" statement
- [ ] Output shorter than input; reports an estimated size reduction
