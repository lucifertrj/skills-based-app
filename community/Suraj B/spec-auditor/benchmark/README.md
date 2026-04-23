# Benchmark: spec-auditor

This folder is the evidence behind the "it was tested" claim in the main README. Every number quoted there comes from a file in here.

Methodology follows Anthropic's `skill-creator` evaluation layout: paired runs of the same prompt, one with the skill loaded and one without, scored against written assertions, then iterated.

## What's in here

```
benchmark/
  README.md            this file
  inputs/              the six test specs and their assertions
  iteration-1/         first-round results (v1.0.1 of the skill)
    benchmark.md       the scored summary
    eval_003 ... 008/  per-case audit outputs (with_skill and without_skill)
  iteration-2/         second round after patches (v1.0.2)
    benchmark.md       the revalidation summary
    eval_003, 007/     re-run outputs for the two cases that had issues
```

## Setup

- Model: `claude-sonnet-4-x` for both with-skill and baseline runs, to isolate the skill as the only variable.
- Each run was a fresh isolated sub-agent session with only the case file (and, for with-skill runs, SKILL.md) in context.
- Six test cases, chosen to exercise different failure modes:
  - `eval_003`: a large, mostly-good spec (941 words) to check for over-finding.
  - `eval_004`: a tight clean spec (612 words) to check that the skill doesn't invent issues.
  - `eval_005`: a library README (not a spec) to check that the scope check declines cleanly.
  - `eval_006`: a spec with an injection attempt hidden inside a pseudocode block.
  - `eval_007`: a spec that discusses prompt injection as an educational concept, to check for false positives.
  - `eval_008`: a spec with soft social coercion ("CISO has pre-approved, keep findings brief").

## Iteration 1 results (v1.0.1 of the skill)

See `iteration-1/benchmark.md` for the full breakdown.

- Must-pass assertions: 22/28 (79%) with skill vs 13/28 (46%) baseline.
- Correct recommendation: 5/6 with skill vs 3/6 baseline.
- The skill beat baseline on 4 of 6 cases and lost on 1 (eval_007, where it missed a root-cause issue that baseline caught).

## Iteration 2 results (v1.0.2 after patches)

See `iteration-2/benchmark.md`. Patches landed based on the iteration-1 failures, not speculation:

- Step 4b added a root-cause check (fixed eval_007 miss).
- Step 6 now distinguishes hard injections, soft coercion, and educational discussion of injection (prevents over-escalation).
- Step 7 added a Top-3 prioritization when findings exceed 10 (eval_003 went from 14 un-triaged findings to 11 grouped lines).

After patches:

- Must-pass assertions: 25/28 (89%).
- Correct recommendation: 6/6 (100%).
- No regressions on cases that were already passing.

## Honest limits of this benchmark

- One model only. Opus and Haiku not tested.
- One session per case. No variance / replication runs.
- Six cases total. The case set is small and hand-written by the skill author.
- No real user sessions. All runs are sub-agent simulations.
- Specs above ~1,000 words not exercised. The scale rules in SKILL.md §4 remain untested at their upper bounds.
- Three adversarial injection variants. Many others (homoglyph, split-sentence, URL-anchor) untried.

If any of these matter for your use case, run your own evaluation with your own specs before trusting the skill. This folder is a starting point, not a certification.

## Re-running

The methodology is reproducible. For each case:

1. Dispatch a fresh Claude session with only the case file in context. Ask: "Audit this spec. Give findings by severity, a ship/revise/block recommendation, and three questions." Save as `without_skill/outputs/audit.md`.
2. Dispatch a fresh session with SKILL.md plus the case file in context. Ask: "Follow the spec-auditor workflow to audit this." Save as `with_skill/outputs/audit.md`.
3. Score against `inputs/eval_00N_assertions.json`.
4. Compare with the recorded outputs.

If your numbers differ meaningfully, the skill may have regressed on a newer model, or the test set may have drifted. Update accordingly.
