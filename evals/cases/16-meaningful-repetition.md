---
id: 16-meaningful-repetition
mode: readable
aggressiveness: conservative
should_trigger: true
---

## Prompt

Trim this release checklist without dropping any required step.

## Input

Release checklist. Before publishing, verify the signature on the installer. Verify the
signature on the SDK package. Verify the signature on the documentation bundle. Each
artifact is signed with a different key, so all three checks are required and none can be
skipped. After the three signatures check out, publish the build to the mirror.

## Rubric

- [ ] All three distinct signature checks survive (installer, SDK package, documentation bundle) — they are NOT merged into one generic "verify signatures" step
- [ ] Keeps the rationale that each artifact uses a different key and all three checks are required
- [ ] Does not treat the repeated "verify the signature" structure as redundancy to cut
- [ ] Final step preserved: publish the build to the mirror
- [ ] Reports a small/modest reduction (the text is already mostly load-bearing); does not over-compress
