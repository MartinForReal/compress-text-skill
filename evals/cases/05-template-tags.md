---
id: 05-template-tags
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress this email template for context, but keep every template tag exactly as-is.

## Input

Hi {{ customer.first_name }},

We are writing to you today because we wanted to let you know, and we really do
mean it, that your order number {{ order.id }} has now been shipped out and is
on its way to you. {% if order.express %}Because you chose our express shipping
option, your package should be arriving very soon.{% endif %}

You can, at any time, track the current status of your package by simply clicking
on the following link right here: {{ tracking_url }}. Thank you so very much for
shopping with us, we truly appreciate it.

Best regards,
The ${STORE_NAME} Team

## Rubric

- [ ] Preserves verbatim and in order: `{{ customer.first_name }}`, `{{ order.id }}`, `{{ tracking_url }}`, `${STORE_NAME}`
- [ ] Preserves the `{% if order.express %}...{% endif %}` block intact, with its conditional text inside
- [ ] No template tag is reordered, merged, dropped, or edited
- [ ] Removes filler ("we really do mean it", "very soon", "simply", "right here", "so very much")
- [ ] Output is shorter than input and reads as fluent prose (readable mode)
- [ ] Greeting, body, and sign-off structure preserved
