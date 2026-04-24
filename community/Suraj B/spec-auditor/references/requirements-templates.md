# Requirements templates

Loaded by `spec-auditor` during Step 3 when five or more detected requirements are missing measurable criteria, a named actor, or a defined failure mode.

Use these templates to rewrite weak requirements. Share them with the spec author as part of the audit remediation.

---

## The three-part requirement

Every technical requirement has three parts:

1. **Acceptance criterion** — a numeric threshold, binary behavior, or observable state change that someone with a terminal can verify.
2. **Named actor** — the service, component, team, or function responsible.
3. **Failure mode** — what happens when the requirement is violated.

Requirements missing any of the three should be flagged. Missing all three is the most common failure mode in practice.

---

## Rewriting weak requirements

### Performance

❌ `The API should respond quickly.`

✅ `The <service-name> API must return 200 OK for all GET /v1/users/{id} requests in under 200 ms at p95, measured over rolling 5-minute windows at 1,000 RPS. When p95 exceeds 400 ms for more than two consecutive windows, the on-call is paged.`

Parts: criterion (p95 < 200ms at 1k RPS), actor (service-name), failure mode (page on sustained breach).

### Correctness

❌ `Errors should be handled gracefully.`

✅ `The payment-service must translate every upstream provider error into one of the documented error codes in §ErrorCodes, log the original error with `error_id` tag at ERROR level, and return HTTP 502 with the translated code in the JSON body. Untranslated errors are a production incident.`

### Availability

❌ `The system should be highly available.`

✅ `The <service-name> must maintain ≥ 99.9% monthly availability as measured by the existing synthetic prober at /healthz. Below 99.9% in any month triggers a blameless postmortem per the engineering handbook.`

Note: "99.9% monthly availability" without a measurement source is still ambiguous. Always name the instrumentation.

### Scalability

❌ `The service should scale to handle growth.`

✅ `The <service-name> must sustain 5,000 RPS with a horizontal-scaling factor of ≤ 2 (i.e. doubling traffic requires at most doubling replica count) up to 50,000 RPS. Beyond 50k RPS the service is permitted to degrade per §GracefulDegradation; below 5k RPS degradation is a bug.`

### Security

❌ `Tokens should be stored securely.`

✅ `Access tokens must be stored encrypted at rest using AES-256-GCM with keys from <kms-service>. Tokens in memory must live no longer than the request that originated them and must be zeroed on request end. Plaintext tokens appearing in logs at any level is a Critical incident.`

### Data integrity

❌ `The data will be validated.`

✅ `The <ingest-service> must validate every inbound record against the Avro schema in <schema-registry-path> before writing to Kafka. Records that fail validation are written to <dead-letter-topic> with the validation error and the record ID; they are not retried automatically.`

### User-facing

❌ `Users should be notified of errors.`

✅ `On any terminal failure in the checkout flow, the web client must render the error banner from <design-system-component-path> within 500 ms of the API response, include the user-facing error code from §ErrorCodes, and log the event to analytics with `event=checkout_error_shown`. Silent failures (no banner, no log) are a customer-facing bug.`

---

## Structured requirement format

For specs that adopt a structured format, this shape works well:

```
R-042: Inbound JWT validation
  Actor:        Auth service (auth-svc)
  Trigger:      Every inbound HTTP request bearing an Authorization header
  Behavior:     Validate signature, issuer, audience, expiry; extract subject claim
  Criterion:    Valid tokens produce a populated request context; invalid tokens
                cause an immediate 401 response with error code AUTH_INVALID
  Failure mode: JWT library exception returns 500 with error code AUTH_INTERNAL,
                does NOT leak validation detail to the client, logs full detail
                at ERROR with request_id
  Priority:     P0
  Owner:        @auth-team
  Tests:        auth_svc/tests/jwt_test.go::TestInboundValidation
```

This format makes Step 3 of the audit nearly automatic — each field maps to one of the three parts (Criterion → acceptance, Actor → named actor, Failure mode → failure mode).

---

## Smells to flag beyond the basics

- **"All of the above."** A requirement that aggregates many unrelated behaviors into one line. Split it.
- **"Plus edge cases."** If the spec says "handle edge cases" without enumerating them, there are no requirements for edge cases — just wishful thinking.
- **Requirement as timeline.** "Ship by Q3" is a commitment, not a requirement. Requirements describe the system; commitments describe the schedule.
- **Requirement as preference.** "We prefer Postgres" is not a requirement unless there is a consequence for using something else. Flag and convert: either "The data layer must be Postgres 14+" or move to §Considered Alternatives.
- **Vacuous acceptance criteria.** "Tests pass" is not a criterion; it just relocates the ambiguity into the test code. Spell out which behaviors the tests must verify.

---

## How to present remediation

When delivering audit findings that use this reference, quote the weak requirement verbatim and propose a rewrite in the three-part form. Do not rewrite silently — the author must see the diff to agree to it. Example finding format:

```
R-03 "The service should handle high load" (Major, missing measurable criterion)
  Suggested rewrite:
    "The <service> must sustain 2,000 RPS at p95 latency under 300 ms for
     GET /v1/*, measured on the production fleet. Below 2,000 RPS with
     latency above 300 ms is a performance incident."
```
