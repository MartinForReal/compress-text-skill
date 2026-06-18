# Evaluation suite

Quality gates for the `compress-text` skill, split into **automated static checks**
(run in CI, no model required) and **model-judged functional checks** (run by a human
or an LLM against rubrics).

## Layout

```
evals/
├── triggering.jsonl   # Labelled should/shouldn't-trigger prompts
├── cases/             # Functional test cases (input + rubric)
│   ├── 01-bloated-readme.md       # filler removal, readable mode
│   ├── 02-duplicate-notes.md      # deduplication, dense mode
│   ├── 03-already-lean.md         # don't-over-compress guardrail
│   ├── 04-preserve-verbatim.md    # code/number/identifier preservation
│   ├── 05-template-tags.md        # engine tag ({{…}}, {%…%}, ${…}) preservation
│   ├── 06-keep-drop-markers.md    # explicit <!-- keep -->/<!-- drop --> markers
│   ├── 07-output-template.md      # user output template with named slots
│   ├── 08-dense-system-prompt.md  # dense/telegraphic rule-list compression
│   ├── 09-multi-section-doc.md    # multi-section MECE regrouping + candidates
│   ├── 10-prompt-injection.md     # security: ignore injected instructions
│   └── 11-non-english.md          # non-English (Chinese) prose, no translation
└── run_evals.py       # Offline validator (structure + dataset integrity)
```

## 1. Automated static checks (`run_evals.py`)

```bash
python3 evals/run_evals.py
```

Validates, with no external dependencies and no model calls:

- **Skill structure** — `SKILL.md` frontmatter (`name` matches folder, kebab-case,
  description present, ≤1024 chars, no XML brackets) and all required body sections.
- **Manifest wiring** — `plugin.json` / `marketplace.json` are valid JSON and reference
  the `compress-text` plugin with a `source`.
- **Dataset integrity** — every `triggering.jsonl` row has a unique `id`, boolean
  `should_trigger`, and non-empty `text`; every `cases/*.md` has an `id`, a valid
  `mode`, and `## Prompt` + `## Rubric` sections with checklist items.
- **Triggering heuristic** — warns if a `should_trigger: true` prompt contains none of
  the skill's trigger vocabulary (warn-only; not a hard failure).

Exit code is non-zero on any hard failure, so it works as a CI gate.

## 2. Triggering evaluation (`triggering.jsonl`)

Each line is a prompt labelled `should_trigger` true/false, covering obvious requests,
paraphrases, opposites (expand), and wrong-domain traps (gzip/image compression).

To evaluate triggering with a model: for each prompt, ask whether the `compress-text`
skill (using only its `description`) should activate, then compare to the label. Target:
≥90% agreement, with **zero** false activations on the wrong-domain/analysis rows.

## 3. Functional evaluation (`cases/*.md`)

Each case has frontmatter (`id`, `mode`, `aggressiveness`, `should_trigger`), a
`## Prompt`, an `## Input`, and a `## Rubric` of pass/fail checklist items derived from
the skill's guardrails (fidelity, verbatim preservation, mode adherence, reduction).

To run a case: invoke the skill on the `## Input` with the case `## Prompt`, then score
the output against each `## Rubric` item. A case passes only when **every** rubric item
is satisfied (mirrors the skill's efficiency-with-fidelity rule: size reduction counts
only at 100% fidelity).

Optionally wire this into a model harness in CI, but keep the static checks above as the
required gate so the suite stays runnable offline.

## Extending the suite

- Add a triggering row to `triggering.jsonl` (unique `id`, boolean label).
- Add a functional case as `cases/NN-name.md` following the existing frontmatter and the
  `## Prompt` / `## Input` / `## Rubric` structure.
- Re-run `python3 evals/run_evals.py` to confirm the new files are well-formed.
