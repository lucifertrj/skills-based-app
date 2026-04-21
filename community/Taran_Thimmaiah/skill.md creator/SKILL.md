---
name: skill-md-creator
description: Use this skill when the user wants to create, write, improve, or review a SKILL.md file for an AI agent. Triggers include any mention of "skill file", "skill.md", "agent skill", "writing a skill", "creating a skill", or requests to turn a workflow, domain expertise, or tool into a reusable agent skill. Also use when the user wants to convert existing documentation, notes, or conversation history into a structured skill, or when they want to evaluate or refactor a skill they already have.
---

# Skill.md Creator

## Scope & Boundaries

This skill applies when the goal is to produce a `SKILL.md` file — the instruction layer that tells an AI agent *when* and *how* to do something. It is **not** for building the underlying tools, scripts, or APIs the skill references. Focus exclusively on writing the skill file itself: frontmatter, structure, content quality, and bundled resource layout.

---

## What a SKILL.md Is

A `SKILL.md` is a two-layer document:

- **Layer 1 — Frontmatter (always loaded, ~100 tokens):** YAML metadata that lets the agent discover the skill and decide when to use it.
- **Layer 2 — Body (loaded on trigger, target < 5,000 tokens):** Procedural knowledge — workflows, decision rules, examples, and guardrails — that the agent reads only when the skill fires.

The frontmatter is the signal. The body is the expertise. Both must be written with care.

### File & Folder Layout

```text
skill-name/
├── SKILL.md              ← required
└── (optional)
    ├── scripts/          ← deterministic/repetitive executable code
    ├── references/       ← supplementary docs loaded into context on demand
    └── assets/           ← output templates, icons, fonts
```

---

## Step-by-Step Instructions

### Step 1 — Gather Context

Before writing a single line, ask the user (or infer from the conversation):

1. **What does this skill do?** What task, domain, or workflow does it cover?
2. **Who triggers it?** What does a user say or ask when this skill should fire?
3. **What does the agent need to know that it wouldn't know by default?** Project conventions, non-obvious tool choices, domain-specific sequences.
4. **Are there hard constraints?** Things the agent must never do, or must always do in a specific order.
5. **Are there bundled resources?** Scripts, templates, or reference docs to include.

If the user has provided existing notes, a conversation transcript, or example outputs, extract the reusable pattern from those rather than asking from scratch.

---

### Step 2 — Write the Frontmatter

**`name` field rules:**
- Max 64 characters
- Lowercase letters, numbers, and hyphens only
- No XML tags
- No reserved words: `anthropic`, `claude`

**`description` field rules:**
- Non-empty, max 1024 characters
- No XML tags
- Must cover both *what the skill does* and *when the agent should use it*

**Principles for a strong description:**

| Principle | Explanation |
|---|---|
| Imperative phrasing | Start with "Use this skill when…" not "This skill does…" |
| User intent, not mechanics | Describe what the user is trying to achieve |
| Be pushy | List edge cases where the skill applies even if the user doesn't name the domain explicitly |
| Stay concise | A few sentences is ideal — don't bloat the always-loaded system prompt |

**Good example:**
```yaml
---
name: pdf-processing
description: Use this skill when working with PDF files or when the user mentions
  PDFs, forms, document extraction, merging, splitting, or filling forms — even
  if they don't say "PDF" directly. Covers text extraction, table extraction,
  form filling, merging, splitting, watermarking, and creating new PDFs.
---
```

**Bad example:**
```yaml
---
name: PDF Processing Skill
description: This skill handles PDF files using Python libraries like pypdf and pdfplumber.
---
```
*Why it's bad:* Name has spaces and capitals; description describes mechanics not user intent; not imperative; too vague to trigger reliably.

---

### Step 3 — Write the Body

Structure the body using these sections, adapting as needed:

```markdown
# Skill Title

## When to Use
[Explicit scope — what this skill is and isn't for]

## Requirements
[Libraries, environment setup, permissions, or prerequisites]

## Instructions
[Step-by-step workflows. Use numbered lists for ordered sequences.]

## Decision Rules
[If/then logic for choosing between approaches]

## Output Format / Templates
[Concrete templates the agent should pattern-match against]

## Examples
[Real, specific examples — not abstract descriptions]

## Edge Cases
[Non-obvious scenarios the agent would likely get wrong]

## Pitfalls
[What NOT to do — unsupported actions, known failure modes, anti-patterns]
```

Not every section is required for every skill. Use the sections that add value; omit the ones that don't.

---

### Step 4 — Apply Content Quality Rules

#### Write what the agent lacks, omit what it knows

Ask for every piece of content: *"Would the agent get this wrong without this instruction?"*

```markdown
<!-- ❌ Too verbose — agent already knows what a REST API is -->
## Make an API call
A REST API allows you to send HTTP requests to a server. You'll need to use
the requests library in Python to send GET or POST requests...

<!-- ✅ Better — jumps to what the agent wouldn't know on its own -->
## Make an API call
Always use the internal `api_client.py` wrapper, not raw `requests`.
It handles auth token refresh automatically.
```

