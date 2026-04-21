# Sentiment Patterns

> Reference patterns for classifying customer sentiment across conversations. Use to score interactions, trigger escalations, and calibrate AI responses.

---

## 1. Positive Sentiment Indicators

| Type | Examples |
|---|---|
| Explicit gratitude | "Thank you so much!", "You're a lifesaver", "Best support I've had" |
| Product praise | "Love this product", "works perfectly", "worth every penny" |
| Outcome satisfaction | "That fixed it! Amazing" |
| Loyalty signal | "I've been with you for years and still love it" |
| Expansion signal | Customer asks about additional products/features |

**Implicit positives:** Casual tone + emoji after resolution · Volunteering to leave a review · Referring a friend mid-conversation

---

## 2. Neutral / Transactional Tone

Neutral = no emotional charge in either direction. Common in routine support.

**Characteristics:** Short factual messages · No frustration or enthusiasm · Matter-of-fact phrasing

| Pattern | Example |
|---|---|
| Info request | "What's the status of order #12345?" |
| Account management | "Can I reset my password?" |
| Product inquiry | "Does this plan include X?" |
| Acknowledgment | "Ok, received. Thanks." |

> ⚠️ Neutral customers can shift negative **2× faster** than positive ones if a service failure occurs mid-conversation.

---

## 3. Negative Sentiment — 4 Levels

| Level | Signals | Response |
|---|---|---|
| **1 – Mildly Negative** | "A bit confused", "been waiting a few days" | Acknowledge promptly, provide clear resolution |
| **2 – Frustrated** | "I've explained this twice", "why is this so complicated?" | Empathy-first, own it, commit to timeline |
| **3 – Angry** | "This is unacceptable", ALL CAPS, blame attribution | De-escalate, loop in supervisor if needed |
| **4 – Critical** | "Canceling", "I'll leave a review", competitor mention | Immediate escalation + recovery playbook |

**High-signal keywords:**

| Category | Keywords |
|---|---|
| Anger | furious, fed up, disgusted, livid |
| Distrust | lied to, scammed, misled, false advertising |
| Resignation | whatever, forget it, doesn't matter, too late |
| Threat | cancel, report, review, social media, lawyer |

---

## 4. Escalating Sentiment (Trend Detection)

**Negative escalation arc to watch:**
```
Neutral inquiry → Mild frustration → Explicit anger → Churn signal
```
**Intervene between steps 2 and 3** — addressing frustration early prevents it reaching critical.

**False recovery warning signs:**
- "Sure" / "fine" / "okay" with no enthusiasm = passive withdrawal, NOT resolved
- No CSAT response = disengaged
- Returns within 7 days on same issue = superficial resolution

| Trend | Action |
|---|---|
| 3 consecutive messages with increasing negativity | 🔴 Escalate immediately |
| Agent response followed by sharper negative reply | 🟠 Agent missed the mark — re-approach |
| Negative → sudden silence with no resolution | 🟡 Follow up before closing |

---

## 5. Sentiment Scoring Quick Reference

| Score | Label | Description |
|---|---|---|
| +2 | Very Positive | Enthusiastic praise, strong loyalty signal |
| +1 | Positive | Polite thanks, mild satisfaction |
| 0 | Neutral | Transactional, no emotional charge |
| −1 | Mildly Negative | Mild frustration, impatience |
| −2 | Negative | Frustration, disappointment, distrust |
| −3 | Very Negative | Anger, ultimatum, churn threat |

**Conversation Score** = average of all messages, weighted toward the most recent 3.  
Score ≤ −1.5 → flag for human review.

---

## 6. Industry Vocabulary Reference

| Vertical | Negative signals to watch |
|---|---|
| SaaS / Tech | "can't log in", "data lost", "bug not fixed", "downtime" |
| E-commerce | "wrong item", "never arrived", "charged twice", "damaged" |
| Fintech | "unauthorized charge", "account frozen", "can't withdraw" |
| Subscription | "charged after canceling", "can't cancel", "renewal I didn't want" |
