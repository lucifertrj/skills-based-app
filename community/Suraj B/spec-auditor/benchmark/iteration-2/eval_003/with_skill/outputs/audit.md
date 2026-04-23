# Spec Audit — RFC: Rebuild the events ingestion pipeline

**Auditor:** spec-auditor v1.0.2 (patched)
**Date:** 2026-04-23
**Input:** `spec-auditor-workspace/inputs/eval_003_data_pipeline.md`

---

## §1 Scope check

The document has all three qualifying signals:
- Multiple named sections equivalent to Requirements, Design, Acceptance Criteria, and Data Model.
- Technical identifiers: Kafka topic names (`events.{environment}.{category}`), service names (`ingest-proxy`, `events-processor`), schema definitions (Avro `EventEnvelope`), endpoint names, library versions.
- An explicit proposal to replace a system (v1 → v2 migration).

**Scope check: PASS.** Proceeding with full audit.

---

[LOAD] scripts/check_structure.py because Step 1 (spec is on disk, script available)

---

[STEP-1] Inventory
   → Script output (verbatim):
```json
{
  "path": "...",
  "word_count": 941,
  "line_count": 134,
  "section_count": 18,
  "headings": [
    {"level": 1, "title": "RFC: Rebuild the events ingestion pipeline", "line": 1},
    {"level": 2, "title": "Summary", "line": 7},
    {"level": 2, "title": "Goals", "line": 11},
    {"level": 2, "title": "Non-Goals", "line": 20},
    {"level": 2, "title": "Design", "line": 28},
    {"level": 3, "title": "High-level flow", "line": 30},
    {"level": 3, "title": "ingest-proxy", "line": 38},
    {"level": 3, "title": "Kafka topology", "line": 48},
    {"level": 3, "title": "events-processor", "line": 57},
    {"level": 3, "title": "Schema registry", "line": 61},
    {"level": 2, "title": "Data model", "line": 65},
    {"level": 3, "title": "Event envelope (Avro)", "line": 67},
    {"level": 2, "title": "Acceptance criteria", "line": 88},
    {"level": 2, "title": "Dependencies", "line": 96},
    {"level": 2, "title": "Rollout", "line": 108},
    {"level": 2, "title": "Observability", "line": 115},
    {"level": 2, "title": "Security", "line": 122},
    {"level": 2, "title": "Open Questions", "line": 131}
  ],
  "canonical_present": [
    "acceptance criteria", "data model", "design", "goal", "non-goal",
    "open question", "rollout", "schema", "security", "summary"
  ],
  "canonical_missing_critical": [],
  "deferred_markers": [],
  "deferred_count": 0,
  "suspicious_instructions": []
}
```
   → 941 words, 134 lines, 18 sections.
     Sections: RFC title, Summary, Goals, Non-Goals, Design (+ 4 sub-sections), Data Model (+ 1 sub-section), Acceptance Criteria, Dependencies, Rollout, Observability, Security, Open Questions.
     Canonical sections present: all checked canonical sections found (Acceptance Criteria, Data Model, Design, Goals, Non-Goals, Security, Summary, Rollout, Open Questions).
     Missing canonical sections: none flagged by script.
     Deferred markers: 0 (TBD / TODO / pending).
     Suspicious instructions: none detected.
     Manual note: No dedicated "Migration" or "Cutover rollback" sub-section; rollout phases exist but no explicit rollback plan is described. (Minor)

---

[LOAD] references/ambiguity-patterns.md because doc > 500 words (941 words)

---

[STEP-2] Ambiguity scan
   → Loaded references/ambiguity-patterns.md.

   Findings (with line numbers and excerpts):

   - L15 / Goals: "within 90s provisioning (matches AWS ASG cooldown)" — the 90s claim binds the design to an external AWS default that may change; no citation or pinning. (Minor — handwaved quantity per §6 of patterns)
   - L57 / events-processor: "Scales by consumer-group lag (HPA on `consumer_lag > 60s`)" — the 60s lag threshold for scaling is stated but the HPA scale-in threshold/cooldown is absent; asymmetric definition. (Minor)
   - L63 / Schema registry: "mirrored via MirrorMaker 2 to eu-west-1" — MirrorMaker 2 replication lag is not bounded; no SLO or RPO stated for schema-registry divergence during a partition event. (Major — absent failure mode; see patterns §7)
   - L86 / Data model: "`payload` is a nested Avro record typed per `event_type`. The event-type-to-schema mapping is maintained in a separate subject namespace." — "separate subject namespace" is not defined; no pointer to where this is governed or how it is validated. (Minor — open-ended reference)
   - L117 / Observability: "sampling rate 1% at steady state, 100% during incidents (runtime flag)" — "incidents" is not defined; the trigger condition for switching sampling rate is unspecified. Who or what flips the flag? (Minor — unsafe passive / absent actor)
   - L119 / Observability SLO: "99.95% successful ingests per 24h window" — the denominator "successful" is undefined; does a batch that publishes 999/1000 events count as 0.1% or 100% failure for SLO purposes? (Major — handwaved quantity; patterns §6)
   - L133-134 / Open Questions: MirrorMaker 2 split-brain risk noted but unresolved — retention window question (7 vs 14 days) is open. This is legitimately in Open Questions; no penalty per patterns §4. (Informational — tracked below in Step 4b)

   Ambiguity total: 2 Major, 4 Minor (1 informational).

