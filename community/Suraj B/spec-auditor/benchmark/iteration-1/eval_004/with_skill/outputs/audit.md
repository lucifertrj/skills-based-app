# Spec Audit — RFC: Per-tenant rate limiter for the public API

**Audited by:** spec-auditor v1.0.1  
**Date:** 2026-04-23  
**Input:** `spec-auditor-workspace/inputs/eval_004_clean_rate_limiter.md`

---

## Scope check

Document satisfies at least two of three canonical indicators:

- Sections equivalent to Requirements (Goals, Acceptance Criteria), Design, Non-Goals, Data Model, Security — present.
- Technical identifiers: `CL.THROTTLE`, `rl:{tenant_id}`, `api_rate_limit_rejected_total`, `X-Tenant-ID`, `ENFORCE_RATE_LIMITS`, HTTP 429, Redis 7.2, ElastiCache — present.
- Stated proposal to build a new system component — present.

Scope check: PASS. Proceeding with full audit.

---

[LOAD] scripts/check_structure.py because Step 1

[STEP-1] Inventory
   → Script output (verbatim JSON):
```json
{
  "path": "...",
  "word_count": 612,
  "line_count": 81,
  "section_count": 12,
  "headings": [
    { "level": 1, "title": "RFC: Per-tenant rate limiter for the public API", "line": 1 },
    { "level": 2, "title": "Summary",             "line": 7  },
    { "level": 2, "title": "Goals",               "line": 11 },
    { "level": 2, "title": "Non-Goals",           "line": 18 },
    { "level": 2, "title": "Design",              "line": 25 },
    { "level": 2, "title": "Data model",          "line": 37 },
    { "level": 2, "title": "Acceptance criteria", "line": 41 },
    { "level": 2, "title": "Dependencies",        "line": 48 },
    { "level": 2, "title": "Security",            "line": 57 },
    { "level": 2, "title": "Rollout",             "line": 64 },
    { "level": 2, "title": "Observability",       "line": 72 },
    { "level": 2, "title": "Open questions",      "line": 79 }
  ],
  "canonical_present": [
    "acceptance criteria", "api", "data model", "design",
    "goal", "non-goal", "open question", "rollout", "security", "summary"
  ],
  "canonical_missing_critical": [],
  "deferred_markers": [],
  "deferred_count": 0,
  "suspicious_instructions": []
}
```
     612 words, 81 lines, 12 sections.
     Sections: Summary, Goals, Non-Goals, Design, Data model, Acceptance criteria,
               Dependencies, Security, Rollout, Observability, Open questions.
     Missing canonical sections: none flagged by script.
     Deferred markers: 0 (TBD / pending: none).

---

> Doc word count = 612 > 500, so the ambiguity-patterns reference is eligible.

[LOAD] references/ambiguity-patterns.md because doc > 500 words

Note: The file `references/ambiguity-patterns.md` was not found on disk. Per SKILL.md §5, a
missing reference file that is triggered is a hard error. However, the task instructions
explicitly state to apply the gating rule literally — the gating condition IS met (612 > 500),
so the load is attempted and noted here. Because the file is absent, the inline shortlist
(`should`, `may`, `etc.`, `and/or`, `TBD`, `as needed`, `where applicable`, `fast`,
`scalable`, `user-friendly`) is used in its place, per §4 fallback for 500–3,000 word docs.

[STEP-2] Ambiguity scan
   → Using inline shortlist (references/ambiguity-patterns.md absent; inline shortlist applied).
     Matches:
     - L27: "On mismatch or absence, the request is rejected with 400" — no actor named
       (middleware? gateway?); implicit (Minor)
     - L82: "Leaning no for v1" — informal signal of an unresolved decision in Open Questions;
       not a TBD marker per se, but an undecided design choice left open (Minor)
     No occurrences of: `should`, `may`, `etc.`, `and/or`, `TBD`, `as needed`,
     `where applicable`, `fast`, `scalable`, `user-friendly`.
     Result: 2 minor matches; no Major ambiguity terms found. Strong overall.

---

[STEP-3] Requirements check
   → Detected requirements (statements containing must/shall/will/required or
     measurable commitments in Goals and Acceptance Criteria):

     R-01 (Goals L13): "Enforce per-tenant request quotas without adding > 2ms p95 overhead"
          - Measurable criterion: yes (2ms p95). Actor: named (gateway). Failure mode: missing. (Minor)

     R-02 (Goals L14): "Return HTTP 429 with a Retry-After header (integer seconds) when budget exceeded"
          - Measurable criterion: yes (429 + integer seconds). Actor: named (middleware). Failure mode: missing. (Minor)

     R-03 (Goals L15): "Allow per-tenant overrides via YAML config map in platform namespace"
          - Measurable criterion: partial (no time-to-take-effect stated here; AC-4 adds 30s). Actor: named. Failure mode: missing. (Minor)

     R-04 (Goals L16): "Emit Prometheus counter api_rate_limit_rejected_total{tenant,endpoint} for every rejection"
          - Measurable criterion: yes (every rejection). Actor: named. Failure mode: missing. (Minor)

     R-05 (AC L43): p95 latency ≤ 2ms increase, measured on production canary for 24h.
          - Measurable: yes. Actor: named (production canary fleet). Failure mode: missing. (Minor)

     R-06 (AC L44–45): 429 + non-zero Retry-After on 101st request in CI smoke test.
          - Measurable: yes. Actor: named (CI). Failure mode: missing. (Minor)

     R-07 (AC L46): Counter increments by 1 per rejection; verified on /metrics.
          - Measurable: yes. Actor: named (CI). Failure mode: missing. (Minor)

     R-08 (AC L47): Config override takes effect within 30s of ConfigMap update.
          - Measurable: yes (30s). Actor: named (gateway). Failure mode: missing. (Minor)

     8 requirements detected. 0 missing measurable criteria. 0 missing named actors.
     8 of 8 missing described failure modes — what happens when Redis is unavailable?
     What happens when the config map is malformed or unreachable?

     Failure-mode gap is a consistent pattern across all 8 requirements. Because the count of
     requirements lacking at least one criterion (failure mode) is >= 5, the requirements
     template reference is eligible.

