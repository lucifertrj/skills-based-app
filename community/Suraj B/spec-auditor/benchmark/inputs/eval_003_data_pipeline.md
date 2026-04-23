# RFC: Rebuild the events ingestion pipeline

**Authors:** platform-data @alina, @marco
**Status:** Draft — review before implementation
**Target rollout:** 2026-Q3

## Summary

We are replacing the existing events ingestion pipeline (`events-ingester-v1`, Go service, SQS + Lambda) with a Kafka-based pipeline (`events-ingester-v2`, Rust). The current pipeline cannot sustain the volume from the new mobile analytics SDK (peak 180k events/s, we currently cap at 60k/s and drop the rest). The v2 design targets 500k events/s sustained with horizontal scaling to 2M events/s.

## Goals

- Sustain 500k events/s ingest with p95 end-to-end latency < 800ms from SDK publish to warehouse-visible.
- Horizontal scaling up to 2M events/s within 90s provisioning (matches AWS ASG cooldown).
- Zero-event-loss guarantee at the ingestion edge (at-least-once; downstream dedup by event_id).
- Schema evolution support via Avro with a schema registry; breaking schema changes require a new topic.
- Replay capability: any 7-day window can be replayed into the warehouse from Kafka.
- Multi-region active-active in us-east-1 and eu-west-1, with per-region partition ownership.

## Non-Goals

- Real-time streaming analytics (still goes through Flink in a separate pipeline).
- Exactly-once delivery guarantees end-to-end (we accept at-least-once; dedup in the warehouse).
- PII scrubbing at the ingest layer (happens in the warehouse ETL; compliance team has signed off).
- Support for legacy v1 SDK clients beyond 2026-Q4 (separate deprecation RFC).
- On-premise deployment (cloud-only).

## Design

### High-level flow

```
Mobile SDK → HTTPS edge (Cloudflare) → ingest-proxy (Rust, ECS)
  → Kafka (MSK, 3 AZs, us-east-1 + eu-west-1) → events-processor (Rust, EKS)
  → Iceberg tables on S3 → Snowflake external tables
```

### ingest-proxy

Written in Rust (Axum + rdkafka). Responsibilities:
- Validate HMAC signature on inbound batches (SDK signs with a per-install key).
- Decode Protobuf batch, transcode to Avro, publish to Kafka.
- Apply per-tenant rate limits (token bucket in Redis cluster).
- Emit OpenTelemetry traces.

Binary size target: under 40MB. Cold start target: under 1.5s. Memory footprint: 256MB per 10k events/s.

### Kafka topology

- Cluster: MSK, 6 brokers per region (c6g.2xlarge), replication factor 3.
- Topics: `events.{environment}.{category}` — e.g., `events.prod.click`, `events.prod.view`.
- Partitions: 192 per topic (sized for 500k/s).
- Retention: 7 days (matches replay target).
- Min in-sync replicas: 2.
- Compression: zstd level 3.

### events-processor

Reads from Kafka, validates Avro, writes to Iceberg. Scales by consumer-group lag (HPA on `consumer_lag > 60s`).

### Schema registry

We will use Confluent Schema Registry in compatibility mode BACKWARD_TRANSITIVE. Registry is deployed as a StatefulSet in us-east-1 and mirrored via MirrorMaker 2 to eu-west-1.

## Data model

### Event envelope (Avro)

```json
{
  "type": "record",
  "name": "EventEnvelope",
  "fields": [
    {"name": "event_id", "type": "string"},
    {"name": "tenant_id", "type": "string"},
    {"name": "install_id", "type": "string"},
    {"name": "sdk_version", "type": "string"},
    {"name": "event_type", "type": "string"},
    {"name": "timestamp_ms", "type": "long"},
    {"name": "ingest_timestamp_ms", "type": "long"},
    {"name": "payload", "type": "bytes"}
  ]
}
```

`payload` is a nested Avro record typed per `event_type`. The event-type-to-schema mapping is maintained in a separate subject namespace.

## Acceptance criteria

1. Ingest-proxy sustains 500k events/s across 48 hours in staging, with p95 latency < 800ms measured at the Cloudflare edge.
2. Replay of a 7-day window completes within 6 hours when triggered with the default parallelism (16 consumer groups).
3. All Avro schemas in the prod registry have a compatibility check in CI that fails the PR if BACKWARD_TRANSITIVE is violated.
4. Cross-region failover (us-east-1 → eu-west-1) completes within 180s in a staged drill, with < 0.01% event loss.
5. The v1 pipeline is decommissioned no later than 2026-Q4 once v2 has run 30 days without an SLO breach.

## Dependencies

| Dependency | Owner | Version | Signed off |
|---|---|---|---|
| MSK (Kafka managed) | AWS platform | Kafka 3.7 | yes |
| Confluent Schema Registry | self-hosted | 7.6.x | in progress — target 2026-04-30 |
| Iceberg on S3 | warehouse team | Iceberg 1.6 | yes |
| Snowflake external tables | data platform | N/A (GA) | yes |
| rdkafka (librdkafka) | vendored | 2.4.0 | yes |
| Redis cluster for rate limits | platform-infra | 7.2 | yes |
| Flink pipeline (separate) | streaming team | N/A | signed off (no blocking dep) |

## Rollout

- Phase 1 (2026-Q2): ingest-proxy deployed to 5% of SDK traffic via Cloudflare weighted routing.
- Phase 2 (2026-Q3): scale to 100% ingest in us-east-1, dual-write to v1 and v2.
- Phase 3 (2026-Q3): enable eu-west-1 region, stop dual-writes, v1 becomes read-only.
- Phase 4 (2026-Q4): v1 decommission.

## Observability

- ingest-proxy emits OTel traces; sampling rate 1% at steady state, 100% during incidents (runtime flag).
- Kafka lag dashboard per topic: `grafana-platform.internal/d/kafka-lag`.
- SLO: p95 < 800ms end-to-end, 99.95% successful ingests per 24h window.
- Pager: Pagerduty `platform-data` rotation, page on lag > 60s for > 5 min or error rate > 0.05% for > 10 min.

## Security

- HMAC signing on all inbound batches (key rotation every 90 days, KMS-managed).
- TLS 1.3 only on edge and internal.
- Kafka ACLs per consumer group; ingest-proxy has publish-only; events-processor has consume-only on `events.*`.
- Avro envelope excludes PII fields by design; `payload` is opaque bytes until warehouse ETL.
- Redis AUTH + TLS; keys expire < 24h.
- No secrets in env vars; all via AWS Secrets Manager with IAM roles.

## Open Questions

- Do we add a DLQ topic for schema-validation failures, or route them to a side-object in S3 and alert? We lean DLQ topic but need agreement from the warehouse team.
- MirrorMaker 2 in active-active has a known split-brain risk under partial network partitions; is the 7-day retention enough slack to recover, or do we need 14?
