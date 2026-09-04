---
name: writing-plans
description: Use only when the user explicitly requests a written implementation plan or selects a plan-driven workflow for substantial multi-step work.
---

<!-- Derived from Superpowers by Jesse Vincent (MIT). See THIRD_PARTY_NOTICES.md. -->

# Writing Implementation Plans

Write a plan that removes meaningful uncertainty without reproducing the implementation in prose.

Include the outcome and acceptance criteria, constraints and non-goals, affected components, ordered work with real dependencies, verification strategy, and unresolved decisions or risks. Inspect the repository first; use exact paths and commands only when known, and do not invent line numbers, signatures, or error text.

Default to an inline plan. Create or commit a durable plan file only when requested. Each task should produce an independently reviewable result; avoid artificial tiny steps, repeated commit instructions, stale code listings, and duplicate design/implementation documents.

After acceptance, use the host's normal execution and workspace features. Do not ask the user to choose an execution framework when the proportional path is obvious.
