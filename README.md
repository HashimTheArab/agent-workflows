# Agent Workflows

Portable, proportional engineering workflows for Codex, Claude Code, and Antigravity—debugging, TDD, verification, planning, review, and agent orchestration without mandatory specs or runtime clutter.

This repository distills the strongest ideas from [Superpowers](https://github.com/obra/superpowers) and [Oh My Codex](https://github.com/Yeachan-Heo/oh-my-codex) into a content-only plugin. It intentionally contains no lifecycle hooks, MCP servers, injected `AGENTS.md`/`CLAUDE.md`, daemons, or repository-local state directories.

## Principles

- Discipline scales automatically: debugging, testing, review handling, and verification activate when relevant.
- Ceremony is explicit: plans, worktrees, multi-agent execution, and adversarial QA run only when requested or deliberately selected.
- Artifacts are optional: ordinary work does not create design specs or planning documents.
- One shared skill library supports Codex and Claude Code.
- Every completion claim is backed by fresh evidence.

## Install in Codex

```bash
codex plugin marketplace add HashimTheArab/agent-workflows
codex plugin add engineering-workflows@hashim-workflows
```

Start a new task after installation so Codex loads the skills.

## Install in Claude Code

```bash
claude plugin marketplace add HashimTheArab/agent-workflows
claude plugin install engineering-workflows@hashim-workflows
```

Run `/reload-plugins` in an existing session, or start a new session.

## Install in Antigravity

```bash
agy plugin install https://github.com/HashimTheArab/agent-workflows
```

Start a new task after installation so Antigravity loads the skills.

## Included workflows

Automatic, narrowly triggered workflows:

- product identity and application-icon design
- systematic debugging
- test-driven development
- verification before completion
- receiving code review
- read-only deep analysis
- evidence-backed best-practice research
- macOS resource/runaway-process triage

Explicit or heavyweight workflows:

- requirements clarification
- code review
- Codex CLI review closeout
- deslop/refactor review
- adversarial QA
- parallel-agent dispatch
- subagent-driven development
- worktree setup and branch finishing
- implementation-plan writing
- skill authoring and validation

## Attribution

Several workflows are adapted from Superpowers and Oh My Codex under their declared MIT licenses. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for provenance and license notices.

## License

MIT. See [LICENSE](LICENSE).
