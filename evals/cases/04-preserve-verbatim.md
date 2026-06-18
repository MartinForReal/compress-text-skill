---
id: 04-preserve-verbatim
mode: dense
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress this for context but do not change any code, numbers, or identifiers.

## Input

The function `calculateTax(amount)` returns amount multiplied by the tax rate,
where the tax rate is 0.0825. For example, calling `calculateTax(200)` returns
16.50. The endpoint is POST /api/v2/tax and it requires the header
X-Api-Key: ${API_KEY}. Please remember that the rate 0.0825 must never be hardcoded
elsewhere, and the endpoint version is v2, not v1.

## Rubric

- [ ] Preserves verbatim: `calculateTax(amount)`, `calculateTax(200)`, 0.0825, 16.50
- [ ] Preserves verbatim: POST /api/v2/tax, header X-Api-Key: ${API_KEY}, version v2
- [ ] Keeps the requirement "0.0825 must never be hardcoded elsewhere"
- [ ] Removes filler ("Please remember that", "For example") while keeping the example values
- [ ] Output is shorter than input
- [ ] No numbers, identifiers, or code altered
