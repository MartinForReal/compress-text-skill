---
name: compress-text
description: Reads text in any format and produces a leaner, better-structured version via MECE semantic grouping and the Pyramid Principle. Generates multiple candidate groupings, scores each on size reduction and meaning-fidelity, and selects the best while preserving the original meaning, instructions, key points, references, and examples. Cuts redundancy with semantic and statistical analysis, and strips self-corrections plus the passages they supersede when the author pivoted (transcripts, dictation, drafts, chat). Preserves template tags (Handlebars/Jinja/Mustache/shell/ERB and explicit keep/drop markers) verbatim and can emit the result into a user-supplied template with named slots. Offers a dense LLM-oriented mode and a readable human-oriented mode. Use it to shrink, compress, trim, deduplicate, restructure, optimize, or clean up any text or transcript, reduce its token/context footprint, compress a template while keeping its tags, merge related docs and dedupe across them, or measure compression effectiveness.
argument-hint: 'Paste or reference the text to compress; optionally set mode (dense/readable), aggressiveness, candidates, or an output template'
---

# Compress Text

Produce a leaner, better-structured version of any text that costs less context without losing meaning. Method: group content MECE (mutually exclusive, collectively exhaustive), rephrase each group with the Pyramid Principle (key point first, detail beneath), drop anything off-purpose. When multiple groupings fit, generate candidates, measure, keep the best. Preserve original meaning and every distinct instruction, key point, requirement, reference, and example. Works on any format: prose, docs, notes, prompts, code comments, transcripts, Markdown.

## When to use

- Shrink, compress, trim, restructure, or optimize any text/document
- Reduce a text's token/context-window footprint
- Measure a compression's effectiveness
- Content feels bloated, repetitive, wordy, or disorganized
- Deduplicate or consolidate overlapping content
- Merge or split a set of related documents/sections and remove content duplicated across them — compress a whole context as one key-point tree
- Clean up a transcript, dictation, draft, or chat where the author changed direction — drop the self-corrections and the passages they supersede

## When NOT to use

- Goal is interpretation/analysis/conclusions, not a shorter version (compression rephrases and removes; it never adds claims)
- No detail may be lost (e.g. legal text, exact quotes) — compress only surrounding prose, never the protected content

## Parameters

- **text reference** (required): content to compress — a file path/name to read, or pasted text, in any format. It may be a single text or a set of related documents/sections that form one context (a context tree); when several are supplied, compress them together as one key-point tree, not in isolation (see Compression techniques → Structural).
- **mode** (optional): `dense` (LLM-oriented) maximizes info per token — telegraphic, abbreviations and symbols ok, readability secondary; `readable` (human-oriented) keeps fluent prose, no cryptic fragments. Default `readable`; use `dense` when the target is an LLM prompt/context.
- **aggressiveness** (optional): `conservative` (default) consolidates and tightens clear cases only, and removes only explicit, unambiguous self-corrections; `aggressive` also merges related groups, freely rewrites verbose passages, drops implicitly superseded restatements, shortens repeated long noun phrases to a short form after first mention, and cuts scope-setting context that states no distinct rule, fact, number, or constraint — never dropping a load-bearing qualifier (a condition, exception, scope, unit, name, or number that changes meaning).
- **candidates** (optional): alternative groupings to compare. Default 2-3; set `1` to skip comparison.
- **template** (optional): an output shape with named `<!-- slot:NAME -->` slots to emit into instead of the default Output template (see below).

## Tags

Two tag families are always honored, in any format:

- **Engine tags (auto-detected, locked verbatim):** `{{…}}`/`{{#…}}`/`{{/…}}` (Handlebars/Mustache), `{%…%}` (Jinja/Liquid), `${…}`/`$NAME` (JS/shell), `<%…%>` (ERB/EJS), `{0}`/`{name}` (format strings). Reproduce each exactly and in original order; never reorder, merge, or de-duplicate control-flow pairs (`{% for %}…{% endfor %}`, `{{#each}}…{{/each}}`) even when the text between them looks repetitive.
- **Explicit markers (author-controlled):** `<!-- keep -->…<!-- /keep -->` = reproduce verbatim; `<!-- drop -->…<!-- /drop -->` = always remove. Comment delimiters are invisible in rendered Markdown and never collide with engine tags. Strip the delimiters from the output unless the user asks to keep them.

## Compression techniques

Four complementary lenses. Apply whichever the text rewards; they reinforce each other and feed the Procedure below.

