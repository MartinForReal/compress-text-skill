#!/usr/bin/env python3
"""Functional evaluation harness for the compress-text skill.

Unlike ``run_evals.py`` (which only static-checks structure and datasets), this
harness scores the skill's *behaviour* against machine-checkable assertions
derived from each case rubric (``evals/functional_checks.json``).

Two modes:

* ``--selftest`` (offline, no model, CI-safe): runs every case's deterministic
  checks against a stored golden ``reference_output``. This proves the check
  engine and the assertions are correct and self-consistent, and gives the suite
  something reproducible to run with no credentials. Exit code is non-zero if any
  reference fails its own checks.

* ``--model`` (live): executes the skill on each case input through an
  OpenAI-chat-completions-compatible endpoint, then runs the same deterministic
  checks on the live output (plus an optional model judge for subjective items).
  Configure with env vars ``LLM_API_BASE``, ``LLM_API_KEY``, ``LLM_MODEL``.
  Reports a scorecard and gates on ``--threshold`` (default 1.0 = all pass).

* ``--grade DIR`` (offline): scores a directory of rollout outputs (one
  ``<case_id>.txt`` per case) against the same checks. This is the SkillOpt
  "score" step for an optimization round — feed the frozen agent's trajectories
  and get a reproducible scorecard with no LLM endpoint.

``--split train|val|all`` restricts any mode to held-in (train) or held-out
(val) cases, enabling SkillOpt's validation-gated updates (accept an edit only if
the held-out ``val`` split improves and ``train`` does not regress).

With no flag: runs ``--model`` when ``LLM_API_KEY`` is set, otherwise falls back
to ``--selftest`` so the command always does something useful offline.

Dependency-free (stdlib only), so it is safe to drop into CI.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "compress-text" / "SKILL.md"
EVALS = ROOT / "evals"
CASES_DIR = EVALS / "cases"
CHECKS = EVALS / "functional_checks.json"

CJK = re.compile(r"[\u3400-\u9fff\uF900-\uFAFF]")
LATIN = re.compile(r"[A-Za-z]")
WORD = re.compile(r"\S+")


# --------------------------------------------------------------------------- #
# Case + checks loading
# --------------------------------------------------------------------------- #
def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[3:end].strip("\n").splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip().strip("'\"")
    return data


def extract_section(text: str, heading: str) -> str:
    """Return the body of a ``## heading`` section up to the next ``## `` heading."""
    pat = re.compile(rf"^{re.escape(heading)}\s*$", re.M)
    m = pat.search(text)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^##\s", text[start:], re.M)
    end = start + nxt.start() if nxt else len(text)
    return text[start:end].strip()


