#!/usr/bin/env python3
"""Evaluation suite for the compress-text skill.

Runs offline, dependency-free checks that gate publishing:

1. Skill structure   - SKILL.md frontmatter + required body sections are valid.
2. Manifest wiring   - plugin.json / marketplace.json are valid and reference the skill.
3. Dataset integrity - triggering.jsonl and cases/*.md parse and are well-formed.
4. Triggering heuristic - sanity-checks the labelled triggering dataset against the
   skill's trigger vocabulary (warn-only; real triggering is judged by a model).

Functional behaviour (does the model actually compress correctly?) is judged by a
human or a model against the rubrics in cases/*.md -- see evals/README.md. This
runner does not call a model, so it is safe to run in CI.

Exit code is non-zero if any hard check fails.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "compress-text" / "SKILL.md"
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
EVALS = ROOT / "evals"

REQUIRED_SECTIONS = [
    "## When to use",
    "## When NOT to use",
    "## Parameters",
    "## Procedure",
    "## Output template",
    "## Success criteria",
    "## Error handling",
    "## Guardrails",
    "## Keywords",
]

# Words that should appear in a genuine "compress this text" request.
TRIGGER_VOCAB = [
    "compress", "shrink", "trim", "condense", "tighten", "restructure",
    "optimize", "deduplicate", "dedupe", "consolidate", "shorter", "shorten",
    "leaner", "denser", "reduce", "token", "context", "bloated", "cut", "fewer",
    "压缩", "精简",
]

failures: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Minimal `key: value` frontmatter parser (no YAML dependency)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip().strip("'\"")
    return data


def check_skill() -> None:
    if not SKILL.exists():
        fail(f"SKILL.md not found at {SKILL}")
        return
    text = SKILL.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    name = fm.get("name", "")
    if name != "compress-text":
        fail(f"frontmatter name '{name}' must equal 'compress-text' (matches folder)")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name or ""):
        fail(f"frontmatter name '{name}' must be lowercase alphanumeric + hyphens (1-64 chars)")

    desc = fm.get("description", "")
    if not desc:
        fail("frontmatter description is empty")
    if len(desc) > 1024:
        fail(f"description is {len(desc)} chars (max 1024)")
    if "<" in desc or ">" in desc:
        fail("description must not contain XML-style angle brackets")
    if not re.search(r"\buse\b", desc, re.IGNORECASE):
        warn("description does not say WHEN to use the skill (no 'use' clause)")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            fail(f"SKILL.md missing required section: {section}")


def check_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        fail(f"missing manifest: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.name}: {exc}")
        return None


def check_manifests() -> None:
    plugin = check_json(PLUGIN)
    if plugin is not None:
        if plugin.get("name") != "compress-text":
            fail("plugin.json name must be 'compress-text'")
        if not isinstance(plugin.get("keywords", []), list):
            fail("plugin.json keywords must be an array")

    mkt = check_json(MARKETPLACE)
    if mkt is not None:
        if not mkt.get("name"):
            fail("marketplace.json missing 'name'")
        owner: Any = mkt.get("owner")
        owner_name = owner.get("name") if hasattr(owner, "get") else None
        if not owner_name:
            fail("marketplace.json owner.name is required")
        plugins: list[dict[str, Any]] = [
            p for p in mkt.get("plugins", []) if isinstance(p, dict)
        ]
        if "compress-text" not in {p.get("name") for p in plugins}:
            fail("marketplace.json plugins[] must include 'compress-text'")
        for p in plugins:
            if not p.get("source"):
                fail(f"marketplace plugin '{p.get('name')}' missing 'source'")


def check_triggering() -> int:
    path = EVALS / "triggering.jsonl"
    if not path.exists():
        fail("evals/triggering.jsonl not found")
        return 0
    count = 0
    seen_ids: set[str] = set()
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"triggering.jsonl line {i}: invalid JSON ({exc})")
            continue
        count += 1
        rid = rec.get("id")
        if not rid:
            fail(f"triggering.jsonl line {i}: missing 'id'")
        elif rid in seen_ids:
            fail(f"triggering.jsonl duplicate id: {rid}")
        else:
            seen_ids.add(rid)
        if not isinstance(rec.get("should_trigger"), bool):
            fail(f"triggering.jsonl {rid}: 'should_trigger' must be a boolean")
        text = rec.get("text", "")
        if not text:
            fail(f"triggering.jsonl {rid}: empty 'text'")
        # Heuristic sanity check (warn-only).
        has_vocab = any(w in text.lower() for w in TRIGGER_VOCAB)
        if rec.get("should_trigger") and not has_vocab:
            warn(f"triggering.jsonl {rid}: should_trigger=true but no trigger keyword found")
    return count


def check_cases() -> int:
    cases_dir = EVALS / "cases"
    if not cases_dir.exists():
        fail("evals/cases/ not found")
        return 0
    files = sorted(cases_dir.glob("*.md"))
    if not files:
        fail("evals/cases/ contains no .md cases")
    for f in files:
        text = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm.get("id"):
            fail(f"{f.name}: frontmatter missing 'id'")
        mode = fm.get("mode")
        if mode not in {"dense", "readable"}:
            fail(f"{f.name}: 'mode' must be 'dense' or 'readable' (got {mode!r})")
        for heading in ("## Prompt", "## Rubric"):
            if heading not in text:
                fail(f"{f.name}: missing section {heading}")
        if "- [ ]" not in text:
            fail(f"{f.name}: rubric has no checklist items")
    return len(files)


def main() -> int:
    check_skill()
    check_manifests()
    n_trig = check_triggering()
    n_cases = check_cases()

    print("compress-text evaluation suite")
    print("------------------------------")
    print(f"  triggering prompts : {n_trig}")
    print(f"  functional cases   : {n_cases}")
    print(f"  warnings           : {len(warnings)}")
    print(f"  failures           : {len(failures)}")

    for w in warnings:
        print(f"  WARN  {w}")
    for fmsg in failures:
        print(f"  FAIL  {fmsg}")

    if failures:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
