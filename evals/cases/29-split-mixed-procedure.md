---
id: 29-split-mixed-procedure
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

This operations draft mixes two procedures together. Compress and restructure it into one lean
guide, removing repeated setup text and separating distinct procedures so readers can follow the
right path.

## Input

# Operations quick guide
Use the internal portal for every request because the portal creates an audit trail. For production
incidents, set the severity, page the on-call engineer if the issue is Sev-1 or Sev-2, and open an
incident channel. For vendor access, use the internal portal, collect a business justification,
manager approval, and an expiry date, then send it to Security for review. For production incidents,
write the timeline and postmortem within three business days. For vendor access, remove the access
when the contract ends. Remember that the internal portal creates an audit trail for every request.

## Rubric

- [ ] Preserves every distinct incident point: severity; page on-call for Sev-1/Sev-2; open an incident channel; timeline/postmortem within three business days
- [ ] Preserves every distinct vendor-access point: business justification; manager approval; expiry date; Security review; remove access when the contract ends
- [ ] Eliminates duplicated setup: the internal portal/audit-trail requirement is stated once, not repeated under both procedures
- [ ] Splits the mixed draft into separate incident and vendor-access paths under one shared setup point
- [ ] Reports a candidate comparison (>=2 candidates) and selects one with a reason
- [ ] Output is shorter than the input and stays readable
