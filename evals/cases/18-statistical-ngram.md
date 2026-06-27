---
id: 18-statistical-ngram
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Deduplicate and tighten this status update; tell me how much was repeated.

## Input

Project status update. The team completed the login feature this week. The login feature
was finished by the team this week. We also note that, as is often the case, progress was
made. Testing is ongoing and testing continues. Please be aware that the deadline is
October 30th. Just to reiterate, the deadline remains October 30th. Overall, things are
going well and we are pleased with the progress that has been made.

## Rubric

- [ ] Consolidates each near-duplicate pair to one statement: login feature completed; testing ongoing; deadline October 30th
- [ ] Drops the pure filler that carries no information ("as is often the case, progress was made", "things are going well and we are pleased with progress", "please be aware", "just to reiterate")
- [ ] Reports how much redundancy was removed (count of duplicate/near-duplicate sentences)
- [ ] Readable; reports an estimated size reduction
- [ ] Keeps the three real facts and invents nothing
