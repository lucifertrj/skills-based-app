# Frustration Signals

> Reference guide for detecting and scoring customer frustration. Use alongside `churn_indicators.md` for risk scoring.

---

## 1. Linguistic Signals

| Signal | Example | Severity |
|---|---|---|
| Absolute language | "always broken", "never works" | 🔴 High |
| Dismissive tone | "whatever", "it doesn't matter anymore" | 🔴 High — withdrawal |
| Sarcasm | "wow, thanks for nothing" | 🟠 Medium-High |
| Repetition emphasis | "I said this ALREADY" | 🟠 Medium-High |
| Complaint stacking | 3+ issues listed in one message | 🟠 Medium-High |
| Passive resignation | "I guess I'll just deal with it" | 🟠 Churn precursor |
| Mild annoyance | "a bit frustrating" | 🟢 Low |

**Punctuation / Format signals:**
- ALL CAPS → High frustration
- 3+ exclamation marks → Medium-High
- Very short reply after long venting history → Withdrawal / High risk

**Structural patterns:**
- Ultimatum: "If X doesn't happen by Y, I will Z" → Critical
- Public threat: "I'm leaving a review" / "I'll post about this" → Reputation risk

---

## 2. Behavioral Signals

| Signal | Risk Level |
|---|---|
| 4+ contacts on same issue (any window) | 🔴 Critical |
| 3 contacts in 1–7 days | 🟠 Medium-High |
| Requesting supervisor / manager | 🟠 Loss of trust |
| Uploading screenshots unprompted | 🟠 Building a case |
| Immediately reopening a closed ticket | 🟠 Unsatisfied with resolution |
| No reply after agent response (48h+) | 🟡 Monitor — possible withdrawal |

---

## 3. Timing Signals

| Contact Time | Implication |
|---|---|
| Late night (10pm–2am) | Issue is severely impacting daily life |
| Multiple contacts in same hour | Panic / acute frustration |
| Weekend contact | High impact — disrupting personal time |
| Follow-up before receiving a reply | Impatience escalating |

**Issue Age Multiplier:**

| Days Open | Frustration Multiplier |
|---|---|
| 0–1 day | 1x |
| 4–7 days | 2x |
| 15+ days | 4x+ (critical, likely churn) |

---

## 4. Frustration Severity Scale (0–10)

| Score | Label | Key Characteristics |
|---|---|---|
| 0–2 | Neutral / Mild | Factual, calm, politely firm |
| 3–5 | Frustrated | Repeated issue, moderately negative |
| 6–7 | Highly Frustrated | Venting, caps, ultimatum hints |
| 8–9 | Angry | Direct anger, blame attribution |
| 10 | Crisis | Churn threat, public complaint, demands supervisor |

**Scoring adjustments:**
- +1 if repeat contact · +1 if high-revenue tier · −1 if historically satisfied

---

## 5. What NOT to Misread as Frustration

- Formal / stilted language ≠ frustrated (some customers write formally)
- Detailed bug descriptions ≠ angry (they're helping you replicate it)
- Short opener ≠ curt (mobile users write briefly)
- Caps in product names ≠ shouting (e.g., "I use JIRA")
