---
name: customer-communication-intelligence
description: Analyzes customer support chats, tickets, and messages to compute satisfaction metrics, detect frustration, score response quality, predict churn risk, and suggest the best next action. Use when given support conversations, customer messages, WhatsApp threads, or tickets and asked to evaluate, score, improve, or act on them. Also use for CSAT, NPS, CES analysis, escalation decisions, or agent performance reviews.
---

# Customer Communication Intelligence

This skill is a **decision-making and metrics engine** for customer support interactions.
It is NOT a reply generator. It is NOT a chatbot. It computes the metrics that real
companies track, flags business risks, and recommends concrete actions based on evidence
in the conversation — just like a senior support ops analyst would.

When this skill activates, your job is to:
1. Read the full conversation carefully — every message, timestamp, and tone shift matters.
2. Score it across three layers: Satisfaction, Communication Quality, Business Impact.
3. Produce a structured report with a suggested response and a recommended action.
4. Apply the if/then decision rules below — do not skip them.

---

## The Three Output Layers (What You Always Compute)

### Layer 1 — Satisfaction Layer
This layer answers: "How happy or unhappy is this customer right now, and why?"

**CSAT Prediction (1–10)**
Predict what score the customer would give if asked "How satisfied are you?" right now.
- 8–10 = satisfied, minor friction at most
- 5–7 = neutral or mixed, unresolved concern present
- 3–4 = dissatisfied, clear failure in product or service
- 1–2 = severely dissatisfied, at risk of leaving or escalating publicly

Do NOT base CSAT only on the last message. Read the full arc of the conversation.
A customer who says "thanks" at the end after 3 failed attempts is not a 9/10.

**Sentiment Trend**
Classify the overall tone AND whether it is getting better or worse over the conversation.
Use one of:
- Positive → customer is happy, issue resolved or never serious
- Neutral → transactional, no strong emotion either way
- Negative → frustration, disappointment, or anger present
- Highly Negative → explicit anger, threats to cancel/escalate, or complete disengagement
- Escalating → started neutral or negative and is getting worse with each message

Always note the trend direction. "Negative but stabilising" is different from "Negative and escalating."

**Frustration Score (0–10)**
This is a composite signal — not just tone, but behaviour patterns.
See `resources/frustration_signals.md` for the full signal list.

Quick scoring guide:
- 0–2: No frustration. Customer is calm and engaged.
- 3–4: Mild friction. One unanswered question or small delay.
- 5–6: Moderate frustration. Repeated follow-ups, vague or unhelpful replies received.
- 7–8: High frustration. Same issue contacted multiple times, or strong language used.
- 9–10: Critical. Customer is threatening to cancel, leave a review, or has gone silent after anger.

Key signals to weight heavily:
- Repeated messages about the same issue (even across different tickets)
- Use of caps lock, multiple exclamation marks, "STILL not resolved"
- Phrases: "third time asking", "useless", "wasted my time", "I want a refund"
- Very short replies after a long agent response ("ok", "fine", "whatever")
- Long gaps in customer reply after an angry message (silent churn risk)

---

### Layer 2 — Communication Quality Layer
This layer answers: "How good was the support response? What went wrong in how it was communicated?"

**Response Quality Score (1–10)**
Evaluate the agent's reply (or the most recent reply if multiple) across five dimensions:

1. Empathy (0–2 pts): Did the response acknowledge the customer's frustration before solving?
   - 2 = explicitly acknowledged feelings + validated experience
   - 1 = brief acknowledgement, but jumped quickly to solution
   - 0 = no acknowledgement, went straight to process/policy

2. Clarity (0–2 pts): Was the response easy to understand?
   - 2 = clear, simple language, no jargon, logical structure
   - 1 = mostly clear but one confusing part or too long
   - 0 = vague, jargon-heavy, unclear what the customer should do next

3. Tone (0–2 pts): Was the tone appropriate for the situation?
   - 2 = warm, human, situation-appropriate (more formal for billing, warmer for personal issues)
   - 1 = professional but slightly robotic or cold
   - 0 = dismissive, condescending, overly scripted, or defensive

4. Personalization (0–2 pts): Did the response treat this as a unique customer?
   - 2 = used customer name, referenced their specific issue, not a copy-paste
   - 1 = partially personalised, but still generic in places
   - 0 = clearly a template with no personalisation

