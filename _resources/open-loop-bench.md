---
title: Open Loop Bench
date: 2025-09-24 09:00:00 +0800
package: oil-loop-bench
version: 0.2.0
license: MIT
stack: Python · Rust
status: beta
programme: Open Loop Bench
summary: Replay harness for comparing industrial models on recorded plant traces.
links:
  Programme: /research/
  Report: /publications/#replay-in-practice-comparing-industrial-models-on-recorded-plant-traces
  Checklist: /publications/#a-small-boring-checklist-for-benchmarking-industrial-ai-at-the-edge
---

Runs a model against a fixed trace with declared deadlines, records lateness instead of aborting,
and hashes the inputs so that a rerun which is not the same rerun is visible. Mean latency is
deliberately not the headline number.
