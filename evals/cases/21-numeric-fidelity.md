---
id: 21-numeric-fidelity
mode: readable
aggressiveness: conservative
should_trigger: true
---

## Prompt

Compress this metrics summary. Keep all the figures.

## Input

Q3 metrics summary. Revenue was $4.2M this quarter, up from $3.1M in Q2. As noted above,
revenue for the quarter landed at $4.2M. Active users grew to 18,400. Monthly churn was
2.3%. The support team closed 1,205 tickets, with a median resolution time of 6 hours. Our
latest NPS score is 47. Overall the numbers look solid and the whole team is happy with
the trajectory we are on.

## Rubric

- [ ] Preserves every distinct figure exactly: $4.2M, $3.1M, 18,400, 2.3%, 1,205 tickets, 6 hours, NPS 47
- [ ] Removes the duplicated "$4.2M" restatement (revenue figure stated once)
- [ ] Cuts the vacuous closing sentiment ("the numbers look solid and the whole team is happy")
- [ ] Does not merge, round, or mangle any number
- [ ] Output shorter than input; reports an estimated size reduction
