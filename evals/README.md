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
│   ├── 11-non-english.md          # non-English (Chinese) prose, no translation
│   ├── 12-pivot-corrections.md    # supersession: drop self-corrections, keep final intent
│   ├── 13-redundancy-stats.md     # statistical redundancy consolidation + reporting
│   ├── 14-chained-supersession.md # [held-out] value pivoted twice (A→B→C); keep only final
│   ├── 15-ambiguous-pivot-flag.md # [held-out] unresolved choice must be flagged, not guessed
│   ├── 16-meaningful-repetition.md# [held-out] load-bearing repetition must not be cut
│   ├── 17-semantic-entailment.md  # [held-out] merge vague/specific pairs sharing no words
│   ├── 18-statistical-ngram.md    # [held-out r01] consolidate near-duplicates + drop filler
│   ├── 19-negation-exception.md   # [held-out r02] keep every buried negation/exception
│   ├── 20-conditional-branches.md # [held-out r02] keep every branch/guard of a runbook
│   ├── 21-numeric-fidelity.md     # [held-out r02] preserve distinct figures, drop duplicate
│   └── 22-conflicting-facts-flag.md # [held-out r02] conflicting facts kept + flagged, not merged
├── functional_checks.json # Deterministic assertions + golden references per case (+ train/val split)
├── run_functional.py  # Functional harness (offline self-test / live model / grade rollouts)
├── skillopt/          # SkillOpt rollout trajectories (round-NN/baseline, round-NN/candidate)
├── OPTIMIZATION_LOG.md # SkillOpt round write-ups (rollout → reflect → edit → validate)
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

## 4. Functional harness (`run_functional.py`)

A deterministic, dependency-free verifier that scores the skill's *behaviour* (not just
structure) against machine-checkable assertions in `functional_checks.json` (verbatim
contains/forbids, regexes, ordering, count caps, word/char compression ratios, CJK / no-translation
ratios). Three modes:

```bash
python3 evals/run_functional.py --selftest          # offline: score golden references (CI-safe)
python3 evals/run_functional.py --model             # live: run the skill via an LLM endpoint
python3 evals/run_functional.py --grade DIR         # offline: score a dir of <case_id>.txt rollouts
```

`--selftest` proves the check engine and assertions are self-consistent by scoring a stored
golden `reference_output` for every case (exit non-zero on any miss) — it runs in CI via
`scripts/validate.sh`. `--model` executes the skill on each case through an
OpenAI-chat-compatible endpoint (`LLM_API_BASE` / `LLM_API_KEY` / `LLM_MODEL`) and scores the
live output. `--grade DIR` scores pre-captured rollout outputs. Any mode accepts
`--split train|val|all` and `--cases id,id`.

## 5. SkillOpt optimization (`OPTIMIZATION_LOG.md`)

The skill is improved with the [SkillOpt](https://microsoft.github.io/SkillOpt/) discipline:
`SKILL.md` is the **trainable state** of a frozen agent, optimized by
*rollout → score → reflect → bounded edit → validate on a held-out set → export*. Cases are
labelled with a `split` in `functional_checks.json`:

- **`train`** (held-in) — the original `01`–`13`; used to design lenses and reflect on failures.
- **`val`** (held-out) — fresh cases in unseen domains, added per round (`14`–`18` round 01,
  `19`–`22` round 02); used **only** as the acceptance gate. An edit is kept only if the `val`
  split improves and `train` does not regress (validation-gated update). When a `val` set
  saturates it is refreshed with harder cases for the next round. Rollout trajectories live in
  `skillopt/`; each round is written up in `OPTIMIZATION_LOG.md`.

## Extending the suite

- Add a triggering row to `triggering.jsonl` (unique `id`, boolean label).
- Add a functional case as `cases/NN-name.md` following the existing frontmatter and the
  `## Prompt` / `## Input` / `## Rubric` structure.
- Re-run `python3 evals/run_evals.py` to confirm the new files are well-formed.