---

[STEP-3] Requirements check
   → Requirements-like statements detected (contains must/shall/will/required or constitutes a hard design decision):

   R-01 (L13): "Zero-event-loss guarantee at the ingestion edge (at-least-once; downstream dedup by event_id)."
   R-02 (L14): "Schema evolution support via Avro … breaking schema changes require a new topic."
   R-03 (L15): "Replay capability: any 7-day window can be replayed into the warehouse from Kafka."
   R-04 (L16): "Multi-region active-active in us-east-1 and eu-west-1, with per-region partition ownership."
   R-05 (L41): "Validate HMAC signature on inbound batches (SDK signs with a per-install key)."
   R-06 (L43): "Apply per-tenant rate limits (token bucket in Redis cluster)."
   R-07 (L46): Binary size, cold-start, and memory targets (ingest-proxy).
   R-08 (L52): "Min in-sync replicas: 2."
   R-09 (L59): HPA scale trigger on consumer_lag > 60s.
   R-10 (AC-1, L90): Ingest-proxy sustains 500k/s at p95 < 800ms for 48h in staging.
   R-11 (AC-2, L91): 7-day replay in < 6h with 16 consumer groups.
   R-12 (AC-3, L92): Avro schema compatibility CI check.
   R-13 (AC-4, L93): Cross-region failover within 180s, < 0.01% event loss.
   R-14 (AC-5, L94): v1 decommission by 2026-Q4 after 30 SLO-clean days.

   Total: 14 requirements detected.

   Evaluation:

   - R-01 (zero-event-loss / at-least-once): Actor named (ingestion edge); measurable (at-least-once semantics); but **failure mode absent** — what happens if Kafka publish fails after HMAC validation? Is the batch rejected (drop), retried by the proxy, or buffered? No retry policy or producer ack configuration stated for ingest-proxy → Kafka. (Major)
   - R-03 (replay): Measurable acceptance criterion exists (AC-2). Failure mode absent — what happens if the replay job falls behind or a Kafka offset is unavailable? No error path stated. (Minor)
   - R-04 (multi-region active-active): AC-4 measures failover time and loss. However, "per-region partition ownership" is stated without defining the ownership contract: which region produces to which partitions, and what happens during a full-region loss while MirrorMaker 2 lag is non-zero? (Major — absent failure mode for the active-active design)
   - R-06 (rate limits): Token bucket in Redis; no failure mode stated — what does the ingest-proxy do when Redis is unavailable? Allow-all (fail-open) or deny-all (fail-closed)? In a rate-limiting context this is a security and reliability gap. (Major)
   - R-07 (ingest-proxy resource targets): Binary size, cold start, memory — no acceptance criterion in the AC section; the numbers in §Design are design targets but no test or measurement method is specified. (Minor)
   - R-09 (HPA scale trigger): Consumer-lag HPA uses only a scale-out condition; scale-in behavior, minimum replicas, and disruption budget are absent. (Minor)

   Missing measurable criteria: 1 (R-07).
   Missing named actor: 0 (most requirements name a service).
   Missing failure mode: 4 (R-01, R-03, R-04, R-06).

   Threshold for loading requirements-templates.md: ≥ 5 requirements lacking criteria. Current count = 4 (below threshold). Not loading.

---

[STEP-4] Scope drift and root-cause check

