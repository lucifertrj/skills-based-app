# RFC Audit: Rebuild the Events Ingestion Pipeline

**Reviewer:** Senior Engineer (audit)
**RFC Status:** Draft — review before implementation
**Audit Date:** 2026-04-23
**Recommendation:** REVISE before implementation

---

## Overall Impression

The RFC is well-structured and shows clear engineering thought: the motivation is concrete (3× throughput gap), the tech choices are defensible (Rust + Kafka on MSK), and the rollout phasing is sound. That said, several gaps would cause production pain if implementation started today. The two open questions at the bottom are actually the two highest-risk items in the whole doc — they belong in the body as resolved decisions, not trailing questions.

---

## Critical

**1. The active-active MirrorMaker 2 split-brain is unresolved and the RFC proposes to ship anyway.**

The open question about MirrorMaker 2 under partial network partition is flagged but left unanswered. In active-active mode, MM2's offset translation is not lossless: duplicate consumer-group offset commits between regions can cause events to be replayed or silently skipped when a partition rebalances after a partition heal. The RFC's acceptance criterion AC-4 (< 0.01% event loss over 180s failover) is almost certainly violated by any realistic split-brain scenario lasting longer than a few seconds. Either (a) the authors have analysis showing the 7-day retention is sufficient slack and should write it down, or (b) 14-day retention or a quorum-based offset store needs to be added before implementation. Shipping with this unresolved is a data-loss risk.

**2. The schema registry sign-off is not complete, and the implementation target is only one week away.**

The dependency table shows Confluent Schema Registry 7.6.x as "in progress — target 2026-04-30." Phase 1 is targeted at 2026-Q2, which starts immediately. The entire Avro encoding pipeline — ingest-proxy transcoding, CI compatibility checks (AC-3), and events-processor validation — all depend on the registry being up and stable. If the registry slips even two weeks, Phase 1 cannot proceed. There is no contingency or fallback described. This should be a hard gate: Phase 1 cannot start until the schema registry is signed off.

---

## Major

**3. The DLQ strategy for schema-validation failures is unresolved, leaving the processor's error path undefined.**

The second open question — DLQ topic vs. S3 side-object — is operational-safety-critical, not a nice-to-have. events-processor cannot be implemented without knowing what to do when an Avro record fails validation. A DLQ topic gives replay; S3 gives cheaper storage but requires a separate replay job. The code paths, alerting thresholds, and reprocessing SLOs differ substantially between the two approaches. This must be decided before any events-processor implementation begins.

**4. The `payload` field is opaque bytes, but there is no contract for how schema-per-event-type resolution works in practice.**

The spec says "`payload` is a nested Avro record typed per `event_type`" and that the event-type-to-schema mapping lives in "a separate subject namespace." This is underspecified. What is the naming convention for subjects? How does the consumer resolve the schema without a schema ID embedded in the payload (standard Confluent wire format puts a 5-byte schema ID prefix on every record)? If the payload is raw bytes without a schema ID, the consumer must look up the schema by `event_type` string at read time — that is a significant operational coupling and a latency source. This needs a concrete example and a wire-format diagram.

**5. Horizontal scaling to 2M events/s "within 90s" is not validated by the acceptance criteria.**

Goal 2 states scale-up to 2M events/s within 90s, matching AWS ASG cooldown. But AC-1 only tests sustained 500k events/s over 48h. There is no acceptance criterion that validates the 2M events/s burst target or the 90s provisioning time. Given that 192 partitions are described as "sized for 500k/s," reaching 2M/s requires adding partitions — which is a Kafka operational event that cannot happen in 90s. Either the partition count is undersized, or the scale-up story relies on something else (more consumers, larger instances) that is not explained.

**6. The p95 latency SLO is measured at two different points with no reconciliation.**

The goal says "p95 < 800ms from SDK publish to warehouse-visible." AC-1 says "p95 latency < 800ms measured at the Cloudflare edge." Those are very different measurement points. Cloudflare-edge latency captures only the ingest-proxy leg; warehouse-visible latency includes Kafka propagation, events-processor write, Iceberg commit, and Snowflake metadata refresh. These can easily add 30–120s in the normal path. The SLO in the Observability section repeats "p95 < 800ms end-to-end" without any analysis of whether that is achievable given Snowflake's external-table refresh cadence. The RFC needs to either (a) decompose the 800ms budget across each hop, or (b) clarify that "warehouse-visible" means "landed in Iceberg" not "queryable in Snowflake."

---

## Minor

**7. HMAC key rotation is every 90 days, but the key compromise story is missing.**

If a per-install HMAC key is compromised (lost device, decompiled APK), how does an operator revoke it before the 90-day cycle? The Security section does not address revocation. This is not a blocker but should be answered before GA.

**8. Replay acceptance criterion (AC-2) does not specify whether the 6-hour window includes Snowflake sync.**

"Completes within 6 hours" is ambiguous: does it mean data is in Iceberg, or queryable in Snowflake? Same issue as finding 6 above, but specifically for the replay SLA.

**9. The events-processor HPA trigger threshold (`consumer_lag > 60s`) conflicts with the pager threshold.**

The pager fires on "lag > 60s for > 5 min." The HPA also triggers on lag > 60s. If the HPA takes 90s to spin up new pods (ASG cooldown), every lag spike of 60s will simultaneously trigger an alert and begin scale-out — meaning engineers will be paged for what is a normal autoscaling event. Either the pager threshold needs to be higher than the HPA threshold, or a duration qualifier should be added to the HPA rule.

---

## Questions for the Authors

1. For the MirrorMaker 2 split-brain concern: has the team run any failure-injection tests on MM2 in active-active mode, and what was the observed event-loss rate during a simulated 60s network partition between regions? If not, what is the plan for doing so before Phase 3?

2. On the 2M events/s scale target: given that Kafka partition count cannot be changed online without a partition reassignment (which takes hours on a large cluster), what is the actual mechanism for going from 500k to 2M events/s within 90s? Is this purely a consumer/producer scaling story, or are you pre-provisioning more partitions than needed at launch?

3. On the `payload` wire format: is the payload bytes field carrying a Confluent-schema-wire-format record (with schema ID prefix) or raw Avro binary? If the latter, how does the events-processor know which schema to use for deserialization without parsing `event_type` first and doing a registry lookup — and what is the latency budget for that lookup at 500k events/s?

---

## Ship / Revise / Block

**REVISE.** The foundation is solid and the RFC is close, but the two open questions are blocking: the MM2 split-brain risk is a potential data-loss bug in production, and the undefined DLQ path means events-processor cannot be fully implemented. The payload wire-format ambiguity (finding 4) and the scale-to-2M story (finding 5) also need answers before engineering estimation can be trusted. Resolve those four items and this RFC is ready to implement.