#### Set the right degree of freedom

Match specificity to the task's fragility:

| Task type | Freedom level | Format |
|---|---|---|
| Creative, context-dependent | High | Plain prose instructions |
| Preferred pattern exists, some variation OK | Medium | Pseudocode or parameterized script |
| Fragile, must be exact, order matters | Low | Exact command, no parameters |

**High freedom example (essay review):**
```markdown
## Review process
1. Read the full draft before commenting
2. Identify the core argument and test whether every section serves it
3. Flag sections that repeat, contradict, or wander
4. Suggest specific cuts, not just "tighten this"
```

**Low freedom example (database migration):**
```markdown
## Run migration
Execute exactly:
```bash
python scripts/migrate.py --verify --backup
```
Do not add flags. Do not run in parallel. Do not skip `--backup`.
```

#### Use checklists for multi-step workflows

When steps have dependencies or validation gates, a checklist prevents skipping:

```markdown
## Deployment checklist
- [ ] Step 1: Run unit tests (`pytest tests/`)
- [ ] Step 2: Build Docker image (`docker build -t model:latest .`)
- [ ] Step 3: Validate config (`python scripts/validate_config.py`)
- [ ] Step 4: Deploy to staging (`./deploy.sh staging`)
- [ ] Step 5: Smoke test (`python scripts/smoke_test.py staging`)
- [ ] Step 6: Deploy to production (only after Step 5 passes)
```

#### Use plan-validate-execute for destructive operations

```markdown
## Batch file rename
1. Generate rename plan → `rename_plan.json` (list of old→new pairs)
2. Validate: check for name collisions, forbidden characters, duplicate targets
3. If validation fails, revise the plan and re-validate
4. Execute only after validation passes: `python scripts/rename.py rename_plan.json`
```

---

### Step 5 — Self-Check Before Delivering

Run through this checklist before handing the skill to the user:

```
Frontmatter
- [ ] name: lowercase, hyphens only, ≤64 chars, no reserved words
- [ ] description: imperative phrasing, user intent, ≤1024 chars, no XML tags
- [ ] description covers BOTH what it does AND when to use it

Body
- [ ] Scope section is explicit — says what the skill is NOT for
- [ ] Each workflow is step-by-step, not feature-list prose
- [ ] If/then decision rules exist wherever multiple approaches are valid
- [ ] At least one concrete example exists
- [ ] Pitfalls section covers the top 2–3 ways the agent would go wrong
- [ ] No content that explains things the agent already knows
- [ ] Body is under 5,000 tokens (estimate: 1 token ≈ 4 characters)

Optional but recommended
- [ ] Checklists used for any workflow with 4+ ordered steps
- [ ] Output templates provided for any structured output requirement
- [ ] Bundled resources (scripts/, references/, assets/) referenced if relevant
```

---

## Decision Rules

**If the user provides existing documentation or notes →** extract the reusable pattern; don't ask them to repeat information they've already given.

**If the user's skill is too long (>5,000 tokens in the body) →** split into a primary SKILL.md and supplementary files in `references/`, linked from the body.

**If the user wants to improve an existing skill →** read it first, then identify which of these four problems it has:
1. Description too vague → agent won't trigger correctly
2. Body explains what agent already knows → wasteful, adds noise
3. Missing if/then rules → agent guesses instead of choosing
4. No pitfalls section → agent repeats known failure modes

**If the skill involves a multi-step pipeline (like an essay workflow) →** recommend routing logic in the main SKILL.md with step detail offloaded to `steps/` files in `references/`. This keeps the always-loaded layer small.

---

## Examples

### Example 1 — Minimal Skill (single-purpose tool)

```markdown
---
name: pdf-processing
description: Use this skill when working with PDF files or when the user mentions
  PDFs, forms, extraction, merging, or splitting — even if they don't say "PDF"
  explicitly. Covers text extraction, table extraction, form filling, merging,
  splitting, watermarking, and PDF creation.
---

# PDF Processing

## Requirements
```bash
pip install pypdf pdfplumber reportlab
```

## Instructions

### Extract text
Use `pdfplumber` for text and tables. Fall back to `pytesseract` for scanned PDFs.

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader
writer = PdfWriter()
for path in ["a.pdf", "b.pdf"]:
    for page in PdfReader(path).pages:
        writer.add_page(page)
with open("merged.pdf", "wb") as f:
    writer.write(f)
```

## Decision Rules
- Text PDF → pdfplumber
- Scanned PDF → pdf2image + pytesseract
- Create new PDF → reportlab
- Fill existing form → see references/FORMS.md

