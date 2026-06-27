---
id: 24-quantifier-bounds
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress these password rules. Keep every limit exact.

## Input

Password requirements for the account system. A password must be at least 12 characters
long; anything shorter than 12 characters is rejected at sign-up. A password may contain no
more than 64 characters. Every password must include at least one uppercase letter and at
least one digit. A password must not reuse any of the user's last 5 passwords. An account
locks after exactly 5 failed login attempts in a row, and once locked it stays locked for at
least 30 minutes. A password reset link is valid for only 15 minutes after it is issued.

## Rubric

- [ ] Keeps the minimum length: at least 12 characters
- [ ] Keeps the maximum length: no more than 64 characters
- [ ] Keeps "at least one uppercase letter" and "at least one digit"
- [ ] Keeps that a password must not reuse the last 5 passwords
- [ ] Keeps the lockout trigger of 5 failed attempts in a row and the at-least-30-minute lock duration
- [ ] Keeps that the reset link is valid for 15 minutes
- [ ] Drops no bound qualifier that changes meaning ("at least", "no more than", the 5-password window)
- [ ] Reports an estimated size reduction
