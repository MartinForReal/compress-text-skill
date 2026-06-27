---
id: 27-cross-context-keypoint-tree
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

These three onboarding docs belong together. Compress and restructure them into one lean
doc, removing anything that is duplicated across them. Generate candidate groupings and
pick the leanest.

## Input

# Onboarding — Repository access
All access to internal systems requires the corporate VPN. To get a repository granted,
request access in the #it-help channel. Repositories also require two-factor
authentication (2FA) to be enabled on your account.

# Onboarding — Database access
All access to internal systems requires the corporate VPN. To get a database granted,
request access in the #it-help channel. Databases also require sign-off from a DBA
before access is provisioned.

# Onboarding — Laptop setup
All access to internal systems requires the corporate VPN. Company laptops must have
full-disk encryption enabled before they touch any internal system.

## Rubric

- [ ] Preserves every distinct key point: corporate VPN required; request access in `#it-help`; repositories require 2FA; databases require DBA sign-off; laptops require full-disk encryption
- [ ] Eliminates the duplicated key point: the VPN requirement is stated once, not three times
- [ ] Hoists the shared sub-point: the `#it-help` request step (shared by repository + database access) is stated once, not twice
- [ ] Builds one key-point tree over the whole context (the shared points sit above the per-resource deltas), not three independent sections each repeating the shared facts
- [ ] Reports a candidate comparison (≥2 candidates) and selects one with a reason
- [ ] Output is shorter than the combined input and stays readable
