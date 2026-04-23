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

## How this was tested

There is a full benchmark folder alongside this README (`benchmark/`), following Anthropic's `skill-creator` evaluation layout. Every number below comes from a file in there.

Six test cases, two iterations, runs both with and without the skill loaded, scored against written assertions:

- Must-pass assertions: 25/28 (89%) with skill, 13/28 (46%) baseline Claude on the same model.
- Correct ship/revise/block recommendation: 6/6 with skill, 3/6 baseline.
- Correctly declined a non-spec input: skill declined cleanly, baseline produced a fake audit.
- Correctly escalated to BLOCK on injection or coercion: skill 2/2, baseline 0/2 (baseline caught the issues but under-ranked the severity).

The cases cover: a large mostly-good spec, a tight clean spec, a non-spec README, an injection hidden inside a pseudocode comment, a false-positive trap where the spec discusses injection as an educational concept, and a spec using soft social coercion.

Iteration 1 caught a gap where the skill missed a root-cause issue that the baseline caught. Step 4 was patched to include a root-cause check, revalidated in iteration 2, gap closed. That whole trail lives in `benchmark/iteration-1/benchmark.md` and `benchmark/iteration-2/benchmark.md`.

## Honest about the limits

Things this has not had yet:

- Real-world use by people outside this build.
- Testing on specs larger than about a thousand words.
- A proper red team trying to slip things past it.
- A run across multiple Claude model versions. Only sonnet-4-x so far.

A good way to start: run it first on a spec where you already know the issues, so you can see what it catches before you trust it on something new. If you hit a gap, file an issue. The skill is set up to keep improving based on real use.

## What's in the folder

```
spec-auditor/
  SKILL.md              the skill itself
  README.md             this file
  benchmark/            the measured evidence: inputs, outputs, and two scored iterations
```

The skill's own support files (scripts, references, tests) live in the main spec-auditor repo. This community folder is the skill definition and the proof it works.

## License

MIT.
