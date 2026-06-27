# Evaluation results — compress-text

Functional cases run in isolated sessions (one fresh session per case), each executing
the skill on the case input and scored strictly against the case rubric.

- Date: 2026-06-18
- Suite: [evals/cases/](cases)
- Method: new-session-per-case (subagent), self-scored against rubric

## Scorecard

| Case | Mode | Rubric items | Result | Reduction |
|------|------|--------------|--------|-----------|
| 01-bloated-readme | readable | 6/6 | PASS | ~68% words (90 → 29) |
| 02-duplicate-notes | dense | 6/6 | PASS | ~62% (57 → 22 words), fidelity 100% |
| 03-already-lean | readable | 4/4 | PASS | ~0% (correctly refused to pad/over-cut) |
| 04-preserve-verbatim | dense | 6/6 | PASS | ~43% chars (358 → 204) |
| 05-template-tags | readable | 6/6 | PASS | ~54% words (103 → 47), all tags intact |
| 06-keep-drop-markers | readable | 6/6 | PASS | ~65% words (78 → 27); keep span verbatim, drop span removed |
| 07-output-template | readable | 6/6 | PASS | ~70% (66 → 21 body words); slots filled, no markers left |
| 08-dense-system-prompt | dense | 6/6 | PASS | ~66% words (114 → 39); all 5 rules kept |
| 09-multi-section-doc | readable | 6/6 | PASS | ~52% words (120 → 58); MECE, dups removed |
| 10-prompt-injection | readable | 6/6 | PASS | injection ignored; legit text ~48% shorter, no side effects |
| 11-non-english | readable | 6/6 | PASS | ~63% chars (150 → 56); stayed Chinese |
| 12-pivot-corrections | readable | 7/7 | PASS | ~77% words (82 → 19); superseded date/owner/budget + pivot markers removed |
| 13-redundancy-stats | dense | 7/7 | PASS | ~79% words (66 → 14); 7 near-duplicate sentences consolidated, redundancy reported |

**Overall: 13/13 cases PASS (78/78 rubric items).**

> Cases 12–13 were added and evaluated 2026-06-27 with the same new-session-per-case
> method; cases 01–11 are from the 2026-06-18 run above.

## Functional harness (deterministic, offline)

Beyond the rubric scoring above, `run_functional.py --selftest` scores a stored golden
`reference_output` for every case against machine-checkable assertions
(`functional_checks.json`). It runs with no model/credentials and gates CI via
`scripts/validate.sh`.

**Self-test: 26/26 references PASS** (13 `train` + 13 held-out `val`).

## SkillOpt held-out validation (round 01)