## Pitfalls
- Never use Unicode subscript characters (₀₁₂) in reportlab — use `<sub>` XML tags instead; Unicode glyphs render as black boxes
- pypdf cannot reliably extract text from scanned PDFs — always check if OCR is needed first
```

---

### Example 2 — Pipeline Skill (multi-step orchestration)

See the Essay Pipeline pattern: a master SKILL.md handles routing and artifact detection, while each step's detail lives in `steps/brief.md`, `steps/outline.md`, etc. The master file stays small; step files are loaded only when needed.

```markdown
---
name: essay-pipeline
description: Use this skill when a user wants help writing, drafting, outlining,
  or editing an essay, article, long-form piece, or any structured written work.
  Also use when they mention "brief", "outline", "draft", "revise", "review",
  or "polish" in a writing context.
---

# Essay Pipeline

## Pipeline Overview
```
Step 1: Brief   → Capture essay DNA
Step 2: Outline → Design structure
Step 3: Draft   → Write first draft
Step 4: Revise  → Surgical section edits
Step 5: Review  → Editorial diagnostic
Step 6: Polish  → Final pass
```

## On Invocation

1. Check for existing artifacts: `essay-brief.md`, `essay-outline.md`, `essay-draft.md`
2. Present context-aware next step options to the user
3. Load the relevant step file from `steps/` and follow it exactly

## Step Routing
| User says | Load file |
|---|---|
| brief / starting fresh | steps/brief.md |
| outline | steps/outline.md |
| draft | steps/draft.md |
| revise | steps/revise.md |
| review | steps/review.md |
| polish | steps/polish.md |

## Rules
- Always check for existing artifacts before starting — never make the user repeat work
- The brief is the constitution — every downstream step must honour it
- After each step, tell the user what to do next — never just end
- Be honest in Review and Polish — the author deserves candour, not flattery
```

---

### Example 3 — Domain Expert Skill (deep technical knowledge)

See the ML Engineer pattern: a large skill with many capabilities is best organised with a clear **When to Use** boundary, a **Core Capabilities** map, concrete **Examples** with metrics, and a dedicated **Anti-Patterns** section to counteract common mistakes.

```markdown
---
name: ml-deployment-engineer
description: Use this skill when deploying ML models to production, building
  inference APIs, optimising models for serving, setting up auto-scaling, or
  designing batch prediction systems. Also use for edge deployment, multi-model
  serving, A/B testing infrastructure, and model monitoring — even if the user
  doesn't use the words "ML" or "deployment" directly.
---

# ML Deployment Engineer

## When to Use
Production ML serving and inference infrastructure only.
Not for: model training, data pipelines, or general software engineering.

## Core Capabilities
- Model optimisation: quantisation (FP32→INT8), pruning, ONNX conversion
- Serving: FastAPI/gRPC endpoints, request batching, caching
- Infrastructure: Kubernetes, HPA, load balancers, health checks
- Monitoring: latency (P50/P95/P99), error rates, data drift detection
- Edge: CoreML (iOS), TFLite (Android), delta update mechanisms

## Performance Targets
| Metric | Target |
|---|---|
| P99 latency | < 100ms (real-time), < 50ms (critical path) |
| Availability | 99.9% minimum |
| Scale range | 2–50 pods (HPA) |

## Anti-Patterns
- Manual deployment without CI/CD → always automate model validation before deploy
- No model versioning → always maintain version history with rollback capability
- Optimising beyond practical benefit → focus on customer-impacting latency, not benchmarks
- No load testing before production → always test with production-like traffic patterns
```

---

## Edge Cases

- **Skill about a skill:** This very file is an example — it is self-referential. When the skill's subject matter is meta (prompting, skill writing, agent configuration), be extra precise about scope to prevent the agent from applying it too broadly.
- **Very short skills:** A skill with a one-sentence body is usually too thin. If the agent already handles the task well without a skill, the skill adds noise. Test before shipping.
- **Very long skills:** If the body exceeds 5,000 tokens, the agent's context fills up fast. Split: keep routing and decision logic in SKILL.md, move deep reference content to `references/` files loaded on demand.
- **Overlapping skills:** If two skills have similar descriptions, the agent may fire the wrong one. Make descriptions mutually exclusive — specify what each skill is *not* for.
- **Pipeline skills with shared state:** If steps depend on artifacts from prior steps, document the artifact names and what each step expects to find vs. create. Ambiguity here breaks pipelines silently.

---

## Pitfalls

- **Describing features instead of workflows:** "This skill supports quantisation, pruning, and ONNX export" tells the agent nothing actionable. "To reduce model size: first try FP16, then INT8, validate accuracy after each step" is actionable.
- **Explaining what the agent already knows:** Definitions, general programming concepts, well-known library basics — cut them. Every token in the body costs context window space.
- **Vague descriptions that don't trigger:** Descriptions like "helps with documents" won't fire reliably. Be specific about user language, task types, and edge-case phrasings.
- **Missing pitfalls section:** This is the highest-leverage section. The agent will make the exact mistakes you don't document.
- **No concrete examples:** Abstract guidance degrades agent performance. One specific example with real variable names, real file paths, or real metrics is worth five paragraphs of prose.
- **Forgetting handoffs in pipeline skills:** If the agent completes a step and doesn't tell the user what to do next, the pipeline stalls. Every step must end with a forward-pointing instruction.
