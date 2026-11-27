# Agent Workflows

A short delivery loop for coding agents, plus a few specialist skills, packaged as one plugin for Claude Code and
Codex. The plugin is content only: no hooks, MCP servers, daemons or injected `AGENTS.md`/`CLAUDE.md`.

## Skills

- `delivery-loop`: cut a change to done lines and a size budget, build the smallest version, run a blind size check,
  then at most three review rounds. Loads on ordinary coding tasks.
- `simplify-diff`: find the smallest correct version of an overgrown diff; the method behind the size check.
- `best-practice-research`: answer version-sensitive or external-standard questions from primary sources.
- `design-product-identity`: design and ship a product logo or app-icon family.
- `macos-resource-triage`: find what is making a Mac hot or slow.

## Principles

- Cut before code: at most five done lines and a size budget. Only the owner settles product decisions.
- A PR under review takes no new behavior; new decisions become new PRs.
- Review is capped at three rounds. A P2 fix may only change, narrow or delete code.
- Review bots are advisory. Repo rules add gates, device checks and rollout.
- Skills stay short and do not restate what the host already does well.

## Install

Codex:

```bash
codex plugin marketplace add HashimTheArab/agent-workflows
codex plugin add engineering-workflows@hashim-workflows
```

Claude Code:

```bash
claude plugin marketplace add HashimTheArab/agent-workflows
claude plugin install engineering-workflows@hashim-workflows
```

Start a new session (or run `/reload-plugins` in Claude Code) after installing.

## AGENTS.md block

The hard rules live once, between the `agents-block` markers in
[`delivery-loop/SKILL.md`](plugins/engineering-workflows/skills/delivery-loop/SKILL.md). Repos that opt in carry a
copy so every agent sees them even when the plugin is not loaded. A maintainer writes and checks the copies:

```bash
python3 scripts/agents_block.py sync path/to/AGENTS.md   # write or replace the block; appends it if absent
python3 scripts/agents_block.py check path/to/AGENTS.md  # exit 1 if missing, hand-edited or behind the source
python3 scripts/agents_block.py status [path ...]        # print the source hash and each file's state
```

Symlinked `AGENTS.md` files are followed and text outside the markers is left alone. The copy starts with a
`source: agent-workflows <sha> sha256:<hash>` line. A consumer repo can catch hand edits in CI without this repo:

```bash
sed -n '/^<!-- agents-block:start -->$/,/^<!-- agents-block:end -->$/p' AGENTS.md | sed '1,2d;$d' | shasum -a 256
```

and compare the result with the recorded hash.

## Credits

Earlier versions adapted ideas from [Superpowers](https://github.com/obra/superpowers) and
[Oh My Codex](https://github.com/Yeachan-Heo/oh-my-codex). The current text is written from scratch.

## License

MIT. See [LICENSE](LICENSE).
