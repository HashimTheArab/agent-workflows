---
name: macos-resource-triage
description: Diagnose what's overloading a hot or sluggish Mac. Checks load average against core count, ranks top CPU/memory consumers, and walks process trees to find runaway agent sessions (leftover AI coding-assistant sessions are a common cause). Use when a Mac's fans are loud, the machine feels sluggish, or someone asks what is using CPU/memory/resources.
---

# macOS Resource Triage

## Overview

Diagnose a hot or sluggish Mac before guessing. A single process's %CPU rarely
tells the full story — the more reliable signal is system-wide queueing, and the
most common hidden cause on developer machines is an accumulated tree of AI agent
sessions (coding assistants, browser-automation tools) that spawn MCP servers or
workers and never get cleaned up.

**Announce at start:** "I'm using the macos-resource-triage skill to diagnose resource usage."

## Step 1: Load Average vs Core Count

```bash
sysctl -n hw.ncpu
uptime
```

Load average should be roughly <= core count. A load average many multiples of
the core count (e.g. 10x+) means severe process queueing — that is the real
heat/fan signal, more reliable than any single %CPU reading.

## Step 2: Rank Top Consumers

```bash
ps -Ao pid,pcpu,pmem,comm -r | head -15      # by CPU
ps -Ao pid,pcpu,pmem,rss,comm -m | head -15  # by memory
vm_stat | grep "Pages free"                  # memory pressure (page size 16384 on Apple Silicon)
```

## Step 3: Look for Accumulated Agent Sessions

A single %CPU snapshot understates the problem when the cost is spread across a
process **tree** rather than one PID. On developer machines running AI coding
assistants, check for:

- Long-running CLI agent sessions (e.g. a background/auto-approve flag on a
  coding-assistant CLI) that have been running for days:
  ```bash
  ps -Ao pid,ppid,etime,command | grep -- '<flag-that-marks-a-background-session>'
  ```
  Each one typically spawns its own MCP-server/tool-worker children that don't
  get reaped once the parent goes idle.
- Desktop-app "computer use" / autonomous-agent features (a chat app's built-in
  coding agent, browser-automation daemons, etc.) that keep a session alive in
  the background:
  ```bash
  ps -Ao pid,ppid,etime,command | grep -i 'kernel.js\|computer-use\|agent-runner'
  ```
  These can silently grow to hundreds of descendant processes over days if a
  session gets stuck (e.g. looping on shell calls) instead of finishing and
  exiting.

For any suspect session, get its age and working directory so you can describe
what's piled up and where:

```bash
ps -o etime= -p <pid>
lsof -a -p <pid> -d cwd 2>/dev/null | awk 'NR==2{print $NF}'
```

## Step 4: Sum a Process Tree Correctly

Do not recurse with plain `/bin/bash` on macOS — the shipped bash (3.2) has no
associative arrays; `declare -A` fails and silently corrupts the walk. Use zsh
(`typeset -A`) or Python with an explicit **visited set**. PIDs can churn fast
enough (rapid worker spawn/exit) that a naive walk double-counts, or hangs
without a cycle guard.

```python
import subprocess, collections

out = subprocess.run(["ps", "-Ao", "pid=,ppid=,pcpu=,rss=,comm="], capture_output=True, text=True).stdout
procs, children = {}, collections.defaultdict(list)
for line in out.splitlines():
    parts = line.split(None, 4)
    if len(parts) < 5:
        continue
    pid, ppid, cpu, rss, comm = parts
    pid, ppid = int(pid), int(ppid)
    procs[pid] = (float(cpu), int(rss), comm)
    children[ppid].append(pid)

def tree_totals(root):
    seen, stack = set(), [root]
    n = cpu = rss = 0
    while stack:
        p = stack.pop()
        if p in seen or p not in procs:
            continue
        seen.add(p)
        n += 1
        c, r, _ = procs[p]
        cpu += c
        rss += r
        stack.extend(ch for ch in children.get(p, []) if ch not in seen)
    return n, cpu, rss / 1024  # process count, cpu%, memory MB
```

A large tree total is not automatically a script bug — cross-check with
`ps -Ao pid,ppid,pcpu,rss,comm | grep <name>` before assuming the number is
wrong. Trees under agent-heavy apps legitimately reach hundreds of processes.

## Step 5: Never Kill Without Asking

Background sessions may hold in-progress work. Before running `kill` on
anything:

1. List candidate PIDs with age and working directory.
2. Ask the user which ones to terminate — do not assume old means unwanted.
3. Prefer `kill -TERM <pid>` on the specific stuck session over quitting the
   whole host app, unless the user asks for the broader reset.
4. After killing, re-check load average and the tree total to confirm the fix
   landed, and check for orphaned siblings/children that survived the parent's
   exit.

## Quick Reference

| Signal | Command | What it means |
|---|---|---|
| Load average | `uptime` vs `sysctl -n hw.ncpu` | >> core count = severe queueing |
| Free memory | `vm_stat \| grep "Pages free"` | Near-zero free pages = memory pressure driving CPU (swap/compression) |
| Top CPU | `ps -Ao pid,pcpu,pmem,comm -r` | Single hot processes |
| Top memory | `ps -Ao pid,pcpu,pmem,rss,comm -m` | Single memory hogs |
| Session age/cwd | `ps -o etime=`, `lsof -a -d cwd` | Distinguish stale sessions from active ones |
| Tree totals | Python BFS with visited set | True cost of an agent session, not just its root PID |

## Common Mistakes

### Trusting a single PID's %CPU
- **Problem:** A stuck agent session's cost is spread across dozens of child
  processes; the root PID alone can look idle.
- **Fix:** Always sum the whole process tree (Step 4), not just the process the
  user pointed at.

### Recursing in `/bin/bash`
- **Problem:** macOS's default `/bin/bash` (3.2) doesn't support associative
  arrays; `declare -A` fails, and tree sums silently come out wrong.
- **Fix:** Use zsh or Python for any process-tree walk.

### Assuming a big tree total is a bug
- **Problem:** Dismissing a genuinely huge number (hundreds of processes,
  double-digit GB) as a script error.
- **Fix:** Cross-check with a plain `ps | grep` before concluding the walk is
  wrong — agent-heavy apps really can fan out that far.

### Killing without confirmation
- **Problem:** Terminating a session that held unsaved in-progress agent work.
- **Fix:** Always list PID + age + cwd and get explicit confirmation before
  `kill`.

## Red Flags

**Never:**
- Kill a process or process tree without listing it for the user and getting
  confirmation first.
- Assume a large process count under one root is a measurement bug without
  cross-checking.
- Recurse a process tree in plain `/bin/bash` on macOS.

**Always:**
- Check load average against core count before looking at individual
  processes.
- Sum whole process trees, not single PIDs, when judging an agent session's
  cost.
- Report age and working directory for any session you're proposing to kill.
- Re-verify system state (load average, tree totals) after killing anything.
