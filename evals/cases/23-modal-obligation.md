---
id: 23-modal-obligation
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress this API integration guide. Keep every requirement level exact.

## Input

Guidelines for integrating with the Payments API. Clients must authenticate every request
with a valid API key; a request without a valid API key will be rejected, so authenticating
every request is mandatory. Clients should retry a failed request that returns a 503 status,
using exponential backoff, because a 503 means the service is temporarily unavailable.
Clients may cache successful GET responses for up to 60 seconds to reduce load, but this
caching is entirely optional. Clients must never log the full card number; writing a full
card number to the logs is strictly prohibited. When a payment is declined, clients should
show the user the decline reason returned by the API. Clients may use either the v2 or the
v3 endpoint, though v3 is recommended.

## Rubric

- [ ] Keeps the requirement (must) to authenticate every request with a valid API key — not softened to a bare imperative
- [ ] Keeps the recommendation (should) to retry on 503 with exponential backoff, distinct from a hard requirement
- [ ] Keeps that caching GET responses for up to 60 seconds is optional (may)
- [ ] Preserves the prohibition: must never log the full card number
- [ ] Keeps the recommendation (should) to show the decline reason
- [ ] Keeps that v3 is recommended while v2 is still allowed (may use either)
- [ ] Does not flatten the distinct obligation levels (must / should / may) into uniform imperatives
- [ ] Reports an estimated size reduction
