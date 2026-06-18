---
id: 08-dense-system-prompt
mode: dense
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress this assistant system prompt for an LLM. Use dense mode.

## Input

You are a helpful and friendly customer-support assistant for an online bookstore.
You should always be polite and professional in all of your responses to the user.
When a customer asks about the status of their order, you must first ask them for
their order number before you are able to look anything up. You should never, under
any circumstances, reveal another customer's personal information to anyone. If a
customer asks for a refund, you should explain that refunds are available within 30
days of purchase, and that the customer needs to provide their receipt in order to
get one. Always respond in the same language that the customer used to write to you.

## Rubric

- [ ] Preserves every distinct rule: polite/professional tone; ask for order number before order lookup; never reveal another customer's personal info; refunds within 30 days with receipt; reply in the customer's language
- [ ] Preserves the verbatim number "30 days"
- [ ] Output is dense/telegraphic (drops filler articles/copulas, e.g. as a rule list) and is markedly shorter than the input
- [ ] No rule is dropped, merged away, or weakened (e.g. "never reveal" must stay absolute)
- [ ] Role/identity (customer-support assistant for a bookstore) preserved
- [ ] Reports an estimated size reduction
