---
id: 07-output-template
mode: readable
aggressiveness: conservative
should_trigger: true
---

## Prompt

Compress this release note and emit it into the output template below.

template:
```
### <!-- slot:title -->
<!-- slot:compressed -->
_Size: <!-- slot:reduction -->_
```

## Input

Title: Version 2.4 Release

In this brand-new and very exciting release, which we are super thrilled about,
we have finally gone ahead and added the long-awaited dark mode feature that so
many of you have been asking us about for such a long time now. We also, on top
of that, fixed a rather nasty bug where the export button would, somewhat
annoyingly, fail silently without showing any error message at all to the user.

## Rubric

- [ ] Output uses the supplied template shape: an `###` heading, then body, then an italic size line
- [ ] `slot:title` filled with the title ("Version 2.4 Release")
- [ ] `slot:compressed` filled with the compressed body (dark mode added; export-button silent-failure bug fixed)
- [ ] `slot:reduction` filled with an estimated size reduction (e.g. a percentage)
- [ ] No `<!-- slot:NAME -->` markers remain in the output
- [ ] Removes filler ("brand-new and very exciting", "super thrilled", "finally gone ahead", "such a long time") while keeping both changes
