---
name: deep-analysis
description: Use when the user asks to analyze, investigate, explain why something happens, or provide a grounded cross-file explanation without modifying code.
---

<!-- Adapted from concepts in Oh My Codex by Yeachan Heo and contributors (declared MIT). See THIRD_PARTY_NOTICES.md. -->

# Read-Only Deep Analysis

Answer the user's actual question through repository evidence. This workflow is read-only: do not edit files or silently turn diagnosis into implementation.

## Method

1. Restate the question narrowly.
2. Inspect the smallest set of relevant files, tests, configuration, history, and generated artifacts.
3. Rank plausible explanations by evidentiary strength.
4. Separate direct evidence from inference and unknowns.
5. Stop when additional inspection would not materially change the answer.

Use parallel exploration only for independent search surfaces. Do not delegate trivial lookups.

## Evidence rules

- Cite concrete file paths and tight line references for material claims.
- Label conclusions as evidence, inference, or unknown.
- Do not present architectural preference as repository fact.
- Prefer current code and tests over stale prose.
- When sources conflict, explain the conflict rather than selecting one silently.

## Output

Lead with the conclusion, followed by:

- ranked synthesis;
- strongest supporting evidence;
- material inferences;
- unresolved unknowns or limits.

If a next step would reduce uncertainty, recommend one discriminating read-only probe. Do not append a generic implementation plan.
