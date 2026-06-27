---
id: 14-chained-supersession
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Tighten these standup notes. Keep only what we actually settled on and drop the back-and-forth.

## Input

Standup notes. For the API rate limit, let's set it to 100 requests per minute.
Hmm, actually 100 might be too low for the mobile clients, so make it 500 per minute.
Wait, no — 500 will blow our infra budget, so let's settle on 300 requests per minute.
For the database, we'll use MongoDB. Actually, scratch that: the team knows Postgres
better, so use Postgres. The deploy target stays AWS us-east-1; no change there.

## Rubric

- [ ] Final API rate limit is 300 requests/minute; neither 100 nor 500 is presented as the limit (both earlier values dropped, not just the first)
- [ ] Database is Postgres; MongoDB is gone
- [ ] Deploy target AWS us-east-1 is kept unchanged
- [ ] Every self-correction marker is removed ("hmm", "actually", "wait, no", "scratch that")
- [ ] Output is shorter than the input and stays readable; reports an estimated size reduction
- [ ] Does not invent any value; only the settled decisions remain