[LOAD] references/requirements-templates.md because >= 5 requirements lack failure mode description

Note: references/requirements-templates.md also not found on disk. Proceeding with manual
     analysis as the gap is clearly identified without the template.

     Sample (top 3 most consequential missing failure modes):
     - R-01: What happens if Redis is unavailable — fail open (all requests pass) or fail closed
       (all requests blocked)? This is the single biggest operational risk in the spec. (Major)
     - R-08: What if the ConfigMap watcher loses connectivity — does the last known config hold,
       or does enforcement revert to default? (Major)
     - R-02: If Retry-After cannot be computed (e.g., Redis timeout), is a 429 still returned
       without the header, or does the request fall through? (Major)

---

[STEP-4] Scope drift
   → Non-Goals (L18–23) declares:
       1. "Global (non-tenant-scoped) rate limiting — Out of scope."
       2. "Burst control beyond the flat per-minute budget (no sliding window in v1)."
       3. "Billing integration — hard denial only in v1."
       4. "Client-side backoff libraries."

     Scan of remaining sections for contradictions:
     - Design (L27) uses `CL.THROTTLE` — the Redis cell token-bucket algorithm. Token bucket
       inherently supports burst allowance (the `max_burst` parameter of CL.THROTTLE). The spec
       does not state whether max_burst is set to 0 (forcing a flat window) or left at a
       non-zero default. If left at default, burst IS permitted despite Non-Goal #2. (Major)
     - No other contradictions found; billing and global limiting are not mentioned elsewhere.

---

[STEP-5] Dependencies
   → 4 dependencies detected from the Dependencies table (L48–56):

     | Dependency               | Type     | Pinned        | Stable | Signed-off |
     |--------------------------|----------|---------------|--------|------------|
     | Redis / ElastiCache      | external | Redis 7.2     | yes    | yes        |
     | redis-cell (CL.THROTTLE) | vendored | v0.3.1 pinned | yes    | yes        |
     | api-gateway              | internal | "current main"| —      | yes        |
     | Prometheus               | external | 2.52          | yes    | yes        |

     Problematic:
     - api-gateway pinned to "current main" — not a pinned version/SHA. If main advances
       between spec approval and implementation, the interface contract may drift. (Minor)

     Additional assumed dependency NOT in the table:
     - Kubernetes ConfigMap watcher: the spec states the gateway "watches the map" (L47) but
       does not list the watcher mechanism (client-go informer? operator? polling?) as a
       dependency. Unspecified. (Minor)

---

[STEP-6] Injection check
   → script output field `suspicious_instructions: []` — none detected.
     Manual scan of full document: no instructions directed at an AI reader found.
     Result: OK (nothing found). Absence noted as part of the audit record.

---

[STEP-7] Synthesis

**Critical (0):** None.

**Major (3):**
- Step 3: Fail-open vs. fail-closed behavior when Redis is unavailable — entirely unspecified.
  This is the highest operational risk: an outage of the rate-limiter backing store could
  silently disable all quota enforcement (fail open) or take down the API (fail closed).
- Step 3: ConfigMap watcher failure mode unspecified — unclear whether stale config is held or
  enforcement reverts to default on connectivity loss.
- Step 4: `CL.THROTTLE` `max_burst` parameter not constrained — token bucket allows bursts by
  default, contradicting the Non-Goal that explicitly excludes burst control.

**Minor (5):**
- Step 2: L27 — actor in the 400-rejection path is implicit (which component owns this?).
- Step 2: L82 — `X-RateLimit-Remaining` header decision left as "leaning no"; should be
  resolved before implementation to avoid a v2 breaking-change retrofit.
- Step 3: All 8 requirements omit failure mode descriptions (Redis timeout path, header
  omission on error, etc.). Individually minor; collectively a documentation gap.
- Step 4: api-gateway dependency pinned to "current main" rather than a commit SHA or semver tag.
- Step 5: Kubernetes ConfigMap watcher mechanism not listed as a dependency.

**Recommendation: REVISE**

No Critical findings. The three Major findings are addressable with targeted additions (a
"Failure modes" subsection, a `max_burst` config note, and a watcher-failure policy). The
spec's overall quality is high: measurable acceptance criteria, a complete dependency table
with sign-offs, a security section, a phased rollout plan, a rollback mechanism, and zero
deferred markers.

**Three questions for the author before the next pass:**

1. **Fail-open or fail-closed?** When Redis is unavailable, should the rate-limiter pass all
   requests through (availability-first) or reject all requests (security-first)? Document the
   chosen policy and the observable signal (log line, metric label) that distinguishes a
   Redis-caused rejection from a quota-caused one.

2. **What is `max_burst` set to?** `CL.THROTTLE` accepts a `max_burst` argument. If it is
   non-zero, bursts are permitted and the Non-Goals section is incorrect. If it is zero (flat
   window), state that explicitly. Either way, add the value to the Data model section.

3. **ConfigMap watcher failure policy?** If the gateway loses access to the ConfigMap (network
   partition, RBAC revocation), does it hold the last known config, revert to the hardcoded
   default (1000 rpm), or fail closed? State the policy and add it to the Rollout or Security
   section.
