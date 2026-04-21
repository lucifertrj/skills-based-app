
This file is loaded on demand when the SKILL.md body doesn't cover a specific situation. Reference it when you need deeper guidance on: frontmatter specification, description writing, skill taxonomy, token budgeting, evaluation, refactoring, or multi-file architecture.

---

## Table of Contents

1. [Full Frontmatter Specification](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#1-full-frontmatter-specification)
2. [Description Writing Workshop](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#2-description-writing-workshop)
3. [Skill Taxonomy — Choosing the Right Pattern](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#3-skill-taxonomy--choosing-the-right-pattern)
4. [Token Budget Guide](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#4-token-budget-guide)
5. [Body Section Reference](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#5-body-section-reference)
6. [Writing Patterns Catalog](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#6-writing-patterns-catalog)
7. [Multi-File Skill Architecture](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#7-multi-file-skill-architecture)
8. [Refactoring an Existing Skill](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#8-refactoring-an-existing-skill)
9. [Skill Evaluation Guide](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#9-skill-evaluation-guide)
10. [Quick Lookup — Common Mistakes & Fixes](https://claude.ai/chat/8d896793-4b1c-48fc-a218-685fcea24a8a#10-quick-lookup--common-mistakes--fixes)

---

## 1. Full Frontmatter Specification

### `name` field

|Rule|Detail|
|---|---|
|Max length|64 characters|
|Allowed characters|Lowercase letters `a–z`, digits `0–9`, hyphens `-`|
|Forbidden|Spaces, uppercase, underscores, dots, XML tags|
|Reserved words|Cannot contain `anthropic` or `claude` anywhere in the string|
|Convention|Use noun-phrase format: `pdf-processing`, `essay-pipeline`, `ml-deployment-engineer`|

**Valid names:**

```
data-analyst
sql-query-builder
react-component-generator
k8s-deployment-helper
```

**Invalid names:**

```
PDF Processing Skill     ← spaces and capitals
claude_assistant         ← underscore, reserved word
my.skill.v2              ← dots
anthropic-helper         ← reserved word
```

### `description` field

|Rule|Detail|
|---|---|
|Min length|1 character (non-empty)|
|Max length|1024 characters|
|Forbidden|XML tags (`<tag>`, `</tag>`)|
|Tone|Imperative — instructs the agent, not describes the skill|
|Must include|What it does AND when to use it|

### YAML formatting notes

- Multi-line descriptions use `|` (literal block) or inline wrapping with indentation
- Keep frontmatter as the very first thing in the file — no blank lines before `---`
- Use `>-` for folded descriptions that should be treated as a single line:

```yaml
---
name: csv-data-analyst
description: >-
  Use this skill when the user wants to analyse, clean, transform, or visualise
  data from CSV files. Also use for pandas workflows, data aggregation, summary
  statistics, and chart generation from tabular data — even if the user doesn't
  say "CSV" or "pandas" explicitly.
---
```

---

## 2. Description Writing Workshop

### The four-part test

A strong description answers all four:

1. **What does it do?** (the capability)
2. **When should the agent use it?** (the trigger conditions)
3. **What user language fires it?** (keywords and phrases)
4. **What adjacent cases should it also cover?** (the "even if" cases)

### Before / after rewrites

**Rewrite 1 — Too mechanical**

```
Before:
"Handles ML model deployment using Docker, Kubernetes, and FastAPI."

After:
"Use this skill when deploying ML models to production, building inference
APIs, or optimising models for serving. Also use for auto-scaling, batch
prediction, edge deployment, and model monitoring — even if the user
doesn't say 'deployment' or 'ML' directly."
```

_What changed:_ Switched from listing tools to describing user goals. Added "even if" coverage for indirect triggers.

**Rewrite 2 — Too vague**

```
Before:
"Helps with writing tasks and documents."

After:
"Use this skill when a user wants help writing, drafting, outlining,
revising, or polishing any essay, article, report, or long-form piece.
Also use when they mention brief, outline, draft, revise, review, or
polish in a writing context — even for short pieces under 500 words."
```

_What changed:_ Named the specific writing stages. Named the artifacts. Included short-piece edge case.

**Rewrite 3 — Misses indirect triggers**

```
Before:
"Use this skill when the user asks about PDF files."

After:
"Use this skill when working with PDF files or when the user mentions
forms, document extraction, merging files, splitting pages, watermarks,
or filling out paperwork — even if they never say 'PDF' explicitly."
```

_What changed:_ Added the downstream intent words (forms, watermarks, paperwork) that appear in user messages before they think to name the file type.

### Description length calibration

|Skill complexity|Recommended description length|
|---|---|
|Single-purpose tool (one task)|1–2 sentences, ~100–150 chars|
|Domain expert (multiple capabilities)|3–4 sentences, ~300–500 chars|
|Multi-step pipeline|4–5 sentences, ~500–700 chars, name each step trigger|

Never pad a description to seem more comprehensive. Every extra word is loaded at agent startup for every conversation. Keep it dense and purposeful.

---

## 3. Skill Taxonomy — Choosing the Right Pattern

There are four recurring skill archetypes. Matching the right pattern to the task saves significant rework.

### Archetype A — Single-Purpose Tool

**Profile:** One task, one workflow, one output format.

**Examples:** `pdf-processing`, `csv-importer`, `image-resizer`

**Characteristics:**

- Short body (500–1500 tokens)
- One primary workflow section
- Decision rules cover format/library choice only
- No routing logic needed

**Template:**

```markdown
# Tool Name

## Requirements
[dependencies]

## Instructions
[single workflow, step-by-step]

## Decision Rules
[if input is X → use Y]

## Pitfalls
[top 2–3 failure modes]
```

---

### Archetype B — Domain Expert

**Profile:** Deep knowledge across many related tasks in one domain.

**Examples:** `ml-deployment-engineer`, `security-auditor`, `database-architect`

**Characteristics:**

- Medium-to-large body (2000–4000 tokens)
- Capabilities map (not a feature list — map each capability to a workflow)
- Performance targets and constraints are explicit
- Anti-patterns section is critical — expert skills are triggered for complex tasks where the agent is most likely to make subtle mistakes

**Template:**

```markdown
# Expert Title

## When to Use / Scope
[explicit in-scope and out-of-scope]

## Core Capabilities
[capability → brief workflow, not just a bullet]

## Performance Targets / Constraints
[concrete numbers, SLAs, thresholds]

## Decision Rules
[how to choose approach given context]

## Examples
[real scenario with inputs and outputs]

## Anti-Patterns
[domain-specific mistakes + corrections]
```

---

### Archetype C — Pipeline Orchestrator

**Profile:** A sequence of steps with shared state, where each step builds on the last.

**Examples:** `essay-pipeline`, `data-cleaning-pipeline`, `release-workflow`

**Characteristics:**

- Master SKILL.md is intentionally thin — it handles routing only
- Step detail lives in `references/steps/` and is loaded on demand
- State is tracked through artifacts (files) the pipeline creates and reads
- Routing logic must be explicit (see Step Routing table pattern)
- Every step ends with a handoff instruction

**Template:**

```markdown
# Pipeline Name

## Pipeline Overview
[visual: Step 1 → Step 2 → ... Step N]

## On Invocation
1. Detect current state (check for artifact files)
2. Present context-aware options to user
3. Load the relevant step file from references/steps/

## Step Routing
| User says | Artifact exists | Load file |
|---|---|---|
| [trigger] | [condition] | steps/X.md |

## Artifact Map
| File | Created by | Read by |
|---|---|---|
| output-brief.md | Step 1 | Steps 2–6 |

## Pipeline Rules
[invariants that apply across all steps]
```

---

### Archetype D — Workflow Automation

**Profile:** Automates a specific repeatable process, often involving scripts, external tools, or file I/O.

**Examples:** `git-release-manager`, `pdf-form-filler`, `batch-image-processor`

**Characteristics:**

- Low freedom — steps are fragile and must be exact
- Plan-validate-execute pattern is almost always appropriate
- Scripts live in `scripts/` and are referenced, not reproduced inline
- Checklists prevent step-skipping

**Template:**

```markdown
# Automation Name

## Prerequisites
[environment, permissions, dependencies]

## Workflow

### Step 1 — Plan
[what to generate, what format, where to save]

### Step 2 — Validate
[run scripts/validate.py; what errors mean; how to fix]

### Step 3 — Execute
[run scripts/execute.py; only after validation passes]

## Checklist
- [ ] Step 1 complete
- [ ] Step 2 passed
- [ ] Step 3 executed

## Pitfalls
[what goes wrong if steps are skipped or reordered]
```

---

## 4. Token Budget Guide

The body should stay under 5,000 tokens. Here's how to estimate and manage spend:

### Rough token estimates

|Content type|Tokens per unit|
|---|---|
|One prose sentence|~15–25 tokens|
|One bullet point|~10–20 tokens|
|One code line|~10–15 tokens|
|10-row markdown table|~80–120 tokens|
|One full code block (20 lines)|~200–300 tokens|

### Budget allocation by archetype

|Archetype|Prose|Code|Tables|Headings/structure|
|---|---|---|---|---|
|Single-Purpose Tool|~300|~400|~100|~100|
|Domain Expert|~800|~600|~300|~200|
|Pipeline Orchestrator|~600|~200|~300|~200|
|Workflow Automation|~400|~800|~200|~150|

### What to cut when over budget

Priority order for cuts:

1. **Explanations of things the agent already knows.** These are pure waste — identify them with the "Would the agent get this wrong?" test.
2. **Redundant examples.** One good example beats two mediocre ones. Cut the weaker example, not both.
3. **Over-specified decision rules.** If a decision rule describes a case that never comes up in practice, remove it.
4. **Long introductory prose.** Agents don't need context-setting paragraphs. Start with the first actionable instruction.
5. **Verbose code comments.** Comments in code snippets should only explain the non-obvious. Remove anything that restates what the code clearly shows.

### What to move to references/ when over budget

Move to supplementary files (not cut entirely) when content is:

- Needed occasionally but not every time the skill fires
- A deep-dive extension of a summary in the main body
- A long template or script that would bloat the always-loaded context

---

## 5. Body Section Reference

A catalogue of every named section, what it should contain, and when to include it.

### `## When to Use` / `## Scope`

**Include when:** The skill's domain overlaps with adjacent skills, or when the user might trigger this skill for tasks it shouldn't handle. **Content:** 2–4 sentences max. State what's in scope, then explicitly state what's out of scope. **Anti-pattern:** Repeating the frontmatter description verbatim — the body scope should be _more specific_, not a copy.

### `## Requirements`

**Include when:** The skill needs libraries, environment variables, permissions, or external tools that aren't universally available. **Content:** Exact install commands, minimum versions if they matter, environment setup steps. **Anti-pattern:** Listing every transitive dependency — only list what the agent needs to explicitly install or configure.

### `## Instructions`

**Include when:** Always — this is the core of the skill. **Content:** Numbered, ordered steps for each workflow. One subsection per distinct workflow. Use `###` subheadings. **Anti-pattern:** Unnumbered prose paragraphs for ordered processes — agents skip steps when order isn't explicit.

### `## Decision Rules`

**Include when:** There are multiple valid approaches and the agent needs criteria to choose between them. **Content:** Plain-language if/then statements. One condition per rule. Keep each rule to one line if possible. **Anti-pattern:** Decision rules that are actually just capability listings ("if user wants text extraction, use pdfplumber" — this belongs in Instructions, not Decision Rules, if it's the only option).

### `## Output Format` / `## Templates`

**Include when:** The skill produces structured output (reports, configs, code files) and format consistency matters. **Content:** Literal template with placeholders. Use `[PLACEHOLDER]` syntax for things the agent fills in. **Anti-pattern:** Describing the format in prose instead of showing it — agents pattern-match against templates far more reliably than they follow format descriptions.

### `## Examples`

**Include when:** Always for non-trivial skills. The more complex the skill, the more examples matter. **Content:** Real scenario → real input → real output. Use actual file names, variable names, and metric values. Avoid "example_input" and "sample_data" as placeholder names. **Anti-pattern:** Abstract examples ("User asks to process a document → agent processes the document") — these teach nothing.

### `## Edge Cases`

**Include when:** There are non-obvious situations that would cause the agent to apply the wrong approach. **Content:** Named scenarios with explicit handling instructions. Format: "If [condition] → [do this instead]." **Anti-pattern:** Listing every possible edge case — focus on the ones the agent would actually get wrong.

### `## Pitfalls`

**Include when:** Always — even simple skills have at least one or two. **Content:** Specific mistakes + why they happen + what to do instead. Be concrete: "Never use X because Y; use Z instead." **Anti-pattern:** Generic warnings like "Be careful with edge cases" — this is noise.

### `## Anti-Patterns` (variant of Pitfalls for expert skills)

**Include when:** The skill covers a domain where there are well-known bad practices that developers commonly reach for. **Content:** Named anti-pattern → why it's harmful → the correct alternative. **Anti-pattern:** Listing anti-patterns without explaining the correct replacement — agents need the corrective action, not just the prohibition.

---

## 6. Writing Patterns Catalog

Reusable structural patterns for common situations.

### Pattern: The Routing Table

Use in pipeline and orchestrator skills where the agent must choose which sub-file to load.

```markdown
## Step Routing

| User says | Condition | Action |
|---|---|---|
| "brief" or starting fresh | No artifacts exist | Load steps/brief.md |
| "outline" | brief.md exists | Load steps/outline.md |
| "draft" | outline.md exists | Load steps/draft.md |
| "revise" / "edit" | draft.md exists | Load steps/revise.md |
| Any step | Named explicitly | Load that step regardless of state |
```

### Pattern: The Artifact Map

Use when a pipeline produces files that downstream steps depend on.

```markdown
## Artifact Map

| File | Created by | Expected by | Contents |
|---|---|---|---|
| `essay-brief.md` | Step 1: Brief | All steps | Voice, tone, constraints, goal |
| `essay-outline.md` | Step 2: Outline | Step 3: Draft | Section headers and key points |
| `essay-draft.md` | Step 3: Draft | Steps 4–6 | Full draft text |
```

### Pattern: The Decision Tree

Use when the right approach depends on multiple chained conditions.

```markdown
## Which tool to use

1. Is the PDF scanned (image-based)?
   - Yes → use `pdf2image` + `pytesseract` (OCR)
   - No → continue to 2

2. Do you need tables?
   - Yes → use `pdfplumber`
   - No → continue to 3

3. Do you need to preserve layout/columns?
   - Yes → use `pdfplumber` with layout mode
   - No → use `pypdf` (fastest)
```

### Pattern: The Performance Contract

Use in infrastructure and system skills to make targets explicit.

```markdown
## Performance Targets

| Metric | Minimum | Target | Alert threshold |
|---|---|---|---|
| P99 API latency | < 200ms | < 50ms | > 150ms |
| Throughput | 500 RPS | 2000 RPS | < 400 RPS |
| Availability | 99.9% | 99.99% | < 99.9% |
| Error rate | < 1% | < 0.1% | > 0.5% |
```

### Pattern: The Handoff Block

Use at the end of every step in a pipeline skill to prevent the pipeline from stalling.

```markdown
---
**Step complete.** Your outline is saved to `essay-outline.md`.

**What's next:**
→ **Draft** — write the full first draft using this outline (recommended)
→ **Revise the outline** — if something feels off before you write

Tell me which to do, or type a step name: `brief` · `outline` · `draft` · `revise` · `review` · `polish`
```

### Pattern: The Validation Loop

Use for any operation where the agent's output needs to be checked before proceeding.

```markdown
## Validation loop

1. Generate output
2. Run validation: `python scripts/validate.py output/`
3. Review errors:
   - `MISSING_FIELD: X` → add field X to the input data
   - `TYPE_MISMATCH: X` → check expected type in schema.json
   - `DUPLICATE_KEY: X` → deduplicate before re-running
4. Fix issues and return to step 1
5. Proceed only when validation exits with code 0
```

---

## 7. Multi-File Skill Architecture

When a skill's total content exceeds the 5,000-token body budget, split it across files.

### Folder layout options

**Option A — References folder (most common)**

```text
skill-name/
├── SKILL.md                    ← routing + core instructions (~2000 tokens)
└── references/
    ├── ADVANCED.md             ← deep-dive content loaded on demand
    ├── TROUBLESHOOTING.md      ← error handling loaded when things go wrong
    └── EXAMPLES.md             ← extended examples loaded when needed
```

**Option B — Steps folder (pipeline skills)**

```text
essay-pipeline/
├── SKILL.md                    ← pipeline overview + routing only
└── references/
    └── steps/
        ├── brief.md
        ├── outline.md
        ├── draft.md
        ├── revise.md
        ├── review.md
        └── polish.md
```

**Option C — Scripts + assets (automation skills)**

```text
pdf-form-filler/
├── SKILL.md
├── scripts/
│   ├── analyze_form.py
│   ├── validate_fields.py
│   └── fill_form.py
└── assets/
    └── field_type_schema.json
```

### How to link to supplementary files in the body

Always tell the agent explicitly when to load a supplementary file:

```markdown
## Form filling

For basic form filling, follow the instructions below.
For complex forms with conditional fields or signature blocks, load
`references/ADVANCED.md` and follow the advanced workflow instead.

### Basic form filling
[instructions here]
```

Don't just put a link and hope the agent reads it. State the condition that triggers loading it.

### What goes where

|Content type|Location|
|---|---|
|Routing logic and core workflow|SKILL.md body|
|Step detail for pipeline stages|references/steps/|
|Error messages and fixes|references/TROUBLESHOOTING.md|
|Extended examples|references/EXAMPLES.md|
|Deep-dive for advanced cases|references/ADVANCED.md|
|Deterministic executable code|scripts/|
|Output templates (long)|assets/|
|Output templates (short, < 30 lines)|Inline in SKILL.md|

---

## 8. Refactoring an Existing Skill

When asked to improve an existing skill, diagnose before rewriting.

### Diagnostic checklist

Run through these checks in order:

**Layer 1 — Frontmatter problems (highest impact)**

- [ ] Does the description use imperative phrasing ("Use this skill when...")?
- [ ] Does the description describe user intent or tool mechanics?
- [ ] Would this description fire on all the ways a user might phrase the request?
- [ ] Is the name lowercase, hyphens only, no reserved words?

**Layer 2 — Body structure problems**

- [ ] Is there a scope section? Does it say what the skill is NOT for?
- [ ] Are workflows written as ordered steps or as prose paragraphs?
- [ ] Are there if/then decision rules, or does the agent have to guess?
- [ ] Is there at least one concrete example?
- [ ] Is there a pitfalls section?

**Layer 3 — Content quality problems**

- [ ] Does any section explain things the agent already knows?
- [ ] Are examples abstract or concrete?
- [ ] Are the pitfalls specific ("Never use X because Y") or generic ("Be careful")?
- [ ] Is the body over 5,000 tokens? If so, what can move to references/?

### Common refactor patterns

**Problem:** Description is passive

```
Before: "This skill is for working with CSV files and data analysis."
After:  "Use this skill when analysing, cleaning, or transforming CSV data,
         or when the user mentions pandas, dataframes, or tabular analysis."
```

**Problem:** Instructions are a feature list, not a workflow

```
Before:
## Features
- Merge PDFs
- Split PDFs
- Extract text
- Add watermarks

After:
## Instructions

### To merge PDFs
1. Collect input file paths as a list
2. Use PdfWriter to add each page [code snippet]
3. Write output to merged.pdf

### To extract text
[step-by-step...]
```

**Problem:** Missing decision rules

```
Before: [no decision rules section — agent picks library by chance]

After:
## Decision Rules
- Input is text-based PDF → pdfplumber
- Input is scanned/image PDF → pdf2image + pytesseract
- Need to create new PDF from scratch → reportlab
- Need to fill an existing form → see references/FORMS.md
```

**Problem:** Pitfalls are vague

```
Before: "Be careful with edge cases when processing PDFs."

After:
## Pitfalls
- Never use Unicode subscripts (₀₁₂) in reportlab — they render as black boxes.
  Use XML `<sub>` tags inside Paragraph objects instead.
- pypdf.extract_text() returns empty string for scanned PDFs — check for this
  before reporting "no text found"; the PDF may need OCR instead.
```

---

## 9. Skill Evaluation Guide

Before shipping a skill, test it against these three scenarios.

### Test 1 — Trigger accuracy

Ask the agent five different ways a user might phrase the request this skill covers. The skill should fire on all five. If it misses, the description needs broader trigger language.

Example for a CSV skill:

```
✓ "Can you analyse this CSV file for me?"
✓ "I have a spreadsheet with sales data I need to summarise"
✓ "Help me clean this pandas dataframe"
✓ "There's a TSV file I need to filter"
✓ "I need some charts from this tabular data"   ← skill should still fire
```

### Test 2 — Boundary accuracy

Ask something adjacent but outside the skill's scope. The skill should NOT fire.

```
CSV skill should NOT fire for:
✗ "Can you help me with this Excel file?" (→ xlsx skill)
✗ "I need to query my SQL database" (→ sql skill)
✗ "Here's a JSON file I need to parse" (→ general coding)
```

If the skill fires on out-of-scope requests, make the description more exclusive and add an explicit scope boundary in the body.

### Test 3 — Output quality

Run the skill on a representative real task. Check:

1. Did the agent follow the step-by-step instructions in order?
2. Did the agent apply the correct decision rule for the input?
3. Did the output match the template (if one was provided)?
4. Did any of the documented pitfalls occur anyway?

If pitfalls still occur after documentation, the pitfall description needs to be more specific and placed closer to the relevant instruction rather than in a separate section at the end.

---

## 10. Quick Lookup — Common Mistakes & Fixes

|Mistake|Symptom|Fix|
|---|---|---|
|Description describes mechanics, not intent|Skill doesn't trigger when user phrases request naturally|Rewrite to "Use this skill when [user wants to]..."|
|Body explains what agent already knows|Skill fires but produces generic output|Delete anything the agent would write correctly without the skill|
|No if/then decision rules|Agent picks a tool or approach inconsistently|Add a Decision Rules section with explicit conditions|
|No concrete examples|Agent follows structure but produces wrong output|Add one real example with real variable names and outputs|
|Pitfalls are vague|Agent repeats known mistakes despite pitfalls section|Make each pitfall specific: "Never X because Y; use Z instead"|
|Body over 5,000 tokens|Skill loads but eats context budget|Split into SKILL.md + references/ files|
|Two skills with overlapping descriptions|Wrong skill fires|Add explicit "Not for: X" line to each skill's scope section|
|Pipeline step ends without handoff|User doesn't know what to do next|Add a Handoff block at the end of every step|
|Missing scope section|Skill applied to tasks it wasn't designed for|Add "## When to Use" with explicit in-scope and out-of-scope|
|Template described in prose|Agent produces inconsistently formatted output|Replace prose description with a literal template using `[PLACEHOLDER]`|