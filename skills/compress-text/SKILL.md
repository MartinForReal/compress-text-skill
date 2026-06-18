---
name: compress-text
description: Reads any text content in any format and produces a leaner, better-structured version using semantic grouping with MECE and the Pyramid Principle. It generates multiple candidate groupings, scores each on size reduction and meaning-fidelity, and selects the best while preserving the original meaning, instructions, key points, references, and examples. Use this whenever the user wants to shrink, compress, trim, deduplicate, restructure, or optimize any text, reduce its token/context footprint, or measure compression effectiveness.
---

# Compress Text

Produce a leaner, better-structured version of any text that uses less context window without losing meaning. The method: organize content into MECE groups (mutually exclusive, collectively exhaustive), rephrase each with the Pyramid Principle (key point first, detail beneath), and drop anything that does not serve the text's purpose. When more than one sensible grouping exists, generate a few candidates, measure each, and keep the best. Preserve the original meaning and every distinct instruction, key point, requirement, reference, and example. This works on text in any format: prose, docs, notes, prompts, code comments, transcripts, or Markdown.

## When to use this skill

- The user wants to shrink, compress, trim, restructure, or optimize any text or document
- The user wants to reduce a piece of text's token or context-window footprint
- The user wants to measure how effective a compression is
- The user says some content feels bloated, repetitive, wordy, or disorganized
- The user wants to deduplicate or consolidate overlapping content

## Parameters

- text reference (required): the content to compress, as a file path/name to read, or pasted text in any format.
- aggressiveness (optional): conservative (default) consolidates and tightens clear cases only; aggressive also merges related groups and rewrites verbose passages freely.
- candidates (optional): how many alternative groupings to compare. Default 2-3; set 1 to skip comparison.

## Step 1: Load the source text

Read the content's full current version, from the given path/name or the pasted text. Never work from memory of a previous version, so recent edits are not dropped.

## Step 2: Anchor on purpose and inventory what to preserve

State the text's purpose in one line; this is the test for what stays. Then count the load-bearing elements, which become the fidelity baseline for Step 6:

- Distinct instructions, steps, or requirements
- Structure and ordering the reader or tooling depends on
- Key claims, decisions, and definitions
- References, links, parameters, names, numbers, and required inputs/outputs
- Verbatim spans where exact content or format matters (code, quotes, tables, identifiers)

Compression changes how briefly these are expressed, never whether they exist. Reproduce verbatim spans exactly unless they contain genuine redundancy.

## Step 3: Generate candidate groupings (MECE)

Produce the number of candidates set by the candidates parameter (default 2-3), each clustering content so every idea sits in exactly one group (mutually exclusive) and every preserved element maps to a group (collectively exhaustive). Make candidates genuinely different by varying the grouping axis (by topic, by reader task, by section, or by content type), because different axes expose different redundancies and reveal the leanest structure.

## Step 4: Rephrase each candidate with the Pyramid Principle

In every group, lead with the key point, then nest qualifiers, steps, and examples beneath it. While rephrasing:

- Merge duplicates into the single most specific, accurate version
- Use direct, active phrasing
- Cut filler and hedging ("please note that", "it is important to", "as mentioned above")
- Do not restate in prose what a list, example, or heading already shows
- Keep wording fuller wherever a briefer version would change meaning

## Step 5: Eliminate unrelated content

Remove anything failing the Step 2 purpose test: tangents, background that informs no decision or action, and content outside scope. Keep and flag anything ambiguous rather than guessing.

## Step 6: Measure each candidate

Score every candidate on size and meaning, since shorter is only better if the content survives:

- Size reduction: token reduction % (best proxy for context savings; an estimate), with word/character count as fallback. Report before to after.
- Fidelity coverage: share of Step 2 elements surviving, per category and overall; target 100%.
- MECE audit: ideas appearing in more than one group (must be 0) and preserved elements left ungrouped (must be 0).
- Readability check (optional, strongest): confirm a reader can still find each key point and follow the flow; each lost or buried point is a fidelity failure.

## Step 7: Select the best and report

Apply the efficiency-with-fidelity rule: a candidate's size reduction counts only if fidelity is 100% and the MECE audit is clean. Among passing candidates pick the largest reduction, breaking ties by cleaner Pyramid structure then better readability. If none reach 100% fidelity, present the closest and explain the gap rather than shipping a lossy version. Reassemble the winner, preserving any title and the structure readers or tooling rely on, then report using the template below.

## Output template

```
## Compressed text: <title or first line>

<full rephrased text of the selected candidate>

---

### Candidate comparison
| Candidate | Grouping axis | Size reduction | Fidelity | MECE clean? |
|-----------|---------------|----------------|----------|-------------|
| A         | <axis>        | ~<percent>%    | <n/n>    | yes/no      |
| B         | <axis>        | ~<percent>%    | <n/n>    | yes/no      |
Selected: <candidate> - <why it won>

### Preserved intact
- <count> instructions/requirements, <count> references, <count> verbatim spans/examples, structure

### How it was compressed
- MECE grouping: <ideas consolidated; duplicates removed>
- Pyramid rephrasing: <key-point-first rewrites and tightening>
- Removed as unrelated: <what was dropped and why>

### Estimated size reduction
~<before> tokens/words -> ~<after> (~<percent>% smaller)
```

## Success criteria

- [ ] Meaning fully preserved (fidelity coverage 100%)
- [ ] Multiple candidates generated, measured, and compared (unless candidates=1)
- [ ] Selected candidate has the best size reduction among those passing the efficiency-with-fidelity rule
- [ ] Groups are MECE and each leads with its key point (Pyramid Principle)
- [ ] Title and structure preserved; candidate-comparison metrics reported

## Error handling

- Source can't be read: ask the user to paste the text.
- Text already lean: say so and report a small or zero reduction rather than cutting meaningful content to hit a target.
- No candidate reaches 100% fidelity: present the closest, explain what couldn't be preserved, and let the user decide.
- A rephrase or removal risks changing meaning: keep the original and note why in the report.

## Guardrails

- Preserve meaning above all: only rephrase, regroup, or remove when meaning is fully retained, and never invent details not in the source.
- Never drop a distinct instruction, requirement, reference, or example, and never alter verbatim spans (code, quotes, identifiers) except to remove genuine duplication.
- Remove content only when it fails the purpose test, never just to save space; when in doubt, keep and flag it.

## Keywords

compress text, shrink content, trim text, restructure, reduce tokens, save context window, measure effectiveness, pyramid principle, MECE, candidate grouping, semantic grouping, deduplicate, summarize, optimize, bloated content
