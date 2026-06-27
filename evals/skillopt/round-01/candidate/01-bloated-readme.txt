## Compressed text: Getting started

Getting started:
1. Install the required dependencies.
2. Run the build command to build the project.
3. Run the start command; the server runs on port 3000.

---

### Candidate comparison
| Candidate | Grouping axis | Size reduction | Fidelity | MECE clean? |
|-----------|---------------|----------------|----------|-------------|
| A         | Setup steps in order | ~70% | 4/4 | yes |
| B         | Prerequisite plus commands | ~66% | 4/4 | yes |
Selected: A - It kept the dependency, build, start, and port facts in order with the largest readable reduction.

### Preserved intact
- 3 instructions/requirements, 4 references/names/numbers, 0 verbatim spans/examples, setup-step order

### How it was compressed
- MECE grouping: Consolidated the README section into prerequisite, build, and start steps.
- Redundancy removed: 4 repeated/near-duplicate statements consolidated: required dependencies, build/building, start server, and port 3000.
- Pyramid rephrasing: Converted bloated prose into a numbered getting-started sequence.
- Removed as unrelated: Filler and hedging such as "it is important to note," "basically," and "as mentioned above" were dropped.

### Estimated size reduction
~90 words -> ~27 (~70% smaller)
