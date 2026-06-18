# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/MartinForReal/compress-text-skill/releases/tag/v0.1.0
