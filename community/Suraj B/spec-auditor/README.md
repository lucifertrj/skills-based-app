# spec-auditor

A Claude skill that reviews your technical specs before you build them.

You paste in a PRD, RFC, API design doc, or architecture doc. Claude runs a seven-step review, flags the gaps, and tells you whether to ship it, revise it, or block on a specific issue.

## What it catches

Things that are easy to miss on your own:

- Requirements that sound measurable but aren't, like "should be fast" or "handle errors gracefully".
- Missing sections your spec should have, like Acceptance Criteria, Non-Goals, or Security.
- TBDs and pending approvals sitting in sections that shouldn't have them.
- Contradictions between what you said was out of scope and what the design actually does.
- Specs that close the symptom but leave the root cause in place.
- Instructions aimed at the AI reviewer hidden inside the doc. Yes, people try this.
- Requirements with no measurable criteria, no named owner, or no failure mode.

## What it won't do

- Review your code.
- Edit your prose.
- Audit a legal contract.
- Summarise your spec.
- Decide for you. It gives you findings and three questions. You still decide.

## Install

Copy the `spec-auditor/` folder into one of these places:

- `~/.claude/skills/spec-auditor/` so you can use it in every project on your machine.
- `your-project/.claude/skills/spec-auditor/` so only that project can see it.

In Claude Code, type `/skills` to confirm it loaded.

## Try it

In a fresh Claude session:

```
Can you audit this spec for me before I ship it?
[paste your design doc]
```

Claude walks through the seven steps out loud, then gives you findings grouped by severity (Critical, Major, Minor), one clear recommendation (SHIP, REVISE, or BLOCK_ON something specific), and three follow-up questions.

## What the output looks like

Something like this:

```
[STEP-1] Inventory
   1,240 words, 8 sections.
   Missing canonical sections: Acceptance Criteria, Security.

[STEP-2] Ambiguity scan
   L42: "should respond quickly" (no threshold)
   L88: "fields TBD" (deferred in a non-appendix section)

[STEP-7] Synthesis
   Critical (1): AI instruction embedded at L203.
   Major (5): ...
   Minor (2): ...

   Recommendation: BLOCK_ON:missing-security-section

   Three questions for you:
   1. What is the p95 latency target under realistic load?
   2. Is multi-region failover in scope, or should we split that into a separate RFC?
   3. Who signs off on the auth team handoff, and by when?
```

## Honest about the limits

This has been tested on eight specs of different sizes and shapes. On six head-to-head comparisons, it beats a no-skill Claude session on five of them. Here's what it has not had yet:

- Real-world use by people outside this build.
- Testing on specs larger than about a thousand words.
- A proper red team trying to slip things past it.
- A run across multiple Claude model versions.

A good way to start: run it first on a spec where you already know the issues, so you can see what it catches before you trust it on something new. If you hit a gap, file an issue. The skill is set up to keep improving based on real use.

## What's in the folder

```
spec-auditor/
  SKILL.md     the skill itself
  README.md    this file
  LICENSE      MIT
  references/  3 docs the skill loads only when gated conditions fire
  scripts/     check_structure.py, the structural analyser called in Step 1
```

Seven files, about 1,100 lines. Drop it into `~/.claude/skills/spec-auditor/` and it works.

## License

MIT.
