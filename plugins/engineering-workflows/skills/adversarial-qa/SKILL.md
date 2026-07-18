---
name: adversarial-qa
description: Use only when the user explicitly requests adversarial, hostile, end-to-end, or release-gate QA beyond the project's normal verification suite.
---

<!-- Adapted from concepts in Oh My Codex by Yeachan Heo and contributors (declared MIT). See THIRD_PARTY_NOTICES.md. -->

# Adversarial QA

Try to disprove release readiness using high-value hostile scenarios. This is an explicit heavyweight workflow, not a default completion step.

## Scenario matrix

Select applicable categories:

- malformed, missing, oversized, or boundary input;
- interruption, retry, timeout, partial failure, and recovery;
- concurrent or reordered operations;
- stale caches, state, credentials, or version skew;
- authorization, injection, traversal, and trust-boundary abuse;
- misleading success output or silent data loss;
- upgrade, rollback, and compatibility behavior;
- accessibility, responsive layout, or interaction-state failures for UI work.

Prioritize scenarios by impact and likelihood. Do not generate a large checklist merely to appear thorough.

## Loop

1. Define the release claim and normal verification baseline.
2. Create a bounded scenario matrix with expected outcomes.
3. Run the highest-value scenarios and capture exact evidence.
4. Classify failures by root cause, severity, and reproducibility.
5. Fix only when the user asked for remediation; otherwise report.
6. Re-run failed scenarios plus the normal regression suite.
7. Clean up temporary data and processes.

Use operating-system temporary storage for QA artifacts unless the user requests a durable report.

## Verdict

Return `PASS`, `FAIL`, or `PARTIAL`, with:

- scenarios executed;
- failures and reproductions;
- fixes and re-test evidence, if authorized;
- skipped scenarios and why;
- remaining release risk.
