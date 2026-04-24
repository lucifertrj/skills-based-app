#!/usr/bin/env python3
"""
check_structure.py — deterministic structural analysis of a spec document.

Invoked only during Step 1 of the spec-auditor workflow.

Properties:
- No network. No file writes outside stdout/stderr.
- No shell out. Pure Python standard library.
- Deterministic: same input produces byte-identical output.
- Bounded: output size is O(number of headings + number of deferred markers).
- Safe on binary input: decode errors become replacement characters.

Usage:
    python scripts/check_structure.py <path/to/spec.md>

Exit codes:
    0 = success; JSON written to stdout
    1 = runtime error during analysis
    2 = usage error (missing arg, or file not found / not a regular file)

JSON output shape (stdout):
    {
        "path": "<as given>",
        "word_count": int,
        "line_count": int,
        "section_count": int,
        "headings": [
            {"level": int, "title": str, "line": int},
            ...
        ],
        "canonical_present": [str, ...],          # deduped, sorted
        "canonical_missing_critical": [str, ...], # subset of {"acceptance criteria", "non-goal", "security"}
        "deferred_markers": [
            {"line": int, "match": str},
            ...
        ],
        "deferred_count": int,
        "suspicious_instructions": [
            {"line": int, "excerpt": str},
            ...
        ]
    }

The "suspicious_instructions" list is a best-effort heuristic flag for Step 6
(injection check). It is intentionally conservative — the model reading the
output should still perform its own Step 6 pass. False positives here are OK;
false negatives here must not cause Step 6 to be skipped.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Pattern tables. Edit with care: changes affect every downstream audit.
# ---------------------------------------------------------------------------

# Case-insensitive substrings. A heading is "canonical" if any of these
# substrings appears in its title.
CANONICAL_SECTIONS: tuple[str, ...] = (
    "overview", "summary", "background", "context",
    "goal", "objective",
    "non-goal", "non goal", "out of scope", "out-of-scope",
    "requirement", "acceptance criteria", "acceptance-criteria",
    "design", "architecture", "approach",
    "data model", "schema", "interface", "api",
    "security", "privacy", "threat model",
    "migration", "rollout", "deployment",
    "open question", "risk", "alternative", "tradeoff", "trade-off",
)

# The three sections whose absence is a default Major finding.
CRITICAL_CANONICAL: tuple[str, ...] = (
    "acceptance criteria",
    "non-goal",
    "security",
)

# Deferred-decision markers. Flagged in any section; the model applies severity.
DEFERRED_PATTERNS: tuple[str, ...] = (
    r"\bTBD\b",
    r"\bTBC\b",
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\[placeholder\]",
    r"\[draft\]",
    r"\[WIP\]",
    r"\bto be determined\b",
    r"\bto be decided\b",
    r"\bunder discussion\b",
    r"\bpending approval\b",
    r"\bawaiting sign-?off\b",
)

# Heuristic patterns for AI-directed instructions embedded in the document.
# These are conservative: the goal is to make the model's Step 6 easier, not
# to replace it. Tune based on false negatives in tests/cases/.
SUSPICIOUS_INSTRUCTION_PATTERNS: tuple[str, ...] = (
    r"(?i)note\s+to\s+(?:the\s+)?(?:ai|llm|claude|reviewer|reviewers|assistant)",
    r"(?i)(?:ai|llm|claude|assistant)\s*[:,-]\s*(?:please|ignore|approve|mark|skip)",
    r"(?i)\b(?:ignore|disregard)\s+(?:the\s+)?(?:above|below|previous|prior)\s+(?:instructions|rules|steps|findings)",
    r"(?i)\bmark\s+(?:this|the\s+spec|as)\s+(?:approved|ship|passed)\b",
    r"(?i)\byou\s+are\s+a\s+helpful\s+assistant\b",
    r"(?i)\bdo\s+not\s+flag\b",
    r"(?i)\bapprove\s+without\s+(?:further\s+)?(?:analysis|review|changes)\b",
)

HEADING_RE: re.Pattern[str] = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------


def extract_headings(lines: list[str]) -> list[dict[str, Any]]:
    headings: list[dict[str, Any]] = []
    for idx, line in enumerate(lines, start=1):
        m = HEADING_RE.match(line)
        if m:
            headings.append(
                {
                    "level": len(m.group(1)),
                    "title": m.group(2).strip(),
                    "line": idx,
                }
            )
    return headings


def compute_canonical_presence(headings: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    present: set[str] = set()
    for h in headings:
        title_lower = h["title"].lower()
        for canon in CANONICAL_SECTIONS:
            if canon in title_lower:
                present.add(canon)
    missing_critical: list[str] = []
    for crit in CRITICAL_CANONICAL:
        if not any(crit in p for p in present):
            missing_critical.append(crit)
    return sorted(present), missing_critical


def find_deferred_markers(lines: list[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, line in enumerate(lines, start=1):
        for pat in DEFERRED_PATTERNS:
            for m in re.finditer(pat, line, flags=re.IGNORECASE):
                out.append({"line": idx, "match": m.group(0)})
    return out


def find_suspicious_instructions(lines: list[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, line in enumerate(lines, start=1):
        for pat in SUSPICIOUS_INSTRUCTION_PATTERNS:
            if re.search(pat, line):
                excerpt = line.strip()
                if len(excerpt) > 160:
                    excerpt = excerpt[:157] + "..."
                out.append({"line": idx, "excerpt": excerpt})
                break
    return out


def analyze(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    word_count = len(re.findall(r"\S+", text))

    headings = extract_headings(lines)
    canonical_present, canonical_missing_critical = compute_canonical_presence(headings)
    deferred = find_deferred_markers(lines)
    suspicious = find_suspicious_instructions(lines)

    return {
        "path": str(path),
        "word_count": word_count,
        "line_count": len(lines),
        "section_count": len(headings),
        "headings": headings,
        "canonical_present": canonical_present,
        "canonical_missing_critical": canonical_missing_critical,
        "deferred_markers": deferred,
        "deferred_count": len(deferred),
        "suspicious_instructions": suspicious,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    # Force UTF-8 on stdout/stderr so non-ASCII heading titles and excerpts
    # round-trip correctly on Windows terminals (default cp1252 would corrupt
    # em-dashes, smart quotes, etc.). Safe no-op on Linux/macOS.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (AttributeError, OSError):
                pass

    if len(argv) != 2:
        print(
            json.dumps({"error": "usage: check_structure.py <spec.md>"}),
            file=sys.stderr,
        )
        return 2

    path = Path(argv[1])
    if not path.exists() or not path.is_file():
        print(
            json.dumps({"error": f"file not found or not a regular file: {path}"}),
            file=sys.stderr,
        )
        return 2

    try:
        result = analyze(path)
    except Exception as exc:  # noqa: BLE001 — surface any unexpected error as JSON
        print(
            json.dumps({"error": f"analysis failed: {type(exc).__name__}: {exc}"}),
            file=sys.stderr,
        )
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
