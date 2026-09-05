---
name: finishing-a-development-branch
description: Use when implementation is verified but the user has not specified whether to merge, open a pull request, keep the branch, or discard it.
---

<!-- Derived from Superpowers by Jesse Vincent (MIT). See THIRD_PARTY_NOTICES.md. -->

# Finishing a Development Branch

Follow the user's chosen integration path and existing authorization. If none was chosen, leave the verified work in place and report its branch and status; ask only when a decision is needed to finish the requested task.

Before integration, inspect the current changes, branch or detached HEAD, target ref, and registered worktrees. Keep unrelated work out of commits and pushes. Use existing verification evidence when it still covers the final changes; resolve relevant failures before claiming readiness.

For a requested push or pull request, use the specified target. If a new branch is needed, choose a descriptive unused name unless the user supplied one. Detached HEAD does not require a branch-name question: create a branch when needed or push the intended commit to an explicitly authorized target. Never force-push without explicit authorization.

For a pull request, use repository tooling and default to ready for review. Verify its URL, head, base, draft state, and rendered body afterward. Follow the repository's review and checks requirements through completion.

For a local merge, use the target branch's registered worktree when available. Preserve unrelated tracked, untracked, and ignored files; their presence alone is not a blocker. If switching or merging could overwrite them, use a separate worktree or ask about the specific conflict. Verify the merged result with checks appropriate to the change.

Discard and cleanup require authorization for the specific changes, commits, branches, or worktree paths affected. Inspect untracked and ignored files before any removal, and recheck that the target has not changed before deleting it. Never remove the main worktree. Keep worktrees and branches associated with open pull requests unless their cleanup is explicitly authorized. Remote branch deletion requires a separate request.
