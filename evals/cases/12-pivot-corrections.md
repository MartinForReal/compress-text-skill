---
id: 12-pivot-corrections
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Clean up this dictated planning note. Keep only what I landed on and cut the parts where I corrected myself.

## Input

Okay, for the launch date let's go with March 15th. Actually, wait — scratch that:
marketing said March 15th collides with the conference, so the launch date is March 22nd.
The owner of the launch is Sam. No, I mean — Sam is on PTO that week, so let's make Priya
the owner instead. Budget is $50k. On second thought, ignore the $50k: finance approved
$65k, so the budget is $65k. We'll keep using the existing CI pipeline; that part doesn't
change.

## Rubric

- [ ] Final launch date is March 22nd; March 15th is no longer presented as the launch date and the "scratch that" marker is gone
- [ ] Owner is Priya; Sam is no longer presented as the owner and the "no, I mean" correction marker is gone
- [ ] Budget is $65k; $50k is no longer presented as the budget and the "on second thought"/"ignore" markers are gone
- [ ] Keeps the unchanged fact: continue using the existing CI pipeline
- [ ] No self-correction connectives remain ("actually", "wait", "scratch that", "no, I mean", "on second thought", "ignore")
- [ ] Output is shorter than the input and stays readable prose; reports an estimated size reduction
- [ ] Does not invent any decision the note didn't land on (only the final intent is kept)
