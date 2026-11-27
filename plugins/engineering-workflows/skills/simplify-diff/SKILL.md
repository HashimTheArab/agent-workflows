---
name: simplify-diff
description: Use when a diff looks too big for the behavior it adds (mirrored types, field-by-field copying, parallel lists, edit sites that grow with each new field), or for the blind size check before review.
---

# Simplify Diff

Count maintained facts and edit sites, not lines. A diff is overgrown when one new field or case forces edits in
places that only repeat what another place already owns.

## As the blind size check

- Work from the done lines and the diff only. Do not read the design note, the PR discussion or the author's case
  until your estimate is written.
- Describe the smallest correct version: what it keeps, what it drops, and a size estimate in the same units as the
  budget (non-test lines, files, new concepts).
- Each piece of state, type, lock, layer, option or parameter stays only if a done line fails without it in a case
  someone realistically hits. Fail-loud checks, input validation, idempotency and bounded reads stay.
- Return the verdict (size justified or not), the estimate, the main weight drivers and what the smaller version
  gives up. The caller compares the estimate with the diff and the budget.

## Method

1. Find the real boundaries. Trace who consumes each type or format: persisted data, network or ABI contracts and
   independently deployed clients are real; an internal type that only looks like a DTO is not.
2. Name the one to three biggest weight drivers. For each, say what fact it repeats and every place a future field
   would need another edit.
3. Remove the repetition at its source:
   - delete wrappers, branches, layers and options that carry no behavior;
   - use one type across internal boundaries that change together;
   - use value copies instead of hand-written clone code;
   - let the owner of a field declare its rule once and derive lists, UI entries, sanitizers and projections from it;
   - where derivation does not fit, add an exhaustiveness check that fails when a new member is not handled;
   - keep a separate adapter only at a real persistence, network, ABI or deployment boundary.
4. Prefer plain code over reflection, code generation or a framework unless it removes more than it adds.
5. Do the structural deletion first, then local cleanup. Update all controlled callers together, keep the
   behavior tests, and rerun them.
6. Read the result again. Repeat while a large block only moves, mirrors or lists data that something else owns.

## Fallbacks

- Delete a fallback that hides a failure: a swallowed error, a default that pretends to succeed, a retry that masks
  a bug.
- Keep a fallback that is a stated product need or a proven compatibility path, and say which.
- If you cannot tell and the choice changes behavior users see, ask that one question before editing.

## Traps

- "It follows the existing pattern": check whether the pattern is what makes the diff grow.
- "Tests pass": tests prove behavior, not that the design is the right size.
- "A later cleanup can fix it": if this change multiplies the pattern, fix the root now.
- A smaller diff bought by deleting useful tests, validation or real compatibility code is not simpler.
