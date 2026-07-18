---
name: deslop
description: Use only when the user explicitly asks to remove AI slop, simplify generated code, clean up unnecessary abstractions, or perform a behavior-preserving maintainability pass.
---

<!-- Adapted from concepts in Oh My Codex by Yeachan Heo and contributors (declared MIT). See THIRD_PARTY_NOTICES.md. -->

# Deslop

Improve maintainability without broad rewrites or behavior drift.

## Process

1. Establish the exact file and behavior scope.
2. Inspect tests and public contracts before editing.
3. Add a regression test first when behavior is insufficiently protected.
4. Identify concrete smells: duplication, dead code, unnecessary wrappers, speculative abstractions, weak boundaries, masking fallbacks, or comments that narrate obvious code.
5. Make one smell-focused pass at a time.
6. Run targeted verification after each behavioral boundary changes.
7. Review the final diff for accidental expansion.

Prefer deletion, existing utilities, and existing patterns. Add no dependency unless explicitly requested.

## Fallback classification

- Remove a fallback that masks a defect, silently swallows failure, or manufactures success.
- Preserve a grounded fallback that represents an intentional product requirement or verified compatibility path.
- If classification is ambiguous and changes public behavior, surface that single decision before editing.

## Completion report

Report:

- files simplified;
- abstractions or dead paths removed;
- behavior-preservation evidence;
- remaining risks or intentionally retained complexity.

Do not create cleanup plans or state directories unless the user explicitly requests a durable artifact.