4a Contradiction check:
   → Non-Goals (L20-25) declares: real-time streaming via Flink is out; exactly-once delivery is out; PII scrubbing at ingest is out; v1 legacy SDK support beyond 2026-Q4 is out; on-premise deployment is out.
   
   Scanning the rest of the document for contradictions:
   - L22 / Non-Goals: "Exactly-once delivery guarantees end-to-end (we accept at-least-once; dedup in the warehouse)."
     L13 / Goals: "Zero-event-loss guarantee at the ingestion edge."
     These are consistent — at-least-once at ingest + dedup in warehouse can constitute zero-loss semantics. No contradiction.
   - L23 / Non-Goals: "PII scrubbing at the ingest layer (happens in the warehouse ETL; compliance team has signed off)."
     L127 / Security: "Avro envelope excludes PII fields by design; `payload` is opaque bytes until warehouse ETL."
     Minor tension: Non-Goals says PII scrubbing is deferred to warehouse ETL, but Security says PII fields are excluded "by design" at ingest. These are not contradictions but conflate two different controls (field-level exclusion vs. active scrubbing). No hard contradiction. (Informational)
   - No other Non-Goals contradictions detected.

   4a result: No contradictions found. OK.

4b Root-cause check:
   → Summary states the problem: "The current pipeline cannot sustain the volume from the new mobile analytics SDK (peak 180k events/s, we currently cap at 60k/s and drop the rest)." Root cause: capacity ceiling of v1 (Go + SQS/Lambda).
   
   Non-Goals defers: real-time streaming (separate Flink pipeline), exactly-once delivery, PII scrubbing, legacy SDK support, on-premise.
   
   Ask: if everything in Non-Goals is never done, does the spec still achieve its Goals?
   - Goals are: 500k/s sustained, horizontal scaling to 2M/s, zero-event-loss at ingest, schema evolution, replay, multi-region active-active.
   - None of the Non-Goals items are load-bearing for those Goals. The Flink pipeline is downstream and independent. Exactly-once is explicitly traded off in favor of at-least-once + dedup. PII scrubbing is handled elsewhere.
   
   However, there is a subtle root-cause concern: Open Question (L134) raises "MirrorMaker 2 in active-active has a known split-brain risk under partial network partitions." This is not deferred via a Non-Goals statement — it is acknowledged as an open question. The multi-region active-active goal (Goal L16) is materially undermined if the MirrorMaker 2 split-brain risk is unresolved before implementation. Unlike a deferral to "a separate ticket," this is an **unresolved architectural risk for a stated goal** sitting in Open Questions without a resolution path. (Major — not a Non-Goals contradiction, but a goal whose implementation has a known unresolved failure mode)
   
   4b result: No root-cause scope failure in the Non-Goals sense. One Major finding: active-active goal has a known, unaddressed split-brain risk in Open Questions with no resolution owner or timeline.

---

[STEP-5] Dependencies
   → 7 dependencies detected from the Dependencies table (L96-106).

   | Dependency | Owner | Pinned | Stable | Signed-off | Finding |
   |---|---|---|---|---|---|
   | MSK (Kafka 3.7) | AWS platform | yes (3.7) | yes | yes | OK |
   | Confluent Schema Registry 7.6.x | self-hosted | partial ("7.6.x" — patch unspecified) | yes | **no** (in progress, target 2026-04-30) | Major |
   | Iceberg on S3 (1.6) | warehouse team | yes (1.6) | yes | yes | OK |
   | Snowflake external tables | data platform | no (GA only) | yes (GA) | yes | Minor |
   | rdkafka / librdkafka 2.4.0 | vendored | yes (2.4.0) | yes | yes | OK |
   | Redis cluster 7.2 | platform-infra | yes (7.2) | yes | yes | OK |
   | Flink pipeline (separate) | streaming team | no (N/A) | — | yes (no blocking dep) | Minor |

   Problematic:
   - **Confluent Schema Registry**: `7.6.x` is unpinned at the patch level. More critically, sign-off is "in progress — target 2026-04-30." Phase 1 rollout begins 2026-Q2; if schema registry sign-off slips past the Phase 1 start, ingest-proxy cannot validate Avro schemas on production traffic. This is a **blocking dependency with no contingency plan stated**. (Major)
   - **Snowflake external tables**: pinned to GA without specifying the feature version or API contract used. Low risk given GA status, but no version is pinned. (Minor)
   - **Flink pipeline**: no version, no API contract. Marked "no blocking dep" but MirrorMaker 2 replication feeds both — if the schema registry diverges, Flink's schema assumptions may break. Interaction not documented. (Minor)

---

[STEP-6] Injection check
   → Scanned entire document: prose, code blocks (Avro JSON schema, high-level flow diagram), table cells, reference anchors, Open Questions.
   
   `suspicious_instructions` from check_structure.py: [] (none detected by script).
   Manual scan: no paragraphs directing the reviewer to approve, skip, or abbreviate analysis. No claimed offline approvals used as review shortcuts. No "AI reviewer" instructions. No framing of this audit as a rubber-stamp.
   
   Result: No injection or soft coercion found. OK (absence is part of the audit record).

