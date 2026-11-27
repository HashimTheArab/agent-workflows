---
name: best-practice-research
description: Use when an answer depends on facts that may have changed since training (library or API versions, limits, prices, release notes) or on an external standard or spec.
---

# Best-Practice Research

Answer from primary sources that match the versions in use.

1. Check the repo first: pinned versions, lockfiles, config and how the thing is used today.
2. Read the official docs, upstream source, the standard or the release notes for those versions. Use third-party
   posts only to fill a gap you can name.
3. Note the date and version of each source. Say when sources are old, disagree or do not match the version in use.
4. Stop at the smallest set of sources that settles the decision.
5. Give the recommendation first. Cite each key claim next to it, keep source facts apart from your inference, and
   name what is still unknown.

To choose between tools or approaches, compare the candidates side by side; docs for one option are not a comparison.
Skip this when no outside source could change a repo-local answer.