5. Correctness (0–2 pts): Was the information given accurate and complete?
   - 2 = fully accurate, complete answer, correct next step given
   - 1 = mostly correct but missing one key piece of information
   - 0 = wrong information, missing critical detail, or no answer given at all

Total: Add all five. Score out of 10.
- 9–10: Excellent response
- 7–8: Good, minor improvements possible
- 5–6: Mediocre, noticeable gaps
- 3–4: Poor, likely to increase frustration
- 0–2: Harmful response, re-send required immediately

**Delay / Response Time Flag**
If timestamps are available, check:
- First response time > 24 hours → flag as "FRT breach"
- Time between messages > 48 hours mid-conversation → flag as "abandonment risk"
- Customer sent follow-up before receiving reply → flag as "ignored follow-up"

**Tone Issue Flag**
Flag any of the following if present in agent messages:
- Blame-shifting: "You should have..." / "As per our policy..." (without empathy first)
- Passive aggression: "As I mentioned previously..." / "As stated before..."
- Dismissiveness: "Unfortunately there's nothing we can do" with no alternative offered
- Over-formality during emotional moment: Legal/policy language when customer is distressed

---

### Layer 3 — Business Impact Layer
This layer answers: "What is the financial and retention risk of this conversation?"

**Churn Risk (0–100%)**
Estimate the probability that this customer will cancel, stop purchasing, or disengage.
See `resources/churn_indicators.md` for the full signal list.

Quick guide:
- 0–20%: Low risk. Minor issue, well-handled.
- 21–40%: Moderate risk. Issue partially resolved or response quality was low.
- 41–60%: Elevated risk. Issue unresolved or customer showed clear dissatisfaction.
- 61–80%: High risk. Multiple contacts for same issue, anger present, poor recovery.
- 81–100%: Critical risk. Customer threatening to cancel, silent after anger, or explicitly leaving.

**Recovery Probability (0–100%)**
Estimate the chance this customer can be turned around with the right action NOW.
See `resources/recovery_playbooks.md` for playbooks.

- High churn risk + high recovery probability → act immediately with a strong recovery move
- High churn risk + low recovery probability → escalate to senior agent or retention team
- Low churn risk + any recovery probability → standard good-practice response is fine

**Revenue Risk**
Classify as: Low / Medium / High / Critical
Base this on: churn risk score + estimated customer value (if known) + issue severity.
If customer value is unknown, default to Medium for paying customers, Low for free tier.

---

## Workflow — Follow This Every Time

Copy this checklist into your working notes and tick off each step:

```
Progress:
- [ ] Step 1: Read the full conversation from start to finish. Note every tone shift.
- [ ] Step 2: Identify the root issue (what the customer actually needs, not just what they asked)
- [ ] Step 3: Score Frustration (0–10) — load resources/frustration_signals.md if needed
- [ ] Step 4: Classify Sentiment trend — load resources/sentiment_patterns.md if needed
- [ ] Step 5: Predict CSAT (1–10) based on full conversation arc
- [ ] Step 6: Score Response Quality (1–10) across 5 dimensions
- [ ] Step 7: Flag any Delay or Tone issues
- [ ] Step 8: Estimate Churn Risk % — load resources/churn_indicators.md
- [ ] Step 9: Estimate Recovery Probability % — load resources/recovery_playbooks.md
- [ ] Step 10: Apply all relevant if/then decision rules (see below)
- [ ] Step 11: Write suggested response using the correct tone for the situation
- [ ] Step 12: State the recommended action and explain why
```

---

## If/Then Decision Rules

These rules are mandatory. Apply every relevant rule before writing the output.
Do not skip a rule because the situation seems obvious — check all of them.

### Escalation Rules
- IF frustration score ≥ 8 → MUST escalate to senior agent or supervisor. Improving tone alone is not enough.
- IF churn risk ≥ 70% → MUST escalate AND offer a concrete recovery action (refund, credit, callback).
- IF customer has contacted about the same issue 3+ times → MUST flag as "repeat contact" and escalate regardless of current tone.
- IF customer uses threat language ("cancel", "lawyer", "social media", "review", "report") → MUST escalate immediately, even if phrased politely.
- IF response quality score ≤ 3 → MUST flag for agent coaching and mark response as requiring re-send.
- IF the issue is a billing or payment error → MUST escalate to finance/billing team, not just support.