def load_cases() -> dict[str, dict[str, str]]:
    cases: dict[str, dict[str, str]] = {}
    for f in sorted(CASES_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        cid = fm.get("id") or f.stem
        cases[cid] = {
            "file": f.name,
            "mode": fm.get("mode", ""),
            "aggressiveness": fm.get("aggressiveness", ""),
            "prompt": extract_section(text, "## Prompt"),
            "input": extract_section(text, "## Input"),
            "rubric": extract_section(text, "## Rubric"),
        }
    return cases


# --------------------------------------------------------------------------- #
# Text helpers + deterministic check engine
# --------------------------------------------------------------------------- #
def words(text: str) -> int:
    return len(WORD.findall(text))


def nonspace_chars(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def extract_body(output: str) -> str:
    """Best-effort extraction of the compressed body from a skill output.

    Splits on the first horizontal rule (the default template divider). Drops a
    leading ``## Compressed text:`` / ``### ...`` title line. For user-template
    outputs with no divider, returns the whole thing (the checks still apply)."""
    head = re.split(r"\n-{3,}\n", output, maxsplit=1)[0]
    lines = head.splitlines()
    if lines and re.match(r"^\s*#{2,6}\s", lines[0]):
        lines = lines[1:]
    return "\n".join(lines).strip()


def _ordered_contains(text: str, needles: list[str]) -> str | None:
    pos = 0
    for n in needles:
        idx = text.find(n, pos)
        if idx == -1:
            return n
        pos = idx + len(n)
    return None


def run_checks(scope_name: str, spec: dict[str, Any], text: str,
               input_words: int, input_chars: int) -> list[str]:
    """Return a list of failure messages for one scope's checks (empty = pass)."""
    fails: list[str] = []
    low = text.lower()

    if "must_contain" in spec:
        for s in spec["must_contain"]:
            if s not in text:
                fails.append(f"[{scope_name}] missing verbatim {s!r}")
    if "must_contain_ci" in spec:
        for s in spec["must_contain_ci"]:
            if s.lower() not in low:
                fails.append(f"[{scope_name}] missing {s!r}")
    if "must_contain_any" in spec:
        opts = spec["must_contain_any"]
        if not any(s.lower() in low for s in opts):
            fails.append(f"[{scope_name}] none of {opts} present")
    if "forbid_ci" in spec:
        for s in spec["forbid_ci"]:
            if s.lower() in low:
                fails.append(f"[{scope_name}] forbidden text present: {s!r}")
    if "forbid_regex" in spec:
        for rx in spec["forbid_regex"]:
            if re.search(rx, text, re.I | re.M):
                fails.append(f"[{scope_name}] forbidden pattern matched: {rx!r}")
    if "require_regex" in spec:
        for rx in spec["require_regex"]:
            if not re.search(rx, text, re.I | re.M):
                fails.append(f"[{scope_name}] required pattern missing: {rx!r}")
    if "ordered_contains" in spec:
        miss = _ordered_contains(text, spec["ordered_contains"])
        if miss is not None:
            fails.append(f"[{scope_name}] {miss!r} missing or out of order")
    if "max_count_ci" in spec:
        for phrase, cap in spec["max_count_ci"].items():
            n = low.count(phrase.lower())
            if n > cap:
                fails.append(f"[{scope_name}] {phrase!r} appears {n}x (max {cap}) — not consolidated")
    if "cjk_required" in spec and spec["cjk_required"]:
        if not CJK.search(text):
            fails.append(f"[{scope_name}] expected CJK characters, found none")
    if "max_latin_ratio" in spec:
        nz = nonspace_chars(text) or 1
        ratio = len(LATIN.findall(text)) / nz
        if ratio > spec["max_latin_ratio"]:
            fails.append(f"[{scope_name}] Latin-letter ratio {ratio:.2f} > {spec['max_latin_ratio']} (looks translated)")
    if "max_word_ratio" in spec and input_words:
        ratio = words(text) / input_words
        if ratio > spec["max_word_ratio"]:
            fails.append(f"[{scope_name}] word ratio {ratio:.2f} > {spec['max_word_ratio']} (not compressed enough)")
    if "min_word_ratio" in spec and input_words:
        ratio = words(text) / input_words
        if ratio < spec["min_word_ratio"]:
            fails.append(f"[{scope_name}] word ratio {ratio:.2f} < {spec['min_word_ratio']} (over-cut/padded)")
    if "max_char_ratio" in spec and input_chars:
        ratio = nonspace_chars(text) / input_chars
        if ratio > spec["max_char_ratio"]:
            fails.append(f"[{scope_name}] char ratio {ratio:.2f} > {spec['max_char_ratio']} (not compressed enough)")
    return fails


def score_output(case_id: str, output: str, case: dict[str, str],
                 checks: dict[str, Any]) -> list[str]:
    spec = checks[case_id]["checks"]
    iw, ic = words(case["input"]), nonspace_chars(case["input"])
    body = extract_body(output)
    fails: list[str] = []
    fails += run_checks("body", spec.get("body", {}), body, iw, ic)
    fails += run_checks("full", spec.get("full", {}), output, iw, ic)
    return fails


# --------------------------------------------------------------------------- #
# Live model execution (OpenAI chat-completions compatible)
# --------------------------------------------------------------------------- #
def call_llm(system: str, user: str) -> str:
    base = os.environ.get("LLM_API_BASE", "https://api.openai.com/v1").rstrip("/")
    key = os.environ["LLM_API_KEY"]
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    payload = {
        "model": model,
        "temperature": float(os.environ.get("LLM_TEMPERATURE", "0")),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def execute_skill(case: dict[str, str]) -> str:
    skill = SKILL.read_text(encoding="utf-8")
    system = (
        "You are an agent equipped with the following Skill. Apply it faithfully "
        "to the user's request. Output only what the Skill's output template "
        "specifies — no preamble.\n\n" + skill
    )
    user = (
        f"{case['prompt']}\n\n"
        f"(mode={case['mode']}, aggressiveness={case['aggressiveness']})\n\n"
        f"Text to compress:\n{case['input']}"
    )
    return call_llm(system, user)


# --------------------------------------------------------------------------- #
# Runners
# --------------------------------------------------------------------------- #
def selected_cases(cases: dict, checks: dict, only: list[str] | None,
                   split: str = "all") -> list[str]:
    ids = [c for c in checks if not c.startswith("_") and c in cases]
    if split and split != "all":
        ids = [c for c in ids if checks[c].get("split", "train") == split]
    if only:
        ids = [c for c in ids if c in only]
    return ids


def run_selftest(cases: dict, checks: dict, only: list[str] | None, split: str = "all") -> int:
    print("compress-text functional self-test (offline, golden references)")
    print("-" * 62)
    failed = 0
    for cid in selected_cases(cases, checks, only, split):
        ref = checks[cid].get("reference_output")
        if ref is None:
            print(f"  SKIP  {cid} (no reference_output)")
            continue
        fails = score_output(cid, ref, cases[cid], checks)
        if fails:
            failed += 1
            print(f"  FAIL  {cid}")
            for f in fails:
                print(f"          {f}")
        else:
            print(f"  PASS  {cid}  [{checks[cid].get('split', 'train')}]")
    print("-" * 62)
    print(f"  {'FAIL' if failed else 'PASS'}: {failed} case(s) with failing checks")
    return 1 if failed else 0


def run_grade(cases: dict, checks: dict, grade_dir: Path, only: list[str] | None,
              split: str, threshold: float) -> int:
    """Score a directory of rollout outputs (``<case_id>.txt``) against the checks.

    This is the SkillOpt 'score' step: feed the frozen agent's trajectories (one
    text file per case) and get a deterministic, reproducible scorecard. Lets an
    A/B / optimization round be graded offline without an LLM endpoint."""
    print(f"compress-text functional grade (rollout dir: {grade_dir})")
    print("-" * 62)
    valid = set(selected_cases(cases, checks, only, split))
    files = sorted(grade_dir.glob("*.txt"))
    if not files:
        print(f"  no *.txt rollout files in {grade_dir}", file=sys.stderr)
        return 1
    passed = total = 0
    for f in files:
        cid = f.stem
        if cid not in valid:
            print(f"  SKIP  {cid} (not in checks/split)")
            continue
        total += 1
        output = f.read_text(encoding="utf-8")
        fails = score_output(cid, output, cases[cid], checks)
        if fails:
            print(f"  FAIL  {cid}  [{checks[cid].get('split', 'train')}]")
            for x in fails:
                print(f"          {x}")
        else:
            passed += 1
            print(f"  PASS  {cid}  [{checks[cid].get('split', 'train')}]")
    rate = passed / total if total else 0.0
    print("-" * 62)
    print(f"  graded {passed}/{total} = {rate:.0%} (threshold {threshold:.0%})")
    return 0 if rate >= threshold else 1


def run_model(cases: dict, checks: dict, only: list[str] | None, threshold: float,
              split: str = "all") -> int:
    print("compress-text functional eval (live model)")
    print(f"  model={os.environ.get('LLM_MODEL', 'gpt-4o-mini')} base={os.environ.get('LLM_API_BASE', 'https://api.openai.com/v1')}")
    print("-" * 62)
    ids = selected_cases(cases, checks, only, split)
    passed = 0
    for cid in ids:
        try:
            output = execute_skill(cases[cid])
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"  ERROR {cid}: {exc}")
            continue
        fails = score_output(cid, output, cases[cid], checks)
        if fails:
            print(f"  FAIL  {cid}")
            for f in fails:
                print(f"          {f}")
        else:
            passed += 1
            print(f"  PASS  {cid}")
    rate = passed / len(ids) if ids else 0.0
    print("-" * 62)
    print(f"  pass rate: {passed}/{len(ids)} = {rate:.0%} (threshold {threshold:.0%})")
    return 0 if rate >= threshold else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Functional eval harness for compress-text.")
    ap.add_argument("--selftest", action="store_true", help="offline: score golden references")
    ap.add_argument("--model", action="store_true", help="live: run the skill via an LLM endpoint")
    ap.add_argument("--grade", default="", help="offline: score a dir of <case_id>.txt rollout outputs")
    ap.add_argument("--split", default="all", choices=["all", "train", "val"],
                    help="restrict to held-in (train) or held-out (val) cases")
    ap.add_argument("--cases", default="", help="comma-separated case ids to run (default: all)")
    ap.add_argument("--threshold", type=float, default=1.0, help="model/grade pass-rate gate (0-1)")
    args = ap.parse_args()

    if not CHECKS.exists():
        print(f"missing {CHECKS}", file=sys.stderr)
        return 1
    cases = load_cases()
    checks = json.loads(CHECKS.read_text(encoding="utf-8"))
    only = [c.strip() for c in args.cases.split(",") if c.strip()] or None

    # Validate every checks entry maps to a real case.
    orphans = [c for c in checks if not c.startswith("_") and c not in cases]
    if orphans:
        print(f"checks reference unknown case ids: {orphans}", file=sys.stderr)
        return 1

    if args.grade:
        return run_grade(cases, checks, Path(args.grade), only, args.split, args.threshold)
    use_model = args.model or (not args.selftest and bool(os.environ.get("LLM_API_KEY")))
    if use_model:
        if not os.environ.get("LLM_API_KEY"):
            print("LLM_API_KEY not set — cannot run --model mode.", file=sys.stderr)
            return 1
        return run_model(cases, checks, only, args.threshold, args.split)
    return run_selftest(cases, checks, only, args.split)


if __name__ == "__main__":
    raise SystemExit(main())
