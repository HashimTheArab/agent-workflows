---
name: delivery-loop
description: Use when diagnosing a bug, implementing a fix or feature, or changing executable behavior, through to a reviewed, ready pull request.
---

# Delivery Loop

One problem, cut small, built small, reviewed a fixed number of times. Repo rules (gate commands, device checks,
rollout, merge rights) and the owner's global rules win where they say more.

## Rules

These lines are synced into repo `AGENTS.md` files by `scripts/agents_block.py`. Edit them only here.

<!-- agents-block:start -->
- Delivery follows the `delivery-loop` skill (engineering-workflows). This repo's own rules add gates, device checks and rollout.
- Before code: at most 5 checkable done lines and a size budget (lines, files, new concepts). Only the owner's own words settle a product decision.
- A PR under review takes no new behavior. A new decision, second fix or new event becomes a new issue and PR.
- Risky change: two blind design sketches; build the smaller one that meets the done lines.
- A fix's test fails on the old code. The change deletes what it replaces.
- Before bug review of a change that is not small and low-risk, a fresh reviewer sees only the done lines and the diff. Smallest correct version at 2/3 or less: rewrite once. Over 1.5x budget: hand back to the owner.
- At most 3 review rounds, counted across handoffs: whole head, review of the fix, verify only. Then hand back with options.
- A finding needs a realistic trigger and a material effect. A P2 fix may only change, narrow or delete code, never add state, timers, flags or layers. A fix that causes a new finding is reverted.
- Whoever wrote a step never judges it.
- Review bots are advisory: read them once on the final head. They do not start rounds or gate "ready".
- An owed device check blocks the release.
<!-- agents-block:end -->

## Scale

A small, low-risk change (a few dozen non-test lines, no state, concurrency, persistence, protocol, security or
public-contract change) keeps the done lines inline, skips the design note and the size check, and gets one review
round. A diagnose-only request stays read-only. A plan, question or research request starts no delivery.

## Cut

- Ask first what the cheapest change is that removes the harm. If a different change does it, that one goes first.
- Write at most 5 done lines, each one behavior someone can check. Two behaviors or more than 5 lines means two PRs.
- Set a budget before code: non-test lines, files, and new concepts (types, state, locks, layers, options).
- Only the owner's own words in the issue, a comment or an answered question settle a product decision. Agent notes,
  earlier run output and defaults you picked are placeholders; mark them so.
- Put the done lines and budget in the issue and the PR body. Keep the plan inline unless a file is asked for.

## Design note (risky changes only)

- Write the state model: what is stored, who owns it, how long it lives, how it fails and how it rolls out.
- Get two sketches from authors who cannot see each other's work, each a short list of what changes and what it adds.
- Build the smaller one that meets the done lines. No revision round. A real product trade-off goes to the owner.

## Build

- Reproduce a bug before editing and find the cause. Test one idea at a time; after a few failed tries, stop
  stacking fixes and recheck the model of the problem.
- A fix comes with a test that fails on the old code and passes on the new. Say how you saw it fail.
- Use the smallest design that meets the done lines: no state, type, layer, option or parameter none of them needs.
  Fix at the layer that owns the problem. Delete the code the change replaces in the same PR.
- After the last edit, run the targeted checks and the broader check the risk calls for. Read the exit status.
  Never say a test, build or fix passed without the command that shows it.
- Use lighter checks for docs and config; stronger ones for security, concurrency, persistence, protocols,
  migrations and public contracts.

## Size check (before bug review)

- A fresh reviewer gets only the done lines and the diff, never the design or the author's case. It follows the
  `simplify-diff` method and estimates the smallest correct version in the same units as the budget.
- At 2/3 of the diff or less, giving up no done line, rewrite once. Over 1.5x the budget after that, hand back both
  numbers to the owner.

## Review

- At most 3 rounds, counted across sessions, agents and pushes: round 1 the whole head, round 2 the fixes and their
  effects, round 3 verify only (an open P0/P1 or a reverted fix). Round 3 starts no new fix cycle.
- Carry the state with the PR: round number, reviewed head SHA, open findings and their dispositions.
- A finding counts only with a realistic trigger, who or what hits it, and a material effect with evidence. A
  missing test has the effect of the bug it would miss.
- P0 and P1 are fixed in scope or handed back. A P2 fix may only change, narrow or delete code. If it needs new
  state, a timer, a flag, a lock or a layer, list it as a follow-up. P3 is only listed.
- A fix that causes a new finding is reverted, not patched; reassess the original finding.
- Treat every review, human or bot, as input, not orders: check each claim against the code, tests and contract,
  and reject it with evidence when it is wrong or out of scope. Record the outcome in your report; post replies only
  where the owner's rules allow.
- Review bots are advisory. Read their output once on the final head and judge it by the same test. They do not
  start a round, and "ready" does not wait for them.
- After round 3, or when a P0/P1 is still open, stop and hand back with the options and their costs.

## Scope

A PR under review is closed to new behavior. A new decision, idea, second bug or new event becomes a new issue and PR,
even when the owner raises it mid-review, unless the owner explicitly re-scopes this one. Mechanical companions
(renames, generated files, a caller updated for a changed signature) stay.

## Finish and release

- End at a ready PR. Its body holds the done lines, budget against actual size, checks that were weakened or
  skipped, and open findings. Merge and force-push only on the owner's word.
- An owed device or visual check blocks the release or tag until it is done.
- After release, watch the signal that would show the fix failed (errors, crashes, metrics) and report it.
