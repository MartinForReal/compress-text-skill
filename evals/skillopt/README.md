# SkillOpt round artifacts

Rollout trajectories (the frozen agent's actual outputs) captured during each
[SkillOpt](https://microsoft.github.io/SkillOpt/) optimization round. They are the
*evidence* the optimization log reasons over, kept in-repo so every accept/reject
decision is reproducible.

```
skillopt/
├── round-01/
│   ├── baseline/    # outputs of the pre-edit (committed) skill on the held-out cases
│   └── candidate/   # outputs of the post-edit skill on held-out + train-anchor cases
├── round-02/
│   ├── baseline/    # pre-edit skill on the refreshed held-out cases (19–22)
│   └── candidate/   # post-edit skill on held-out + aggressive over-cut anchors (04/05/09)
└── round-03/        # REJECTED edit — kept as the evidence behind the no-ship decision
    ├── baseline/    # committed skill on the refreshed held-out cases (23–26), 1/4
    └── candidate/   # trial (since-reverted) edit on held-out (0/4) + restraint anchors (03/04/16)
```

Each file is named `<case_id>.txt` and contains exactly what an end user would receive.
Re-score any directory deterministically (no model/credentials needed):

```bash
# round 01 — held-out gate
python3 evals/run_functional.py --grade evals/skillopt/round-01/baseline  --split val
python3 evals/run_functional.py --grade evals/skillopt/round-01/candidate --split val
# round 01 — train no-regression anchors
python3 evals/run_functional.py --grade evals/skillopt/round-01/candidate \
  --cases 01-bloated-readme,03-already-lean,13-redundancy-stats

# round 02 — refreshed held-out gate (cases 19–22)
python3 evals/run_functional.py --grade evals/skillopt/round-02/baseline \
  --cases 19-negation-exception,20-conditional-branches,21-numeric-fidelity,22-conflicting-facts-flag
python3 evals/run_functional.py --grade evals/skillopt/round-02/candidate \
  --cases 19-negation-exception,20-conditional-branches,21-numeric-fidelity,22-conflicting-facts-flag
# round 02 — aggressive over-cut anchors
python3 evals/run_functional.py --grade evals/skillopt/round-02/candidate \
  --cases 04-preserve-verbatim,05-template-tags,09-multi-section-doc

# round 03 — refreshed held-out gate (cases 23–26): baseline 1/4 vs trial candidate 0/4 (NOT improved -> edit rejected)
python3 evals/run_functional.py --grade evals/skillopt/round-03/baseline \
  --cases 23-modal-obligation,24-quantifier-bounds,25-acronym-first-use,26-precedence-rule
python3 evals/run_functional.py --grade evals/skillopt/round-03/candidate \
  --cases 23-modal-obligation,24-quantifier-bounds,25-acronym-first-use,26-precedence-rule
# round 03 — restraint anchors (the edit's risk direction; all clean)
python3 evals/run_functional.py --grade evals/skillopt/round-03/candidate \
  --cases 03-already-lean,04-preserve-verbatim,16-meaningful-repetition
```

See [`../OPTIMIZATION_LOG.md`](../OPTIMIZATION_LOG.md) for the full round write-up.
