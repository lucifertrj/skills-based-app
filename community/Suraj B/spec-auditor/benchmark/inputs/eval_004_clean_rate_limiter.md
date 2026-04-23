# RFC: Per-tenant rate limiter for the public API

**Authors:** api-platform @hari
**Status:** Draft — review before implementation
**Target rollout:** 2026-04-30

## Summary

Add a per-tenant rate limiter in front of the public REST API. Default budget is 1000 rpm per tenant; enterprise tenants can be overridden via a config map. Excess requests return HTTP 429 with a `Retry-After` header.

## Goals

- Enforce per-tenant request quotas without adding > 2ms p95 overhead to normal requests.
- Return HTTP 429 with a `Retry-After` header (integer seconds) when the budget is exceeded.
- Allow per-tenant overrides via a YAML config map in the platform namespace.
- Emit a Prometheus counter `api_rate_limit_rejected_total{tenant,endpoint}` for every rejection.

## Non-Goals

- Global (non-tenant-scoped) rate limiting. Out of scope.
- Burst control beyond the flat per-minute budget (no sliding window in v1).
- Billing integration. Hard denial only in v1; paid overage comes in a follow-up.
- Client-side backoff libraries — clients are expected to honor `Retry-After`.

## Design

We will use a Redis-backed token-bucket implementation via `redis-cell` (module `CL.THROTTLE`). The rate-limiter middleware sits in the gateway (`api-gateway`, Go, before the auth middleware on purpose — we want to apply limits on invalid tokens too, to prevent credential-stuffing amplification).

Middleware ordering:

```
request → tls → rate-limit → auth → authorization → handler
```

The rate-limit middleware extracts the tenant ID from the path (`/v1/tenants/{tid}/...`) or from the `X-Tenant-ID` header. On mismatch or absence, the request is rejected with 400.

## Data model

No persistent changes. Redis keys: `rl:{tenant_id}` (TTL 120s, managed by `CL.THROTTLE`). Config map: `kube-system/api-rate-limits` with keys `default` and `tenant:<id>`.

## Acceptance criteria

1. `p95(latency)` for requests below budget does not increase by more than 2ms, measured on the production canary fleet for 24h.
2. Rate-limit rejections return 429 with integer `Retry-After`; verified by a CI smoke test that issues 1100 requests/min to a test tenant and asserts the 101st request onward returns 429 with a non-zero `Retry-After`.
3. Prometheus counter `api_rate_limit_rejected_total` increments by 1 per rejection; verified by a CI assertion on the `/metrics` endpoint.
4. A tenant override in the config map takes effect within 30s of the ConfigMap update (gateway watches the map).

## Dependencies

| Dependency | Owner | Version | Signed off |
|---|---|---|---|
| Redis (managed, ElastiCache) | platform-infra | Redis 7.2 | yes |
| redis-cell module | vendored | v0.3.1 (pinned) | yes |
| api-gateway | api-platform | current main | yes |
| Prometheus | observability | 2.52 | yes |

## Security

- The rate-limit middleware sits **before** auth deliberately, to block brute-force and credential-stuffing amplification.
- `X-Tenant-ID` header is never trusted on paths that carry the tenant ID in the URL; the URL wins.
- Redis is VPC-internal only; TLS; AUTH password rotated every 90 days via KMS-backed Secrets Manager.
- Rejections are logged at INFO level with tenant ID; no header or body of the rejected request is logged (prevents token leakage from header stuffing).

## Rollout

- Week 1: shadow-mode (evaluate the bucket, emit metrics, never reject). Verify the counter increments as expected.
- Week 2: enforce on 10% of tenants via a feature flag.
- Week 3: enforce globally.

Rollback plan: flip the `ENFORCE_RATE_LIMITS=false` env var on the api-gateway. This is tested in the staging canary every release.

## Observability

- `api_rate_limit_rejected_total{tenant,endpoint}` — Prometheus counter (primary).
- `api_rate_limit_tokens_remaining{tenant}` — Prometheus gauge sampled at 10s.
- Grafana dashboard: `grafana.internal/d/api-rate-limits`.
- Alert: `sum by (tenant) (rate(api_rate_limit_rejected_total[5m])) > 10` for > 10 min pages the tenant-liaison rotation.

## Open questions

- Do we expose `X-RateLimit-Remaining` to clients in v1, or wait for v2? Leaning no for v1 to keep clients from optimizing to just-below-budget.
