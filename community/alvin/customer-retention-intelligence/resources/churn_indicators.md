# Churn Indicators

> Reference guide for identifying customers at risk of churning. Use alongside `frustration_signals.md` and `recovery_playbooks.md`.

---

## 1. High-Risk Phrases

| Phrase / Pattern | Risk Level |
|---|---|
| "cancel my account" / "cancel subscription" | 🔴 Critical |
| "switching to [competitor]" | 🔴 Critical |
| "this is the last time" | 🔴 Critical |
| "I've had enough" / "fed up" | 🟠 High |
| "nothing ever gets fixed" | 🟠 High |
| "disappointed" / "used to love this product" | 🟡 Medium |
| "thinking about my options" | 🟡 Medium |

---

## 2. Behavioral Churn Signals

- **3+ contacts in 7 days** on same issue → Medium risk
- **5+ contacts in 14 days** → High risk
- **2+ escalations in 30 days** → Critical risk
- Reopening a resolved ticket within 24 hours
- Duplicate tickets across channels (email + chat + phone)
- Short curt replies ("fine", "okay") after expressing anger — withdrawal signal
- Declined resolution offer with no counter-reason

---

## 3. Issue Type → Churn Correlation

| Issue Category | Churn Probability |
|---|---|
| Payment failure (unresolved 48h+) | 70–85% |
| Product completely broken / unusable | 65–80% |
| Repeated same issue (3rd+ occurrence) | 60–75% |
| Billing overcharge (unresolved) | 60–75% |
| Long shipping delay (10+ days late) | 50–65% |
| Single negative interaction (resolved) | 5–15% |

---

## 4. Churn Risk Scoring (1–5 per dimension)

| Dimension | Low (1) | High (5) |
|---|---|---|
| Language sentiment | Polite, calm | Angry, ultimatum |
| Contact frequency | First contact | 4+ contacts same issue |
| Issue severity | Minor inconvenience | Product unusable / financial loss |
| Resolution history | Resolved first time | Multiple unresolved |

**Total Score:** 4–8 = Low · 9–15 = Medium · 16–20 = High · 21–25 = Critical

---

## 5. Revenue Risk Tiers

| Tier | Annual Value | Response SLA |
|---|---|---|
| Critical | > $10,000/yr | < 1 hour |
| High | $2,000–$10,000/yr | < 4 hours |
| Medium | $500–$2,000/yr | < 24 hours |
| Low | < $500/yr | < 48 hours |

---

## 6. Automated Flag Triggers

Flag a customer for retention review when any of these occur:
1. NPS score ≤ 5 or CSAT ≤ 2/5
2. Subscription downgrade or cancellation page visited
3. Third contact on same issue within 10 days
4. Competitor mentioned by name
5. Full refund requested
6. Escalation triggered more than once in 60 days
