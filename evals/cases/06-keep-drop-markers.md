---
id: 06-keep-drop-markers
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress this note. Honor the keep/drop markers.

## Input

Our staging URL is <!-- keep -->https://staging.acme.example/api/v3<!-- /keep -->
and you should, generally speaking, use it for all of your pre-production testing
work before you go ahead and ship anything to production.

<!-- drop -->TODO(me): rewrite this whole paragraph later, it's a mess and I hate it.<!-- /drop -->

Please also remember, and this is quite important, that the on-call rotation
handoff happens every single Monday at 09:00 UTC, without exception, every week.

## Rubric

- [ ] Reproduces the `<!-- keep -->` span verbatim: `https://staging.acme.example/api/v3`
- [ ] Removes the entire `<!-- drop -->` span (the TODO line) from the output
- [ ] Strips the marker delimiters themselves (no `<!-- keep -->` / `<!-- drop -->` text in output)
- [ ] Keeps both surviving facts: staging URL is for pre-production testing; on-call handoff Mondays 09:00 UTC
- [ ] Removes filler ("generally speaking", "go ahead and", "and this is quite important", "without exception, every week")
- [ ] Output is shorter than input and reads as fluent prose