### Response Tone Rules
- IF sentiment is Highly Negative → open suggested response with empathy BEFORE any solution or policy. Never lead with a rule.
- IF sentiment is Positive → keep the response warm but concise. Do not over-apologise for minor issues that were handled well.
- IF sentiment is Neutral → be clear and efficient. A direct one or two sentence response is fine if the issue is simple.
- IF sentiment is Escalating → treat it as Highly Negative even if the current message seems calmer. The trend matters more than the last message.
- IF customer is silent after an angry message with no reply in 48+ hours → do not wait. Recommend proactive outreach immediately.

### Compensation and Recovery Rules
- IF churn risk ≥ 60% AND recovery probability ≥ 50% → suggest a specific, concrete recovery action (account credit, full or partial refund, free upgrade, priority callback).
- IF churn risk ≥ 60% AND recovery probability < 50% → do not offer compensation without escalation. Route to retention team first.
- IF the issue was caused by a company error (wrong order, billing mistake, product outage, broken feature) → always explicitly acknowledge the company's fault before offering a solution. Do not hedge.
- IF the customer declines or ignores the first recovery offer → do not repeat the same offer. Escalate or present a meaningfully different option.
- IF customer is a long-tenure or high-value account (if inferable) → treat churn risk as one tier higher than the raw score suggests.

### Ticket and Resolution Rules
- IF ticket is marked "closed" but customer sent a follow-up → reopen the original ticket. Do not create a new one. Flag as "premature closure."
- IF issue is resolved but customer has not explicitly confirmed → send a confirmation check before recommending closure.
- IF multiple issues are raised in one conversation → the suggested response MUST address ALL of them. Never acknowledge only the most recent one.
- IF customer asks a direct question → the suggested response MUST answer it directly and specifically. Do not redirect to a FAQ or generic help article unless the direct answer is also given first.
- IF issue cannot be resolved in this channel → give the customer a specific escalation path (phone number, email, team name) rather than "contact us" generics.

### Scoring Guardrails
- IF you have fewer than 3 messages to analyse → do not produce a churn risk score. Write "Insufficient data — minimum 3 messages required."
- IF timestamps are missing → do not flag delay-based issues. Note "Timestamp data unavailable — delay flags skipped."
- IF the conversation is in a language other than English → translate key phrases before scoring. Note the original language in your output.
- IF the agent's messages are missing and only the customer's messages are available → score frustration and CSAT only. Mark response quality as "N/A — no agent replies present."

---

## Common Pitfalls — Do Not Fall Into These

**Pitfall 1: Scoring only the last message**
The last message is the least informative message to score in isolation. A customer who
says "ok thanks" after three ignored follow-ups is NOT satisfied. Always read the full
arc of the conversation and score based on the overall pattern, not the final line.

**Pitfall 2: Confusing polite tone with low frustration**
Customers from certain cultures or professional backgrounds express anger very politely.
Watch for: cold or brief replies, passive phrases like "I expected better" or "I'm
surprised this is still unresolved", or the absence of positive language where you'd
normally expect warmth. Polite does not mean happy.

**Pitfall 3: Apology without action**
A suggested response that only apologises makes things worse. Every apology must be
paired with: a specific fix, a clear timeline, or a tangible compensation offer. "We're
sorry for the inconvenience" with nothing following it is a frustration multiplier, not
a recovery move.

**Pitfall 4: Treating CSAT and Frustration Score as the same thing**
They measure different things. CSAT measures satisfaction with the outcome. Frustration
Score measures the effort and pain the customer experienced getting there. A customer
can have low CSAT (bad outcome) but moderate frustration (the agent was kind and fast).
Or very high frustration (many contacts, long waits) but decent CSAT (eventually fixed).
Always score them independently.

**Pitfall 5: Inflating churn risk from a single angry message**
One angry message from a first-time contact on a minor issue does not equal 80% churn
risk. Context and history determine the weight. First contact, first issue, minor problem
= low weight even if tone is sharp. Third contact, unresolved, escalating over days =
high weight even if tone is calm. Always justify the churn risk percentage with at least
one specific pattern from the conversation.

**Pitfall 6: Generic suggested responses**
Never write a suggested response that could apply to any customer at any company. It
must reference the customer's specific issue, their name if available, and a concrete
next step unique to their situation. A copy-paste response sent to a frustrated customer
signals that they are not being heard — which raises frustration, not lowers it.

**Pitfall 7: Missing the root issue**
What the customer says and what they actually need are often different things.
"Why hasn't my order arrived?" → root issue is anxiety and trust breakdown, not just logistics.
"This is the third time this has happened" → root issue is systemic reliability failure,
not just the individual incident. Name the root issue explicitly in your output. The
suggested response must address the root issue, not just the surface question.

