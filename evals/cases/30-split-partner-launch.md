---
id: 30-split-partner-launch
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

This draft combines two partner launch handoffs. Compress and restructure it into a lean note,
removing duplicated launch requirements and separating the API launch work from the marketing launch
work.

## Input

# Partner launch handoff
Every partner launch needs a named launch owner and a dated checklist. The partner API launch sends
sandbox credentials, verifies the OAuth redirect URI, and publishes the API changelog. The partner
marketing launch needs approved logo placement, a customer quote, and campaign UTM parameters. Every
partner launch needs a named launch owner and a dated checklist. The API launch must rotate the test
secret after sandbox validation. The marketing launch must schedule the social posts. Do not bundle
API checklist items into the marketing handoff.

## Rubric

- [ ] Preserves the shared launch requirements: named launch owner and dated checklist
- [ ] Preserves every API-launch point: sandbox credentials; OAuth redirect URI; API changelog; rotate the test secret after sandbox validation
- [ ] Preserves every marketing-launch point: approved logo placement; customer quote; campaign UTM parameters; social posts
- [ ] Eliminates duplicated launch requirements: launch owner and dated checklist each appear once
- [ ] Splits the combined draft into API launch vs marketing launch branches under the shared core
- [ ] Reports a candidate comparison (>=2 candidates) and selects one with a reason
- [ ] Output is shorter than the input and stays readable
