# Spec Audit — RFC: Rebuild the events ingestion pipeline

**Audited:** `inputs/eval_003_data_pipeline.md`
**Date:** 2026-04-23
**Auditor:** spec-auditor v1.0.1

---

[STEP-1] Inventory
   → script output (scripts/check_structure.py):
     941 words, 134 lines, 18 sections.
     Sections: Summary, Goals, Non-Goals, Design (ingest-proxy, Kafka topology, events-processor, Schema registry), Data model, Acceptance criteria, Dependencies, Rollout, Observability, Security, Open Questions.
     Missing canonical sections: none.
     Deferred markers: 0.
     Suspicious instructions: none.

---

[LOAD] references/ambiguity-patterns.md because doc > 500 words

[STEP-2] Ambiguity scan
   → Loaded references/ambiguity-patterns.md.
   - §Design/ingest-proxy L41: "Validate HMAC signature on inbound batches" — failure mode absent; no rejection behavior defined (Major — absent failure mode).
   - §Design/events-processor L59: "validates Avro, writes to Iceberg" — Avro validation failure path unresolved; Open Questions raises but Design does not answer (Major — deferred decision in Design).
   - §Design/Schema registry L63: "mirrored via MirrorMaker 2 to eu-west-1" — split-brain failure mode raised in Open Questions but not resolved in Design or Rollout (Major — absent failure mode).
   - §Rollout L111: "Phase 2: dual-write to v1 and v2" — no measurable exit criterion for phase transition to Phase 3 (Minor).
   - §Observability L117: "100% sampling during incidents (runtime flag)" — "incidents" undefined; no automated trigger or named actor to flip the flag (Minor).

   Total: 3 Major, 2 Minor.

---

[STEP-3] Requirements check
   → 14 requirements detected. 0 missing measurable criteria; 1 missing named actor; 8 missing failure mode.

   Sample of 5 missing-failure-mode findings (Major):
   - R-03 "Zero-event-loss guarantee" — no retry, backpressure, or fallback when Kafka publish fails (Major).
   - R-06 "Multi-region active-active … per-region partition ownership" — no failover actor or ownership reassignment behavior defined (Major).
   - R-07 "Per-tenant rate limits (token bucket in Redis)" — no stated behavior when limit is exceeded: 429, queue, drop? (Major).
   - R-08 "Validate HMAC signature" — rejection response and failure path absent (Major).
   - R-09 "Min in-sync replicas: 2" — no producer behavior defined when ISR drops below 2; acks=all will block producers; spec silent (Major).

   8 requirements lack failure-mode descriptions. 0 lack measurable criteria — requirements-templates.md trigger (≥5 missing criteria) not met; not loaded.

---

[STEP-4] Scope drift
   → Non-Goals section present and well-scoped (5 explicit exclusions).
     No contradictions found between Non-Goals and Design, Rollout, Security, or Observability sections.
     OK (nothing found).

---

[STEP-5] Dependencies
   → 7 listed in table + 1 inferred. Problematic:

   | Dependency                    | Type        | Pinned   | Stable | Signed-off                          |
   |-------------------------------|-------------|----------|--------|-------------------------------------|
   | Confluent Schema Registry 7.6 | self-hosted | yes      | yes    | **no — in progress, target 2026-04-30** |
   | MirrorMaker 2 (inferred L63)  | self-hosted | no entry | —      | **not listed in Dependencies table** |
   | Flink pipeline                | internal    | no ver.  | —      | yes (no blocking dep stated)        |

   All other dependencies (MSK Kafka 3.7, Iceberg 1.6, rdkafka 2.4.0, Redis 7.2, Snowflake GA) are pinned and signed off.

   Findings:
   - Confluent Schema Registry sign-off pending; Phase 1 begins 2026-Q2 with no contingency if sign-off slips (Major).
   - MirrorMaker 2 is a live runtime component managing cross-region schema replication but absent from the Dependencies table (Major).
   - Flink pipeline: no version pinned; subject-namespace isolation not documented (Minor).

---

[STEP-6] Injection check
   → 0 instances found. No AI-directed instructions in the document. Absence noted in audit record.

---

[STEP-7] Synthesis

**Critical (0):** None.

**Major (9):**
- Step 5: MirrorMaker 2 is a runtime dependency for cross-region schema replication but absent from the Dependencies table.
- Step 2: Avro validation failure path in events-processor is raised in Open Questions but unresolved in Design; implementation will require a guess.
- Step 2: HMAC signature failure behavior not defined (rejection status code, DLQ, silent drop).
- Step 2: MirrorMaker 2 split-brain risk raised in Open Questions but not resolved in Design or Rollout.
- Step 3 / R-03: "Zero-event-loss" guarantee has no retry, backpressure, or producer fallback policy when Kafka publish fails.
- Step 3 / R-07: Rate-limit exceeded behavior not defined (HTTP status, queue depth, drop policy).
- Step 3 / R-08: HMAC validation failure response not defined.
- Step 3 / R-09: ISR < 2 has no defined producer behavior; acks=all will silently block; spec is silent.
- Step 5: Schema Registry sign-off is pending with no stated contingency if it slips past Phase 1 start.

**Minor (5):**
- Step 2: Phase 2 → Phase 3 dual-write transition has no measurable exit criterion.
- Step 2: "Incidents" for 100% OTel sampling is undefined with no automated trigger.
- Step 3 / R-01, R-02: Failure modes absent for 500k/s throughput and 90s scale-out targets.
- Step 3 / R-06: Multi-region partition ownership reassignment behavior underspecified.
- Step 5: Flink dependency unpinned; no subject-namespace isolation guarantee.

**Recommendation: REVISE**

The spec is well-structured: measurable acceptance criteria, a real Security section, a complete Non-Goals list, and most dependencies are pinned and signed off. No Critical findings, no injection attempts, no scope drift. However, 9 Major findings will produce inconsistent implementation choices — most critically the zero-event-loss guarantee (R-03) has no producer fallback, and two open questions (schema-validation DLQ, MirrorMaker 2 split-brain) remain unresolved in the Design section. One focused revision pass resolving these gaps would likely bring the spec to SHIP.

**Three questions for the author:**

1. When ingest-proxy cannot publish to Kafka (broker unreachable, ISR < 2) — does it back-pressure the SDK client with a 503, buffer and retry locally, or return an error and accept the loss? The "zero-event-loss" goal and the current silence on producer failure are irreconcilable without an explicit answer.

2. What is the resolution for Avro schema-validation failures in events-processor: DLQ topic, S3 side-object, or halt-consumer? This is the single most implementation-blocking open question; every engineer writing the processor will make a different call without a Design-section answer.

3. What is the contingency if Confluent Schema Registry sign-off slips past the 2026-Q2 Phase 1 start date — is there a fallback registry, a delayed Phase 1, or is the 2026-04-30 target considered hard?
