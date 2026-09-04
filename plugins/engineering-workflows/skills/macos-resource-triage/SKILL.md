---
name: macos-resource-triage
description: Use when a Mac is hot, slow, memory-constrained, or has loud fans and current CPU, memory, or runaway process usage needs diagnosis.
---

# macOS Resource Triage

Measure system pressure before blaming one process.

1. Compare load with logical cores using `uptime` and `sysctl -n hw.ncpu`.
2. Rank CPU and memory consumers with `ps -Ao pid,ppid,etime,pcpu,pmem,rss,command -r` and `-m`; check `vm_stat` for memory pressure.
3. For agent, browser-automation, or developer-tool sessions, inspect the full parent/child tree. Record each candidate root PID, age, command, and working directory (`lsof -a -p PID -d cwd`) because a quiet parent may own many expensive children.
4. Cross-check surprising totals against a fresh `ps` snapshot. PID churn can invalidate naive recursive counts; use a visited set when scripting a tree walk.
5. Report the measured bottleneck and candidate sessions. Do not terminate anything during a diagnose-only request.

Before any `kill`, show the exact PIDs and ask which sessions to terminate; old sessions may hold active work. Prefer `TERM` on the specific root over quitting its host application. After authorized termination, re-run load, memory, and process-tree checks and report survivors.