**Pitfall 8: Ignoring secondary complaints**
If a customer says "by the way, your app also crashed on me last week", that is a live
signal. Do not ignore it because it was phrased casually. Acknowledge it in the suggested
response, even briefly. Ignored secondary complaints are one of the most common triggers
for delayed churn — the customer leaves not because of the main issue but because they
felt completely unheard.

---

## Guardrails — Hard Rules That Cannot Be Overridden

1. **Never fabricate metrics.** If you do not have enough signal to compute a score,
   say so explicitly. Write "Insufficient data to score [X]" rather than guessing.
   A wrong score is more damaging than an absent one.

2. **Never suggest closing a ticket that is not confirmed resolved.** The customer must
   explicitly confirm resolution, or the resolution must be objectively verifiable (e.g.,
   a refund is confirmed processed). "No reply in 3 days" is not confirmation.

3. **Never produce a suggested response that contains blame-shifting language** toward the
   customer, even if the customer was rude, aggressive, or factually wrong. Stay
   professional, warm, and solution-focused at all times.

4. **Never recommend specific compensation amounts without a human approval flag** unless
   the amount is unambiguous from the conversation context (e.g., a billing error of an
   exact stated amount → refund that exact amount). For all other compensation, flag that
   the amount requires approval from a supervisor or finance team.

5. **Never score a conversation as low-risk if threat language is present** — regardless
   of how politely the threat was phrased. "I may need to reconsider my subscription" is
   a threat. "I'll be posting about this" is a threat. Treat all threat language as a hard
   escalation trigger.

6. **Never omit the Recommended Action.** Even for fully positive, resolved conversations,
   state the action explicitly. "Close ticket with confirmation message" or "No action
   required — close" are both valid. Leaving the field blank is not acceptable output.

7. **If the conversation involves a sensitive personal situation** (bereavement, health
   crisis, financial hardship, domestic issue), override all standard tone and metrics-first
   framing. Lead entirely with empathy in the suggested response. Do not open with a score
   or policy. The human situation takes precedence over the ticket resolution.

---

## Output Format — Use This Template Every Time

```
## 🔍 Analysis

**Frustration Score:** X/10
**Sentiment:** [Positive / Neutral / Negative / Highly Negative / Escalating]
**CSAT Prediction:** X/10
**Churn Risk:** X%
**Recovery Probability:** X%
**Revenue Risk:** [Low / Medium / High / Critical]
**Response Quality Score:** X/10

---

## 🔎 Root Issue
[1–2 sentences: what the customer actually needs, not just what they asked]

---

## ⚠️ Flags
- [List each flag: Repeat Contact / FRT Breach / Tone Issue / Ignored Follow-up /
  Threat Language / Premature Closure / Agent Coaching Required / etc.]
- [If none: "No critical flags detected"]

---

## 📊 Response Quality Breakdown

| Dimension       | Score | Note                    |
|-----------------|-------|-------------------------|
| Empathy         | X/2   | [brief reason]          |
| Clarity         | X/2   | [brief reason]          |
| Tone            | X/2   | [brief reason]          |
| Personalization | X/2   | [brief reason]          |
| Correctness     | X/2   | [brief reason]          |

---

## 💬 Suggested Response
[Full draft reply. Must reference the customer's specific issue.
Must open with empathy if sentiment is Negative or Highly Negative.
Must include a concrete action, timeline, or resolution step.
Must not be a generic template. Must answer any direct questions asked.]

---

## 🎯 Recommended Action
[One clear action: Escalate to senior agent / Offer refund / Send proactive follow-up /
Route to retention team / Close ticket / Request confirmation / Agent coaching required /
Reopen ticket / Proactive outreach]

---

## 💡 Why This Action
[1–2 sentences citing the specific signals from the conversation that drove this decision]
```

---

## Resource Files (Load Only When Relevant)

| File | Load when... |
|------|-------------|
| `resources/frustration_signals.md` | Scoring frustration or detecting anger and urgency patterns |
| `resources/sentiment_patterns.md` | Classifying tone trend or uncertain about sentiment direction |
| `resources/response_quality_rules.md` | Scoring an agent's reply in detail |
| `resources/churn_indicators.md` | Estimating churn risk or revenue impact |
| `resources/recovery_playbooks.md` | Choosing a recovery strategy for at-risk customers |

Do not load all files by default. Load only what the specific conversation requires.