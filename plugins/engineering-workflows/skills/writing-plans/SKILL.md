---
name: writing-plans
description: Use only when the user explicitly requests a written implementation plan or selects a plan-driven execution workflow for substantial multi-step work.
---

<!-- Derived from Superpowers by Jesse Vincent (MIT). See THIRD_PARTY_NOTICES.md. -->

# Writing Implementation Plans

Write a plan that removes meaningful uncertainty without reproducing the implementation in prose.

## Artifact policy

- Default to an inline plan.
- Write a repository file only when the user requests a durable plan or another explicitly selected workflow requires one.
- Never commit a plan unless the user asked for a committed artifact.
- Do not create both a design document and an implementation plan when one artifact is sufficient.

## Plan contents

Include:

1. the outcome and acceptance criteria;
2. relevant constraints and non-goals;
3. the files or components likely to change;
4. ordered implementation steps with dependencies;
5. the test and verification strategy;
6. material risks or decisions that remain open.

Use exact paths and commands when known. Do not invent line numbers, signatures, or expected error text before inspecting the repository.

## Granularity

Each task should produce an independently reviewable result. Avoid artificial two-minute steps, repeated commit instructions, and complete code listings that will immediately become stale.

Split a task only when a reviewer could reasonably approve one part while rejecting another.

## Execution handoff

After the plan is accepted:

- execute directly when tasks are coupled or small;
- use `engineering-workflows:subagent-driven-development` only when the user selected it and tasks are independently delegable;
- use `engineering-workflows:using-git-worktrees` only when isolation is actually needed.

Do not ask the user to choose an execution framework when there is an obvious proportional default.
