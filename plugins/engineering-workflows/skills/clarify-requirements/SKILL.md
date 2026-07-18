---
name: clarify-requirements
description: Use when a requested change is genuinely ambiguous about its goal, boundaries, acceptance criteria, or irreversible tradeoffs; skip when repository context supports a safe, reasonable interpretation.
---

<!-- Adapted from concepts in Oh My Codex by Yeachan Heo and contributors (declared MIT). See THIRD_PARTY_NOTICES.md. -->

# Clarify Requirements

Turn material ambiguity into an execution-ready brief without making ordinary work wait for ceremony.

## Proportionality rule

Clarify only uncertainty that could materially change the implementation, public behavior, data model, safety, or scope. Do not interview the user about facts that repository inspection can answer.

Do not create a spec or plan file unless the user explicitly requests that artifact or explicitly selects a plan-driven handoff workflow. Task size alone is not authorization to write one.

Ask exactly one question per turn. Never batch several clarification questions into a list.

<HARD-GATE>
Your clarification turn may contain a short current understanding followed by exactly one question. A numbered questionnaire, bullets containing separate questions, or one sentence containing several independent questions violates this workflow. Ask the highest-impact question and wait for the answer before asking another.
</HARD-GATE>

## Process

1. Inspect the relevant repository context first.
2. State the current understanding in two or three sentences.
3. Identify the single highest-impact unresolved decision.
4. Ask exactly one concise question.
5. Repeat only while another answer could materially change the result.
6. Summarize the agreed goal, non-goals, acceptance criteria, and decision boundaries inline.
7. Continue into implementation unless the user asked only for clarification or planning.

Prefer a proposed default with rationale over an open-ended question:

> I recommend A because the existing code already treats X as authoritative. Should I proceed with A, or is B intentional?

The two alternatives in this example resolve one decision. Do not attach questions about platforms, deadlines, storage, UX, or secondary edge cases to the same turn.

## Stop conditions

Stop clarifying when:

- the goal and success criteria are testable;
- non-goals prevent obvious scope creep;
- remaining choices are reversible implementation details;
- repository conventions supply a safe default.

Do not ask for approval after every section. One final correction opportunity is enough for a complex inline brief; simple tasks need none.

## Output contract

Keep the result conversational:

- Goal
- In scope
- Out of scope
- Acceptance criteria
- Decisions still reserved for the user

If no durable artifact was explicitly requested, do not write one.
