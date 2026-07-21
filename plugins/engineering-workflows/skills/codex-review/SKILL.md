---
name: codex-review
description: Use when running Codex CLI code review for uncommitted changes, a PR branch, or a specific commit, especially for second-model review or merge-readiness closeout.
---

# Codex Review

Use `codex review` as an advisory closeout check. Verify every finding against the real code path, dependency behavior, and relevant tests before accepting it.

**Core principle:** A clean model review supplements behavioral evidence; it does not replace tests.

Use `engineering-workflows:code-review` for a generic reviewer-subagent workflow. Use this skill when the requested reviewer is specifically the Codex CLI or an installed wrapper around it.

## Target Selection

| Work to review | Command |
|---|---|
| Dirty unstaged, staged, or untracked patch | `codex review --uncommitted` |
| Committed PR or feature branch | `codex review --base "origin/$base"` |
| One committed change | `codex review --commit HEAD` |

For a PR branch, resolve its actual base instead of assuming `main`:

```bash
base=$(gh pr view --json baseRefName --jq .baseRefName)
git fetch origin "$base"
codex review --base "origin/$base"
```

Do not use `--uncommitted` on a clean PR branch: it proves only that no local patch exists. Do not pass an inline prompt with `--base`; current Codex CLI versions reject that combination.

## Review Loop

Before reviewing, record the request, target/base, intended behavior, owner boundary, changed files, and approximate non-test LOC.

1. Format first if formatting may move lines.
2. Run the correctly targeted review and relevant behavioral tests. Tests and review may run concurrently when independent.
3. Verify each finding in the real code and adjacent paths. Read primary dependency documentation or source when the claim depends on external behavior.
4. Classify accepted findings:
   - **In-scope blocker:** introduced by this diff, within the same owner boundary, and fixable without changing the task contract.
   - **Follow-up:** real but adjacent cleanup, broader hardening, or a sibling surface.
   - **Stop and escalate:** requires a new public API, protocol, configuration, storage, owner boundary, or product decision.
5. Fix only when the user authorized changes. Add a regression test for changed behavior, rerun focused tests, and rerun the same review target.
6. Stop when the review completes successfully with no accepted or actionable findings.

If a review-triggered change expands beyond twice the original files or non-test LOC, or two fix cycles fail to converge, stop and report the scope break.

## Review Invariants

- Treat output as advisory; never apply findings blindly.
- Reject speculative edge cases, cosmetic churn, and broad rewrites that do not improve the reported bug class.
- Never switch or override the review model. On capacity exhaustion, retry the same command with the same model a few times, then report the limitation.
- If an installed wrapper defines a successful, non-empty run with no accepted/actionable findings as clean, trust that contract. Do not rerun solely to obtain a nicer sentence.
- A successful review does not prove user-visible behavior; run proportionate tests or behavior validation.
- Review-only authorization does not permit edits, commits, or pushes.
- After an authorized fix, rerun the affected tests and review. Stop after the first clean rerun.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Running `--uncommitted` on a clean pushed branch | Review against the PR's actual base |
| Assuming `origin/main` | Read `baseRefName` from the PR |
| Switching models after capacity errors | Retry the same command and model |
| Re-running a clean wrapper for prettier output | Accept its documented success contract |
| Treating review as proof | Run focused behavioral validation |
| Pushing fixes during a review-only request | Report findings and wait for authorization |

## Final Report

Include:

- the exact review command and target;
- tests or behavioral proof run;
- accepted and rejected findings, with brief reasons;
- the final clean result, or the precise reason the review remained inconclusive;
- any intentionally deferred follow-ups or scope escalation.
