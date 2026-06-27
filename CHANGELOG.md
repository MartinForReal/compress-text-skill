# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Three named compression lenses** in [SKILL.md](skills/compress-text/SKILL.md), with a
  new "Compression techniques" section and matching procedure/guardrail/success-criteria
  updates:
  - **Semantic** — merge paraphrases and entailments into the single most specific
    statement (meaning-level dedup that catches restatements sharing no words).
  - **Statistical** — scan repeated n-grams, near-duplicate sentences, and low
    information-density filler to target redundancy objectively, and report how much
    redundancy was removed alongside the size reduction.
  - **Supersession (pivots)** — in transcripts, dictation, drafts, and chat, drop
    self-correction markers ("actually", "scratch that", "I mean", "instead", …) together
    with the passages they supersede, keeping only the final intent; ambiguous pivots are
    kept and flagged. Conservative removes explicit corrections only; aggressive also drops
    implicitly superseded restatements.
- Two functional eval cases: `12-pivot-corrections.md` (supersession) and
  `13-redundancy-stats.md` (statistical consolidation + reporting), plus two triggering
  rows for transcript/pivot cleanup.
- **Functional eval harness** (`evals/run_functional.py`, stdlib-only): deterministic
  behaviour checks (`evals/functional_checks.json`) with an offline `--selftest` (scores a
  golden reference per case; wired into `scripts/validate.sh`), a live `--model` mode, and a
  `--grade DIR` mode for scoring rollout outputs. Supports `--split train|val|all`.
- **SkillOpt optimization loop** ([microsoft.github.io/SkillOpt](https://microsoft.github.io/SkillOpt/)):
  a held-out validation split (fresh cases `14`–`18`) gates skill edits, so changes are kept
  only when they improve held-out `val` without regressing `train`. Round trajectories live in
  `evals/skillopt/`; each round is written up in `evals/OPTIMIZATION_LOG.md`.
- **Statistical-lens refinement (round 01, validation-gated):** treat upbeat status-padding
  / vacuous sentiment ("overall, things are going well") as low-density filler. Held-out pass
  rate 4/5 → 5/5, no training regression.
- **Aggressive-mode density (round 02, validation-gated):** `aggressive` now shortens repeated
  long noun phrases after first mention and cuts scope-setting context that states no distinct
  rule, fact, number, or constraint — with a caveat that never drops a load-bearing qualifier.
  Held-out set refreshed with 4 new `val` cases (`19`–`22`: negations/exceptions, conditional
  branches, numeric fidelity, factual-contradiction flagging); held-out ratio-gate 2/4 → 3/4 with
  no fidelity regression and over-cut anchors (`04`/`09`) clean.
- **Held-out probes (round 03):** 4 new `val` cases (`23`–`26`: modal obligation must/should/may,
  numeric quantifier-bounds, first-use acronym expansion, authority/precedence rules) added as
  standing held-out probes. `23` confirmed the skill already preserves modal obligation levels;
  `24`/`25`/`26` document an unaddressed under-tightening gradient on low-density prose.

### Changed

- Eval suite grows from 13 to 26 functional cases (13 held-out `val` cases for SkillOpt across three
  rounds); static validator and offline self-test (26/26) both green.

### Notes

- **Round 03 evaluated a bounded edit that was rejected** (no skill change). A low-density-tightening
  edit was drafted to close the `24`/`25`/`26` gradient, but the frozen agent's run-to-run variance
  exceeded the edit's effect, so the held-out gate did not improve (1/4 → 0/4). Per the SkillOpt
  acceptance rule the edit was reverted; `SKILL.md` is unchanged. See `evals/OPTIMIZATION_LOG.md`.

## [0.1.0] - 2026-06-18

### Added

- `compress-text` Agent Skill ([skills/compress-text/SKILL.md](skills/compress-text/SKILL.md))
  using MECE grouping and the Pyramid Principle, with candidate scoring on size reduction
  and meaning-fidelity, plus dense (LLM) and readable (human) output modes.
- Template support: auto-detected engine tags (Handlebars/Mustache/Jinja/Liquid/shell/ERB)
  and explicit `<!-- keep -->`/`<!-- drop -->` markers are preserved verbatim, and results
  can be emitted into a user-supplied output template with named `<!-- slot:NAME -->` slots.
- Claude Code plugin manifest (`.claude-plugin/plugin.json`) and marketplace catalog
  (`.claude-plugin/marketplace.json`).
- Skill-bundle build script (`scripts/build-skill-bundle.sh`) producing a distributable
  `.zip` for claude.ai / the Skills API / Foundry.
- Evaluation suite (`evals/`): 27-prompt labelled triggering dataset, 11 functional rubric
  cases (filler removal, deduplication, verbatim/template-tag preservation, output slots,
  dense/readable modes, multi-section MECE, prompt-injection resistance, non-English), an
  offline validator (`evals/run_evals.py`), and a results scorecard (`evals/RESULTS.md`).
- Repository validation script (`scripts/validate.sh`) and GitHub Actions CI
  (`.github/workflows/ci.yml`).

[Unreleased]: https://github.com/MartinForReal/compress-text-skill/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MartinForReal/compress-text-skill/releases/tag/v0.1.0
