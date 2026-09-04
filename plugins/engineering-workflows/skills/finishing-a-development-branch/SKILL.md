---
name: finishing-a-development-branch
description: Use when implementation is verified but the user has not specified whether to merge, open a pull request, keep the branch, or discard it.
---

<!-- Derived from Superpowers by Jesse Vincent (MIT). See THIRD_PARTY_NOTICES.md. -->

# Finishing a Development Branch

Run the verification that proves the work is ready. If it fails, report the failure and stop.

Before executing any requested or selected path, inspect `git status --short --ignored`, the current symbolic branch, resolved git/common directories, and `git worktree list --porcelain`. Resolve the actual base branch; do not assume `main`. Unconditionally classify the checkout as normal/named, normal/detached, linked/named, or linked/detached.

If no path was chosen, offer choices by name: merge locally, push and create a ready pull request, keep as-is, or discard. On either detached state, omit merge. Never interpret a bare number; ask for the choice name.

For detached work, reject local merge. A pull request requires an exact user-provided branch name. Check local and remote collisions, then push `HEAD:refs/heads/<name>`. Never remove the main worktree or attempt branch deletion for either detached state.

For any pull request, push first and create it with repository tooling. Default to ready; request draft state only when the user explicitly asked. Query it afterward and verify the URL, open state, expected draft state, head ref, base ref, and rendered body.

For local merge, require `git status --short --ignored` to produce no output in both the current/source and selected base worktrees; otherwise preserve them and ask what to do. Use the base's registered worktree when one exists. If none exists, switch the current clean normal/named checkout to the base; from linked/named work, locate a clean normal worktree and switch it, or stop for direction when none is safe. Merge and re-run verification. Move every source worktree off the feature branch—to the base when available there, otherwise detached at the verified merged base commit—without removing the main worktree. Then remove any authorized linked feature worktree and delete the local branch.

For discard, show unique commit IDs, `git status --short --ignored`, the current branch/ref if any, relevant pull-request association, and the canonical registered worktree path. Require explicit confirmation of that complete snapshot, including every commit, file state, ref, pull-request disposition, and worktree path that will be affected. Immediately before each deletion, re-read and compare the entire snapshot; stop if anything changed. For normal/named work, switch the main worktree to the resolved base before deleting the local branch, or detach it at the resolved base commit when that branch is checked out elsewhere. For normal/detached work, remove only the specifically confirmed changes, then switch the preserved main worktree to the base or detach it at the resolved base commit; there is no branch to delete. Never remove the main worktree. A content-only workflow has no creation provenance: remove only a non-main worktree with host-provided provenance or confirmation of that exact registered path. Delete only the local branch; remote deletion requires a separate request. Preserve worktrees associated with open pull requests unless the user explicitly authorizes that exact cleanup. Never force-push, force-remove, or discard uncommitted work without explicit authorization.
