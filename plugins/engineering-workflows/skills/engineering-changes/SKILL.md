---
name: engineering-changes
description: Use when diagnosing a bug, implementing a fix or feature, or changing executable behavior that needs proportional investigation, testing, and verification.
---

<!-- Derived from Superpowers by Jesse Vincent (MIT). See THIRD_PARTY_NOTICES.md. -->

# Engineering Changes

Match rigor to risk while keeping one evidence loop.

1. Inspect relevant code, constraints, errors, and recent changes. Reproduce a bug when practical and identify the likely root cause before editing. Diagnose-only requests stay read-only.
2. Choose the smallest test boundary that can disprove the intended behavior. For a bug, prefer a focused regression test that fails for the observed symptom. Use `engineering-workflows:test-driven-development` only when strict TDD was explicitly requested.
3. Make the smallest coherent change. Test one hypothesis at a time; if several attempts fail, stop stacking fixes and reassess the model or architecture.
4. After the last relevant edit, run targeted verification plus the smallest broader check justified by risk. Read the exit status and output; do not infer success from a partial or stale run.
5. Report what changed, the fresh evidence, and any unresolved risk. Never claim a test, build, or fix passed without the command that proves it.

Use lighter checks for documentation, metadata, generated artifacts, or non-executable configuration. Use stronger checks for security, concurrency, persistence, protocols, migrations, and public contracts.
