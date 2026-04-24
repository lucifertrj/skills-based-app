# Ambiguity patterns

Loaded by `spec-auditor` during Step 2 when the document exceeds 500 words. On shorter docs, the inline shortlist in `SKILL.md` is sufficient.

Each pattern carries a default severity. Promote or demote by one level based on context (e.g. a weak modal in a Requirements section is a Major finding; the same word in an Overview is Minor).

---

## 1. Weak modal verbs — default: Minor, Major in Requirements

Words that indicate a requirement is not actually required.

| Word | Suggested replacement | Notes |
|---|---|---|
| `should` | `must` (if required) or `may` (if optional) | Most common offender. Always flag in Requirements. |
| `may` | fine when truly optional; flag if it modifies a requirement | |
| `could`, `might`, `can potentially` | `will` (if decided) or move to Open Questions | Often a hedge against undecided work. |
| `ideally`, `preferably` | remove; spell out the fallback | "Ideally under 100ms" → "must be under 100ms; if unachievable, document in §Tradeoffs." |
| `where appropriate`, `as appropriate`, `where applicable` | enumerate the cases | An unenumerated conditional is an unbounded one. |

---

## 2. Open-ended lists — default: Minor, Major if in an API or data model

Constructs that imply "and more, figure it out."

- `etc.`, `and so on`, `and the like`
- `e.g.` followed by a non-exhaustive list without "but not limited to"
- `such as X` with no closing boundary
- `and/or` — almost always means the author hasn't decided which one

In API or data-model sections, open-ended lists are Major — the implementation has to enumerate something eventually, and leaving it undecided defers the decision to whoever writes the code first.

---

## 3. Unmeasurable qualifiers — default: Major

Subjective terms that cannot be tested. These must be replaced with measurable criteria before the spec is accepted.

- **Performance:** `fast`, `slow`, `responsive`, `snappy`, `low-latency`, `high-throughput`, `real-time` (without a specific deadline)
- **UX:** `user-friendly`, `intuitive`, `clean`, `elegant`, `seamless`, `frictionless`
- **Quality:** `robust`, `reliable`, `solid`, `production-grade`, `enterprise-ready`
- **Scale:** `scalable`, `high-scale`, `web-scale`, `handles large load`
- **Effort:** `lightweight`, `minimal overhead`, `simple`, `easy to maintain`
- **Correctness:** `best-effort`, `reasonable`, `approximate`, `good enough`
- **Security:** `secure`, `safe`, `private` (without threat model or standard)
- **Availability:** `highly available`, `always on`, `resilient`

Replacement shape: "Fast" is not a requirement. "p95 under 200 ms at 1k concurrent users, measured on the production fleet" is.

---

## 4. Deferred decisions — default: Major, Critical in a non-appendix section of a ship-ready spec

Markers that signal the spec is not actually done.

- `TBD`, `TBC`, `TODO`, `FIXME`
- `[placeholder]`, `[draft]`, `[WIP]`
- `to be determined`, `to be decided`, `under discussion`
- `pending approval from X`, `awaiting sign-off`
- `(XXX)` as a comment-style inline marker

Any of these in a Requirements, Design, Data Model, API, Security, or Rollout section is a Major finding. Two or more in any such section is Critical — the spec is not ready for implementation, and further audit will produce findings that the author would invalidate with the next revision.

An appendix, Open Questions section, or explicit "Risks and Unknowns" section may contain deferred markers without penalty — that is what those sections are for.

---

## 5. Unsafe passive voice — default: Minor, Major if in Requirements

Requirements stated without a named actor leave the implementation ambiguous: the code author has to guess who or what is responsible.

Examples to flag:

- "The data will be validated." — by what? at what layer?
- "Errors should be logged." — by which service? with what severity?
- "The user is notified." — how? through what channel? who sends?
- "Access is restricted." — by whom? at what point in the flow?
- "Caching is applied." — in which layer? with what invalidation?

Rewrite pattern: `<actor> <verb> <object> <when/condition>`. E.g. "The Auth service validates inbound JWTs before forwarding to upstream handlers, returning 401 on failure."

Flag passive voice only when a requirement or design decision is being stated. Passive voice in narrative sections (Overview, Background) is fine.

---

## 6. Handwaved quantities — default: Major

Numbers that sound specific but aren't.

- "Up to" without a bound ("supports up to many users")
- "Millions of", "thousands of" without an actual range
- "Big", "small", "large" as qualifiers on any measurable
- Percentages without a denominator ("99% uptime" — over what window?)
- Time spans without a horizon ("quick startup" — compared to what?)

If the spec states a number, that number must be a concrete, measurable value with defined units and a defined measurement context.

---

## 7. Absent failure modes — default: Major

Every requirement that assumes success without describing failure is incomplete. Pattern to flag:

- "The system retries on failure" — how many times? with what backoff? what if all retries fail?
- "Requests are queued" — bounded? what happens at overflow?
- "Fallback to cache" — for how long? what if cache is also unavailable?
- "Graceful degradation" — degrade how? which features go dark?

Finding wording: "R-N describes success path but not failure behavior."

---

## 8. Extending this list

Rules for additions:

- Add a new category only if a repeated Step-2 finding does not fit an existing category.
- Include a default severity and at least one concrete example.
- Language-specific style preferences (e.g. Oxford comma rules, American vs British spelling) do **not** belong here — those are an editor-skill concern.
- Keep each category under ~12 patterns. A reference file that exceeds ~300 lines no longer fits comfortably in context alongside a long spec.
