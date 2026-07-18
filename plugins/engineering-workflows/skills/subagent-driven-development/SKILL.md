---
name: subagent-driven-development
description: Use only when the user explicitly requests agent-driven execution of an accepted plan whose tasks can be delegated independently in the current session.
---

<!-- Derived from Superpowers by Jesse Vincent (MIT). See THIRD_PARTY_NOTICES.md. -->

# Subagent-Driven Development

Execute a substantial plan with fresh, bounded implementer contexts and independent review. Do not use this workflow for a small or tightly coupled change.

## Preconditions

- The user explicitly selected agent-driven execution.
- Requirements and acceptance criteria are stable.
- Tasks have clear ownership and limited shared-file contention.
- The environment provides subagents.

If these conditions are not met, execute directly.

## Task loop

For each task:

1. Prepare a self-contained task brief from `implementer-prompt.md` containing scope, interfaces, acceptance criteria, allowed files, and verification commands.
2. Dispatch one fresh implementer.
3. Answer blocking questions without widening scope silently.
4. Inspect the implementer's diff and verification evidence.
5. Prepare a review brief from `task-reviewer-prompt.md` without leaking the intended verdict.
6. Dispatch a fresh reviewer.
7. Send critical or important findings back for correction and re-review.
8. Record completion in the host's native task/plan state. Do not create repository-local workflow state directories.

Continue through all accepted tasks without asking “should I continue?” after each one.

## Context discipline

- Give agents only the task-local context they need.
- Pass file paths or a temporary diff file rather than pasting large diffs into conversation history.
- Put temporary review artifacts in the operating system's temporary directory, not the repository.
- Review delegated evidence yourself before accepting completion.

## Final review

After all tasks pass task-level review:

1. Run the complete relevant verification suite.
2. Dispatch a fresh whole-change reviewer using `../code-review/code-reviewer.md`.
3. Resolve critical and important findings.
4. Use `engineering-workflows:verification-before-completion` before reporting success.
5. Use `engineering-workflows:finishing-a-development-branch` only when branch integration is in scope.

## Failure handling

If a task fails repeatedly, stop delegating variations of the same approach. Summarize the evidence, reassess the task boundary, and escalate only the decision that blocks progress.