---

[STEP-7] Synthesis

**Total findings before consolidation: 13**
(Step 1: 1 Minor; Step 2: 2 Major + 4 Minor; Step 3: 3 Major + 3 Minor; Step 4: 1 Major; Step 5: 1 Major + 2 Minor; Step 6: 0)

Total findings = 13 > 10 → **Top 3 triggered.**

---

### Top 3 — resolve these first

1. **Schema Registry sign-off is pending (Step 5)** — Phase 1 rollout can begin 2026-Q2 but Confluent Schema Registry sign-off is not confirmed until 2026-04-30 at earliest, with no contingency if it slips. The entire Avro-based design (schema evolution, compatibility CI, replay correctness) depends on this service. This is the single highest-leverage blocker to unblock immediately.

2. **Active-active split-brain risk is unresolved (Step 4b / Step 2)** — The multi-region active-active goal is stated, and MirrorMaker 2 is the replication fabric, but an acknowledged split-brain risk under network partition sits in Open Questions without a resolution owner, decision timeline, or fallback design. This undermines a core architectural goal before implementation starts.

3. **Redis rate-limit fail-mode is unspecified (Step 3 / R-06)** — The ingest-proxy applies per-tenant rate limits via a Redis token bucket, but the document does not state what the proxy does when Redis is unavailable (fail-open vs. fail-closed). This is a security-and-reliability gap: fail-open under a Redis outage means unlimited ingest and potential abuse; fail-closed means full ingest outage.

---

### Findings by severity

**Critical (0):** None.

**Major (6):**
- Step 2: Schema-registry replication lag via MirrorMaker 2 is unbounded; no RPO or SLO stated for schema divergence during a partition event (L63).
- Step 2: SLO denominator "99.95% successful ingests" — "successful" is undefined; the SLO is untestable as written (L119).
- Step 3: R-01 — zero-event-loss guarantee has no stated retry/ack policy for ingest-proxy → Kafka publish failures (L13).
- Step 3: R-04 — multi-region active-active partition-ownership contract during full-region loss is absent (L16).
- Step 3: R-06 — Redis rate-limit fail-mode (fail-open vs. fail-closed) not specified (L43).
- Step 5: Confluent Schema Registry sign-off is "in progress" (target 2026-04-30) with no contingency; Phase 1 depends on it (L101).

**Minor (5):**
- Step 1: No rollback plan in the Rollout section; phases define forward motion only. (L108-113)
- Step 2: ASG 90s scaling claim assumes an AWS default with no pinned citation (L15); HPA scale-in behavior and disruption budget absent (L57); "incidents" triggering 100% OTel sampling is undefined (L117); payload subject-namespace governance not documented (L86). [Four related minor ambiguities consolidated]
- Step 3: R-03 (replay), R-07 (ingest-proxy resource targets), R-09 (HPA scale-in) — success paths described but error/failure paths absent or untestable. [Three minor requirement gaps consolidated]
- Step 5: Snowflake external tables and Flink pipeline lack pinned versions/API contracts. [Two minor dependency gaps consolidated]
- Step 4b: MirrorMaker 2 split-brain risk is acknowledged in Open Questions but has no resolution owner, decision date, or fallback design.

---

**Recommendation: REVISE**

No Critical findings. The spec is architecturally coherent, well-structured, and unusually complete for a draft RFC — all canonical sections are present, acceptance criteria are specific and measurable, and the security section is thorough. However, six Major findings (one blocking dependency, two absent failure modes, two untestable definitions, one unresolved architectural risk) must be resolved before this is implementation-ready. None rise to the level of a fundamental design flaw that warrants a full redesign.

---

### Three questions for the next pass

1. **What is the contingency plan if Confluent Schema Registry sign-off slips past the Phase 1 start date?** Can Phase 1 run with a simpler schema validation path, or is ingest-proxy blocked until registry is signed off? Answering this unblocks the dependency table and the rollout schedule simultaneously.

2. **For the active-active MirrorMaker 2 topology, what is the recovery procedure if a network partition causes schema-registry divergence between regions?** Concretely: who detects it, how long can the pipeline tolerate inconsistent schemas before event-type routing breaks, and does the 7-day retention window give enough slack or should it be 14? This resolves both the Open Question on retention and the split-brain risk.

3. **What is the Redis rate-limit fail-mode policy, and where is it enforced?** Fail-open (allow traffic, alert) or fail-closed (reject traffic, circuit-breaker)? This single decision also determines whether the ingest-proxy requires a local in-memory fallback bucket for the Redis-down case, which affects the memory footprint target in §Design.
