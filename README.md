# compress-text-skill

An [Agent Skill](https://agentskills.io/) that compresses and restructures any text
using **MECE** grouping and the **Pyramid Principle**. It generates multiple candidate
groupings, scores each on size reduction and meaning-fidelity, and ships the best one —
preserving every instruction, key point, reference, and example.

It compresses through three complementary lenses:

- **Semantic** — merge paraphrases and entailments into the single most specific statement (meaning-level dedup, even when wordings differ).
- **Statistical** — scan for repeated n-grams, near-duplicate sentences, and low-density filler to target redundancy objectively and report how much was removed.
- **Supersession (pivots)** — in transcripts, dictation, drafts, and chat, drop self-corrections ("actually", "scratch that", "I mean", "instead") together with the passages they supersede, keeping only the final intent.

Supports two output modes:

- **dense** (LLM-oriented): maximize information per token for prompts and context.
- **readable** (human-oriented): keep natural, fluent prose for people.

It also preserves **template tags** verbatim — auto-detected engine tags
(Handlebars/Mustache/Jinja/Liquid/shell/ERB) and explicit `<!-- keep -->` / `<!-- drop -->`
markers — and can emit the result into a user-supplied output template with named
`<!-- slot:NAME -->` slots.

## Repository layout

```
compress-text-skill/
├── .claude-plugin/
│   ├── plugin.json          # Claude Code plugin manifest
│   └── marketplace.json     # Claude Code marketplace catalog (this repo)
├── .github/
│   └── workflows/ci.yml     # CI: validate + run evals + build bundle
├── skills/
│   └── compress-text/
│       └── SKILL.md          # The skill
├── evals/                   # Evaluation suite (see evals/README.md)
├── scripts/
│   ├── build-skill-bundle.sh
│   └── validate.sh
├── CHANGELOG.md
├── LICENSE
└── README.md
```

This repo is both a **Claude Code plugin** (root contains `skills/`) and a
**marketplace** that lists that plugin.

## Install via Claude Code plugin marketplace

```bash
# Add this repo as a marketplace
/plugin marketplace add MartinForReal/compress-text-skill

# Install the plugin
/plugin install compress-text@martinforreal-skills
```

Once installed, ask Claude to "compress this text" (or invoke the skill directly) and it
will apply the MECE + Pyramid workflow.

To validate the manifests locally before publishing:

```bash
claude plugin validate . --strict
```

## Publish the skill bundle (claude.ai / Skills API / Foundry)

Build a distributable `.zip` bundle:

```bash
./scripts/build-skill-bundle.sh
# -> dist/compress-text-skill.zip  (contains compress-text/SKILL.md)
```

Then upload the zip wherever Agent Skills are accepted:

- **claude.ai** — Settings → Capabilities → Skills → Upload skill
- **Claude Skills API** — `POST` the bundle to the Skills endpoint
- **Claude Platform on AWS / Microsoft Foundry** — upload via the Skills API

## Usage examples

- "Compress this for an LLM prompt: …" (dense mode)
- "Shorten these meeting notes but keep them readable" (readable mode)
- "Deduplicate and restructure this doc, show me the candidate comparison"
- "Clean up this dictated note: drop the parts where I changed my mind and keep the final decisions" (pivot/supersession)
- "Compress this and tell me how much redundancy you removed" (statistical reporting)
- "Compress this email template but keep the `{{ tags }}` untouched"
- "Compress #file:notes.md and report the token reduction"

## Development

Validate everything (manifests, skill structure, eval datasets) before publishing:

```bash
./scripts/validate.sh
```

Run just the evaluation suite (offline static checks, no model required):

```bash
python3 evals/run_evals.py            # structure + dataset integrity
python3 evals/run_functional.py --selftest   # deterministic behaviour checks (22/22 cases)
```

The suite also includes a labelled triggering dataset, functional rubric cases for
model-judged evaluation, and a [SkillOpt](https://microsoft.github.io/SkillOpt/)
held-out validation loop (train/val split + `evals/OPTIMIZATION_LOG.md`) that gates skill
edits on generalization — see [evals/README.md](evals/README.md). CI runs the validator
and builds the bundle on every push and pull request.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](./LICENSE)