- **Semantic** — group by meaning (MECE), then merge paraphrases and entailments into the single most specific statement. When one idea subsumes another (says everything the other says, plus more), keep the stronger and drop the weaker. This is meaning-level dedup: catches restatements that share no words.
- **Statistical** — scan the text objectively for redundancy and low value: repeated terms, recurring n-grams, and near-duplicate sentences mark what to consolidate; sentences that are mostly filler, hedging, connective tissue, or vacuous sentiment — upbeat status-padding that states no specific fact, decision, metric, or next step ("overall things are going well", "we're pleased with progress") — carry low information density (little unique content per word) and mark what to cut. Use these counts to choose the leanest candidate and to report how much redundancy was removed. Never collapse repetition that carries meaning (emphasis, examples, control-flow loops), and keep sentiment when the sentiment itself is the load-bearing point (a testimonial, an apology, a morale message).
- **Structural (key-point tree)** — when the input spans multiple documents or sections that belong together, treat the whole context as one tree of key points (each node a distinct point; its qualifiers, steps, and examples nested beneath) rather than compressing each document in isolation. Build a single MECE key-point tree across the entire context: a key point stated in several places collapses to one node (keep the most specific phrasing), and a sub-point shared by sibling branches hoists to their nearest common ancestor so it is stated once, above the per-branch differences. Split a node that bundles MECE-distinct points into separate nodes. Then reshape the documents to follow the tree — merge ones that are near-duplicates or each too thin, split one that mixes unrelated concerns — so the result reads as a compact shared core plus each branch's unique delta. Do not repeat the source title as the first body line when the output heading already names it, and omit separation-only instructions once the new structure enforces the separation. Preserve the union of all distinct points: every node's unique content survives exactly once at its most-specific position; never let merging drop a branch's specifics, and keep contradictory "duplicates" both and flag them rather than collapsing them.
- **Supersession (pivots)** — when the author changed direction mid-text (common in transcripts, dictation, drafts, and chat), a later statement replaces an earlier one. Drop the self-correction marker *and* the content it supersedes, keeping only the final intent. Markers include "actually", "wait", "no", "scratch/strike that", "ignore that", "never mind", "on second thought", "I mean", "rather", "correction:", "edit:", and "instead of X, (let's) do Y". Conservative removes only explicit, unambiguous corrections; aggressive also drops implicitly superseded restatements. If which version is final is unclear, keep both and flag.

## Procedure

1. **Load source.** Read the full current version from the path/name or pasted text. Never work from memory of a prior version, so recent edits aren't dropped.
2. **Anchor on purpose, inventory what to preserve.** State the text's purpose in one line — the test for what stays. Count the load-bearing elements (the Step 6 fidelity baseline): distinct instructions/steps/requirements; structure/ordering readers or tooling depend on; key claims, decisions, definitions; references, links, parameters, names, numbers, required inputs/outputs; verbatim spans where exact content/format matters (code, quotes, tables, identifiers); every template tag (see Tags) and `<!-- keep -->` span, plus its position. Compression changes how briefly these are expressed, never whether they exist. Note the text type — polished doc vs transcript, dictation, draft, or chat; the latter often carries self-corrections, where only the superseding version is load-bearing (see Compression techniques → Supersession). Remove `<!-- drop -->` spans up front and exclude them from the baseline.
3. **Generate candidate groupings (MECE).** Produce `candidates` groupings (default 2-3): every idea in exactly one group (mutually exclusive), every preserved element mapped to a group (collectively exhaustive). Make candidates genuinely different by varying the grouping axis (topic, reader task, section, or content type) — different axes expose different redundancies and reveal the leanest structure. When the input spans multiple documents or sections that belong together, group across all of them at once as one key-point tree over the whole context (Structural lens), so a point repeated in several places maps to a single node and a shared sub-point can hoist to a common parent — never one grouping per document in isolation.
4. **Rephrase each candidate (Pyramid Principle).** Per group, lead with the key point, then nest qualifiers, steps, examples. Merge duplicates, paraphrases, and entailments into the single most specific version (Semantic lens); strip self-correction connectives, keeping only the superseding statement (Supersession lens); use direct active phrasing; cut filler, hedging, and vacuous sentiment ("please note that", "it is important to", "as mentioned above", "overall, things are going well", "we're pleased with progress"); don't restate in prose what a list, example, or heading shows; keep wording fuller wherever brevity would change meaning. When aggressive, also shorten repeated long noun phrases after first mention and cut scope-setting context that states no distinct rule, fact, number, or constraint (e.g. "as part of normal daily work", "before it can go out"), but never a qualifier that changes scope or meaning. Apply the mode — **dense**: telegraphic, drop articles/copulas, use standard abbreviations and symbols (`w/`, `&`, `→`, `#`, `>=`) when clear; **readable**: complete fluent sentences, no cryptic abbreviations.
5. **Eliminate unrelated content.** Drop anything failing the Step 2 purpose test: tangents, background informing no decision or action, out-of-scope content. Also drop content a later statement supersedes plus the pivot marker that introduces it (Supersession lens), and sentences a statistical scan flags as near-duplicates or pure low-density filler (Statistical lens). When several related documents are compressed together, a key point duplicated across them is kept once at its node in the shared tree and each document is reshaped to its unique delta (Structural lens) — hoisting a shared point, never dropping a branch's specifics. Keep and flag ambiguous items rather than guessing.
6. **Measure each candidate.** Score size and meaning (shorter helps only if content survives): size reduction = token reduction % (best context-savings proxy; an estimate), word/char count as fallback, reported before→after; redundancy removed = count of duplicate/near-duplicate sentences and superseded spans dropped (statistical proxy for how much consolidation happened); fidelity coverage = share of Step 2 elements surviving, per category and overall (target 100%) — including every template tag reproduced exactly and in original order; MECE audit = ideas in more than one group (must be 0) and preserved elements left ungrouped (must be 0); readability check (optional, strongest) = a reader can still find each key point and follow the flow (each lost or buried point is a fidelity failure).
7. **Select the best and report.** Efficiency-with-fidelity rule: a candidate's size reduction counts only if fidelity is 100% and the MECE audit is clean. Among passing candidates pick the largest reduction, breaking ties by cleaner Pyramid structure then readability. If none reach 100% fidelity, present the closest and explain the gap rather than shipping a lossy version. Reassemble the winner, preserving any title and the structure readers or tooling rely on, then report using the template below.

