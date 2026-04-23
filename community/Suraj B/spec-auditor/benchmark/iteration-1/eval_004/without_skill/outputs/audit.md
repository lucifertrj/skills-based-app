# Audit: RFC — Per-Tenant Rate Limiter for the Public API

**Auditor:** Senior Engineering Review
**Date:** 2026-04-23
**Spec reviewed:** `eval_004_clean_rate_limiter.md`

---

## Summary Judgment

**REVISE before shipping.** The design is largely sound — good use of redis-cell, sensible rollout phases, clear non-goals, and solid security reasoning for pre-auth placement. However, several gaps in the spec must be addressed before implementation begins. None are blockers individually, but together they represent enough undefined behavior to risk a bumpy launch.

---

## Findings

### Critical

**C1 — Tenant ID trust boundary is underspecified for header-only paths.**
The spec states the URL path wins on mismatch with `X-Tenant-ID`, and requests with absence/mismatch return 400. However, the spec does not define what happens on routes that carry NO tenant ID in the URL (e.g., admin or webhook endpoints that use only the header). Since the middleware runs before auth, a missing or spoofed `X-Tenant-ID` on such paths could either reject valid traffic or allow unlimited-rate calls against an unscoped bucket. The exact extraction logic per route class must be spelled out.

**C2 — No Redis failure mode defined.**
The spec is silent on what happens when the Redis call times out or the cluster is unavailable. In a pre-auth position, a Redis outage means the entire API gateway could hard-fail or, conversely, silently open the rate-limit gate. Neither outcome is acceptable without an explicit policy (fail-open vs. fail-closed) and a tested circuit-breaker path.

---

### Major

**M1 — Config-map reload window is under-specified.**
Acceptance criterion 4 says overrides take effect within 30s, but the spec does not state whether old limits continue enforcing during the reload window, whether reloads are atomic per-tenant, or what happens to in-flight requests during a hot reload. A misconfigured reload could temporarily lock out a high-value enterprise tenant.

**M2 — Shadow-mode metric naming gap.**
During Week 1 (shadow mode), the counter `api_rate_limit_rejected_total` will increment for "would-be" rejections — but clients will not receive 429s. If dashboards and the alert rule (`rate > 10`) are live during shadow week, the ops team will get paged on phantom rejections. The spec should either suppress the alert during shadow week or introduce a label (e.g., `mode="shadow"`) to distinguish shadow from enforced events.

**M3 — No rate on the `Retry-After` value computation.**
The spec says `Retry-After` is an integer number of seconds but does not state the formula. For a 1000 rpm token bucket, the naive value might be a constant 60s, which is unhelpful if the tenant is only 1 token over budget. Clients need an accurate value to back off correctly without hammering the gateway repeatedly.

---

### Minor

**m1 — Alert threshold is a single global value.**
The alert fires if any tenant exceeds 10 rejections/5m. Enterprise tenants with high legitimate traffic may legitimately generate rejections during traffic spikes. A per-tier threshold (or at least suppression for known-high-volume tenants) would reduce alert fatigue.

**m2 — `X-RateLimit-Remaining` deferred with no revisit date.**
The open question defers this header to v2 with no timeline. Clients currently have no way to self-govern, which may increase rejection volume unnecessarily. Even a rough v2 ETA should be committed so client teams can plan.

**m3 — redis-cell TTL interaction is implicit.**
The spec states the Redis key TTL is 120s (managed by `CL.THROTTLE`), but does not clarify whether this resets on every request or only on key creation. If TTL resets on every hit, a tenant with continuous traffic never expires their key, which is correct — but a tenant that stops for exactly 90–120s may get a double-allowance window. This edge case should be explicitly acknowledged.

---

## Three Questions for the Author

1. **What is the fail-open/fail-closed policy on Redis unavailability, and has a Redis-down scenario been tested in staging end-to-end?**

2. **For routes where the tenant ID is header-only (no path segment), what exact logic determines which bucket to charge — and what is the behavior when the header is absent?**

3. **How is the `Retry-After` value computed? Is it static (e.g., always `60`), or is it derived from the token bucket's expected refill time — and is that computation tested in CI?**

---

## Recommendation

**REVISE.** Address C1 and C2 (failure semantics and tenant-ID extraction completeness) before implementation begins. M1–M3 should be resolved before the Week 2 enforcement phase. The rollout plan and observability story are otherwise well-thought-out; this spec is close to shippable.
