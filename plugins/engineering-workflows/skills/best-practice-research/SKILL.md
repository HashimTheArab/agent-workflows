---
name: best-practice-research
description: Use when a technical decision depends on current official documentation, upstream source, standards, release notes, or comparative best-practice evidence.
---

<!-- Adapted from concepts in Oh My Codex by Yeachan Heo and contributors (declared MIT). See THIRD_PARTY_NOTICES.md. -->

# Best-Practice Research

Use this skill when a task depends on current external best practices, version-aware guidance, standards, official recommendations, or upstream behavior. It structures evidence gathering and synthesis; it is not a new research authority.

## Purpose

Produce a cited, reusable answer that separates current external evidence from repository-local facts and dependency-selection decisions. Gather official or upstream evidence, then return it directly to the caller as decision, planning, or implementation input.

## Activate When

- The user asks for best practices, recommended approach, current guidance, official recommendations, standards, or version-aware external behavior.
- A planning, review, or implementation workflow needs current external evidence before it can be correct.
- The task involves an already chosen technology and needs authoritative usage guidance, migration notes, API behavior, lifecycle rules, or current safety guidance.

## Do Not Activate When

- The answer is fully repository-local; use the normal repository inspection path.
- The main question is whether to adopt, replace, upgrade, or compare dependencies; treat that as a dependency-evaluation task and make the comparison explicit.
- The user only needs implementation against already-grounded requirements; continue with implementation.
- The task can be answered from stable local project conventions without current external lookup.

## Specialist Routing

1. Inspect repository-local facts first when current usage, constraints, versions, configuration, or integration points affect the answer.
2. Use the bundled [researcher role](../../agents/researcher.md) for official docs, release notes, standards, migration guides, source-backed examples, and current guidance when independent research improves quality.
3. For adoption, upgrade, replacement, or comparison decisions, evaluate the candidates directly rather than treating usage guidance as a selection answer.
4. Return explicit evidence, uncertainty, and any planning or implementation constraints.

## Source-Quality Rules

- Prefer official documentation, upstream source, release notes, changelogs, standards, and maintainer guidance.
- Include source URLs for material claims.
- State date/version context for current best-practice claims.
- Label third-party summaries as supplemental; do not use them before official/upstream sources.
- Flag stale, conflicting, undocumented, or version-mismatched evidence.
- Do not over-fetch: gather the smallest evidence set that can support the decision.

## Workflow

1. Classify the question: conceptual best practice, implementation guidance, migration/version guidance, standards/compliance guidance, or mixed local + external guidance.
2. Gather repository-local facts when local usage or constraints affect the answer.
3. Gather external evidence, optionally with the bundled researcher role, when current or version-aware practice affects correctness.
4. Synthesize a concise answer with source quality, version/date context, caveats, and an implementation or planning handoff.
5. Stop when the answer is grounded enough for the caller; otherwise report the exact blocker or specialist handoff needed.

## Output Contract

```md
## Best-Practice Research: <question>

### Direct Recommendation
<actionable guidance or decision support>

### Evidence Used
- Official/upstream: <source URL> — <what it establishes>
- Supplemental, if any: <source URL> — <why it is secondary>

### Version / Date Context
<versions, dates, release channels, or unknowns>

### Repo-Local Context
<facts from explore, or "not needed">

### Boundaries / Non-goals
<what this research does not decide>

### Handoff
<planning/execution/test implications>
```

## Stop Rules

- Stop after a source-backed recommendation is reusable by the caller.
- Stop and route upward if the task becomes dependency comparison, broad architecture, or implementation.
- Do not continue researching when remaining work would only polish wording rather than change the recommendation.
