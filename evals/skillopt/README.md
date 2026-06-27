# SkillOpt round artifacts

Rollout trajectories (the frozen agent's actual outputs) captured during each
[SkillOpt](https://microsoft.github.io/SkillOpt/) optimization round. They are the
*evidence* the optimization log reasons over, kept in-repo so every accept/reject
decision is reproducible.

```
skillopt/
└── round-01/
    ├── baseline/    # outputs of the pre-edit (committed) skill on the held-out cases
    └── candidate/   # outputs of the post-edit skill on held-out + train-anchor cases
```

Each file is named `<case_id>.txt` and contains exactly what an end user would receive.
Re-score any directory deterministically (no model/credentials needed):

```bash
# held-out gate
python3 evals/run_functional.py --grade evals/skillopt/round-01/baseline  --split val
python3 evals/run_functional.py --grade evals/skillopt/round-01/candidate --split val
# train no-regression anchors
python3 evals/run_functional.py --grade evals/skillopt/round-01/candidate \
  --cases 01-bloated-readme,03-already-lean,13-redundancy-stats
```

See [`../OPTIMIZATION_LOG.md`](../OPTIMIZATION_LOG.md) for the full round write-up.