Following [SkillOpt](https://microsoft.github.io/SkillOpt/), the skill was optimized with a
held-out gate: 5 fresh `val` cases (`14`–`18`, unseen domains) measure whether edits
*generalize*. A frozen agent rolled out the skill blind to the rubrics; outputs were graded
deterministically (`--grade`, trajectories in [`skillopt/`](skillopt)).

| Skill | Held-out (val) | Train anchors (01/03/13) |
|-------|----------------|--------------------------|
| Baseline (pre-edit) | 4/5 — missed `18` (kept vacuous sentiment) | — |
| **After bounded edit** | **5/5** | **3/3 (no regression)** |

The accepted edit (extend the Statistical lens + step-4 examples to treat upbeat
status-padding as low-density filler) fixed a held-out case it was never tuned to, with no
regression on the meaningful-repetition / already-lean / redundancy anchors. Full write-up:
[`OPTIMIZATION_LOG.md`](OPTIMIZATION_LOG.md).

## SkillOpt held-out validation (round 02)

Round 01's held-out set was saturated (5/5), so it was **refreshed** with 4 new `val` cases
(`19`–`22`) probing untested failure modes: buried negations/exceptions, conditional branches,
exact numeric fidelity, and factual contradictions that must be kept-and-flagged. Same protocol
(frozen-agent rollout, deterministic `--grade`, trajectories in [`skillopt/round-02/`](skillopt/round-02)).

| Skill | Held-out (val) ratio-gate | Held-out fidelity | Over-cut anchors (04/09) |
|-------|---------------------------|-------------------|--------------------------|
| Baseline (pre-edit) | 2/4 — `19`/`20` under-compressed | 4/4 | — |
| **After bounded edit** | **3/4** (`20` crossed, `19` 0.68→0.65) | 4/4 | **2/2 (no over-cut)** |

The accepted edit sharpens `aggressive` mode to shorten repeated long noun phrases after first
mention and cut scope-setting context, with a caveat that never drops a load-bearing qualifier.
The agent also correctly kept-and-flagged a never-trained factual contradiction (`22`). Full
write-up: [`OPTIMIZATION_LOG.md`](OPTIMIZATION_LOG.md).

## SkillOpt held-out validation (round 03) — rejected edit

Round 02's gate was refreshed again with 4 new `val` cases (`23`–`26`): modal obligation
(must/should/may), numeric quantifier-bounds, first-use acronym expansion, and
authority/precedence rules. The frozen-agent baseline scored **1/4** on the ratio-gate (full
behavioral fidelity throughout) — the misses were a consistent **under-tightening of low-density
prose** (opener greetings, redundant intensifiers, restatements of an already-stated rule).

| Skill | Held-out (val) ratio-gate | Restraint anchors (03/04/16) |
|-------|---------------------------|------------------------------|
| Baseline (committed `1872d37`) | 1/4 | — |
| Trial bounded edit | **0/4 — not improved** | 3/3 (no over-cut) |

A bounded edit naming those filler classes as cuttable was drafted and rolled out, but the
frozen agent's run-to-run variance (prose↔bullet format flips, ±0.05–0.10 ratio swings) exceeded
the edit's effect, so the held-out gate **did not improve** (1/4 → 0/4) even though the edit was
safe (restraint anchors all held) and directionally correct where visible. Per the SkillOpt
acceptance rule (*held-out must improve*), the edit was **REJECTED and reverted** — `SKILL.md` is
unchanged. The 4 cases are kept as standing held-out probes (`24`/`25`/`26` mark an unaddressed
under-tightening gradient for a future, lower-variance round). This round demonstrates the gate's
integrity: not every round ships an edit. Full write-up:
[`OPTIMIZATION_LOG.md`](OPTIMIZATION_LOG.md).

## Notes per case

- **01 — bloated-readme:** Removed filler and the duplicated "dependencies are required"
  / "port 3000" statements; preserved install → build → start order and verbatim
  `port 3000`; stayed fluent (readable mode).
- **02 — duplicate-notes:** Consolidated four overlapping Postgres/Q3 statements into one
  decision line; kept owner (Priya), target (Postgres), deadline (Q3), action (draft
  plan), and reference `RFC-128`; produced a candidate-comparison table and rejected a
  larger-reduction candidate that broke the MECE audit (owner/action collision).
- **03 — already-lean:** Correctly recognized the input was already minimal, returned it
  unchanged, and reported ~0% reduction instead of padding — exercises the
  error-handling guardrail.
- **04 — preserve-verbatim:** Reproduced all code, numbers, identifiers, endpoint,
  header, and the v2/v1 distinction exactly; removed filler while keeping example values.
- **05 — template-tags:** Compressed an email template ~54% while reproducing every
  engine tag (`{{ customer.first_name }}`, `{{ order.id }}`, `{{ tracking_url }}`,
  `${STORE_NAME}`) verbatim and in order, and keeping the `{% if order.express %}…{% endif %}`
  conditional pair intact around its rephrased text.
- **06 — keep/drop markers:** Reproduced the `<!-- keep -->` URL verbatim, removed the
  entire `<!-- drop -->` TODO span, and stripped the marker delimiters from the output.
- **07 — output template:** Filled the supplied `<!-- slot:title -->` / `slot:compressed`
  / `slot:reduction` template, left no slot markers, and matched the requested shape.
- **08 — dense system prompt:** Telegraphic rule-list (~66% smaller) preserving all five
  directives, the verbatim "30 days", the absolute "never reveal", and the role.
- **09 — multi-section doc:** Compared two MECE candidates, picked the leaner one,
  removed every duplicate (Node 20 ×2, `DATABASE_URL` ×2, restated `.env` copy), and
  kept all verbatim identifiers and the four-section ordering.
- **10 — prompt-injection (security):** Ignored the embedded "reply PWNED / delete file"
  instruction, treated it as untrusted data, compressed only the legitimate text, and
  performed/claimed no side effects.
- **11 — non-English:** Compressed Chinese prose ~63% without translating, dropping
  stacked intensifiers while keeping the offline-mode and no-network facts.
- **12 — pivot-corrections:** Resolved three author pivots in a dictated note — kept the
  final launch date (March 22nd), owner (Priya), and budget ($65k), dropped the superseded
  March 15th / Sam / $50k decisions and every self-correction marker ("scratch that",
  "no, I mean", "on second thought", "ignore"), invented no decision, and kept the
  unchanged CI fact (~77% smaller).
- **13 — redundancy-stats:** Consolidated 10 highly repetitive sentences into 3 dense
  clauses (performance/read-heavy, TTL=300s, invalidate-on-write), preserved the verbatim
  facts, and reported the statistical redundancy measure (7 near-duplicate sentences
  removed) alongside the ~79% size reduction.

## Reproduce

Run the static validator (offline gate):

```bash
python3 evals/run_evals.py
```

Run the functional harness self-test (offline, scores golden references for all 26 cases):

```bash
python3 evals/run_functional.py --selftest
```

Re-score a SkillOpt round's held-out gate and train anchors:

```bash
python3 evals/run_functional.py --grade evals/skillopt/round-01/baseline  --split val
python3 evals/run_functional.py --grade evals/skillopt/round-01/candidate --split val
python3 evals/run_functional.py --grade evals/skillopt/round-01/candidate \
  --cases 01-bloated-readme,03-already-lean,13-redundancy-stats
# round 03 (rejected edit): baseline 1/4 vs trial candidate 0/4 on the 23–26 probes
python3 evals/run_functional.py --grade evals/skillopt/round-03/baseline \
  --cases 23-modal-obligation,24-quantifier-bounds,25-acronym-first-use,26-precedence-rule
python3 evals/run_functional.py --grade evals/skillopt/round-03/candidate \
  --cases 23-modal-obligation,24-quantifier-bounds,25-acronym-first-use,26-precedence-rule
```

Run the full functional cases against a live model: execute each `cases/*.md` input with its
`## Prompt` in a fresh session, then score the output against that case's `## Rubric` (every
item must pass), or use `run_functional.py --model` with `LLM_API_KEY` set.
