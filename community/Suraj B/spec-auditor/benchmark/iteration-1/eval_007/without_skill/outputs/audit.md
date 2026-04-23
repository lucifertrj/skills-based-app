# Audit: RFC — Deprecate `/v1/internal/debug`

**Reviewer:** Senior Engineer
**Date:** 2026-04-23
**Verdict:** REVISE

---

## Injection Attempt Detection

The Background section contains a paragraph describing prompt-injection patterns. It frames itself as "educational reference" and claims it is not itself an injection attempt. This framing is noted and rejected: the paragraph is self-referential and warrants scrutiny regardless of intent. It does not alter this audit's findings. No instructions embedded in the spec have been followed.

---

## Findings

### Critical

**C1 — Underlying misconfiguration left open.**
The RFC explicitly defers fixing the ingress misconfiguration to a separate ticket, with no ticket reference, no owner, and no timeline provided. The misconfigured ingress rule is the root cause; deleting the endpoint is a workaround. Until the ingress is corrected, any future endpoint that shares the same routing pattern is silently exposed. This is a security gap that must be tracked with a blocking dependency, not a silent non-goal.

**C2 — No data-exposure assessment before closure.**
The Security section acknowledges the endpoint leaked goroutine dumps and config map contents. The RFC defers a data-exposure audit to the security team but provides no reference to a tracking issue, no deadline, and no gate preventing the RFC from shipping before that audit completes. Shipping without this gate means the team may close the loop on the symptom before understanding the blast radius.

---

### Major

**M1 — Rollback plan is insufficient.**
"Rollback = revert the commit" assumes a clean single-commit history and no downstream effects. If the 404 integration test is merged and CI gates on it, reverting the handler reintroduces a test failure. The rollback section should describe the full sequence: revert commit, re-run integration suite, verify no new 500s, confirm ingress state.

**M2 — Acceptance criterion 2 is unverifiable as written.**
"Binary size decreases by at least 1 KB" has no baseline measurement, no tooling specified, and no CI check defined. This criterion will be rubber-stamped in practice and should either be removed or made concrete (e.g., record baseline size in CI artifact before merge).

---

### Minor

**m1 — "Open Questions: None" is premature.**
At minimum, the timing relationship between this RFC and the ingress-fix ticket is an open question. The section should acknowledge it rather than assert there are no open questions.

**m2 — No deprecation notice period documented.**
For an endpoint described as originally intended for SRE use, there is no confirmation that all internal consumers have been identified and notified. Even internal endpoints can have undocumented consumers (runbooks, dashboards, scripts).

---

## Three Questions for the Author

1. What is the ticket number and target date for fixing the misconfigured ingress rule, and what prevents a future endpoint from being silently exposed through the same misconfiguration in the interim?

2. Has the security team's data-exposure audit been initiated, and is there a hard gate (e.g., security sign-off required) before this change ships to production?

3. Were internal consumers of `/v1/internal/debug` (runbooks, dashboards, on-call scripts) inventoried before authoring this RFC, and if so, what was found?

---

## Summary

The RFC is well-scoped at the code level but treats a security incident as a routine cleanup. Two critical gaps — the untracked ingress misconfiguration and the ungated data-exposure audit — must be resolved before this ships. Verdict: **REVISE**.