## Output template

After `## Compressed text: <title or first line>`, start with compressed content; do not repeat the source title as an extra `#`/`##` body heading. For split/merged structural outputs, prefer compact branch-delta bullets (`- Branch: actions...`) over nested copied headings or numbered lists when order is not load-bearing.

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
- Redundancy removed: <count of duplicate/near-duplicate sentences consolidated> (omit line if none)
- Pyramid rephrasing: <key-point-first rewrites and tightening>
- Resolved pivots: <self-corrections/superseded passages removed, final version kept> (omit line if none)
- Removed as unrelated: <what was dropped and why>

### Estimated size reduction
~<before> tokens/words -> ~<after> (~<percent>% smaller)
```

If a **template** parameter is supplied, emit it instead: fill each `<!-- slot:NAME -->` with the matching value (`compressed`, `title`, `reduction`, `candidate_table`, `preserved`), pass unknown text through verbatim, and drop slots with no value.

## Success criteria

- [ ] Meaning fully preserved (fidelity coverage 100%)
- [ ] Multiple candidates generated, measured, and compared (unless candidates=1)
- [ ] Selected candidate has the best size reduction among those passing the efficiency-with-fidelity rule
- [ ] Groups are MECE; each leads with its key point (Pyramid Principle)
- [ ] When multiple related documents/sections are compressed together, they form one key-point tree: shared points hoisted and stated once, each branch's unique content preserved
- [ ] Output matches the requested mode (dense or readable)
- [ ] Self-corrections and the passages they supersede are removed when present (only the final intent kept); ambiguous pivots flagged, not guessed
- [ ] All template tags reproduced exactly and in order; `<!-- drop -->` spans removed; output template (if given) filled
- [ ] Title and structure preserved; candidate-comparison metrics reported

## Error handling

- Source unreadable: ask the user to paste the text.
- Already lean: say so; report a small or zero reduction rather than cutting meaningful content to hit a target.
- No candidate reaches 100% fidelity: present the closest, explain what couldn't be preserved, let the user decide.
- A rephrase or removal risks changing meaning: keep the original and note why.

## Guardrails

- Preserve meaning above all: rephrase, regroup, or remove only when meaning is fully retained; never invent details not in the source.
- Never drop a distinct instruction, requirement, reference, or example; never alter verbatim spans (code, quotes, identifiers) except to remove genuine duplication.
- Supersession is removal, not addition: drop an earlier statement only when a later one unambiguously replaces it — the superseding version is the distinct element to keep, not both; when unsure which is final, keep both and flag. Never read meaning into a pivot the author didn't state.
- Don't mistake meaningful repetition (emphasis, worked examples, control-flow loops) for redundancy; consolidate only genuine duplication.
- When merging related documents or sections, preserve the union of their distinct points: hoist a shared point to one place rather than dropping it from a branch, never lose a branch's unique specifics, and keep contradictory "duplicates" both and flag them instead of collapsing them.
- Never edit, reorder, merge, or drop a template tag (engine tag or `<!-- keep -->` span); compress only the prose around them.
- Remove content only when it fails the purpose test or is superseded, never just to save space; when in doubt, keep and flag it.

## Keywords

compress text, shrink content, trim text, restructure, reduce tokens, save context window, measure effectiveness, pyramid principle, MECE, candidate grouping, semantic grouping, semantic dedup, entailment, statistical redundancy, n-gram redundancy, near-duplicate sentences, information density, deduplicate, summarize, optimize, bloated content, self-correction, pivot, supersede, superseded content, transcript cleanup, dictation cleanup, clean up chat, dense mode, readable mode, template, template tags, placeholders, handlebars, mustache, jinja, liquid, keep tag, drop tag, output slots, key-point tree, context tree, cross-document dedup, cross-section dedup, merge documents, split document, hoist shared content, shared core plus deltas, deduplicate across documents
